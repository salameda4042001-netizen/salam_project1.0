import streamlit as st

st.set_page_config(page_title="MBTI 북/영화 추천", page_icon="🧭", layout="centered")

MBTI_LIST = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP",
]

# 각 MBTI 유형별 추천 데이터 (책, 영화, 이유)
RECOMMENDATIONS = {
    "INTJ": {
        "books": [
            ("1984", "조지 오웰 — 체제와 전략을 읽는 통찰력, 당신의 분석 본능과 찰떡 궁합.", "INTJ의 논리적 사고와 비판적 시각이 이 책의 사회 구조 분석과 맞닿습니다."),
            ("Thinking, Fast and Slow", "Daniel Kahneman — 인간의 판단 구조를 해체하며 지적 쾌감을 줍니다.", "데이터와 사고의 체계를 중시하는 당신에게 완벽한 심리학 교양서.")
        ],
        "movies": [
            ("Inception", "복잡한 세계를 설계하는 논리적 천재의 이야기.", "INTJ의 계획적이고 전략적인 성향을 완벽히 반영합니다."),
            ("The Imitation Game", "논리와 비밀, 그리고 천재의 고독.", "문제를 해결하고 구조화하는 당신의 사고방식과 닮았습니다.")
        ]
    },
    "INFP": {
        "books": [
            ("The Little Prince", "생텍쥐페리 — 순수한 감성으로 세상을 바라보는 당신을 위한 고전.", "INFP의 이상주의와 감성적 깊이를 완벽히 대변합니다."),
            ("Norwegian Wood", "무라카미 하루키 — 감정의 깊이를 섬세하게 그린 성장의 이야기.", "감정의 미묘한 변화를 소중히 여기는 당신에게 어울립니다.")
        ],
        "movies": [
            ("Eternal Sunshine of the Spotless Mind", "사랑과 기억의 아픔을 시적으로 풀어낸 감성 영화.", "감정의 복잡함을 예술적으로 표현하는 작품, INFP의 내면과 닮았습니다."),
            ("Lost in Translation", "고독 속에서 진정한 연결을 찾는 부드러운 여정.", "감성과 사색을 즐기는 당신에게 완벽한 영화입니다.")
        ]
    },
    "ENTP": {
        "books": [
            ("Outliers", "말콤 글래드웰 — 성공의 숨은 패턴을 탐구하는 창의적 사고의 결정체.", "ENTP의 호기심과 혁신적 사고를 자극합니다."),
            ("The Innovators", "Walter Isaacson — 세상을 바꾼 아이디어들의 유쾌한 역사.", "발상의 전환과 창의성을 사랑하는 당신에게 딱 맞는 책입니다.")
        ],
        "movies": [
            ("Catch Me If You Can", "즉흥과 재치로 세상을 속이는 천재 사기꾼의 모험.", "즉흥적이면서도 똑똑한 ENTP의 기질과 완벽하게 어울립니다."),
            ("The Big Short", "기발한 발상과 관찰력으로 세상의 허점을 꿰뚫는 이야기.", "논리와 창의성을 동시에 즐기는 당신을 위한 영화입니다.")
        ]
    },
    "INFJ": {
        "books": [
            ("Man's Search for Meaning", "Viktor E. Frankl — 인간 존재의 의미를 찾는 깊은 성찰.", "INFJ의 내면 탐구와 인생의 의미 추구에 완벽히 어울립니다."),
            ("To Kill a Mockingbird", "Harper Lee — 정의와 공감, 당신의 내면과 닮은 따뜻한 이야기.", "도덕적 신념과 타인에 대한 공감이 깊은 INFJ의 가치관과 일치합니다.")
        ],
        "movies": [
            ("Dead Poets Society", "신념과 감성을 일깨우는 영감의 드라마.", "이상과 가치로 사람을 이끄는 INFJ의 영혼과 맞닿은 영화."),
            ("Amélie", "작은 친절이 세상을 바꾸는 이야기.", "조용한 선의와 내면의 따뜻함이 INFJ의 본질을 보여줍니다.")
        ]
    },
    "ESTP": {
        "books": [
            ("Moneyball", "Michael Lewis — 숫자와 실행력으로 승부하는 현실 감각의 리더십.", "ESTP의 즉흥적이고 실용적인 사고에 딱 맞는 전략서."),
            ("Born to Run", "Christopher McDougall — 도전과 에너지를 즐기는 당신에게 완벽한 책.", "신체적 자유와 모험을 즐기는 당신의 본능을 자극합니다.")
        ],
        "movies": [
            ("Fight Club", "본능과 규칙 사이의 긴장감, 행동파 당신의 세계.", "경계를 허무는 ESTP의 반항심과 에너지를 표현한 영화."),
            ("The Fast and the Furious", "속도와 스릴을 즐기는 당신의 심장을 저격합니다.", "아드레날린과 행동 중심적 사고를 즐기는 당신을 위한 작품.")
        ]
    }
}

st.title("MBTI별 책 & 영화 추천기")
st.write("MBTI별로 당신에게 꼭 맞는 책 2권과 영화 2편을 추천합니다.")

mbti = st.selectbox("당신의 MBTI를 선택하세요:", MBTI_LIST)

if mbti:
    rec = RECOMMENDATIONS.get(mbti)
    st.markdown(f"### ✨ {mbti}님을 위한 추천 목록")
    st.write("(작품 요약과 추천 이유를 함께 제공합니다.)")

    st.markdown("**📚 책 추천 (2)**")
    for title, note, reason in rec["books"]:
        st.markdown(f"- **{title}** — {note}\n  - 🧭 추천 이유: {reason}")

    st.markdown("**🎬 영화 추천 (2)**")
    for title, note, reason in rec["movies"]:
        st.markdown(f"- **{title}** — {note}\n  - 🧭 추천 이유: {reason}")

    st.write("---")
    st.caption("이 앱은 Streamlit 기본 라이브러리만으로 작동합니다. 파일명을 'app.py'로 저장하고 Streamlit Cloud에서 실행하세요.")
