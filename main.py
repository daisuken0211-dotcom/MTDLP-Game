# --- web/自動起動でも落ちない print ラッパ ---
import builtins
_real_print = print
def safe_print(*args, **kwargs):
    try:
        _real_print(*args, **kwargs)
    except Exception:
        pass  # 出力先が無い環境でもエラーで止めない
builtins.print = safe_print
# ------------------------------------------------

from mtdlp_mode import start_mtdlp_mode
from daughter_feedback_mode import start_daughter_feedback_mode
from goal_question_training_mode import start_goal_question_training_mode  # 修正
from assessment_mode import start_assessment_mode
from assessment_summary_mode import start_assessment_summary_mode
from goal_agreement_mode import start_goal_agreement_mode
from intervention_mode import start_intervention_mode
from intervention_support_match_mode import start_intervention_support_match_mode
from intervention_support_plan_mode import start_intervention_support_plan_mode

def main():
    start_mtdlp_mode()
    start_daughter_feedback_mode()
    start_goal_question_training_mode()

    goal_text = "週5日、バスに乗って仕事に行く。通勤の途中にモーニングに寄る生活を続けたい。"
    print("\n--- 生活行為目標の確認 ---")
    print("山口美咲さんの生活行為目標は以下の通りです：")
    print(f"『{goal_text}』")
    input("この生活行為目標に基づき、次に必要な評価項目を選んでください。Enterキーでアセスメントに進みます。")

    selected_cards = start_assessment_mode()
    start_assessment_summary_mode(selected_cards, goal_text)
    goal = start_goal_agreement_mode(goal_text)
    start_intervention_mode(goal)
    start_intervention_support_match_mode()
    start_intervention_support_plan_mode()

if __name__ == "__main__":
    main()

# --- オープニングON/OFF ---
try:
    from opening_scene import run_opening_then_start
    ENABLE_OPENING = True     # 導入パートを表示する（Falseにすると従来起動）
except Exception:
    ENABLE_OPENING = False    # opening_scene.pyが無い場合は自動でスキップ

def _entrypoint():
    """
    既存ゲームのエントリポイントを自動検出して起動。
    1) mode_select.start_mode_select()
    2) mtdlp_mode.start_mtdlp_mode()
    3) このファイル内の main() があれば main()
    """
    # 1) モード選択があれば最優先
    try:
        from mode_select import start_mode_select
        if callable(start_mode_select):
            start_mode_select()
            return
    except Exception:
        pass

    # 2) MTDLPモードがあれば次に起動
    try:
        from mtdlp_mode import start_mtdlp_mode
        if callable(start_mtdlp_mode):
            start_mtdlp_mode()
            return
    except Exception:
        pass

    # 3) 既存 main() が定義されていれば最後に呼ぶ
    try:
        _maybe_main = globals().get("main", None)
        if callable(_maybe_main):
            _maybe_main()
            return
    except Exception:
        pass

    # どれも無ければ通知
    print("[main.py] エントリポイントが見つかりませんでした。mode_select / mtdlp_mode / main を確認してください。")

if __name__ == "__main__":
    if ENABLE_OPENING:
        # 導入（街の様子・登場人物紹介）→ 本編
        run_opening_then_start(_entrypoint)
    else:
        # 従来通りに本編のみ
        _entrypoint()

