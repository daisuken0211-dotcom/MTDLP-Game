
def start_goal_agreement_mode(goal_text):
    print("\n--- Phase 4: 合意目標設定 ---")
    print("\nまずは、山口美咲さんに対する合意目標を5W1Hで自由記載してください。")
    print("5W1H（Who, What, When, Where, Why, How）を意識して記述しましょう。")

    user_goal = input("\nあなたの合意目標を記述してください：")

    # 5W1Hキーワード
    who_keywords = ["山口美咲"]
    what_keywords = ["通勤", "日程", "生活"]
    when_keywords = ["週5日", "平日"]
    where_keywords = ["瀬戸市", "職場", "モーニング"]
    why_keywords = ["自立", "維持"]
    how_keywords = ["スマートフォン", "カレンダー", "自己管理"]

    score = 0
    if any(kw in user_goal for kw in who_keywords):
        score += 1
    if any(kw in user_goal for kw in what_keywords):
        score += 1
    if any(kw in user_goal for kw in when_keywords):
        score += 1
    if any(kw in user_goal for kw in where_keywords):
        score += 1
    if any(kw in user_goal for kw in why_keywords):
        score += 1
    if any(kw in user_goal for kw in how_keywords):
        score += 1

    print(f"\n▶ 合意目標スコア：{score}/6 点")
    if score >= 5:
        print("◎ 非常に適切な目標設定です！")
    elif score >= 3:
        print("○ 良い視点ですが、さらに5W1Hを意識すると良いです。")
    else:
        print("△ 目標を見直しましょう。以下に先輩の助言として合意目標の例を示します。")
        print("山口美咲さんは、スマートフォンやカレンダーを活用して、日程を自己管理しながら、平日週5日、瀬戸市の自宅から職場へ通勤しつつモーニングに立ち寄る生活を送る。この生活を継続することで自立した生活を維持することを目指す。")

    print("\n--- Phase 3: 合意形成 モード ---")
    print(f"山口さんの希望として聞き取れた内容：\n▶ {goal_text}\n")
    print("この目標が山口さんの真の希望であるかを確認し、合意形成を図っていきます。")
    input("Enterキーで進めてください...")

    print("\n山口さんと話し合いの結果、以下の目標で合意しました：")
    print("▶ 合意目標：山口美咲さんは、スマートフォンやカレンダーを活用して、日程を自己管理しながら、平日週5日、瀬戸市の自宅から職場へ通勤しつつモーニングに立ち寄る生活を送る。この生活を継続することで自立した生活を維持することを目指す。")

    input("\nEnterキーで次（介入フェーズ）へ進みます。")
    return goal_text
