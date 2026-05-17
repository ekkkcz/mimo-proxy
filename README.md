# mimo-proxy

A lightweight local proxy that strips image content from requests before forwarding to the Mimo API.

## Why?

Mimo is a text-only model. When used with Claude Code, the history may contain image blocks (screenshots, pasted images), causing Mimo to return errors. This proxy automatically replaces image blocks with `[image removed]` placeholders and streams the response back.

## Quick Start

1. Clone or download this repo

2. 复制对应的 `config.json`（已附带，按需替换）：

   - **Token Plan** → 直接用默认的 [`config.json`](config.json)
   - **按量付费** → 用 [`config-pay-as-you-go.json`](config-pay-as-you-go.json)，复制一份改名为 `config.json`

3. 复制对应的 Claude Code 配置到 `~/.claude/settings.json`：

   - **Token Plan**：[`claude-code-settings-token-plan.json`](claude-code-settings-token-plan.json)
   - **按量付费**：[`claude-code-settings-pay-as-you-go.json`](claude-code-settings-pay-as-you-go.json)

   替换其中的 `tp-your-token-plan-key` 或 `sk-your-api-key` 为你在 [Mimo 平台](https://platform.xiaomimimo.com) 获取的 API Key。

4. Start the proxy:

```bash
python proxy.py
```

5. Use Claude Code normally — images in history will be filtered automatically.

## GUI Control Panel

A small desktop widget for starting/stopping the proxy:

```bash
python control.py
```

## config.json

代理从 `config.json` 读取配置，无需设置环境变量：

```json
{
  "listen_port": 15722,
  "mimo_base": "https://token-plan-cn.xiaomimimo.com/anthropic",
  "log_path": "./proxy.log"
}
```

| Key | Default | Description |
|-----|---------|-------------|
| `listen_port` | `15722` | 代理监听端口 |
| `mimo_base` | Token Plan URL | Mimo API 地址，按量付费改为 `https://api.xiaomimimo.com/anthropic` |
| `log_path` | `./proxy.log` | 日志路径 |

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
