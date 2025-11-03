import streamlit as st
st.title('Salam Project')
password=st.text_input('암호을 임력하세요.')
if st.button('button'):
  st.write(password+'님 안녕하세요.')
