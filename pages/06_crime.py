import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.colors as pcolors
import numpy as np

# --- 1. 데이터 로드 및 전처리 ---
# 스트림릿의 캐시 기능을 사용해 데이터를 한 번만 로드합니다.
@st.cache_data
def load_data(file_path):
    """
    CSV 파일을 로드하고 'crime.csv'에 맞춰 전처리합니다.
    - '합계' 행/열 제거
    - 숫자형 데이터 정제 (쉼표 제거, 정수 변환)
    """
    try:
        # 'cp949' 인코딩으로 원본 파일 로드
        df = pd.read_csv(file_path, encoding='cp949')
    except Exception as e:
        st.error(f"파일 로드 중 오류 발생: {e}")
        st.error("파일이 'app.py'와 동일한 위치에 'crime.csv'라는 이름으로 존재해야 합니다.")
        return pd.DataFrame(), []

    # --- 데이터 정제 (이전 분석 기반) ---

    # 3.1. "합계" 행 식별 및 제거
    total_rows_mask = df['범죄대분류'].str.contains('합계|총계', na=False) | \
                      df['범죄중분류'].str.contains('합계|총계', na=False)
    df_cleaned = df[~total_rows_mask].copy()

    # 3.2. "합계" 열 식별
    id_vars = ['범죄대분류', '범죄중분류']
    potential_region_cols = [col for col in df.columns if col not in id_vars]
    total_cols_mask = [col for col in potential_region_cols if '합계' in col or '총계' in col]
    
    # 3.3. "합계" 열을 제외한 지역 열 목록 생성
    region_cols = [col for col in potential_region_cols if col not in total_cols_mask]
    
    # "합계" 열이 제거된 최종 데이터프레임
    df_cleaned = df_cleaned[id_vars + region_cols].copy()

    # 4. 데이터 정제 (숫자형 변환)
    for col in region_cols:
        # 쉼표(,)가 포함된 문자열을 숫자로 변환하기 위해 쉼표 제거
        if df_cleaned[col].dtype == 'object':
            df_cleaned[col] = df_cleaned[col].astype(str).str.replace(',', '', regex=False)
        
        # 숫자로 변환 (변환할 수 없는 값은 NaT/NaN이 됨)
        df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')

    # NaN 값을 0으로 대체
    df_cleaned[region_cols] = df_cleaned[region_cols].fillna(0)
    
    # 정수형으로 변환
    try:
        df_cleaned[region_cols] = df_cleaned[region_cols].astype(int)
    except Exception as e:
        st.error(f"데이터를 정수형으로 변환하는 중 오류 발생: {e}")
        # 오류 발생 시에도 일단 진행
        pass

    return df_cleaned, region_cols

# --- 2. 스트림릿 앱 UI 구성 ---

# 페이지 넓게 사용
st.set_page_config(layout="wide")

# 앱 제목
st.title("📊 지역별 범죄 현황 인터랙티브 대시보드")
st.markdown("`crime.csv` 데이터를 기반으로 특정 지역의 범죄 유형을 시각화합니다.")

# 데이터 로드
df_cleaned, region_cols = load_data('crime.csv')

if not df_cleaned.empty:
    
    # --- 3. 사이드바 - 지역 선택 ---
    st.sidebar.header("📍 지역 선택")
    selected_region = st.sidebar.selectbox(
        "분석할 지역을 선택하세요:",
        options=region_cols,
        index=region_cols.index("서울강남구") # 기본값으로 '서울강남구' 설정
    )

    # --- 4. 메인 화면 - 데이터 분석 및 시각화 ---
    st.header(f"'{selected_region}'의 범죄 현황")

    # 4.1. 선택된 지역의 데이터 추출
    # '범죄대분류', '범죄중분류' 및 선택된 지역의 '건수'만 포함
    region_data = df_cleaned[['범죄대분류', '범죄중분류', selected_region]].copy()
    region_data = region_data.rename(columns={selected_region: '건수'})

    # 4.2. 총 범죄 건수 표시 (Metric)
    total_crimes = region_data['건수'].sum()
    st.metric(label="총 범죄 발생 건수", value=f"{total_crimes:,.0f} 건")

    # 4.3. Plotly 차트 생성 (Top 20)
    
    # 0건이 넘는 범죄만 필터링
    region_data_filtered = region_data[region_data['건수'] > 0]
    
    if region_data_filtered.empty:
        st.warning(f"'{selected_region}'에는 1건 이상의 범죄 데이터가 없습니다.")
    else:
        # 건수가 많은 순으로 정렬 후 상위 20개 선택
        region_data_top20 = region_data_filtered.sort_values(by='건수', ascending=False).head(20)
        
        # Plotly는 y축을 위에서 아래로 그리므로, 오름차순으로 다시 정렬해야
        # 그래프 상단에 가장 큰 값이 오게 됩니다.
        region_data_top20 = region_data_top20.sort_values(by='건수', ascending=True)

        # 4.4. 색상 리스트 생성 (요청사항)
        # 1. (N-1)개는 그라데이션, 1개(가장 큰 값)는 빨간색
        
        # 'Blues' 그라데이션에서 N개의 색상을 샘플링
        num_items = len(region_data_top20)
        # 0.0 (연한 파랑) ~ 0.8 (진한 파랑) 사이의 그라데이션 생성
        color_scale_values = [i / (num_items * 1.25) for i in range(num_items)]
        
        try:
            # plotly 5.20 이상
            gradient_colors = pcolors.sample_colorscale('Blues', color_scale_values)
        except TypeError:
            # 구버전 plotly
            from plotly.colors import colorscale_to_colors
            gradient_colors = colorscale_to_colors(pcolors.sequential.Blues, color_scale_values)


        # 가장 마지막 값(가장 큰 값)을 'red'로 변경
        if gradient_colors:
            gradient_colors[-1] = 'red'
        
        # --- 5. Plotly 그래프 그리기 ---
        fig = go.Figure(go.Bar(
            x=region_data_top20['건수'],
            y=region_data_top20['범죄중분류'],
            orientation='h', # 수평 바 차트
            marker=dict(
                color=gradient_colors, # 위에서 만든 커스텀 색상 리스트 적용
                line=dict(color='rgba(0,0,0,0.5)', width=1) # 바 테두리
            ),
            customdata=region_data_top20['범죄대분류'], # 호버 데이터에 '범죄대분류' 추가
            hovertemplate='<b>%{y}</b><br>' +
                          '발생 건수: %{x:,.0f} 건<br>' +
                          '범죄 대분류: %{customdata}' +
                          '<extra></extra>' # Plotly 기본 호버 툴팁 제거
        ))

        # 차트 레이아웃 업데이트
        fig.update_layout(
            title=dict(
                text=f"<b>'{selected_region}'의 범죄 유형 Top {num_items}</b>",
                font=dict(size=20),
                x=0.5 # 제목 중앙 정렬
            ),
            xaxis_title='발생 건수',
            yaxis_title=None, # Y축 제목 없음 (공간 확보)
            height=max(600, num_items * 30), # 항목 개수에 따라 차트 높이 자동 조절
            margin=dict(l=150, r=20, t=60, b=40), # 좌우 여백 조절
            showlegend=False, # 범례 숨기기
            plot_bgcolor='rgba(0,0,0,0)', # 배경 투명
            paper_bgcolor='rgba(0,0,0,0)'
        )

        # 스트림릿에 차트 표시
        st.plotly_chart(fig, use_container_width=True)

        # 4.5. 원본 데이터 표시 (선택적)
        with st.expander(f"'{selected_region}'의 전체 범죄 데이터 보기 (총 {len(region_data_filtered)}개 유형)"):
            st.dataframe(
                region_data_filtered.sort_values(by='건수', ascending=False), 
                use_container_width=True,
                column_config={
                    "건수": st.column_config.NumberColumn(format="%d 건")
                }
            )

else:
    st.error("데이터 로드에 실패했습니다. 'crime.csv' 파일이 올바른지 확인해주세요.")
