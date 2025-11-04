import streamlit as st
import random
import time

# Streamlit 공포 게임 - 단일 파일 (설치 필요 라이브러리 없음)
# 배포: GitHub에 push 한 뒤 Streamlit Cloud에 연결하세요.

st.set_page_config(page_title="공포게임", layout="centered")

# 기본 CSS로 공포 분위기 연출
st.markdown("""
<style>
body {
  background: radial-gradient(circle at 10% 10%, #0b0b0b 0%, #050505 40%, #000000 100%);
  color: #e6e6e6;
}
.title-flicker {
  font-family: 'Courier New', monospace;
  font-size: 40px;
  text-align: center;
  letter-spacing: 2px;
  animation: flicker 3s infinite;
}
@keyframes flicker {
  0% { opacity: 1; text-shadow: 0 0 8px rgba(255,255,255,0.06);} 
  50% { opacity: 0.6; text-shadow: 0 0 30px rgba(255,0,0,0.06);} 
  100% { opacity: 1; text-shadow: 0 0 8px rgba(255,255,255,0.06);} 
}
.card {
  background: rgba(0,0,0,0.55);
  border-radius: 12px;
  padding: 18px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.7);
}
.choice {
  margin-top: 8px;
}
.small {
  font-size: 13px;
  color: #cfcfcf;
}
</style>
""", unsafe_allow_html=True)

# 초기화
if 'scene' not in st.session_state:
    st.session_state.scene = 'intro'
if 'fear' not in st.session_state:
    st.session_state.fear = 0  # 0~100
if 'torch' not in st.session_state:
    st.session_state.torch = False
if 'found_note' not in st.session_state:
    st.session_state.found_note = False
if 'alive' not in st.session_state:
    st.session_state.alive = True
if 'history' not in st.session_state:
    st.session_state.history = []

# 도우미 함수
def add_history(text):
    st.session_state.history.append(text)

def increase_fear(amount):
    st.session_state.fear = min(100, st.session_state.fear + amount)

def chance(percent):
    return random.random() < percent/100.0

# 화면 렌더링
st.markdown('<div class="title-flicker">어둠 속의 속삭임</div>', unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)

# 진행도 바
st.progress(int(st.session_state.fear))
st.markdown(f"**공포 지수:** {st.session_state.fear}/100")

# 게임 씬들
if st.session_state.scene == 'intro':
    st.write('당신은 낯선 건물의 문턱에 서 있습니다. 바람 한 줌이 등골을 타고 내려갑니다. 누군가 부른 듯한 속삭임이 들립니다...')
    st.write('무엇을 하시겠습니까?')
    col1, col2 = st.columns(2)
    with col1:
        if st.button('들어간다'):
            add_history('문을 열고 안으로 들어갔다.')
            increase_fear(10)
            st.session_state.scene = 'foyer'
    with col2:
        if st.button('돌아간다'):
            add_history('그대로 돌아섰다. 하지만 뒤에는 길이 없다...')
            increase_fear(5)
            st.session_state.scene = 'foyer'

elif st.session_state.scene == 'foyer':
    st.write('어두운 현관입니다. 손전등이 바닥에 떨어져 있습니다. 계단은 위와 아래로 이어져 있습니다.')
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('손전등 줍기'):
            if not st.session_state.torch:
                st.session_state.torch = True
                add_history('손전등을 주웠다. 어둠이 조금 물러났다.')
                st.write('손전등이 켜졌다. 희미한 빛이 주변을 비춘다.')
            else:
                st.write('이미 손전등을 가지고 있다.')
    with col2:
        if st.button('위층으로'):
            add_history('위층으로 향했다.')
            increase_fear(8)
            st.session_state.scene = 'upstairs'
    with col3:
        if st.button('지하로'):
            add_history('지하로 내려갔다.')
            increase_fear(12)
            st.session_state.scene = 'basement'

elif st.session_state.scene == 'upstairs':
    st.write('복도에는 여러 개의 문이 있고, 끝에는 창문 하나가 반쯤 열려 있습니다. 창문 너머 달빛이 손전등과 겹쳐 보입니다.')
    st.write('어떤 문을 선택하겠습니까?')
    c1, c2 = st.columns(2)
    with c1:
        if st.button('왼쪽 방'):
            add_history('왼쪽 방을 열었다.')
            if chance(40):
                st.write('방 안에 오래된 일기장이 있었다. 페이지를 넘기자 발자국이 생생히 느껴졌다.')
                st.session_state.found_note = True
                increase_fear(6)
            else:
                st.write('비어 있었다. 하지만 공기는 차갑다.')
                increase_fear(4)
    with c2:
        if st.button('오른쪽 방'):
            add_history('오른쪽 방을 열었다.')
            if st.session_state.torch:
                st.write('손전등 덕분에 세심히 살필 수 있었다. 그림자 하나가 천장에 스치고 지나갔다.')
                increase_fear(8)
            else:
                st.write('어둠 속에서 무언가 스치고 지나간다...')
                increase_fear(15)
    if st.button('복도로 돌아가기'):
        st.session_state.scene = 'foyer'

elif st.session_state.scene == 'basement':
    st.write('지하는 습기와 냄새로 가득하다. 벽에는 오래된 글씨가 희미하게 보인다.')
    if not st.session_state.found_note and chance(30):
        st.write('바닥 틈에서 종이 조각을 발견했다. "돌아가라" 라고 쓰여 있다.')
        st.session_state.found_note = True
        increase_fear(10)
    col1, col2 = st.columns(2)
    with col1:
        if st.button('깊은 방으로'):
            add_history('지하 깊은 방으로 들어갔다.')
            # 위험한 선택
            if st.session_state.torch:
                st.write('손전등으로 구석을 비추자, 오래된 인형이 당신을 바라본다. 그것의 눈이 반짝인다.')
                if chance(35):
                    st.write('인형이 손을 뻗었다...')
                    increase_fear(25)
                else:
                    st.write('인형은 그저 오래된 장난감일 뿐이었다.')
                    increase_fear(10)
            else:
                st.write('어둠 속에서 무언가가 달려들었다.')
                increase_fear(40)
            # 생사 결정
            if st.session_state.fear >= 80 and chance(60):
                st.write('갑자기 숨이 막히는 공포가 몰려왔다... 정신을 잃었다.')
                st.session_state.alive = False
                st.session_state.scene = 'end_bad'
            else:
                st.write('간신히 빠져나왔다. 숨이 가쁘다.')
                st.session_state.scene = 'foyer'
    with col2:
        if st.button('도망친다'):
            add_history('급히 도망쳤다.')
            increase_fear(5)
            st.session_state.scene = 'foyer'

elif st.session_state.scene == 'end_bad':
    st.markdown('<h3>당신은 어둠 속에 잠겼다...</h3>', unsafe_allow_html=True)
    st.write('끝이 아닌 끝. 기억 저편으로 사라져 간다.')
    if st.button('다시 시작'):
        for k in ['scene','fear','torch','found_note','alive','history']:
            if k in st.session_state:
                del st.session_state[k]
        st.experimental_rerun()

# 단서 기반의 '좋은' 엔딩으로 이동할 수 있는 기회
if st.session_state.alive and st.session_state.scene not in ['end_bad', 'intro']:
    if st.session_state.found_note and st.session_state.torch and chance(25):
        st.session_state.scene = 'secret'

if st.session_state.scene == 'secret':
    st.write('벽에 숨은 문틈이 보인다. 당신이 모은 단서가 반응하는 것 같다.')
    if st.button('문을 연다'):
        add_history('숨겨진 문을 발견하고 열었다.')
        if st.session_state.fear < 60:
            st.session_state.scene = 'end_good'
        else:
            st.session_state.scene = 'end_bad'

if st.session_state.scene == 'end_good':
    st.markdown('<h3>당신은 탈출했다.</h3>', unsafe_allow_html=True)
    st.write('달빛 아래, 당신은 숨을 크게 쉬며 어둠에서 벗어났다. 하지만 속삭임은 언제든 돌아올 수 있다...')
    if st.button('다시 하기'):
        for k in ['scene','fear','torch','found_note','alive','history']:
            if k in st.session_state:
                del st.session_state[k]
        st.experimental_rerun()

# 히스토리 보기
with st.expander('여정 기록'):
    if st.session_state.history:
        for i, h in enumerate(st.session_state.history, 1):
            st.markdown(f"{i}. {h}")
    else:
        st.write('아직 아무 일도 일어나지 않았습니다.')

st.markdown('</div>', unsafe_allow_html=True)

# 작은 도움말
st.markdown('<div class="small">속삭이는 말투로 게임의 문장들을 바꿔보고 싶다면 코드의 문장들을 수정하세요. 이 파일은 Streamlit Cloud에 바로 배포할 수 있습니다.</div>', unsafe_allow_html=True)
