# mimo-proxy

A lightweight local proxy that strips image content from requests before forwarding to the Mimo API.

## Why?

Mimo is a text-only model. When used with Claude Code, the history may contain image blocks (screenshots, pasted images), causing Mimo to return errors. This proxy automatically replaces image blocks with `[image removed]` placeholders and streams the response back.

## Quick Start

1. Clone or download this repo

2. Configure your Claude Code (`~/.claude/settings.json`):

按量付费 (Pay-as-you-go)，API Key 格式 `sk-xxxxx`：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:15722",
    "ANTHROPIC_AUTH_TOKEN": "sk-xxxxx",
    "ANTHROPIC_MODEL": "mimo-v2.5-pro",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "mimo-v2.5-pro",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "mimo-v2.5-pro",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "mimo-v2.5-pro"
  }
}
```

Token Plan (订阅套餐)，API Key 格式 `tp-xxxxx`：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:15722",
    "ANTHROPIC_AUTH_TOKEN": "tp-xxxxx",
    "ANTHROPIC_MODEL": "mimo-v2.5-pro",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "mimo-v2.5-pro",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "mimo-v2.5-pro",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "mimo-v2.5-pro"
  }
}
```

> 前往 [Mimo 平台](https://platform.xiaomimimo.com) 获取你的 API Key。
> Token Plan 用户启动代理时需额外指定 API 地址（见下方环境变量）。

3. Start the proxy:

```bash
python proxy.py
```

4. Use Claude Code normally — images in history will be filtered automatically.

## GUI Control Panel

A small desktop widget for starting/stopping the proxy:

```bash
python control.py
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MIMO_PROXY_PORT` | `15722` | Local port the proxy listens on |
| `MIMO_API_BASE` | `https://token-plan-cn.xiaomimimo.com/anthropic` | Target API endpoint (see below) |
| `MIMO_PROXY_LOG` | `./proxy.log` | Log file path |

**`MIMO_API_BASE` — 按量付费用户需要切换：**

| Subscription | Base URL |
|---|---|
| Token Plan (默认) | `https://token-plan-cn.xiaomimimo.com/anthropic` |
| Pay-as-you-go | `https://api.xiaomimimo.com/anthropic` |

按量付费用户启动代理时指定：

```bash
set MIMO_API_BASE=https://api.xiaomimimo.com/anthropic
python proxy.py
```

## How It Works

```
Claude Code → proxy (15722) → strip images → Mimo API
```

- Image blocks (`type: "image"`, `type: "image_url"`, base64 sources) are replaced with `[image removed]` text blocks
- All other content (text, tool_use, etc.) is passed through unchanged
- Authentication headers are forwarded as-is
- Responses are streamed back without buffering

## Requirements

- Python 3.10+
- Mimo API key ([platform.xiaomimimo.com](https://platform.xiaomimimo.com))
- Claude Code CLI or VS Code extension

## License

MIT
