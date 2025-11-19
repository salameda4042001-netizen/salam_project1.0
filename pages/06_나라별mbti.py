import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="국가별 MBTI 분석", page_icon="🌍", layout="wide")

st.title("🌍 국가별 MBTI 비율 시각화")
st.write("국가를 선택하면 해당 국가의 MBTI 비율을 막대 그래프로 확인할 수 있습니다.")

# CSV load (루트 폴더 위치 기준)
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# 국가 목록 가져오기
countries = df["Country"].dropna().unique().tolist()

# 국가 선택 UI
selected_country = st.selectbox("국가를 선택하세요", countries)

# 선택한 국가의 데이터 추출
row = df[df["Country"] == selected_country].iloc[0]

# MBTI 열 추출 (Country 제외)
mbti_cols = [c for c in df.columns if c != "Country"]
mbti_values = row[mbti_cols].values

# 데이터프레임 생성
chart_df = pd.DataFrame({
    "MBTI": mbti_cols,
    "Value": mbti_values
}).sort_values("Value", ascending=False)

# 색상 설정: 1등(최댓값)은 빨간색, 나머지는 그라데이션
colors = ["red"] + [f"rgba(0,{50 + i*10},255,{0.9 - i*0.03})" for i in range(len(chart_df)-1)]

# plotly 그래프 생성
fig = px.bar(
    chart_df,
    x="MBTI",
    y="Value",
)

# 바 색 적용
fig.update_traces(marker_color=colors)

# 그래프 스타일 조정
fig.update_layout(
    title=f"📊 {selected_country}의 MBTI 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    template="simple_white",
    height=600,
)

st.plotly_chart(fig, use_container_width=True)

# 데이터 테이블도 표시 (옵션)
with st.expander("📄 데이터 값 보기"):
    st.dataframe(chart_df.reset_index(drop=True))
