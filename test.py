方式 1：自动配置脚本（推荐）
bash
运行

# 下载并执行配置脚本
curl -O "https://cdn.bigmodel.cn/install/claude_code_env.sh" && bash ./claude_code_env.sh
# 按提示粘贴你的 API Key
```{insert\_element\_0\_}


如果你已经购买了 智谱 GLM API（尤其是 GLM-4.5 或 GLM-5.0 这种支持“编码计划”的模型），你可以直接把 Claude Code 当作它的“外壳”来使用。

这是目前很多开发者的“省钱大法”：用 Claude Code 优秀的工具执行能力，对接智谱更便宜（甚至更高配）的 API。
实现方案：将 Claude Code 切换到智谱后端

由于 Claude Code 支持通过环境变量重定向 API 地址，你只需要把它的“大脑”指向智谱的服务器即可。
1. 获取智谱的 Claude 兼容地址

智谱通常提供一个兼容 Anthropic 协议的中转地址。根据最新的开发者文档（z.ai），你需要准备：

    API Key: 你在智谱后台申请的 Key。

    Base URL: 通常是 https://api.z.ai/api/anthropic (具体请以智谱后台给你的为准)。

2. 配置环境变量

你需要设置两个关键的环境变量。你可以直接在终端输入（临时生效），或者写入配置文件（永久生效）。

如果你是 Mac/Linux 用户（编辑 ~/.zshrc 或 ~/.bashrc）：
Bash

export ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
export ANTHROPIC_AUTH_TOKEN="你的智谱API_KEY"

如果你是 Windows 用户（PowerShell）：
PowerShell

$env:ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
$env:ANTHROPIC_AUTH_TOKEN="你的智谱API_KEY"

3. 绕过登录冲突（关键一步）

因为你现在用的是智谱的 Key，而不是 Anthropic 官方的账号。如果此时 Claude Code 提示你选择登录方式（就是你刚才看到的 1, 2, 3 选项），请执行：

    完全退出对话界面（输入 /exit）。

    强制注销官方登录：输入 claude logout。

    重新启动：确保上面的环境变量已经设置好，然后输入 claude。

此时，Claude Code 会直接读取 ANTHROPIC_AUTH_TOKEN 环境变量。如果配置正确，它不会再弹出那 3 个选项，而是直接进入对话界面。
4. 如何确认对接成功？

进入 claude 界面后，你可以问它：

    Who are you and what model is this?

    如果它回答自己是 GLM 或提到 Zhipu AI，说明对接成功了。

    如果依然报错 Auth conflict，说明你之前的官方登录信息没删干净。请按照我上一个回答的方法，先执行 claude logout，再确保环境变量里只有智谱的 Key。

⚠️ 注意事项

    模型名称映射：有些版本的 Claude Code 会默认请求 claude-3-5-sonnet。智谱的后端通常会自动把这个请求映射到对应的 GLM 模型（如 GLM-4.6/5.0）。

    Prompt Caching：智谱可能不完全支持 Claude 的缓存机制。如果运行报错，可以在启动时尝试加上 DISABLE_PROMPT_CACHING=true 环境变量。

你需要我帮你写一个一键切换“智谱模式”和“官方模式”的脚本吗？

###########Backup
cat ~/.claude/settings.json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "# 按提示粘贴你的 API Key",
    "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": 1
  }

