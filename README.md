# mimo-proxy

A lightweight local proxy that strips image content from requests before forwarding to the Mimo API.

## Why?

Mimo is a text-only model. When used with Claude Code, the history may contain image blocks (screenshots, pasted images), causing Mimo to return errors. This proxy automatically replaces image blocks with `[image removed]` placeholders and streams the response back.

## Quick Start

1. Clone or download this repo

2. Configure your Claude Code (`~/.claude/settings.json`):

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:15722",
    "ANTHROPIC_AUTH_TOKEN": "your-mimo-api-key",
    "ANTHROPIC_MODEL": "mimo-v2.5-pro",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "mimo-v2.5-pro",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "mimo-v2.5-pro",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "mimo-v2.5-pro"
  }
}
```

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
| `MIMO_API_BASE` | `https://token-plan-cn.xiaomimimo.com/anthropic` | Target API endpoint |
| `MIMO_PROXY_LOG` | `./proxy.log` | Log file path |

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
