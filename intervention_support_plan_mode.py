
def start_intervention_support_plan_mode():
    print("\n=== Phase 6: 支援調整フェーズ（実践思考） ===")
    print("山口さんの状況に応じて、どの支援者に何を依頼すべきかを選びましょう。")

    questions = [
        {
            "situation": "金銭管理の見守りを娘にお願いしたいが、制度的な後見人の相談が必要な段階です。どこに相談すべきですか？",
            "choices": [
                "訪問リハビリの作業療法士",
                "市役所の地域包括支援センター",
                "病院の受付窓口",
                "喫茶店のスタッフ"
            ],
            "answer": 1
        },
        {
            "situation": "最近予定を忘れることが増えてきており、生活リズムを維持したいと思っています。何を誰に依頼するべき？",
            "choices": [
                "カレンダー設置と活用を娘に依頼する",
                "スケジュール管理表を喫茶店に掲示する",
                "職場に毎日の声かけを依頼する",
                "スマホに予定を送信するようケアマネに依頼"
            ],
            "answer": 0
        },
        {
            "situation": "職場で軽度のミスが増えたとき、周囲とどのように連携すべき？",
            "choices": [
                "医師に診断書を書いてもらい、職場に送る",
                "職場スタッフに変化を気づいたら娘やケアマネジャーに連絡するよう依頼",
                "バス運転手に出勤日を毎回伝える",
                "娘に毎日電話してもらう"
            ],
            "answer": 1
        },
        {
            "situation": "将来、就労継続が困難になった場合の代替手段を検討したいとき、どの支援者に何を依頼？",
            "choices": [
                "医師に辞めるかどうか判断を委ねる",
                "喫茶店で働けるか打診する",
                "生活相談員に福祉的就労の情報提供を依頼、作業療法士に職場での評価を依頼",
                "職場に仕事内容を軽くしてもらう"
            ],
            "answer": 2
        }
    ]

    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\nQ{i}: {q['situation']}")
        for idx, opt in enumerate(q["choices"], 1):
            print(f"{idx}. {opt}")
        ans = input("番号を選んでください：")
        if ans.isdigit() and int(ans) - 1 == q["answer"]:
            print("→ 適切な対応です。")
            score += 10
        else:
            correct = q["choices"][q["answer"]]
            print(f"→ 適切ではありません。正解は「{correct}」です。")

    print(f"\n=== 支援調整スコア：{score}点 ===")
    if score >= 30:
        print("実践的な支援調整力があります。支援者との連携も適切です。")
    elif score >= 20:
        print("まずまずですが、一部調整の視点が弱い部分があります。")
    else:
        print("支援の調整について再学習が必要です。")

    input("\nEnterキーで終了します。")
