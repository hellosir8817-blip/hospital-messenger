import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="병원 보안 메신저", layout="wide")

# 구글 시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)

# 데이터 불러오기 (에러 방지를 위해 빈 시트일 경우 대비)
try:
    df = conn.read(ttl=0)
except:
    # 시트가 완전히 비어있을 경우 초기 데이터 프레임 생성
    df = pd.DataFrame(columns=["date", "sender", "sender_dept", "receiver", "receiver_dept", "content", "is_ad", "file_url"])

st.title("🏥 병원 스마트 메신저")

with st.sidebar:
    st.header("👤 내 정보")
    user_id = st.text_input("사번 또는 성함", value="홍길동")
    dept = st.selectbox("소속 부서", ["진료부", "간호부", "행정부", "재활센터", "영양실", "QPS", "감염", "임상병리", "영상의학과"])
    st.write("---")
    target_user = st.text_input("수신자 (전체는 '전체' 입력)", value="전체")

# 메시지 표시
if not df.empty:
    for index, row in df.iterrows():
        # 내 메시지이거나, 나에게 온 메시지이거나, 전체 메시지인 경우만 표시
        if str(row['receiver']) == "전체" or str(row['receiver']) == user_id or str(row['sender']) == user_id:
            with st.chat_message("user" if row['sender'] == user_id else "assistant"):
                st.write(f"**[{row['sender_dept']}] {row['sender']}** → **{row['receiver']}**")
                st.write(row['content'])
                st.caption(str(row['date']))

# 메시지 입력
if prompt := st.chat_input("메시지를 입력하세요..."):
    new_record = pd.DataFrame([{
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sender": user_id,
        "sender_dept": dept,
        "receiver": target_user,
        "receiver_dept": "전체",
        "content": prompt,
        "is_ad": "No",
        "file_url": ""
    }])
    
    # 기존 데이터에 새 레코드 추가
    updated_df = pd.concat([df, new_record], ignore_index=True)
    
    # 시트 업데이트 (안정적인 방식으로 변경)
    conn.update(data=updated_df)
    st.cache_data.clear() # 캐시 강제 삭제
    st.rerun()
