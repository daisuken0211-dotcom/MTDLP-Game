# engine.py — CLI bridge
ENTRYPOINT_MODE = "script"
MODULE_NAME = "main"
FUNCTION_NAME = "main"
SCRIPT_PATH = "main.py"

import builtins, threading, queue, time, runpy, importlib


# --- 抑制したいフレーズ（必要に応じて追加可） ---
SUPPRESS_PHRASES = ["無効な選択です"]


class _CliBridge:
    def __init__(self):
        self.input_q = queue.Queue()
        self.output_q = queue.Queue()
        self.thread = None
        self.started = False
        self.finished = False
        self._orig_input = builtins.input
        self._orig_print = builtins.print

    def _patched_input(self, prompt=""):
        # 入力プロンプトを必ず表示（空promptでも案内を出す）
        if prompt and prompt.strip():
            self.output_q.put(prompt)
        else:
            self.output_q.put("（入力待ちです。最初にEnterを押してください。）")
        return self.input_q.get()

    def _patched_print(self, *args, **kwargs):
        end = kwargs.get("end", "\n")
        sep = kwargs.get("sep", " ")
        text = sep.join(str(a) for a in args) + end
        self.output_q.put(text)

    def _run(self):
        try:
            builtins.input = self._patched_input
            builtins.print = self._patched_print
            if ENTRYPOINT_MODE == "function":
                mod = importlib.import_module(MODULE_NAME)
                func = getattr(mod, FUNCTION_NAME)
                func()
            else:
                runpy.run_path(SCRIPT_PATH, run_name="__main__")
        except SystemExit:
            pass
        except Exception as e:
            self.output_q.put(f"[エラー] {e}\n")
        finally:
            builtins.input = self._orig_input
            builtins.print = self._orig_print
            self.finished = True

    def start(self):
        if not self.started:
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()
            self.started = True

    def push(self, s: str):
        self.input_q.put(s)

    def drain(self, timeout=0.3):
        buf = []
        end_time = time.time() + timeout
        while True:
            remaining = end_time - time.time()
            if remaining <= 0:
                break
            try:
                line = self.output_q.get(timeout=remaining)
                buf.append(line)
            except queue.Empty:
                break
        return "".join(buf)


_BRIDGE = _CliBridge()


def initial_state():
    # had_meaningful_input: 空白以外の最初の入力を済ませたか
    return {"started": False, "finished": False, "had_meaningful_input": False}


def _suppress_if_needed(text: str, allow_errors: bool):
    """allow_errors=False の間は、特定フレーズをフィルタする"""
    if allow_errors:
        return text
    lines = []
    for ln in text.splitlines():
        if any(p in ln for p in SUPPRESS_PHRASES):
            continue
        lines.append(ln)
    return "\n".join(lines).strip()


def step(state, user_input: str):
    # --- 起動時 ---
    if not state.get("started"):
        _BRIDGE.start()
        state["started"] = True

        # 最初の出力/プロンプトが現れるのを最大1.2秒待つ
        out = ""
        deadline = time.time() + 1.2
        while time.time() < deadline:
            chunk = _BRIDGE.drain(timeout=0.25)
            if chunk and chunk.strip():
                out = chunk
                break
            time.sleep(0.05)

        if not out.strip():
            out = "（入力待ちです。ここに答えを入力して送信してください）"

        # ★ まだユーザーが有効入力をしていない間はエラーメッセージを抑制
        out = _suppress_if_needed(out, allow_errors=state.get("had_meaningful_input", False))

        state["finished"] = _BRIDGE.finished
        return out, state

    # --- 通常処理 ---
    if user_input is not None:
        _BRIDGE.push(user_input)
        # 空白以外の入力が来たら以降はエラーメッセージを出す
        if (user_input or "").strip():
            state["had_meaningful_input"] = True

    out = _BRIDGE.drain(timeout=0.6)

    # ★ まだ有効入力前なら、ここでも抑制を適用
    out = _suppress_if_needed(out, allow_errors=state.get("had_meaningful_input", False))

    state["finished"] = _BRIDGE.finished
    if state["finished"] and not out.strip():
        out = "＜シナリオ終了＞\nリセットで最初から再開できます。"
    return out, state
