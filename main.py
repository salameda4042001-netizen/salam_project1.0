import streamlit as st
st.title('Salam Project')
password=st.text_input('암호을 임력하세요.')
Choice=st.selectbox('선택하세요:',['clzls','vlwk'])
if st.button('button'):
  st.info(password+'님 안녕하세요.')
  st.warning(Choice+'반갑습니다.')
  st.error('dlqslek.')
  st.balloons()
