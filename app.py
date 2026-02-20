import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="병원 보안 메신저", layout="wide")

# 구글 시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)

# 데이터 불러오기 함수
def load_data():
    return conn.read(ttl=0) # 실시간을 위해 캐시를 0으로 설정

st.title("🏥 병원 스마트 메신저")

# 사이드바 설정
with st.sidebar:
    st.header("👤 내 정보")
    user_id = st.text_input("사번 또는 성함", value="홍길동")
    dept = st.selectbox("소속 부서", ["진료부", "간호부", "행정부", "재활센터", "영양실", "QPS", "감염", "임상병리", "영상의학과"])
    st.write("---")
    target_user = st.text_input("수신자 (전체는 '전체' 입력)", value="전체")

# 메시지 읽어오기
df = load_data()

# 채팅창 구현 (나에게 온 메시지나 전체 메시지만 필터링)
for index, row in df.iterrows():
    if row['receiver'] == "전체" or row['receiver'] == user_id or row['sender'] == user_id:
        with st.chat_message("user" if row['sender'] == user_id else "assistant"):
            st.write(f"**[{row['sender_dept']}] {row['sender']}** → **{row['receiver']}**")
            st.write(row['content'])
            st.caption(str(row['date']))

# 메시지 입력
if prompt := st.chat_input("메시지를 입력하세요..."):
    new_data = pd.DataFrame([{
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sender": user_id,
        "sender_dept": dept,
        "receiver": target_user,
        "receiver_dept": "전체",
        "content": prompt,
        "is_ad": "No",
        "file_url": ""
    }])
    # 시트에 저장
    updated_df = pd.concat([df, new_data], ignore_index=True)
    conn.update(data=updated_df)
    st.rerun()
