# app.py
import streamlit as st

st.title("📝 ToDoリスト")

# セッションステートの初期化
if "todos" not in st.session_state:
    st.session_state.todos = []

# タスク入力欄
new_task = st.text_input("新しいタスクを入力してください")

# タスク追加ボタン
if st.button("タスクを追加"):
    if new_task.strip() != "":
        st.session_state.todos.append(new_task.strip())

# ToDoリストの表示
st.subheader("タスク一覧")

# 削除対象を一時的に保存するリスト
tasks_to_keep = []

for i, task in enumerate(st.session_state.todos):
    checked = st.checkbox(task, key=f"task_{i}")
    # チェックされていないタスクのみ保持
    if not checked:
        tasks_to_keep.append(task)

# チェックされたタスクを削除
st.session_state.todos = tasks_to_keep
