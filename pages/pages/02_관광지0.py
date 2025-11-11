# app.py
import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title="Seoul Top10 (for foreign visitors)", layout="wide")
st.title("🇰🇷 서울 — 외국인들이 좋아하는 주요 관광지 Top 10")
st.markdown(
    "Folium 지도로 서울 주요 관광지 10곳을 표시합니다. 마커를 클릭하면 간단한 설명이 뜹니다."
)

# Top10 장소(이름, 위도, 경도, 간단설명)
PLACES = [
    ("Gyeongbokgung Palace (경복궁)", 37.5796, 126.9770,
     "조선의 대표 궁궐. 수문장 교대식으로 유명."),
    ("Changdeokgung Palace & Secret Garden (창덕궁·비원)", 37.5794, 126.9910,
     "유네스코 문화유산으로 유명한 궁궐과 후원."),
    ("N Seoul Tower (남산 타워 / N서울타워)", 37.5512, 126.9882,
     "서울 전경을 한눈에 볼 수 있는 전망 명소."),
    ("Myeongdong (명동 쇼핑거리)", 37.5609, 126.9861,
     "쇼핑 & 스트리트 푸드의 메카."),
    ("Bukchon Hanok Village (북촌한옥마을)", 37.5826, 126.9830,
     "전통 한옥이 모여 있는 고즈넉한 마을."),
    ("Insadong (인사동)", 37.5740, 126.9849,
     "전통 공예품, 찻집과 갤러리 골목."),
    ("Hongdae / Hongik Univ. Area (홍대)", 37.5576, 126.9251,
     "젊음의 거리, 스트리트 퍼포먼스와 카페."),
    ("Dongdaemun Design Plaza (동대문 DDP)", 37.5663, 127.0090,
     "미래적 건축과 야간 쇼핑."),
    ("Gwangjang Market (광장시장)", 37.5704, 126.9990,
     "전통 시장 – 빈대떡, 마약김밥 등 길거리 음식 인기."),
    ("Cheonggyecheon Stream / Plaza (청계천/광장)", 37.5660, 126.9770,
     "도심 속 복원된 하천 산책로.")
]

# 지도 초기화 (서울 중심)
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 마커 클러스터
mc = MarkerCluster().add_to(m)

for name, lat, lon, desc in PLACES:
    html_popup = f"""
    <div style="width:220px;">
      <h4 style="margin-bottom:6px;">{name}</h4>
      <p style="margin:0;font-size:13px;">{desc}</p>
      <p style="margin-top:6px;"><a href="https://www.google.com/search?q={name.replace(' ','+')}" target="_blank">더 보기 (Google)</a></p>
    </div>
    """
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(html_popup, max_width=300),
        tooltip=name,
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(mc)

# Streamlit에 표시
st.subheader("지도")
# st_folium을 사용하면 상호작용 가능한 Folium 지도가 Streamlit에 삽입됩니다.
st_data = st_folium(m, width=1100, height=650)

st.sidebar.header("Top 10 장소")
for i, (name, lat, lon, _) in enumerate(PLACES, start=1):
    st.sidebar.markdown(f"{i}. {name} — ({lat:.4f}, {lon:.4f})")

st.sidebar.markdown("---")
st.sidebar.markdown("데이터 출처: VisitKorea, TripAdvisor, VisitSeoul 등.")
