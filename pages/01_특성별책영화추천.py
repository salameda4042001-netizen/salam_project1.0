import streamlit as st

st.set_page_config(page_title="MBTI 북/영화 추천", page_icon="🧭", layout="centered")

MBTI_LIST = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP",
]

# 각 MBTI 유형별 추천 데이터 (책, 요약, 추천 이유) / (영화, 요약, 추천 이유)
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
    "INTP": {
        "books": [
            ("Surely You're Joking, Mr. Feynman!", "리처드 파인만 — 호기심으로 세상을 해부하는 즐거움.", "비판적 호기심과 자유로운 탐구를 즐기는 INTP에 딱 맞습니다."),
            ("Gödel, Escher, Bach", "Douglas Hofstadter — 개념들을 엮어내는 지적 장난.", "복잡한 개념을 연결하는 지적 놀이가 INTP의 사고를 자극합니다.")
        ],
        "movies": [
            ("Good Will Hunting", "세상을 바라보는 천재의 자유로운 사고와 내적 갈등을 그립니다.", "내적 탐구와 문제 해결을 즐기는 INTP의 감정선을 건드립니다."),
            ("The Social Network", "아이디어와 논쟁, 분석적 사고가 빛나는 영화.", "논리와 전략, 아이디어의 전개를 즐기는 분께 추천합니다.")
        ]
    },
    "ENTJ": {
        "books": [
            ("The Lean Startup", "Eric Ries — 효율과 실행력을 무기로 하는 리더에게 필독서.", "목표지향적이고 실행력 있는 ENTJ에게 실전형 통찰을 제공합니다."),
            ("How to Win Friends & Influence People", "Dale Carnegie — 인간관계에서도 전략은 통한다는 증거.", "사람을 이끄는 기술을 실용적으로 배우기 좋습니다.")
        ],
        "movies": [
            ("Wall Street", "권력과 비즈니스의 윤리를 묻는 고전.", "결단력과 영향력을 고민하는 ENTJ에게 흥미로운 사례를 제공합니다."),
            ("The Wolf of Wall Street", "에너지 넘치는 리더십의 어두운 면을 보여줍니다.", "리더십의 양면성을 성찰하게 해주는 작품입니다.")
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
    "ENFJ": {
        "books": [
            ("Educated", "Tara Westover — 한 인간의 성장과 변화, 영감을 주는 실화.", "사람을 돕고 이끄는 ENFJ의 가치와 잘 맞는 사례를 제공합니다."),
            ("The Seven Habits of Highly Effective People", "Stephen R. Covey — 공감과 리더십을 위한 실용적 지침.", "구체적인 행동 지침으로 리더십 역량을 보완해줍니다.")
        ],
        "movies": [
            ("Freedom Writers", "진심과 헌신으로 사람을 변화시키는 교사의 이야기.", "영향력과 공감의 힘을 믿는 ENFJ에게 큰 울림을 줍니다."),
            ("The King's Speech", "두려움을 극복하고 세상과 소통하는 리더의 여정.", "소통과 용기의 메시지가 ENFJ의 강점과 어울립니다.")
        ]
    },
    "ENFP": {
        "books": [
            ("The Alchemist", "Paulo Coelho — 모험과 꿈을 좇는 영혼에게 어울리는 이야기.", "열정과 가능성을 믿는 ENFP의 에너지를 응원합니다."),
            ("Big Magic", "Elizabeth Gilbert — 창의적 에너지를 믿고 나아가는 용기의 책.", "창의성과 모험을 장려하는 실용적인 영감서입니다.")
        ],
        "movies": [
            ("The Truman Show", "세상을 새롭게 발견하는 당신의 상상력에 어울리는 영화.", "자아와 현실을 탐구하는 ENFP에게 생각할 거리를 제공합니다."),
            ("Almost Famous", "열정과 자유를 노래하는 젊음의 로드무비.", "자유로운 영혼과 열정을 즐기는 ENFP에게 추천합니다.")
        ]
    },
    "ISTJ": {
        "books": [
            ("The Diary of a Young Girl", "Anne Frank — 원칙과 책임, 그리고 인간성의 기록.", "책임감과 전통을 중시하는 ISTJ에게 깊은 공감을 줍니다."),
            ("The Road", "Cormac McCarthy — 규율 속에서 인간 본성을 탐구하는 묵직한 여정.", "질서와 현실감 있는 주제를 선호하는 당신에게 적합합니다.")
        ],
        "movies": [
            ("Bridge of Spies", "정의와 책임을 끝까지 지켜내는 냉철한 신념의 이야기.", "절차와 원칙을 중요시하는 ISTJ의 미학과 맞닿습니다."),
            ("A Few Good Men", "진실을 위해 절차를 중시하는 당신에게 어울리는 법정극.", "논리와 책임을 중시하는 당신에게 추천합니다.")
        ]
    },
    "ISFJ": {
        "books": [
            ("Pride and Prejudice", "Jane Austen — 섬세한 인간관계와 따뜻한 책임감을 담은 고전.", "타인을 돌보고 안정감을 주는 ISFJ의 성향에 잘 맞습니다."),
            ("The Nightingale", "Kristin Hannah — 헌신과 용기의 감동 실화.", "헌신적이고 보호적인 당신의 가치와 공명합니다.")
        ],
        "movies": [
            ("The Help", "배려와 용기로 세상을 바꾸는 감동의 이야기.", "타인에 대한 이해와 돌봄을 중시하는 ISFJ에게 추천합니다."),
            ("Up", "작은 약속과 따뜻한 마음이 주는 희망의 모험.", "따뜻하고 안정적인 감성을 즐기는 분께 어울립니다.")
        ]
    },
    "ESTJ": {
        "books": [
            ("Team of Rivals", "Doris Kearns Goodwin — 조직과 리더십의 정석을 보여주는 역사서.", "조직 운영과 실용적 리더십에 관심이 많은 ESTJ에게 유익합니다."),
            ("Extreme Ownership", "Jocko Willink — 리더의 책임감이 모든 것을 바꾼다.", "책임감과 실행력을 중시하는 당신의 철학과 일치합니다.")
        ],
        "movies": [
            ("12 Angry Men", "논리와 절차로 진실을 이끄는 강렬한 드라마.", "절차와 사실에 기반한 설득을 즐기는 ESTJ에게 추천합니다."),
            ("Apollo 13", "위기에서의 조직적 대응과 리더십.", "현실적 문제 해결과 리더십을 보여주는 모범 사례입니다.")
        ]
    },
    "ESFJ": {
        "books": [
            ("Little Women", "Louisa May Alcott — 가족과 사랑을 중심으로 한 따뜻한 이야기.", "사람 중심적이고 온화한 ESFJ의 감성에 잘 맞습니다."),
            ("Becoming", "Michelle Obama — 공감과 헌신으로 세상을 변화시킨 여정.", "공감 능력과 타인을 이끄는 자세를 배우기 좋습니다.")
        ],
        "movies": [
            ("The Blind Side", "타인에게 헌신하며 세상을 밝히는 실화.", "보살핌과 헌신을 중시하는 ESFJ의 가치와 잘 맞습니다."),
            ("The Intern", "세대 간 이해와 유머를 녹여낸 따뜻한 영화.", "사회적 조화와 인간미를 즐기는 당신에게 추천합니다.")
        ]
    },
    "ISTP": {
        "books": [
            ("Into Thin Air", "Jon Krakauer — 생존 본능과 현실적 해결 능력을 자극합니다.", "현장의 문제 해결과 실용적 접근을 선호하는 ISTP에게 적합합니다."),
            ("The Martian", "Andy Weir — 위기 속 문제 해결의 정수를 보여주는 SF 생존기.", "논리적 해결과 실전적 사고를 즐기는 당신에게 딱입니다.")
        ],
        "movies": [
            ("Mad Max: Fury Road", "속도와 기술로 세상을 돌파하는 쿨한 생존자 이야기.", "행동 중심적이고 현실적인 ISTP에게 어울립니다."),
            ("Drive", "무표정 속 완벽한 제어, 당신의 미니멀리즘과 닮았습니다.", "조용하지만 능숙한 행동을 좋아하는 분께 추천합니다.")
        ]
    },
    "ISFP": {
        "books": [
            ("The Secret Life of Bees", "Sue Monk Kidd — 감성적 치유와 성장의 서사.", "감각과 미적 경험을 중시하는 ISFP에게 편안한 위로를 줍니다."),
            ("On the Road", "Jack Kerouac — 자유로운 감성과 여행의 낭만.", "순간을 사는 삶과 감성적 탐험을 좋아하는 당신에게 추천합니다.")
        ],
        "movies": [
            ("Into the Wild", "자연과 자유를 사랑하는 당신의 삶의 철학이 녹아있는 이야기.", "자유와 감성을 중요시하는 ISFP의 정서를 건드립니다."),
            ("Big Fish", "환상과 감성이 어우러진 따뜻한 상상력의 향연.", "낭만적 상상과 감성적 해석을 즐기는 분께 어울립니다.")
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
    },
    "ESFP": {
        "books": [
            ("Eat Pray Love", "Elizabeth Gilbert — 즐거움과 자유를 향한 여행, 당신의 삶 자체처럼.", "경험과 즐거움을 중시하는 ESFP의 성향과 잘 맞습니다."),
            ("Yes Please", "Amy Poehler — 유머와 에너지로 세상을 밝히는 이야기.", "유머와 즉흥성을 사랑하는 당신에게 추천합니다.")
        ],
        "movies": [
            ("La La Land", "꿈과 사랑을 춤처럼 즐기는 낭만적인 당신을 위한 영화.", "감각적이고 즉흥적인 즐거움을 사랑하는 ESFP에게 어울립니다."),
            ("Mamma Mia!", "음악과 유쾌한 감정이 폭발하는 긍정 에너지의 축제.", "파티 같은 에너지와 즐거움을 좋아하는 당신에게 추천합니다.")
        ]
    }
}

st.title("MBTI별 책 & 영화 추천기")
st.write("센스 있고 따뜻한 과학자 비서가 MBTI별로 당신에게 꼭 맞는 책 2권과 영화 2편을 추천합니다.")

mbti = st.selectbox("당신의 MBTI를 선택하세요:", MBTI_LIST)

if mbti:
    rec = RECOMMENDATIONS.get(mbti)
    if rec is None:
        st.warning("앗! 아직 이 MBTI 유형에 대한 추천 데이터가 준비되지 않았어요 😅")
    else:
        st.markdown(f"### ✨ {mbti}님을 위한 추천 목록")
        st.write("(작품 요약과 추천 이유를 함께 제공합니다.)")

        st.markdown("**📚 책 추천 (2)**")
        for title, note, reason in rec["books"]:
            st.markdown(f"- **{title}** — {note}\n  - 🧭 추천 이유: {reason}")

        st.markdown("**🎬 영화 추천 (2)**")
        for title, note, reason in rec["movies"]:
            st.markdown(f"- **{title}** — {note}\n  - 🧭 추천 이유: {reason}")

        # 센스있는 한 줄 마무리
        closing = {
            "INTJ": "계획표에 하나만 더 추가할까요?",
            "INTP": "호기심을 채울 준비 되셨나요?",
            "ENTJ": "다음 목표는 언제인가요, 리더님?",
            "ENTP": "아이디어는 많고 시간은 부족하죠—즐겨보세요.",
            "INFJ": "오늘은 마음의 울림이 필요할지도 몰라요.",
            "INFP": "감성의 바다로 한 발짝 더 들어가볼까요?",
            "ENFJ": "누군가의 마음을 따뜻하게 만들어볼 시간이에요.",
            "ENFP": "즉흥과 열정으로 오늘을 채워보세요!",
            "ISTJ": "질서와 책임감 속에도 작은 여유를 담아보세요.",
            "ISFJ": "당신의 배려는 세상을 더 아름답게 만듭니다.",
            "ESTJ": "리더십과 현실 감각, 오늘도 완벽하시네요.",
            "ESFJ": "따뜻한 미소로 주위를 환하게 만들어주세요.",
            "ISTP": "조용히, 그러나 완벽하게 해결하실 거잖아요.",
            "ISFP": "감성은 언제나 당신의 강점이에요.",
            "ESTP": "도전과 스릴, 오늘도 멋지게 즐기세요.",
            "ESFP": "세상은 당신의 무대예요, 빛나세요!"
        }
        st.info(closing.get(mbti, "읽고/보신 후에 소감 한 줄 남겨주시면 과학자 비서가 뿌듯해합니다."))

        st.write("---")
        st.caption("이 앱은 Streamlit 기본 라이브러리만으로 작동합니다. 파일명을 'app.py'로 저장하고 Streamlit Cloud에서 실행하세요.")
