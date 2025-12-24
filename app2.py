import streamlit as st

def main():
    # --- 頁面設定 ---
    st.set_page_config(page_title="贊助挑戰賽", page_icon="🍀")

    # --- 初始化 Session State (狀態管理) ---
    # 我們需要記住目前題號、分數、以及是否已經回答過當前題目
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'is_answered' not in st.session_state:
        st.session_state.is_answered = False

    # --- 題目資料庫 ---
    # 這裡定義多個題目，每個題目包含問題、選項、正確答案
    questions = [
        {
            "question": "本基金會什麼時候創立的",
            "options": [
                "(A) 11月16號",
                "(B) 12月1號",
                "(C) 7月1號",
                "(D) 5月16號"
            ],
            "answer": "(A) 11月16號"
        },

        {
            "question": "下列敘述何者 '錯誤'？",
            "options": [
                "(A) 12月25日是聖誕節",
                "(B) 11月是重要的月份",
                "(C) 5月是重要的月份",
                "(D) 2月通常有29天"
            ],
            "answer": "(D) 2月通常有29天"
        },
        
        {
            "question": "王小姐通常會在甚麼時候不遵守承諾",
            "options": [
                "(A) 吃飯",
                "(B) 睡覺",
                "(C) 讀書",
                "(D) 工作"
            ],
            "answer": "(B) 睡覺"
        },

        {
            "question": "本基金會宗旨不是甚麼",
            "options": [
                "(A) 讓王小姐開心",
                "(B) 讓王小姐好好吃飯",
                "(C) 讓王小姐好好睡覺",
                "(D) 讓王小姐生氣"
            ],
            "answer": "(D) 讓王小姐生氣"
        }
    ]

    # --- 標題與分數顯示 ---
    st.title("🍀 回答正確獲得大獎")
    st.write(f"目前得分： **{st.session_state.score} 分**")
    st.divider()

    # --- 判斷測驗是否結束 ---
    if st.session_state.current_question_index >= len(questions):
        st.balloons()  # 撒花特效
        final_score = st.session_state.score
        st.header(f"🎉 測驗結束！最終得分：{final_score} / {len(questions)}")
        if final_score <= 1:
            st.error("你很不會回答，本基金會只贊助100元")
        elif 2 <= final_score <= 3:
            st.info("還不錯，本基金會贊助300元")
        elif final_score >= 4:
            st.success("你很棒，本基金會贊助500元")
        
        if st.button("重新開始"):
            # 重置所有狀態
            st.session_state.current_question_index = 0
            st.session_state.score = 0
            st.session_state.is_answered = False
            st.rerun() # 重新執行頁面
        return

    # --- 取得目前題目 ---
    current_q = questions[st.session_state.current_question_index]

    # --- 顯示題目 (Info 樣式) ---
    st.info(f"第 {st.session_state.current_question_index + 1} 題：\n\n{current_q['question']}")

    # --- 選項互動區 ---
    st.markdown("### 請選擇你的答案：")
    
    # 使用 key 來區分每一題的選項狀態，避免換題時殘留上一題的選擇
    # disabled=st.session_state.is_answered 讓使用者在送出後不能修改答案
    user_choice = st.radio(
        "選項", 
        current_q["options"], 
        index=None, 
        label_visibility="collapsed",
        key=f"q_{st.session_state.current_question_index}",
        disabled=st.session_state.is_answered 
    )

    # --- 按鈕邏輯區 ---
    
    # 情況 1: 還沒回答 -> 顯示「送出答案」按鈕
    if not st.session_state.is_answered:
        if st.button("送出答案"):
            if user_choice is None:
                st.warning("請先選擇一個答案！")
            else:
                # 鎖定狀態為已回答
                st.session_state.is_answered = True
                
                # 檢查答案並加分
                if user_choice == current_q["answer"]:
                    st.session_state.score += 1
                
                st.rerun() # 重新整理頁面以顯示結果

    # 情況 2: 已經回答 -> 顯示結果與「下一題」按鈕
    else:
        # 顯示結果回饋
        if user_choice == current_q["answer"]:
            st.success(f"🎉 答對了！答案是 {current_q['answer']}")
        else:
            st.error(f"❌ 答錯了！正確答案是 {current_q['answer']}，你選擇了 {user_choice}")

        # 無論對錯，都顯示下一題按鈕
        if st.button("下一題 ➡"):
            st.session_state.current_question_index += 1
            st.session_state.is_answered = False # 重置回答狀態
            st.rerun() # 進入下一題

if __name__ == "__main__":
    main()