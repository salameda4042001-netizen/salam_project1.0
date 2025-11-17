import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="지하철 승하차 Top10", layout="wide")
st.title("🚇 2025년 10월 지하철 승하차 Top10 분석")

# ===========================================================
# 데이터 불러오기 (pages 폴더 기준)
# ===========================================================
@st.cache_data
def load_data():
    df = pd.read_csv("subway.csv", encoding="utf-8")
    return df

df = load_data()

# 날짜 처리
df["date"] = pd.to_datetime(df["date"])

# 2025년 10월만 필터링
df_oct = df[df["date"].dt.strftime("%Y-%m") == "2025-10"]

# ===========================================================
# 사이드바 UI
# ===========================================================
st.sidebar.header("🔎 조회 조건")

dates = sorted(df_oct["date"].dt.strftime("%Y-%m-%d").unique())
selected_date = st.sidebar.selectbox("날짜 선택", dates)

lines = sorted(df_oct["line"].unique())
selected_line = st.sidebar.selectbox("호선 선택", lines)

# ===========================================================
# 조건 필터링
# ===========================================================
filtered = df_oct[
    (df_oct["date"].dt.strftime("%Y-%m-%d") == selected_date) &
    (df_oct["line"] == selected_line)
].copy()

if filtered.empty:
    st.warning("해당 날짜/호선의 데이터가 없습니다.")
    st.stop()

# 승하차 합계 계산
filtered["total"] = filtered["on"] + filtered["off"]

# Top10
top10 = filtered.sort_values("total", ascending=False).head(10)

# ===========================================================
# 색상 세팅
# ===========================================================
colors = ["red"]  # 1등 빨강

# 2~10등 파랑 → 밝아지는 그라데이션
blue_grad = px.colors.sequential.Blues[2:11]
colors.extend(blue_grad[:9])

# ===========================================================
# Plotly 그래프
# ===========================================================
fig = px.bar(
    top10,
    x="station",
    y="total",
    color=top10.index,
    title=f"📊 {selected_date} / {selected_line} 승하차 총합 Top 10",
    color_discrete_sequence=colors
)

fig.update_layout(
    xaxis_title="역 이름",
    yaxis_title="승하차 합계",
    showlegend=False,
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# ===========================================================
# 데이터 테이블
# ===========================================================
st.subheader("📄 Top10 데이터 상세")
st.dataframe(top10[["station", "on", "off", "total"]])
