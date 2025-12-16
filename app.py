import streamlit as st
import pandas as pd

# 1. タイトル
st.title("📝 Streamlit ToDoリスト")

# 2. セッションステートの初期化
if "todos" not in st.session_state:
    # 各タスクは {"task": str, "done": bool} で管理
    st.session_state.todos = []


# --- メイン画面のレイアウト: 2つのカラムに分割 ---
col_add, col_list = st.columns(2)

# --- (A) 左カラム: タスク追加フォーム ---
with col_add:
    st.subheader("➕ タスクの追加")
    
    # タスク入力欄（keyを指定して、ボタンを押した後にクリアしやすくする）
    new_task = st.text_input("タスクの内容を入力してください", key="task_input")

    # タスク追加ボタン
    if st.button("タスクを追加", key="add_button"):
        if new_task.strip() != "":
            st.session_state.todos.append(
                {"task": new_task.strip(), "done": False}
            )
            # UX改善: 追加後に入力欄をクリア
            st.session_state.task_input = ""
            # 再実行してリストを即座に更新 (必須ではないが、より快適な操作感に)
            st.rerun()

# --- (B) 右カラム: タスク一覧と削除ロジック ---
# このセクションでタスクの表示と更新（チェックボックスの操作）を行います
with col_list:
    st.subheader("✅ タスク一覧")

    # 進捗計算用に、現在のタスクリストの状態をコピー
    # (この後のチェックボックス操作と削除ロジックで st.session_state.todos が更新されるため)
    all_tasks_for_analysis = st.session_state.todos.copy()
    
    remaining_tasks = []

    if not all_tasks_for_analysis:
        st.info("タスクがありません。左側から追加してください。")
    else:
        for i, todo in enumerate(st.session_state.todos):
            # チェックボックスを表示し、状態をセッションステートに反映
            # todo["done"] を初期値として使用
            checked = st.checkbox(todo["task"], value=todo["done"], key=f"task_{i}")
            
            # チェックされたかどうかの状態を更新
            todo["done"] = checked 

            # チェックされていないタスクのみ残す（＝チェックされたら削除される元のロジック）
            if not checked:
                remaining_tasks.append(todo)

    # タスクリストを更新（削除処理の実行）
    st.session_state.todos = remaining_tasks

# --- (C) サイドバー: 進捗分析 ---
# 進捗分析は st.session_state.todos の最新の状態に基づいて計算されます
with st.sidebar:
    st.subheader("📊 進捗分析")

    # 計算には、右カラムの処理の直前でコピーした all_tasks_for_analysis を使用します
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
