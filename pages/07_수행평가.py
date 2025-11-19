import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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

    # --- 데이터 정제 ---
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

    # 범죄 대분류 리스트 추출
    major_crimes = sorted(df_cleaned['범죄대분류'].unique().tolist())
        
    return df_cleaned, region_cols, major_crimes

# --- 공통 함수: 그래프 그리기 ---
def draw_bar_chart(df_plot, x_col, y_col, title, hover_data=None):
    """
    데이터프레임을 받아 그라데이션+빨간색 강조 바 차트를 그립니다.
    """
    # 상위 20개 추출 및 정렬 (Plotly는 아래에서 위로 그리므로 오름차순 정렬)
    df_sorted = df_plot.sort_values(by=x_col, ascending=True)
    
    num_items = len(df_sorted)
    
    # 색상 생성 (Blues 그라데이션 + 1등 Red)
    color_scale_values = [i / (num_items * 1.25) for i in range(num_items)]
    try:
        gradient_colors = pcolors.sample_colorscale('Blues', color_scale_values)
    except:
        from plotly.colors import colorscale_to_colors
        gradient_colors = colorscale_to_colors(pcolors.sequential.Blues, color_scale_values)

    if gradient_colors:
        gradient_colors[-1] = 'red' # 1등 강조

    # 그래프 생성
    fig = go.Figure(go.Bar(
        x=df_sorted[x_col],
        y=df_sorted[y_col],
        orientation='h',
        marker=dict(
            color=gradient_colors,
            line=dict(color='rgba(0,0,0,0.5)', width=1)
        ),
        # 호버 데이터 처리
        customdata=df_sorted[hover_data] if hover_data else None,
        hovertemplate='<b>%{y}</b><br>' +
                      '발생 건수: %{x:,.0f} 건<br>' +
                      (f'{hover_data}: %{{customdata}}<br>' if hover_data else '') +
                      '<extra></extra>'
    ))

    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=20), x=0.5),
        xaxis_title='발생 건수',
        yaxis_title=None,
        height=max(600, num_items * 30),
        margin=dict(l=150, r=20, t=60, b=40),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    return df_sorted.sort_values(by=x_col, ascending=False) # 테이블용 내림차순 반환


# --- 2. 스트림릿 앱 UI 구성 ---
st.set_page_config(layout="wide")
st.title("📊 지역별/범죄별 현황 대시보드")

df_cleaned, region_cols, major_crimes = load_data('crime.csv')

if not df_cleaned.empty:
    
    # === 사이드바: 모드 선택 ===
    st.sidebar.header("🔍 분석 모드")
    analysis_mode = st.sidebar.radio(
        "보고 싶은 데이터를 선택하세요:",
        ["지역별 범죄 현황", "범죄별 지역 순위"]
    )
    st.sidebar.markdown("---")

    # ==========================================
    # MODE 1: 지역별 범죄 현황 (기존 기능)
    # ==========================================
    if analysis_mode == "지역별 범죄 현황":
        st.sidebar.header("📍 옵션 선택")
        
        # 지역 선택
        selected_region = st.sidebar.selectbox(
            "지역 선택:", region_cols, index=region_cols.index("서울강남구") if "서울강남구" in region_cols else 0
        )
        
        # 대분류 필터
        crime_filter_options = ['전체'] + major_crimes
        selected_major_crime = st.sidebar.selectbox(
            "범죄 대분류 필터:", crime_filter_options, index=0
        )

        # 헤더
        st.header(f"🏘️ '{selected_region}' 발생 범죄 순위")
        sub_text = f"전체 범죄 유형" if selected_major_crime == '전체' else f"'{selected_major_crime}' 관련 범죄"
        st.markdown(f"**{sub_text}** 중 발생 건수가 높은 순서대로 보여줍니다.")

        # 데이터 필터링
        region_data = df_cleaned[['범죄대분류', '범죄중분류', selected_region]].copy()
        region_data = region_data.rename(columns={selected_region: '건수'})

        if selected_major_crime != '전체':
            region_data = region_data[region_data['범죄대분류'] == selected_major_crime]

        # 0건 제외 및 Top 20 추출
        df_plot = region_data[region_data['건수'] > 0].sort_values(by='건수', ascending=False).head(20)

        if df_plot.empty:
            st.warning("데이터가 없습니다.")
        else:
            # Metric
            total = region_data['건수'].sum()
            st.metric("총 발생 건수", f"{total:,.0f} 건")
            
            # 차트 그리기
            df_table = draw_bar_chart(
                df_plot, 
                x_col='건수', 
                y_col='범죄중분류', 
                title=f"{selected_region} - 범죄 유형 Top 20",
                hover_data='범죄대분류'
            )
            
            # 테이블
            with st.expander("데이터 상세 보기"):
                st.dataframe(df_table, use_container_width=True, hide_index=True)

    # ==========================================
    # MODE 2: 범죄별 지역 순위 (신규 기능)
    # ==========================================
    else:
        st.sidebar.header("🚨 옵션 선택")
        
        # 1. 대분류 선택 (중분류 목록을 좁히기 위함)
        selected_major_for_rank = st.sidebar.selectbox(
            "범죄 대분류 선택:", major_crimes
        )
        
        # 2. 중분류 선택 (선택된 대분류에 해당하는 것만 표시)
        filtered_middle_crimes = df_cleaned[
            df_cleaned['범죄대분류'] == selected_major_for_rank
        ]['범죄중분류'].unique()
        
        selected_crime_type = st.sidebar.selectbox(
            "상세 범죄 종류 선택:", sorted(filtered_middle_crimes)
        )

        # 헤더
        st.header(f"🏆 '{selected_crime_type}' 최다 발생 지역 순위")
        st.markdown(f"선택하신 **'{selected_crime_type}'** 범죄가 가장 많이 발생한 지역 상위 20곳을 보여줍니다.")

        # 데이터 처리: 해당 범죄의 지역별 값을 추출하여 DataFrame으로 변환
        # 1. 해당 범죄 행 찾기
        target_row = df_cleaned[
            (df_cleaned['범죄대분류'] == selected_major_for_rank) & 
            (df_cleaned['범죄중분류'] == selected_crime_type)
        ]
        
        if target_row.empty:
            st.error("해당 데이터를 찾을 수 없습니다.")
        else:
            # 2. 지역 컬럼만 잘라내고 Transpose (행/열 전환)
            # target_row[region_cols]는 (1, N) 형태이므로 .T를 하면 (N, 1) 형태가 됨
            crime_by_region = target_row[region_cols].T
            crime_by_region.columns = ['건수'] # 컬럼명 변경
            crime_by_region.index.name = '지역' # 인덱스 이름 변경
            crime_by_region = crime_by_region.reset_index() # 인덱스를 컬럼으로 변환

            # 3. 0건 제외 및 Top 20 정렬
            df_plot_rank = crime_by_region[crime_by_region['건수'] > 0].sort_values(by='건수', ascending=False).head(20)

            # Metric
            total_nationwide = crime_by_region['건수'].sum()
            st.metric(f"'{selected_crime_type}' 전국 총 발생 건수", f"{total_nationwide:,.0f} 건")

            if df_plot_rank.empty:
                st.warning("해당 범죄 발생 건수가 있는 지역이 없습니다.")
            else:
                # 차트 그리기 (함수 재사용)
                # 이번에는 Y축이 '지역', X축이 '건수'
                df_table_rank = draw_bar_chart(
                    df_plot_rank,
                    x_col='건수',
                    y_col='지역',
                    title=f"'{selected_crime_type}' 발생 지역 Top 20",
                    hover_data=None
                )

                # 테이블
                with st.expander("데이터 상세 보기"):
                     st.dataframe(
                        df_table_rank, 
                        use_container_width=True, 
                        hide_index=True,
                        column_config={
                            "건수": st.column_config.NumberColumn(format="%d 건")
                        }
                    )

else:
    st.error("데이터 로드 실패")
