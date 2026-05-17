# mimo-proxy

让Mimo纯文本模型在 Claude Code 中不再因图片报错的本地代理。

## 问题

Mimo-v2.5-pro(以下简称Mimo,其他不可识图的Mimo模型也可用) 是纯文本模型，但 Claude Code 的对话历史中可能包含图片（截图、粘贴的图片），导致 Mimo 直接报错。本代理在请求到达 Mimo 前自动剥离图片内容，替换为占位文本，并流式转发响应。

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/ekkkcz/mimo-proxy.git
cd mimo-proxy
```

### 2. 选择配置

根据你的 Mimo 订阅方式选择：

| | Token Plan（订阅套餐） | 按量付费 |
|---|---|---|
| 代理配置 | `config.json`（默认，无需改动） | 复制 `config-pay-as-you-go.json` 改名为 `config.json` |
| Claude Code 配置 | `claude-code-settings-token-plan.json` | `claude-code-settings-pay-as-you-go.json` |
| API Key 格式 | `tp-xxxxx` | `sk-xxxxx` |

### 3. 填写 API Key

> **打开你选的 `claude-code-settings-*.json`，把 `ANTHROPIC_AUTH_TOKEN` 的值替换成你自己的 Mimo API Key：**
>
> - Token Plan：`"ANTHROPIC_AUTH_TOKEN": "tp-your-token-plan-key"` → 改成你的 `tp-` 开头的 Key
> - 按量付费：`"ANTHROPIC_AUTH_TOKEN": "sk-your-api-key"` → 改成你的 `sk-` 开头的 Key
>
> 然后复制全部内容到你的 Claude Code 配置文件 `~/.claude/settings.json`。

### 4. 启动代理

```bash
python proxy.py
```

### 5. 完成

正常使用 Claude Code 即可，对话中的图片会被自动过滤。

## GUI 控制面板

桌面小工具，一键启停代理：

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

| 字段 | 默认值 | 说明 |
|-----|---------|------|
| `listen_port` | `15722` | 代理监听端口 |
| `mimo_base` | Token Plan URL | 按量付费改为 `https://api.xiaomimimo.com/anthropic` |
| `log_path` | `./proxy.log` | 日志路径 |

## 工作原理

```
Claude Code → proxy (15722) → 剥离图片 → Mimo API
```

- 图片内容块（`image`、`image_url`、base64）替换为 `[image removed]` 文本
- 其他内容（文字、tool_use 等）原样透传
- 认证头直接转发，不做修改
- 响应流式返回，不缓冲

## 环境要求

- Python 3.10+
- Mimo API Key（[platform.xiaomimimo.com](https://platform.xiaomimimo.com)）
- Claude Code CLI 或 VS Code 插件

## License

MIT
