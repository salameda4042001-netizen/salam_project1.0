import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.colors as pcolors
import numpy as np

# --- 1. 데이터 로드 및 전처리 ---
@st.cache_data
def load_data(file_path):
    """
    CSV 파일을 로드하고 전처리합니다.
    """
    try:
        # 'cp949' 인코딩으로 원본 파일 로드
        df = pd.read_csv(file_path, encoding='cp949')
    except Exception as e:
        st.error(f"파일 로드 중 오류 발생: {e}")
        st.error("파일이 'app.py'와 동일한 위치에 'crime.csv'라는 이름으로 존재해야 합니다.")
        return pd.DataFrame(), [], []

    # 1. "합계" 행 식별 및 제거
    total_rows_mask = df['범죄대분류'].str.contains('합계|총계', na=False) | \
                      df['범죄중분류'].str.contains('합계|총계', na=False)
    df_cleaned = df[~total_rows_mask].copy()

    # 2. "합계" 열 식별 및 지역 컬럼 추출
    id_vars = ['범죄대분류', '범죄중분류']
    potential_region_cols = [col for col in df.columns if col not in id_vars]
    total_cols_mask = [col for col in potential_region_cols if '합계' in col or '총계' in col]
    region_cols = [col for col in potential_region_cols if col not in total_cols_mask]
    
    df_cleaned = df_cleaned[id_vars + region_cols].copy()

    # 3. 숫자형 변환
    for col in region_cols:
        if df_cleaned[col].dtype == 'object':
            df_cleaned[col] = df_cleaned[col].astype(str).str.replace(',', '', regex=False)
        df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')

    df_cleaned[region_cols] = df_cleaned[region_cols].fillna(0)
    try:
        df_cleaned[region_cols] = df_cleaned[region_cols].astype(int)
    except:
        pass

    major_crimes = sorted(df_cleaned['범죄대분류'].unique().tolist())
        
    return df_cleaned, region_cols, major_crimes

# --- 공통 함수: 커스텀 바 차트 ---
def draw_bar_chart(df_plot, x_col, y_col, title, hover_data=None, color_col=None):
    df_sorted = df_plot.sort_values(by=x_col, ascending=True)
    num_items = len(df_sorted)
    
    # 색상 로직
    if color_col:
        # 별도 컬러 컬럼이 있으면 Plotly Express 기본 색상 사용 (비교 차트용)
        marker_settings = {}
    else:
        # 그라데이션 + 1등 강조 로직
        color_scale_values = [i / (num_items * 1.25) for i in range(num_items)]
        try:
            gradient_colors = pcolors.sample_colorscale('Blues', color_scale_values)
        except:
            from plotly.colors import colorscale_to_colors
            gradient_colors = colorscale_to_colors(pcolors.sequential.Blues, color_scale_values)
        if gradient_colors:
            gradient_colors[-1] = 'red'
        marker_settings = dict(color=gradient_colors, line=dict(color='rgba(0,0,0,0.5)', width=1))

    fig = go.Figure(go.Bar(
        x=df_sorted[x_col],
        y=df_sorted[y_col],
        orientation='h',
        marker=marker_settings,
        customdata=df_sorted[hover_data] if hover_data else None,
        hovertemplate='<b>%{y}</b><br>' + '건수: %{x:,.0f}<br>' + (f'{hover_data}: %{{customdata}}<br>' if hover_data else '') + '<extra></extra>'
    ))

    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=18), x=0.5),
        xaxis_title='발생 건수',
        yaxis_title=None,
        height=max(500, num_items * 25),
        margin=dict(l=10, r=10, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# --- 2. 스트림릿 앱 UI ---
st.set_page_config(layout="wide", page_title="범죄 데이터 종합 분석")

st.title("🚔 전국 범죄 데이터 종합 대시보드")
st.markdown("---")

df_cleaned, region_cols, major_crimes = load_data('crime.csv')

if not df_cleaned.empty:
    
    # 탭 구성
    tab1, tab2, tab3, tab4 = st.tabs(["🏘️ 지역별 분석", "🔍 범죄별 분석", "⚔️ 지역 1:1 비교", "🔥 히트맵 & 통계"])

    # ==========================================
    # TAB 1: 지역별 상세 분석 (기존 기능 + 도넛 차트)
    # ==========================================
    with tab1:
        col_opt, col_main = st.columns([1, 3])
        
        with col_opt:
            st.subheader("설정")
            sel_region = st.selectbox("지역 선택", region_cols, index=0)
            sel_major = st.selectbox("대분류 필터", ['전체'] + major_crimes, index=0)

        with col_main:
            # 데이터 준비
            region_df = df_cleaned[['범죄대분류', '범죄중분류', sel_region]].copy()
            region_df = region_df.rename(columns={sel_region: '건수'})
            
            # 1. 상단: 주요 지표 및 도넛 차트
            c1, c2 = st.columns([1, 2])
            
            with c1:
                total = region_df['건수'].sum()
                st.metric(f"{sel_region} 총 범죄", f"{total:,.0f} 건")
                
                # 대분류별 비율 (도넛 차트)
                pie_df = region_df.groupby('범죄대분류')['건수'].sum().reset_index()
                fig_pie = px.pie(pie_df, values='건수', names='범죄대분류', hole=0.4, title=f"{sel_region} 범죄 유형 비율")
                fig_pie.update_layout(showlegend=False, margin=dict(t=40, b=0, l=0, r=0), height=250)
                st.plotly_chart(fig_pie, use_container_width=True)

            with c2:
                # 2. 상세 랭킹 (바 차트)
                if sel_major != '전체':
                    region_df = region_df[region_df['범죄대분류'] == sel_major]
                
                plot_df = region_df[region_df['건수'] > 0].sort_values(by='건수', ascending=False).head(15)
                
                if plot_df.empty:
                    st.warning("표시할 데이터가 없습니다.")
                else:
                    fig_bar = draw_bar_chart(plot_df, '건수', '범죄중분류', f"{sel_region} 상세 범죄 순위 (Top 15)", hover_data='범죄대분류')
                    st.plotly_chart(fig_bar, use_container_width=True)

    # ==========================================
    # TAB 2: 범죄별 랭킹 (기존 기능 강화)
    # ==========================================
    with tab2:
        col_opt2, col_main2 = st.columns([1, 3])
        with col_opt2:
            st.subheader("설정")
            major_cat = st.selectbox("대분류", major_crimes, key='t2_major')
            # 선택된 대분류에 맞는 중분류만 필터링
            filtered_subs = df_cleaned[df_cleaned['범죄대분류'] == major_cat]['범죄중분류'].unique()
            sub_cat = st.selectbox("상세 범죄명", sorted(filtered_subs), key='t2_sub')
        
        with col_main2:
            # 데이터 추출
            target_row = df_cleaned[(df_cleaned['범죄대분류'] == major_cat) & (df_cleaned['범죄중분류'] == sub_cat)]
            
            if not target_row.empty:
                crime_by_reg = target_row[region_cols].T.reset_index()
                crime_by_reg.columns = ['지역', '건수']
                
                # 통계 지표
                avg_cnt = crime_by_reg['건수'].mean()
                max_reg = crime_by_reg.loc[crime_by_reg['건수'].idxmax()]
                
                m1, m2, m3 = st.columns(3)
                m1.metric("전국 총 발생", f"{crime_by_reg['건수'].sum():,.0f} 건")
                m2.metric("지역 평균 발생", f"{avg_cnt:,.1f} 건")
                m3.metric("최다 발생 지역", f"{max_reg['지역']} ({max_reg['건수']}건)")

                # 랭킹 차트
                rank_df = crime_by_reg[crime_by_reg['건수'] > 0].sort_values(by='건수', ascending=False).head(17)
                fig_rank = draw_bar_chart(rank_df, '건수', '지역', f"'{sub_cat}' 지역별 발생 순위")
                st.plotly_chart(fig_rank, use_container_width=True)
            else:
                st.error("데이터 없음")

    # ==========================================
    # TAB 3: 지역 1:1 비교 (신규 기능)
    # ==========================================
    with tab3:
        st.subheader("⚔️ 두 지역 간 범죄 현황 비교")
        c_sel1, c_sel2 = st.columns(2)
        with c_sel1:
            r1 = st.selectbox("지역 A", region_cols, index=0)
        with c_sel2:
            # 지역 B는 지역 A와 다른 것을 기본값으로
            default_idx = 1 if len(region_cols) > 1 else 0
            r2 = st.selectbox("지역 B", region_cols, index=default_idx)

        if r1 == r2:
            st.warning("서로 다른 두 지역을 선택해주세요.")
        else:
            # 데이터 준비
            comp_df = df_cleaned[['범죄대분류', '범죄중분류', r1, r2]].copy()
            
            # 총계 비교
            total_r1 = comp_df[r1].sum()
            total_r2 = comp_df[r2].sum()
            
            mc1, mc2 = st.columns(2)
            mc1.metric(f"{r1} 총 범죄", f"{total_r1:,.0f}", delta=f"{total_r1 - total_r2:,.0f} (vs {r2})")
            mc2.metric(f"{r2} 총 범죄", f"{total_r2:,.0f}", delta=f"{total_r2 - total_r1:,.0f} (vs {r1})")
            
            st.markdown("---")
            
            # Top 범죄 비교 차트 (Grouped Bar Chart)
            # 지역 A 기준 Top 10 범죄를 뽑아서 B와 비교
            top_crimes = comp_df.sort_values(by=r1, ascending=False).head(10)
            
            # Plotly Express로 변환하기 위해 Melting
            melted = top_crimes.melt(id_vars=['범죄중분류'], value_vars=[r1, r2], var_name='지역', value_name='건수')
            
            fig_comp = px.bar(
                melted, x='건수', y='범죄중분류', color='지역', barmode='group',
                title=f"{r1} 기준 주요 범죄 Top 10 비교",
                height=600, orientation='h'
            )
            # 내림차순 정렬 효과
            fig_comp.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_comp, use_container_width=True)

    # ==========================================
    # TAB 4: 히트맵 & 종합 통계 (신규 기능)
    # ==========================================
    with tab4:
        st.subheader("🔥 전국 범죄 대분류 히트맵")
        st.caption("지역별로 어떤 유형의 범죄가 집중되는지 색상의 진하기로 파악할 수 있습니다.")
        
        # 히트맵용 데이터 집계 (행: 지역, 열: 대분류, 값: 건수 합계)
        # 1. Melt
        heatmap_base = df_cleaned.melt(id_vars=['범죄대분류', '범죄중분류'], value_vars=region_cols, var_name='지역', value_name='건수')
        # 2. Groupby
        heatmap_data = heatmap_base.groupby(['지역', '범죄대분류'])['건수'].sum().reset_index()
        # 3. Pivot
        heatmap_pivot = heatmap_data.pivot(index='지역', columns='범죄대분류', values='건수')
        
        # 히트맵 그리기
        fig_heat = px.imshow(
            heatmap_pivot,
            labels=dict(x="범죄 유형", y="지역", color="발생 건수"),
            x=heatmap_pivot.columns,
            y=heatmap_pivot.index,
            aspect="auto",
            color_continuous_scale="Reds" # 붉은색 계열
        )
        fig_heat.update_layout(height=700)
        st.plotly_chart(fig_heat, use_container_width=True)
        
        st.markdown("### 📝 전체 데이터 원본")
        with st.expander("클릭하여 원본 데이터 펼치기"):
            st.dataframe(df_cleaned, use_container_width=True)

else:
    st.error("데이터를 로드할 수 없습니다.")
