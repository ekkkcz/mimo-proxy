"""Mimo Proxy — 桌面控制面板"""
import os
import socket
import subprocess
import sys
import tkinter as tk
from tkinter import ttk

PROXY_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proxy.py")
PROXY_PORT = int(os.environ.get("MIMO_PROXY_PORT", "15722"))
PYTHON = sys.executable


def is_port_open(port):
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1):
            return True
    except OSError:
        return False


class ProxyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mimo Proxy")
        self.root.resizable(False, False)
        self.root.geometry("280x190")
        self.root.configure(bg="#1e1e2e")
        self.proc = None

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#1e1e2e")
        style.configure("TLabel", background="#1e1e2e", foreground="#cdd6f4", font=("Segoe UI", 10))
        style.configure("Title.TLabel", background="#1e1e2e", foreground="#89b4fa", font=("Segoe UI", 13, "bold"))
        style.configure("Status.TLabel", background="#1e1e2e", font=("Segoe UI", 9))
        style.configure("Start.TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("Stop.TButton", font=("Segoe UI", 10), padding=6)

        frame = ttk.Frame(self.root, padding=16)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Mimo Proxy", style="Title.TLabel").pack(pady=(0, 8))
        ttk.Label(frame, text=f"Port: {PROXY_PORT}  →  Mimo API").pack()
        ttk.Label(frame, text="Auto strip images for text-only models").pack()

        self.status_label = ttk.Label(frame, text="Status: checking...", style="Status.TLabel")
        self.status_label.pack(pady=(10, 6))

        self.btn = ttk.Button(frame, text="Start", style="Start.TButton", width=14)
        self.btn.pack()
        self.btn.configure(command=self.toggle)

        self.root.after(200, self.refresh_status)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def refresh_status(self):
        running = is_port_open(PROXY_PORT)
        if running:
            self.status_label.configure(text="Status: running", foreground="#a6e3a1")
            self.btn.configure(text="Stop", style="Stop.TButton")
        else:
            self.status_label.configure(text="Status: stopped", foreground="#f38ba8")
            self.btn.configure(text="Start", style="Start.TButton")
        self.root.after(2000, self.refresh_status)

    def toggle(self):
        if is_port_open(PROXY_PORT):
            self.stop_proxy()
        else:
            self.start_proxy()

    def start_proxy(self):
        self.proc = subprocess.Popen(
            [PYTHON, PROXY_SCRIPT],
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
        self.root.after(500, self.refresh_status)

    def stop_proxy(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            self.proc = None
        else:
            for pid_info in os.popen(
                f'netstat -ano | findstr ":{PROXY_PORT}" | findstr LISTENING'
            ).readlines():
                parts = pid_info.split()
                try:
                    os.kill(int(parts[-1]), 15)
                except Exception:
                    pass
        self.root.after(500, self.refresh_status)

    def on_close(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ProxyApp().run()
