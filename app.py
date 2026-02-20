import streamlit as st

# 1. 앱 페이지 설정
st.set_page_config(page_title="병원 메신저", page_icon="🏥")

# 2. 제목
st.title("🏥 병원 스마트 메신저")
st.caption("병원 업무 효율화를 위한 실시간 소통 도구")

# 3. 사용자 정보 설정 (사이드바)
with st.sidebar:
    st.header("👤 내 정보")
    user_name = st.text_input("성함 또는 사번", value="홍길동")
    
    # '행정'에서 '행정부'로 수정되었습니다.
    dept = st.selectbox("소속 부서", [
        "진료부", "간호부", "행정부", "재활센터", 
        "영양실", "QPS", "감염", "임상병리", "영상의학과"
    ])
    st.write("---")
    st.caption("양지 AI 스터디 그룹 제작")

# 4. 채팅 화면 로직
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 메시지 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(f"**{msg['user']} ({msg['dept']})**")
        st.write(msg["content"])

# 메시지 입력
if prompt := st.chat_input("메시지를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "user": user_name, "dept": dept, "content": prompt})
    st.rerun()
