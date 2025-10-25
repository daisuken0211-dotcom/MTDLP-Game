# ============================
# opening_launcher.py
# ============================
# 目的：
# ・既存 main.py を変更せずに、
#   オープニング（opening_scene.py）を最初に表示してから
#   本編（mode_select または main）を自動起動する。
# ・Tkinterベースで動作。非常に軽量。
# ============================

import importlib

try:
    # opening_scene.py から関数を読み込み
    from opening_scene import run_opening_then_start
except Exception as e:
    print("[ERROR] opening_scene.py が見つかりません。")
    print(e)
    exit(1)

def start_existing_game():
    """
    既存のゲームを自動で探して起動。
    優先順位：
      1) mode_select.start_mode_select()
      2) mtdlp_mode.start_mtdlp_mode()
      3) main.main()
    """
    for mod_name, func_name in [
        ("mode_select", "start_mode_select"),
        ("mtdlp_mode", "start_mtdlp_mode"),
        ("main", "main"),
    ]:
        try:
            mod = importlib.import_module(mod_name)
            func = getattr(mod, func_name, None)
            if callable(func):
                print(f"[INFO] {mod_name}.{func_name}() を起動します。")
                func()
                return
        except ModuleNotFoundError:
            continue
        except Exception as e:
            print(f"[WARN] {mod_name} の起動時にエラー: {e}")
    print("[ERROR] 起動できるエントリポイントが見つかりません。mode_select.py または main.py を確認してください。")

if __name__ == "__main__":
    print("🎬 オープニングを開始します...")
    run_opening_then_start(start_existing_game)