
def start_assessment_mode():
    print("\n--- Phase 2: アセスメント モード ---")
    print("山口さんの希望する生活行為の達成を妨げている要因、山口さんの現状の強みの視点から、必要と思われる評価項目を選びましょう。")
    input("Enterキーで開始します...")

    cards = [
        ("バスの時刻を覚えておけるか", "心身機能", "b144", 10),
        ("職場までの通勤ルートを歩けるか", "活動", "d460", 10),
        ("通勤ルートを確認し、起こりうるリスクの把握をする（歩道・信号等）", "環境因子", "e150", 10),
        ("送迎車の利用が可能か（送迎車がどの様な状態かを確認する）", "環境因子", "e310", 7),
        ("料理の頻度", "活動", "d630", 2),
        ("右上肢の筋力（MMT）", "心身機能", "b730", 7),
        ("天候等の変化に対応出来るか", "環境因子", "e225", 8),
        ("家族の同意・支援", "環境因子", "e310", 9),
        ("スケジュールの自己管理", "心身機能", "b1642", 8),
        ("HDS-Rスコア", "心身機能", "b117", 9),
        ("スマホの利用能力はどうか。地図アプリは使えるか", "活動", "d360", 6),
        ("週5日間の勤務を維持できるか", "活動", "d850", 10),
        ("困った際に連絡することが出来るか", "環境因子", "e540", 10),
        ("自宅内の整理整頓", "活動", "d640", 5),
        ("娘がどの程度協力できるか。今後の生活の変化においても対応できるか", "環境因子", "e310", 7),
        ("近所の方や、会社の方の相談支援の状況はどうか", "環境因子", "e580", 6)
    ]

    selected_cards = []
    print("カードは全て大切です。その中からより適切だと思うものを8枚選んでください。")
    for i, (text, category, code, score) in enumerate(cards):
        print(f"{i+1}: {text}（{category}, {code}）")

    while len(selected_cards) < 8:
        try:
            choice = int(input(f"選択 {len(selected_cards)+1}/8 → 番号を入力："))
            if 1 <= choice <= len(cards):
                selected_cards.append(cards[choice - 1])
            else:
                print("無効な番号です。")
        except ValueError:
            print("数字を入力してください。")

    print("\n=== アセスメント選択結果 ===")
    total_score = 0
    for card in selected_cards:
        print(f"- {card[0]}（{card[1]}, {card[2]}）")
        total_score += card[3]
    print(f"合計スコア：{total_score}点")

    input("\nEnterキーで次へ進みます。")
    return selected_cards
