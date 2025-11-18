import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="지역별 땅값 분석", layout="wide")

st.title("🏙️ 지역별 땅값 분석 + 지도 시각화 (Plotly)")

# ---------------------------
# 1) CSV 업로드
# ---------------------------
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 지역 컬럼 추정
    region_candidates = [c for c in df.columns if "지역" in c or "구" in c or "시" in c or "region" in c.lower()]
    price_candidates = [c for c in df.columns if "값" in c or "가격" in c or "지" in c or "price" in c.lower()]
    lat_candidates = [c for c in df.columns if "lat" in c.lower() or "위도" in c]
    lon_candidates = [c for c in df.columns if "lon" in c.lower() or "lng" in c.lower() or "경도" in c]

    if region_candidates and price_candidates:
        region_col = st.selectbox("지역 컬럼을 선택하세요", region_candidates)
        price_col = st.selectbox("땅값 컬럼을 선택하세요", price_candidates)

        # 위도/경도 선택 (지도 시각화에 필요)
        if lat_candidates and lon_candidates:
            lat_col = st.selectbox("위도( lat ) 컬럼 선택", lat_candidates)
            lon_col = st.selectbox("경도( lon ) 컬럼 선택", lon_candidates)
        else:
            st.error("⚠️ 지도 시각화를 위해 위도(lat), 경도(lon) 컬럼이 필요합니다.")
            st.stop()

        # ---------------------------
        # 2) 지역 선택
        # ---------------------------
        regions = sorted(df[region_col].unique())
        selected_region = st.selectbox("지역을 선택하세요", regions)

        # ---------------------------
        # 3) 지역 필터링
        # ---------------------------
        filtered = df[df[region_col] == selected_region].copy()

        # ---------------------------
        # 4) 막대 그래프 색상 (1등=빨간색)
        # ---------------------------
        filtered_sorted = filtered.sort_values(price_col, ascending=False).reset_index(drop=True)

        max_v = filtered_sorted[price_col].max()
        min_v = filtered_sorted[price_col].min()

        plot_colors = []
        for i, val in enumerate(filtered_sorted[price_col]):
            if i == 0:
                plot_colors.append("red")
            else:
                ratio = (val - min_v) / (max_v - min_v + 1e-9)
                r = int(50 - 40 * ratio)
                g = int(150 - 100 * ratio)
                b = int(255 - 150 * ratio)
                plot_colors.append(f"rgb({r},{g},{b})")

        # ---------------------------
        # 5) 막대 그래프
        # ---------------------------
        st.subheader("📊 선택 지역의 땅값 막대 그래프")
        fig_bar = px.bar(
            filtered_sorted,
            x=region_col,
            y=price_col,
            title=f"{selected_region} 지역 땅값 분석",
        )
        fig_bar.update_traces(marker_color=plot_colors)
        st.plotly_chart(fig_bar, use_container_width=True)

        # ---------------------------
        # 6) 지도 시각화 (Plotly Scatter Mapbox)
        # ---------------------------
        st.subheader("🗺️ 지도 시각화 (Plotly Map)")

        # Plotly 기본 토큰 없이 가능한 무료 tileset 사용
        fig_map = px.scatter_mapbox(
            filtered,
            lat=lat_col,
            lon=lon_col,
            color=price_col,
            size=price_col,
            hover_name=region_col,
            zoom=10,
            height=600,
            color_continuous_scale="Turbo",
        )

        # Mapbox 오픈 소스 스타일 사용 (무료)
        fig_map.update_layout(mapbox_style="open-street-map")
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        st.plotly_chart(fig_map, use_container_width=True)

    else:
        st.error("⚠️ 지역 또는 땅값 관련 컬럼을 찾을 수 없습니다.")
else:
    st.info("CSV 파일을 업로드하면 분석이 시작됩니다.")
