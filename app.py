import streamlit as st
import pandas as pd

# ------------------------------------------------
# コールバック関数: 入力欄をクリアする処理
def clear_task_input():
    # 'task_input' というキーを持つセッションステートの値を空にする
    st.session_state.task_input = ""
# ------------------------------------------------


# 1. タイトル
st.title("📝 Streamlit ToDoリスト")

# 2. セッションステートの初期化
if "todos" not in st.session_state:
    st.session_state.todos = []

# --- メイン画面のレイアウト: 2つのカラムに分割 ---
col_add, col_list = st.columns(2)

# --- (A) 左カラム: タスク追加フォーム ---
with col_add:
    st.subheader("➕ タスクの追加")
    
    # タスク入力欄（keyを指定）
    new_task = st.text_input("タスクの内容を入力してください", key="task_input")

    # タスク追加ボタン
    # 'on_click' にタスク追加と入力クリアの両方を行うロジックを直接埋め込む関数を定義
    def add_and_clear():
        if st.session_state.task_input.strip() != "":
            st.session_state.todos.append(
                {"task": st.session_state.task_input.strip(), "done": False}
            )
            # コールバック内で入力欄をクリア
            clear_task_input()

    # on_clickにタスク追加とクリアを行う関数を設定
    st.button("タスクを追加", key="add_button", on_click=add_and_clear)


# --- (B) 右カラム: タスク一覧と削除ロジック ---
with col_list:
    st.subheader("✅ タスク一覧")

    all_tasks_for_analysis = st.session_state.todos.copy()
    remaining_tasks = []

    if not all_tasks_for_analysis:
        st.info("タスクがありません。左側から追加してください。")
    else:
        for i, todo in enumerate(st.session_state.todos):
            checked = st.checkbox(todo["task"], value=todo["done"], key=f"task_{i}")
            
            # チェックされたかどうかの状態を更新
            todo["done"] = checked 

            # チェックされていないタスクのみ残す
            if not checked:
                remaining_tasks.append(todo)

    # タスクリストを更新（削除処理の実行）
    st.session_state.todos = remaining_tasks

# --- (C) サイドバー: 進捗分析 ---
with st.sidebar:
    st.subheader("📊 進捗分析")

    completed_count = sum(1 for t in all_tasks_for_analysis if t["done"])
    incomplete_count = sum(1 for t in all_tasks_for_analysis if not t["done"])
    total_count = len(all_tasks_for_analysis)

    if total_count > 0:
        st.metric("合計タスク数", total_count)
        st.metric("完了したタスク", completed_count)
        st.metric("未完了のタスク", incomplete_count)
        
        # Pandas DataFrame を作成
        df = pd.DataFrame(
            {
                "状態": ["完了", "未完了"],
                "タスク数": [completed_count, incomplete_count],
            }
        )
    
        # 棒グラフ表示
        st.bar_chart(df.set_index("状態"))
    else:
        st.info("分析データがありません。タスクを追加してください。")
