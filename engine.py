# engine.py — CLI bridge
ENTRYPOINT_MODE = "function"
MODULE_NAME = "main"
FUNCTION_NAME = "main"
SCRIPT_PATH = "main.py"

import builtins, threading, queue, time, runpy, importlib

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
        if prompt:
            self.output_q.put(prompt)
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
    return {"started": False, "finished": False}

def step(state, user_input: str):
    if not state.get("started"):
        _BRIDGE.start()
        state["started"] = True
        out = _BRIDGE.drain()
        state["finished"] = _BRIDGE.finished
        return out, state
    if user_input is not None:
        _BRIDGE.push(user_input)
    out = _BRIDGE.drain()
    state["finished"] = _BRIDGE.finished
    if state["finished"] and not out.strip():
        out = "＜シナリオ終了＞\nリセットで最初から再開できます。"
    return out, state
