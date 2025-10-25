def start_goal_induction_phase():
    print("=== MTDLP目標誘導フェーズ：山口 美咲さん ===\n")
    print("山口さん（52歳）は若年性認知症の診断を受けており、記憶の保持に課題があります。")
    print("作業療法士として、生活の中で大切にしたい活動を引き出す質問をしていきましょう。")
    input("Enterキーで質問開始...")

    score = 0
    hints = []

    # 質問1
    print("\nQ1: まずどんな質問をしますか？")
    print("1: 『普段、どんな生活をされていますか？』")
    print("2: 『最近、不安に思うことはありますか？』")
    print("3: 『一人で何か困っていることはありますか？』")
    q1 = input("番号を選んでください：")
    if q1 == "2":
        print("山口さん「バスに乗るとき、降りる場所を忘れそうで怖いんです」")
        hints.append("バス移動")
        score += 10
    elif q1 == "1":
        print("山口さん「毎日家事をして、たまにメモを見て買い物します」")
        hints.append("日常生活")
        score += 6
    elif q1 == "3":
        print("山口さん「通勤がうまくいかない日があります…」")
        hints.append("通勤不安")
        score += 8

    # 質問2
    print("\nQ2: 次にどんな質問をしますか？")
    print("1: 『何かやめたくないこと、ありますか？』")
    print("2: 『やっていて楽しいことは何ですか？』")
    print("3: 『今後の生活で、どうしていきたいと思いますか？』")
    q2 = input("番号を選んでください：")
    if q2 == "1":
        print("山口さん「できれば…今の仕事は続けたいんです」")
        hints.append("仕事継続")
        score += 12
    elif q2 == "3":
        print("山口さん「少しでも自分でできるようにしたいです」")
        hints.append("自立志向")
        score += 9
    elif q2 == "2":
        print("山口さん「娘と夕飯を一緒に作るのが楽しいです」")
        hints.append("家庭役割")
        score += 6

    # 質問3
    print("\nQ3: 具体的な行動に関する質問をします")
    print("1: 『通勤はどのようにしていますか？』")
    print("2: 『買い物はどうされていますか？』")
    print("3: 『今の仕事の内容は？』")
    q3 = input("番号を選んでください：")
    if q3 == "1":
        print("山口さん「バスで通ってます。でも時々不安になるんです…」")
        hints.append("通勤バス")
        score += 10
    elif q3 == "2":
        print("山口さん「買い物はメモを見ながら、一人で行ってます」")
        hints.append("買い物自立")
        score += 7
    elif q3 == "3":
        print("山口さん「事務作業をしてます。パソコンは使えます」")
        hints.append("仕事能力")
        score += 8

    print("\n=== インタビューのまとめ ===")
    print("山口さんの発言から見えてきたキーワード：")
    for h in hints:
        print(f"- {h}")

    print(f"\n情報収集スコア：{score}点")

    if "仕事継続" in hints and "バス移動" in hints:
        goal = "一人でバスに乗って通勤できるように支援する"
    elif "仕事継続" in hints:
        goal = "職場での活動継続を支援する"
    elif "通勤不安" in hints:
        goal = "通勤ルートの安全確認と不安軽減"
    else:
        goal = "日常生活の中で自立を目指す"

    print(f"\n▶ 推定される生活行為仮目標：『{goal}』")

    input("\nEnterキーでアセスメント作成フェーズへ進みます。")

    print("\n※ 次のフェーズは現在準備中です。")
