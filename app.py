# app.py
import streamlit as st
import pandas as pd

st.title("📝 ToDoリスト")

# セッションステートの初期化
if "todos" not in st.session_state:
    # 各タスクは {"task": str, "done": bool} で管理
    st.session_state.todos = []

# タスク入力欄
new_task = st.text_input("新しいタスクを入力してください")

# タスク追加ボタン
if st.button("タスクを追加"):
    if new_task.strip() != "":
        st.session_state.todos.append(
            {"task": new_task.strip(), "done": False}
        )

st.subheader("タスク一覧")

# 削除後に残すタスク
remaining_tasks = []

for i, todo in enumerate(st.session_state.todos):
    checked = st.checkbox(todo["task"], key=f"task_{i}")
    todo["done"] = checked

    # チェックされていないタスクのみ保持（＝チェックされたら削除）
    if not checked:
        remaining_tasks.append(todo)

# 進捗計算用に、削除前の状態を保存
all_tasks = st.session_state.todos.copy()

# タスク更新
st.session_state.todos = remaining_tasks

# ===== 進捗分析 =====
st.subheader("📊 進捗分析")

completed_count = sum(1 for t in all_tasks if t["done"])
incomplete_count = sum(1 for t in all_tasks if not t["done"])

# Pandas DataFrame を作成
df = pd.DataFrame(
    {
        "状態": ["完了", "未完了"],
        "タスク数": [completed_count, incomplete_count],
    }
)

# 棒グラフ表示
st.bar_chart(df.set_index("状態"))
