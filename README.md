# StayCode

StayCode 是 Python 终端 Coding Agent，提供 CLI、Textual TUI、模型调用、文件与命令工具、MCP、Skills、Hooks、会话记忆、团队协作、Git worktree 和 Remote 界面。

本版本用于个人演示：完整沿用原项目框架、模块和功能，仅统一 StayCode 品牌、包名、命令及数据路径，清理重复宣传文案。来源与第三方许可见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## 安装与启动

需要 Python 3.11 或更高版本。克隆仓库后，在 PowerShell 中按原锁文件安装依赖：

```powershell
git clone https://github.com/stay2002/Staycode-Agent.git
cd Staycode-Agent
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install uv
.\.venv\Scripts\uv.exe sync --frozen --inexact
.\.venv\Scripts\staycode.exe --help
```

`--inexact` 保留虚拟环境中的安装工具；产品依赖仍使用 `uv.lock` 中的版本。

首次安装时，将[公开配置示例](examples/config.yaml.example)复制为 `.staycode/config.yaml`；已有配置时直接编辑，不要覆盖：

```powershell
Copy-Item examples/config.yaml.example .staycode/config.yaml
```

然后填写自己的模型服务。例如使用兼容 OpenAI 的服务时：

```yaml
providers:
  - name: personal-provider
    protocol: openai-compat
    base_url: https://your-provider.example/v1
    model: your-model-name
    api_key: ""
permission_mode: default
```

将地址和模型替换为自己服务的实际值，通过 `OPENAI_API_KEY` 环境变量提供密钥，或在本地配置的 `api_key` 中填写。Anthropic 协议使用 `ANTHROPIC_API_KEY`；配置文件也支持本地填写密钥。

```powershell
# 启动交互界面
.\.venv\Scripts\staycode.exe

# 单次任务
.\.venv\Scripts\staycode.exe -p "解释当前项目的目录结构"

# 原有 NDJSON 输出与 Remote 入口
.\.venv\Scripts\staycode.exe -p "解释当前项目的目录结构" --output-format stream-json
.\.venv\Scripts\staycode.exe --remote

# Python 模块入口
.\.venv\Scripts\python.exe -m staycode --help
```

Remote 沿用原实现的 `0.0.0.0:18888` 监听及访问控制行为，演示应在可信本地环境进行。真实任务调用已配置的模型服务；本次没有新增离线演示模式。

## 项目结构

- `staycode/`：完整产品源码，子模块布局和接口保持原样。
- `tests/`：原有测试，仅同步品牌、包名和路径引用。
- `.staycode/`：配置示例、技能及运行数据目录。
- `STAYCODE.md`：产品加载的项目指令；通用 `AGENTS.md` 规则继续沿用。
- [AGENT.MD](AGENT.MD)：本次工作目标、范围和继续方式。

产品使用 `staycode` 命令、`.staycode` 数据目录和 `STAYCODE_*` 专属环境变量。不提供旧命令别名或旧数据自动迁移。工具名、CLI 参数、配置字段、依赖和版本保持原样。

Git 仓库包含随项目提供的 `.staycode/skills/`。实际 API 配置、会话、记忆、历史记录、日志、虚拟环境和本机验证输出由 `.gitignore` 排除；这些文件继续保存在本机。历史文档中指向 `docs/analysis/evidence/` 的运行日志和截图仅在原本地工作目录可用，仓库保留不含密钥的源码清单与品牌映射。历史源码链接基于原本地快照；在 GitHub 或其他目录阅读时，请按对应模块的相对路径定位源码。

## 文档

- [Agent 开发逐章学习手册](docs/learning/Agent开发学习手册.md)：面向有 LLM 应用经验的开发者，18 章源码课程、实验和验收标准。
- [离线 HTML 阅读版](docs/learning/Agent开发学习手册.html)：章节导航、搜索、进度记录和打印。
- [当前源码导航](docs/learning/源码导航.md)与[学习验证记录](docs/learning/验证记录.md)。

- [品牌替换设计及计划图](docs/05-staycode-rewrite-design.md)
- [实施记录](docs/06-rewrite-roadmap.md)
- [本次验证报告](docs/08-branding-validation.md)
- [GitHub 发布范围与验证](docs/09-github-publication.md)

此前的[项目全景](docs/00-project-overview.md)、[核心运行时](docs/analysis/01-core-runtime.md)、[工具与扩展](docs/analysis/02-tools-and-extensions.md)、[协作与记忆](docs/analysis/03-collaboration-memory-worktree.md)、[交互与验证](docs/analysis/04-interface-and-validation.md)及[源码索引](docs/analysis/07-source-inventory.md)保留为原项目研究资料。其中旧名称、行号和重构建议是历史记录，不代表本次实施范围，也不代表已修复原有问题。
