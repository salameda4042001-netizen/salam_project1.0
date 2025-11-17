import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="지하철 승하차 Top10 시각화", layout="wide")

st.title("🚇 2025년 10월 지하철 승하차 Top10 분석")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("subway.csv")
    return df

df = load_data()

# -----------------------------
# 날짜 & 호선 선택 UI
# -----------------------------
st.sidebar.header("🔎 조회 조건")

# 2025년 10월 날짜만 필터링
df['date'] = pd.to_datetime(df['date'])
df_oct = df[df['date'].dt.strftime("%Y-%m").eq("2025-10")]

available_dates = sorted(df_oct['date'].dt.strftime("%Y-%m-%d").unique())
selected_date = st.sidebar.selectbox("날짜 선택", available_dates)

available_lines = sorted(df_oct['line'].unique())
selected_line = st.sidebar.selectbox("호선 선택", available_lines)

# -----------------------------
# 조건에 맞는 데이터 필터링
# -----------------------------
filtered = df_oct[
    (df_oct['date'].dt.strftime("%Y-%m-%d") == selected_date) &
    (df_oct['line'] == selected_line)
].copy()

# 승하차 합계 컬럼
filtered["total"] = filtered["on"] + filtered["off"]

# Top10 추출
top10 = filtered.sort_values("total", ascending=False).head(10)

if top10.empty:
    st.warning("📭 해당 날짜/호선 데이터가 없습니다.")
    st.stop()

# -----------------------------
# 색상 세팅
# -----------------------------
# 1등 = 빨강
colors = ["red"]

# 2~10등 = 파란색 → 점점 밝아지는 그라데이션
blue_shades = px.colors.sequential.Blues[3:10]  # 7개의 블루 계열
colors.extend(blue_shades)

# -----------------------------
# Plotly 그래프 생성
# -----------------------------
fig = px.bar(
    top10,
    x="station",
    y="total",
    color=top10.index,   # 색 구분을 위해 index 사용
    color_discrete_sequence=colors,
    title=f"📈 {selected_date} / {selected_line} 승하차 총합 Top 10",
)

fig.update_layout(
    xaxis_title="역",
    yaxis_title="승하차 총합",
    showlegend=False,
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 데이터 테이블 표시
# -----------------------------
st.subheader("📄 Top10 데이터")
st.dataframe(top10[["station", "on", "off", "total"]])
