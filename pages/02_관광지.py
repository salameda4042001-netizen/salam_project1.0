# app.py
import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title="Seoul Top10 (for foreign visitors)", layout="wide")
st.title("🇰🇷 외국인들이 좋아하는 서울 주요 관광지 Top 10")

st.markdown(
    "서울을 처음 방문한 외국인들에게 인기 있는 10곳의 명소를 Folium 지도로 살펴보세요. "
    "마커를 클릭하면 해당 관광지의 간단한 설명이 아래에 표시됩니다."
)

# 관광지 데이터
PLACES = [
    ("Gyeongbokgung Palace (경복궁)", 37.5796, 126.9770,
     "조선의 대표 궁궐로, 화려한 근정전과 수문장 교대식이 인기입니다."),
    ("Changdeokgung Palace & Secret Garden (창덕궁·비원)", 37.5794, 126.9910,
     "유네스코 문화유산으로 등록된 고궁. 자연과 조화를 이룬 비원이 유명합니다."),
    ("N Seoul Tower (남산타워)", 37.5512, 126.9882,
     "서울의 랜드마크 전망대. 야경 명소이자 사랑의 자물쇠로 유명합니다."),
    ("Myeongdong (명동)", 37.5609, 126.9861,
     "서울의 대표 쇼핑 거리로, 화장품·패션·길거리 음식이 인기를 끕니다."),
    ("Bukchon Hanok Village (북촌한옥마을)", 37.5826, 126.9830,
     "조선시대 양반가의 한옥이 모여 있는 전통마을로, 사진 명소입니다."),
    ("Insadong (인사동)", 37.5740, 126.9849,
     "전통 공예품과 찻집, 갤러리들이 모여 있어 한국 문화의 정취를 느낄 수 있습니다."),
    ("Hongdae (홍대)", 37.5576, 126.9251,
     "젊음의 거리로, 거리공연과 카페·클럽 문화가 활발합니다."),
    ("Dongdaemun Design Plaza (DDP)", 37.5663, 127.0090,
     "자하 하디드의 미래적 건축물로, 야경과 전시회로 인기입니다."),
    ("Gwangjang Market (광장시장)", 37.5704, 126.9990,
     "100년 전통의 시장으로, 빈대떡·마약김밥 등 한국 길거리 음식 천국입니다."),
    ("Cheonggyecheon Stream (청계천)", 37.5660, 126.9770,
     "도심 속 복원된 하천 산책로로, 낮에는 산책, 밤에는 조명이 아름답습니다.")
]

# 지도 초기화
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)
mc = MarkerCluster().add_to(m)

# folium 마커 생성
for name, lat, lon, desc in PLACES:
    folium.Marker(
        location=[lat, lon],
        popup=name,  # 간단한 이름만 표시
        tooltip=name,
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(mc)

# 지도 표시 (70% 크기 정도)
col1, col2, col3 = st.columns([0.15, 0.7, 0.15])
with col2:
    st_folium_output = st_folium(m, width=900, height=500)

# 마커 클릭 감지
clicked_info = st_folium_output.get("last_object_clicked_popup")

# 클릭된 관광지 설명 표시
if clicked_info:
    selected_name = clicked_info
    for name, lat, lon, desc in PLACES:
        if name == selected_name:
            st.markdown(f"### 📍 {name}")
            st.write(desc)
            st.markdown(
                f"[🔎 Google에서 더 보기](https://www.google.com/search?q={name.replace(' ', '+')})"
            )
            break
else:
    st.info("지도의 마커를 클릭하면 관광지 설명이 여기에 표시됩니다 😊")

st.markdown("---")

# 지도 아래 관광지 요약
st.subheader("🗺️ 서울 Top10 관광지 요약")

cols = st.columns(2)
for i, (name, lat, lon, desc) in enumerate(PLACES):
    with cols[i % 2]:
        st.markdown(f"**{i+1}. {name}**")
        st.write(f"📍 위도 {lat:.4f}, 경도 {lon:.4f}")
        st.caption(desc)
