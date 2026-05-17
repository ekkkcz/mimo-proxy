# mimo-proxy

A lightweight local proxy that strips image content from requests before forwarding to the Mimo API.

## Why?

Mimo is a text-only model. When used with Claude Code, the history may contain image blocks (screenshots, pasted images), causing Mimo to return errors. This proxy automatically replaces image blocks with `[image removed]` placeholders and streams the response back.

## Quick Start

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/mimo-proxy.git
cd mimo-proxy
```

### 2. Choose your config

根据你的 Mimo 订阅方式选择：

| | Token Plan | 按量付费 |
|---|---|---|
| 代理配置 | `config.json` (默认，无需改动) | 复制 `config-pay-as-you-go.json` 改名为 `config.json` |
| Claude Code 配置 | `claude-code-settings-token-plan.json` | `claude-code-settings-pay-as-you-go.json` |
| API Key 格式 | `tp-xxxxx` | `sk-xxxxx` |

### 3. Set your API Key

> **打开你选的 `claude-code-settings-*.json`，把 `ANTHROPIC_AUTH_TOKEN` 的值替换成你自己的 Mimo API Key：**
>
> - Token Plan：`"ANTHROPIC_AUTH_TOKEN": "tp-your-token-plan-key"` → 改成你的 `tp-` 开头的 Key
> - 按量付费：`"ANTHROPIC_AUTH_TOKEN": "sk-your-api-key"` → 改成你的 `sk-` 开头的 Key
>
> 然后复制全部内容到你的 Claude Code 配置文件 `~/.claude/settings.json`。

### 4. Start proxy

```bash
python proxy.py
```

### 5. Done

Use Claude Code normally — images in history will be filtered automatically.

## GUI Control Panel

A small desktop widget for starting/stopping the proxy:

```bash
python control.py
```

## config.json

代理从 `config.json` 读取配置：

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
| `mimo_base` | Token Plan URL | 按量付费改为 `https://api.xiaomimimo.com/anthropic` |
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
