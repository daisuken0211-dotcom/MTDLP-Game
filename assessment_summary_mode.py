def start_assessment_summary_mode(selected_cards, goal_text):
    print("\n--- Phase 2.5: アセスメント演習シート表示モード ---")
    print("\n◆ 生活行為目標（聞き取りから抽出）：")
    print(f"▶ {goal_text}\n")

    print("◆ 選択されたアセスメント項目：")
    for desc, domain, icf, _ in selected_cards:
        print(f"- {desc}（{domain}, {icf}）")

    print("\n◆ 先輩のヒント（予後予測のポイント）：")
    print("- 娘の支援：夜間訪問、しばらく同居、将来は別居予定")
    print("- 会社の支援：理解ある社長・同僚、仕事の配慮あり")
    print("- 環境の変化：娘の結婚、夫の単身赴任→定年後合流予定")
    print("- 認知症の進行：現状は軽度、今後進行の可能性")
    print("- 多職種支援：OT、医療、家族、地域支援の連携が鍵")
    print("- 合意目標へつなげるには、5W1Hを意識しよう")

    print("\n◆ あなたの1ヶ月後の予後予測を自由に記述してください：")
    month1 = input("→ ")

    print("\n◆ あなたの3ヶ月後の予後予測を自由に記述してください：")
    month3 = input("→ ")

    # キーワード定義
    keywords = ['通勤', '娘', '支援', '認知症', '時間', 'カレンダー', 'スマホ', '習慣', 'モーニング', '会社']

    def score_text(text):
        return sum(1 for word in keywords if word in text)

    score1 = score_text(month1)
    score3 = score_text(month3)
    total_score = score1 + score3

    print(f"\n▶ あなたの予後予測スコアは：{total_score}/20 点です。")
    if total_score >= 15:
        print("◎ 非常に良い予後予測です！")
    elif total_score >= 10:
        print("○ 良い着眼点ですが、もう少し深めても良いでしょう。")
    else:
        print("△ 予後予測を見直しましょう。")
        while True:
            choice = input("再記入しますか？（1: はい / 2: 先輩の予後予測を確認）→ ")
            if choice == "1":
                return start_assessment_summary_mode(selected_cards, goal_text)
            elif choice == "2":
                print("\n【先輩の予後予測】")
                print("【1ヶ月】")
                print("山口美咲さんは、娘の夜間訪問支援とカレンダーの活用により、通勤時刻やモーニングの予定を把握することができる。")
                print("スマートフォンのリマインダー機能を補助に用い、時間の管理と習慣の定着ができる。")
                print("認知症による記憶障害はあるが、現在は軽度であり、職場の社長や同僚の理解のもと、通勤と事務作業を継続できる。")

                print("\n【3ヶ月】")
                print("山口美咲さんは、引き続き週5日間バス通勤を維持し、途中のモーニングでの立ち寄りも生活の一部と実施可能。")
                print("娘は結婚後も近隣に住み、夜間の声かけや支援が継続できる。時間の管理はスマホのアプリとカレンダーを併用することで改善され、")
                print("職場からの支援や喫茶店の店員の支援、OT等の多職種支援により継続可能。")
                print("現在の自立生活が維持されているが、今後の環境変化を見据えた支援体制の見直しを担当ケアマネと共に共有可能。")
                break
            else:
                print("無効な入力です。1か2を入力してください。")

    input("\nEnterキーで次に進みます。")