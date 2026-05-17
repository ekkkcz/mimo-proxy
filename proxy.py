"""
Mimo Proxy — 图片过滤 + 流式转发代理。
在 Claude Code 与 Mimo API 之间自动剥离 image content block，
避免纯文本模型因收到图片而报错。
"""
import http.server
import json
import os
import ssl
import urllib.request
from datetime import datetime

# ========== 配置 ==========
LISTEN_PORT = int(os.environ.get("MIMO_PROXY_PORT", "15722"))
MIMO_BASE = os.environ.get(
    "MIMO_API_BASE",
    "https://api.xiaomimimo.com/anthropic",
)
LOG_PATH = os.environ.get(
    "MIMO_PROXY_LOG",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "proxy.log"),
)
# ==========================


def log(msg: str):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")


def strip_images(messages: list) -> tuple[list, int]:
    removed = 0
    cleaned = []
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, list):
            new_content = []
            for block in content:
                t = block.get("type", "")
                if t in ("image", "image_url"):
                    removed += 1
                    new_content.append({"type": "text", "text": "[image removed]"})
                    continue
                if isinstance(block, dict) and block.get("source", {}).get("type") == "base64":
                    removed += 1
                    new_content.append({"type": "text", "text": "[image removed]"})
                    continue
                new_content.append(block)
            if not new_content:
                new_content = [{"type": "text", "text": "[empty message]"}]
            msg = {**msg, "content": new_content}
        cleaned.append(msg)
    return cleaned, removed


class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        cl = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(cl)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._stream(body)
            return

        model = data.get("model", "")
        log(f"REQ model={model} msgs={len(data.get('messages', []))}")

        if "messages" in data:
            new_msgs, removed = strip_images(data["messages"])
            data["messages"] = new_msgs
            if removed > 0:
                log(f"STRIP {removed} images")

        body = json.dumps(data, ensure_ascii=False).encode()
        self._stream(body)

    def _stream(self, body: bytes):
        url = f"{MIMO_BASE}{self.path}"
        log(f"FWD {url}")
        fwd_headers = {}
        for k, v in self.headers.items():
            if k.lower() in ("host", "content-length"):
                continue
            fwd_headers[k] = v
        from urllib.parse import urlparse
        fwd_headers["Host"] = urlparse(MIMO_BASE).hostname
        req = urllib.request.Request(url, data=body, method="POST", headers=fwd_headers)
        try:
            ctx = ssl.create_default_context()
            resp = urllib.request.urlopen(req, timeout=600, context=ctx)
            self.send_response(resp.status)
            for k, v in resp.headers.items():
                if k.lower() not in ("transfer-encoding", "connection"):
                    self.send_header(k, v)
            self.end_headers()
            while True:
                chunk = resp.read(8192)
                if not chunk:
                    break
                self.wfile.write(chunk)
                self.wfile.flush()
        except Exception as e:
            log(f"ERR {e}")
            self.send_response(502)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def log_message(self, fmt, *args):
        pass


def main():
    server = http.server.ThreadingHTTPServer(("127.0.0.1", LISTEN_PORT), ProxyHandler)
    print(f"[mimo-proxy] 127.0.0.1:{LISTEN_PORT} -> {MIMO_BASE} | strip images + stream")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
