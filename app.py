import streamlit as st

# --- 1. 앱 기본 설정 ---
st.set_page_config(page_title="행정법 OX 훈련소", page_icon="⚖️")
st.title("🎯 이승민의 콕! 행정법 실전 OX")

# --- 2. 수험생 진행 상태 저장 ---
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0         # 현재 문제 번호
    st.session_state.score = 0               # 점수
    st.session_state.wrong_notes = []        # 틀린 문제 보관함
    st.session_state.mode = 'normal'         # 'normal'(실전) or 'review'(오답)
    st.session_state.show_exp = False        # 해설 노출 여부
    st.session_state.is_correct = False      # 정답 여부

# --- 3. 문제 데이터베이스 ---
# 💡 여기에 첨부하실 교재의 지문, 정답, 해설을 추가하시면 됩니다.
all_questions = [
    {
        "id": 1, 
        "q": "통치행위는 고도의 정치적 성격을 띠는 국가행위로서 사법심사의 대상에서 제외될 수 있으나, 헌법재판소는 국민의 기본권 침해와 직접 관련되는 경우에는 심사 대상이 된다고 본다.", 
        "a": "O", 
        "exp": "대법원과 헌법재판소 모두 통치행위를 인정하나, 헌법재판소는 기본권 침해와 직접 관련된 경우 사법심사가 가능하다고 판시하였습니다."
    },
    {
        "id": 2, 
        "q": "신뢰보호의 원칙상 행정청의 공적인 견해표명 여부를 판단할 때에는 반드시 행정조직상의 형식적 권한분장에 구속된다.", 
        "a": "X", 
        "exp": "조직상의 권한 유무에 구속되지 않고, 상대방의 신뢰가능성을 기준으로 실질적으로 판단해야 합니다."
    },
    {
        "id": 3, 
        "q": "행정처분의 무효확인소송에서는 사정판결이 허용된다.", 
        "a": "X", 
        "exp": "행정소송법상 무효확인소송에는 사정판결 규정이 준용되지 않으므로 허용되지 않습니다."
    }
]

# 출제 모드에 따른 문제 목록 설정
active_q = st.session_state.wrong_notes if st.session_state.mode == 'review' else all_questions

# --- 4. 정답 채점 및 진행 함수 ---
def check_ans(user_ans):
    correct_ans = active_q[st.session_state.current_idx]['a']
    if user_ans == correct_ans:
        st.session_state.score += 1
        st.session_state.is_correct = True
    else:
        st.session_state.is_correct = False
        q_data = active_q[st.session_state.current_idx]
        if q_data not in st.session_state.wrong_notes:
            st.session_state.wrong_notes.append(q_data)
    st.session_state.show_exp = True

def next_q():
    st.session_state.current_idx += 1
    st.session_state.show_exp = False

# --- 5. 앱 화면 UI 구성 ---
# 준비된 문제를 모두 풀었을 때 (결과 및 오답 반복)
if st.session_state.current_idx >= len(active_q):
    st.success("🎉 준비된 문제를 모두 완료하셨습니다!")
    
    if st.session_state.mode == 'normal':
        st.subheader(f"🏆 최종 점수: {st.session_state.score} / {len(all_questions)}점")
    
    # 틀린 문제가 있을 경우 오답 무한반복 기능 활성화
    if st.session_state.wrong_notes:
        st.warning(f"🔥 복습해야 할 오답: {len(st.session_state.wrong_notes)}개")
        if st.button("📝 틀린 문제만 다시 풀기", use_container_width=True):
            st.session_state.current_idx = 0
            st.session_state.score = 0
            st.session_state.mode = 'review'
            st.session_state.show_exp = False
            st.rerun()
    else:
        st.balloons()
        st.info("완벽합니다! 틀린 문제가 하나도 없습니다.")
        
    st.markdown("---")
    if st.button("🔄 처음부터 전체 다시 풀기", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# 문제 풀이 진행 중 화면
else:
    q_data = active_q[st.session_state.current_idx]
    mode_str = "🔥 [오답 복습 무한반복]" if st.session_state.mode == 'review' else "📚 [실전 문제 풀이]"
    
    st.caption(f"{mode_str} 진행률: {st.session_state.current_idx + 1} / {len(active_q)}")
    st.progress((st.session_state.current_idx) / len(active_q))
    
    st.markdown(f"### Q. {q_data['q']}")
    st.write("")
    
    # 정답 입력 전
    if not st.session_state.show_exp:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⭕ 맞다 (O)", use_container_width=True): check_ans("O")
        with col2:
            if st.button("❌ 틀리다 (X)", use_container_width=True): check_ans("X")
            
    # 정답 입력 후 (해설 및 정답 확인)
    else:
        if st.session_state.is_correct:
            st.success("정답입니다! 👏")
        else:
            st.error(f"오답입니다. (정답: {q_data['a']}) 🥲")
            
        st.info(f"💡 **해설:** {q_data['exp']}")
        
        if st.button("다음 문제 ➡️", use_container_width=True):
            next_q()
            st.rerun()
