import random

def start_goal_question_training_mode():
    total_score = 0
    print("""【状況1】山口さんは、「モーニングに行くのが楽しみで、会社に行く途中に寄ってるんです」と話されています。
ご本人にとって日常の楽しみであるこの習慣が、生活や通勤にどのように影響しているかをより深く理解するために、あなたならどのような質問をしますか？
以下から適切と思うものをすべて選んでください（例: 1 2 4）""")
    options = [
        "頻度について聞く",
        "喫茶店の店員との関係を聞く",
        "時間通りに終えられているかを聞く",
        "メニューの内容を詳しく聞く",
        "他の喫茶店との比較を聞く",
    ]
    random.shuffle(options)
    for i, opt in enumerate(options):
        print(f"{i+1}: {opt}")
    selected = input("選択肢番号をスペース区切りで入力してください：").split()
    selected_indices = [int(x)-1 for x in selected if x.isdigit()]
    correct_answers = [options.index(opt) for i, opt in enumerate(options) if opt in [
        "頻度について聞く",
        "喫茶店の店員との関係を聞く",
        "時間通りに終えられているかを聞く",
    ]]
    score = sum(1 for idx in selected_indices if idx in correct_answers)
    print(f"▶ この質問のスコア：{score}/3 点\n")
    total_score += score
    print("""【状況2】娘さんは、「母はメモをしているようですが、どこに置いたか分からなくなるようで…」と困っています。
ご本人の記憶障害への対応として、メモや他の記録手段を活用した工夫を考える必要があります。
こうした背景を踏まえて、あなたならどのような質問を娘さんにしますか？
以下から適切と思うものをすべて選んでください（例: 1 3 5）""")
    options = [
        "スマホは使えますか？",
        "どんなときにメモを取っていますか？",
        "メモを取ったことを忘れてしまう頻度を聞く",
        "メモ帳のフォントサイズは適切かを聞く",
        "メーカーを確認する",
    ]
    random.shuffle(options)
    for i, opt in enumerate(options):
        print(f"{i+1}: {opt}")
    selected = input("選択肢番号をスペース区切りで入力してください：").split()
    selected_indices = [int(x)-1 for x in selected if x.isdigit()]
    correct_answers = [options.index(opt) for i, opt in enumerate(options) if opt in [
        "スマホは使えますか？",
        "どんなときにメモを取っていますか？",
        "メモを取ったことを忘れてしまう頻度を聞く",
    ]]
    score = sum(1 for idx in selected_indices if idx in correct_answers)
    print(f"▶ この質問のスコア：{score}/3 点\n")
    total_score += score
    print("""【状況3】娘さんは、「しばらくは夜に様子を見に行けますが、結婚して別居する予定なんです」と話しています。
現在は夜間の見守り支援が可能ですが、将来的には支援体制の変更が必要になるかもしれません。
こうした変化を見据えて、あなたならどのような質問を娘さんにしますか？
以下から適切と思うものをすべて選んでください（例: 2 3 4）""")
    options = [
        "夫の協力は得られそうか？",
        "実家にどれくらいの頻度で行けそうか？",
        "近所の人に頼れそうか？",
        "結婚式の日程を聞く",
        "予算について聞く",
    ]
    random.shuffle(options)
    for i, opt in enumerate(options):
        print(f"{i+1}: {opt}")
    selected = input("選択肢番号をスペース区切りで入力してください：").split()
    selected_indices = [int(x)-1 for x in selected if x.isdigit()]
    correct_answers = [options.index(opt) for i, opt in enumerate(options) if opt in [
        "夫の協力は得られそうか？",
        "実家にどれくらいの頻度で行けそうか？",
        "近所の人に頼れそうか？",
    ]]
    score = sum(1 for idx in selected_indices if idx in correct_answers)
    print(f"▶ この質問のスコア：{score}/3 点\n")
    total_score += score
    print(f"=== 総合スコア：{total_score}/9 点 ===")
    if total_score >= 7:
        print("◎ 素晴らしい質問力です！")
    elif total_score >= 5:
        print("○ 良い着眼点ですが、さらに深めても良いです。")
    else:
        print("△ 質問の幅や深さをもう一度振り返って練習してみましょう。")