# ===============================
# opening_scene.py（新規追加）
# ===============================
# 目的：最初に「登場人物・街の様子の紹介」を静止画＋テキストで表示し、
#       終了後に既存の本編（mode_select もしくは mtdlp_mode など）へ移行します。
# 依存：標準の Tkinter のみ（Pillow 不要）。PNG/GIF を想定。
# 画像が無い場合でも、色背景＋テキストで表示できるようにフォールバックします。

import os
import tkinter as tk
from tkinter import ttk

# --- ユーザーが差し替えるだけで使えるスライド定義（例） ---
SLIDES = [
    {
        "title": "この街のこと",
        "text": "穏やかな住宅街。\n坂道と並木、朝のバスが生活を運ぶ。",
        "bg_path": "assets/basutei01.png",  # バス停
        "portrait_path": None,
    },
    {
        "title": "街の拠点",
        "text": "駅前のガラス張りの建物は\n地域の相談や支援のハブになっている。",
        "bg_path": "assets/ekibiru01.png",  # 駅ビル
        "portrait_path": None,
    },
    {
        "title": "暮らしの場",
        "text": "山口家のリビング。\nここで日々の会話や相談が生まれる。",
        "bg_path": "assets/jitakuRe.png",   # リビング
        "portrait_path": None,
    },
    {
        "title": "登場人物：山口 美咲さん",
        "text": "52歳・若年性認知症。娘と二人暮らし。\n笑顔を大切に、日々の暮らしを整えている。",
        "bg_path": "assets/jitakuRe.png",
        "portrait_path": "assets/yamaguchi01.png",  # 立ち絵
    },
    {
        "title": "登場人物：洋子さん",
        "text": "美咲さんの娘。仕事と結婚準備の合間に、\n母の生活を支えながら相談に訪れた。",
        "bg_path": "assets/jitakuRe.png",
        "portrait_path": "assets/musume04.png",  # 立ち絵
    },
]

# 背景のデフォルト色
DEFAULT_BG = "#f5f7fb"

class OpeningScene(tk.Frame):
    def __init__(self, master, slides, on_done, width=900, height=600):
        super().__init__(master, width=width, height=height, bg=DEFAULT_BG)
        self.master = master
        self.slides = slides
        self.on_done = on_done
        self.width = width
        self.height = height

        self.pack_propagate(False)

        # 上：タイトル、中央：背景＋立ち絵、下：本文＋ボタン
        self.title_label = ttk.Label(self, text="", font=("TkDefaultFont", 18, "bold"))
        self.title_label.pack(pady=(16, 8))

        self.canvas = tk.Canvas(self, width=width-40, height=360, bg=DEFAULT_BG, highlightthickness=0)
        self.canvas.pack()

        body_frame = ttk.Frame(self)
        body_frame.pack(fill="x", expand=False, pady=(8, 12), padx=16)

        self.text_label = ttk.Label(body_frame, text="", justify="left", anchor="w")
        self.text_label.pack(side="left", fill="both", expand=True)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=(0, 16))

        self.skip_btn = ttk.Button(btn_frame, text="スキップ", command=self.finish)
        self.skip_btn.pack(side="left", padx=8)
        self.next_btn = ttk.Button(btn_frame, text="次へ ▶", command=self.next_slide)
        self.next_btn.pack(side="left", padx=8)

        # 画像オブジェクトの参照保持（GC対策）
        self._bg_img = None
        self._portrait_img = None

        self.index = -1
        self.next_slide()

    def _load_image_safe(self, path, width=None, height=None):
        """Tkinter PhotoImage を安全に読み込む。失敗したら None を返す。"""
        if not path or not os.path.exists(path):
            return None
        try:
            img = tk.PhotoImage(file=path)
            if width and height:
                # subsample を使って簡易リサイズ（等倍以下のみ）。
                # 必要なら等倍に近い比率で分母を計算。
                w, h = img.width(), img.height()
                if w > 0 and h > 0 and (w > width or h > height):
                    x = max(1, int(round(w / width)))
                    y = max(1, int(round(h / height)))
                    img = img.subsample(x, y)
            return img
        except Exception:
            return None

    def _render_slide(self, slide):
        self.canvas.delete("all")
        self._bg_img = self._load_image_safe(slide.get("bg_path"), width=self.width-40, height=360)
        if self._bg_img is not None:
            self.canvas.create_image((self.width-40)//2, 180, image=self._bg_img)
        else:
            self.canvas.create_rectangle(0, 0, self.width-40, 360, fill=DEFAULT_BG, width=0)

        self._portrait_img = self._load_image_safe(slide.get("portrait_path"), width=360, height=360)
        if self._portrait_img is not None:
            # 右側に立ち絵を表示
            self.canvas.create_image(self.width-40-200, 200, image=self._portrait_img)

        self.title_label.config(text=slide.get("title", ""))
        self.text_label.config(text=slide.get("text", ""))

    def next_slide(self):
        self.index += 1
        if self.index >= len(self.slides):
            self.finish()
            return
        self._render_slide(self.slides[self.index])

    def finish(self):
        if callable(self.on_done):
            self.on_done()

# -------------------------
# 既存本編へバトンを渡すランチャ
# -------------------------

def run_opening_then_start(entrypoint_callable=None):
    """小さなウィンドウでオープニングを表示し、終了後に entrypoint_callable を呼ぶ。
    entrypoint_callable が None の場合は、mode_select または mtdlp_mode を自動探索。
    """
    def _proceed_to_main():
        root.destroy()
        # 既存のエントリポイントに移行
        if callable(entrypoint_callable):
            entrypoint_callable()
            return
        # 自動探索：mode_select → mtdlp_mode → main の順
        for mod_name, candidate in (
            ("mode_select", "start_mode_select"),
            ("mtdlp_mode", "start_mtdlp_mode"),
            ("main", "main"),
        ):
            try:
                mod = __import__(mod_name)
                func = getattr(mod, candidate, None)
                if callable(func):
                    func()
                    return
            except Exception:
                pass
        print("[opening_scene] エントリポイントが見つかりませんでした。")

    root = tk.Tk()
    root.title("オープニング")
    root.geometry("900x600")

    # mac のフォーカス対策
    try:
        root.attributes("-topmost", True)
        root.update()
        root.attributes("-topmost", False)
    except Exception:
        pass

    app = OpeningScene(root, SLIDES, on_done=_proceed_to_main)
    app.pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    # 単体テスト用：このファイルだけ実行した場合は、
    # スライド後に mode_select / mtdlp_mode / main の順で探索して移行します。
    run_opening_then_start()



# 使い方：
# 1) この opening_scene.py をプロジェクト直下に追加
# 2) assets フォルダ（assets/bg_city.png など）を任意で用意（無くても動く）
# 3) main.py に上記パッチを挿入（既存構造に合わせて _entrypoint 内を調整）
# 4) 実行：python main.py
#
# メモリ負荷の目安：
# ・静止画（PNG/GIF）数枚＋テキストのみ → 数十MB以下で超軽量
# ・画像が大きすぎる場合のみ subsample で縮小読込（簡易）
# ・音や動画が無い限り、Raspberry Pi や Render でも快適に動作
#
# 以上。