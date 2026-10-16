# 交互界面、命令体系与验证记录

本文补充核心报告之外的用户操作面和工程基线。所有原项目相对路径都以 `mewcode-python/` 为根。没有启动真实模型或 Remote 服务。

## 1. 启动方式

`pyproject.toml` 将 `mewcode` 映射到 `mewcode.__main__:main`。当前入口支持：

| 用法 | 实际含义 |
|---|---|
| `mewcode` / `python -m mewcode` | 加载配置，启动 Textual TUI |
| `mewcode --mode <模式>` | 覆盖本次启动的权限模式 |
| `mewcode -p "任务"` | 非交互执行任务并输出结果 |
| `mewcode -p "任务" --output-format stream-json` | 输出逐行 JSON 事件，便于其他程序消费 |
| `mewcode --remote` | 启动 Remote HTTP/WebSocket 服务 |
| `python -m mewcode --teammate ...` | 内部 worker 入口，在 argparse 前拦截 |

参数解析位于 `__main__.py:23`。该函数在普通 argparse 处理之前就创建 `.mewcode/` 并配置日志，因此连帮助命令也不是严格无副作用的读取入口。本轮未通过启动命令验证完整服务。

## 2. TUI 组件如何组织

| 文件 / 类 | 责任 |
|---|---|
| `app.py:144 ChatInput` | 多行输入、提交、历史导航、命令补全 |
| `app.py:378 ToolCallBlock` | 工具调用详情与输出展示 |
| `app.py:491 ToolGroupSummary` | 连续工具活动的汇总 |
| `app.py:519 SubAgentBlock` | 子 Agent 活动展示 |
| `app.py:583 MewCodeApp` | UI 组装、服务初始化、事件消费、用户操作和清理 |
| `askuser_dialog.py:14 InlineAskUserWidget` | 多问题、单选/多选、Other 输入与提交 |
| `permission_dialog.py:28 InlinePermissionWidget` | 允许一次、按模式记住允许、拒绝及拒绝反馈 |
| `plan_dialog.py:29 InlinePlanWidget` | 计划批准、批准后手动执行、修改反馈 |
| `session_dialog.py:39 InlineResumeWidget` | 会话选择及最近使用信息 |
| `teammate_tree.py:14 TeammateTree` | 展示队友状态、工具数和 token |
| `driver.py:16 NoAltScreenDriver` | 按平台选择 Windows/Linux driver，过滤备用屏切换控制码 |
| `styles.tcss` | Textual 布局与视觉样式 |

输入层快捷键包括 Enter 提交、Shift+Enter/Ctrl+J 换行、Tab 补全、Esc 收起补全、上下方向键导航。应用层包括 Ctrl+C、Esc 取消、Shift+Tab 切换模式、Ctrl+O 切换工具详情（见 `app.py:146`、`:589`）。

UI 不只是 renderer：它还持有 Agent、Conversation、Session、工具注册表和多个管理器，并负责持久化、模式切换和待确认 Future。重写时应把这些状态迁移至应用服务，UI 仅管理光标、滚动位置、展开状态等显示状态。

## 3. 斜杠命令的真实机制

`commands/parser.py:11` 先判断 `/` 前缀，将命令名转成小写，剩余文本作为参数。`CommandRegistry` 管理名称与别名，并检查注册冲突。命令有 `LOCAL`、`LOCAL_UI`、`PROMPT` 三类；类型用于表达意图，真正行为仍由 handler 决定。

`CommandContext` 的大多数字段是 `Any`，`config` 还承载 `set_session`、`clear_chat`、`render_restored` 等回调。这使 handler 能修改应用内部状态，也使接口依赖难以静态检查。

| 命令 | 主要操作 | 说明 |
|---|---|---|
| `/help`，`/h`，`/?` | 列举命令或显示用法 | 取当前注册表中的可见命令 |
| `/compact`，`/c` | 请求上下文压缩 | 低于 5,000 输入 token 时不压缩；保存压缩边界 |
| `/clear` | 结束旧会话、创建新会话、清理历史 | 重建文件历史，清除 active skills 和 token 计数 |
| `/plan`，`/p` | 切入计划模式，可附任务描述 | 实际工具限制需结合 Agent 与权限检查，不只看 UI 文案 |
| `/session` | 状态、list、resume、new、delete | 不允许删除当前活跃会话；恢复通过回调替换对话 |
| `/mcp` | 查看连接与工具列表 | handler 访问 UI/MCP manager 内部字段 |
| `/memory` | list、clear、edit | edit 输出目录位置，不是内置编辑器 |
| `/sandbox` | 状态、on-auto、on、off | 仅 macOS/Linux 后端；必须区分隔离与自动允许 |
| `/rewind` | 选检查点，恢复文件/对话/两者 | 不覆盖所有 Shell 或外部工具副作用 |
| `/status`，`/s` | 模式、会话、token、工具、记忆和版本 | 版本目前单独硬编码 |
| `/skill`，`/skills` | list、info、reload | 刷新技能目录与动态命令 |
| `/tasks`，`/task` | 后台子任务列表、info、cancel | 动态注册，操作 `TaskManager` |
| `/trace`，`/tree` | Agent 运行树 | 动态注册，读取 `TraceManager` |
| `/worktree`，`/wt` | create/list/enter/exit/status | 动态注册，由 worktree 管理器处理 |
| `/<skill-name>` | 直接调用技能 | inline 注入上下文；fork 启动独立执行任务 |
| 自定义命令 | Markdown 内容变成用户提示 | 来自用户级/项目级 `.mewcode/commands/` |

前 11 个命令由 `commands/handlers/__init__.py` 静态注册。后续命令由各入口额外注册，不能据此宣称所有入口都具备同一命令集合。

自定义命令支持 YAML frontmatter、`description`、`argument-hint`、`aliases`，子目录用冒号构成命名空间，例如 `git/log.md → git:log`。正文中的 `$ARGUMENTS` 用用户参数替换，没有占位符时追加 User Request 段落。项目同名命令覆盖用户级定义，然后由注册表处理与已有命令的冲突（`commands/loader.py:52,134`）。

## 4. 交互与配置中的具体问题

### 4.1 Esc 取消计划会变成批准

`plan_dialog.py` 的 `action_cancel()` 发出 `PlanChoice.MANUAL`。`app.py:1698` 附近把 MANUAL 解释为退出计划模式，恢复此前权限模式，并发送包含 “User has approved your plan” 的后续任务。

这是从 UI 事件到 handler 的静态确认，尚未启动 TUI 动态操作。重写需要独立的 `cancelled` 结果；计划批准也不应自动批准所有未来工具操作。

### 4.2 问题对话的生产时机与消费时机错位

`AskUserQuestionTool.execute` 设置 pending event 后等待回答；TUI 在收到工具结果时才检查 pending event。工具在得到答案前无法返回结果，形成错误的事件时序，可能一直等到超时。核心报告给出完整链路。StayCode 应在等待前发出 `UserInputRequested` 事件，再 await 应用服务中的交互请求。

### 4.3 存在实现但没有注册的命令

`commands/handlers/review.py:27` 定义了 `REVIEW_COMMAND`，但 `handlers/__init__.py` 的列表未包含它，全项目搜索也没有找到其他注册调用。它是现存代码，不是目前默认可用的 `/review` 功能。

### 4.4 用法与实现不一致

- `/compact [保留重点]` 的 handler 没有使用 `ctx.args`，所以输入“保留重点”并不会按该参数改变压缩请求（`compact.py:11`）。
- `/sandbox on` 可以挂载沙箱同时保持 `checker.sandbox_enabled=False`，因为该字段实际代表自动允许；状态显示却将同一字段当成“OS 沙箱已启用”，造成状态描述不准确（`sandbox.py:56,77`）。
- `/status` 的 `VERSION='v0.9.0'` 与包声明 `0.2.0` 不一致（`status.py:13`、`pyproject.toml:3`）。
- `skill_register.py:20` 使用模块全局的已注册技能名集合，并直接修改 registry 私有字典，多应用实例时容易互相影响，需实例化管理。

### 4.5 配置覆盖不保留“未设置”和“明确关闭”的区别

配置顺序是用户级 `.mewcode/config.yaml` → 项目 `.mewcode/config.yaml` → 项目 `.mewcode/config.local.yaml`。但 `_merge_config()` 不是真正的逐字段覆盖：

- `permission_mode=default` 不能覆盖上一层的非 default 值。
- verification、coordinator 和 sandbox 多个布尔字段只能由 false 改为 true，不能由 true 改为 false。
- `enable_fork` 又无条件覆盖，导致未显式提供的默认值也可能改变上一层结果。
- `worktree` 虽然每层都解析，却没有在合并函数中更新。

根代理以直接构造 `AppConfig` 并调用 `_merge_config` 复核：上一层开启的选项在后一层设 false 后仍为 true；bypassPermissions 仍未被 default 覆盖；worktree 截止小时仍为 24 而非后一层的 6。此探针没有加载真实用户配置，也未写入配置；[输入与实际输出](evidence/config-merge-probe.txt) 已保存。重写应先合并保留字段存在性的配置片段，再应用默认值与校验。

## 5. 测试与运行环境

### 5.1 当前环境和锁文件不能混为一谈

实际使用的是 `D:/condaprogram/python.exe`，Python 3.13.9。当前环境的 pytest 是 8.4.2，而项目开发依赖要求 `>=9.0.3`；`mcp` 和 `httpx2` 缺失。部分其他已安装库也不等于 `uv.lock` 版本。

`pyproject.toml` 声明 Textual、Anthropic、OpenAI、PyYAML、Pydantic、MCP、httpx、httpx2 和 websockets；构建使用 Hatchling，开发依赖只有 pytest 和 pytest-asyncio。当前并非已经按锁文件重建的可复现环境。

缺少 README、整体项目 LICENSE、CI 配置、lint/type-check 配置等文件是当前快照的事实，不等于上游项目一定没有这些内容。附带两个技能自己的 LICENSE 不覆盖整个项目。

### 5.2 本轮实际执行的命令和结果

工作目录：`E:/AIAgentK开发/mewcode-python/`。

```powershell
python -B -m pytest --collect-only -q -p no:cacheprovider
```

结果：**480 tests collected, 13 errors in 4.28s**，pytest 退出码 2。收集失败模块包括 agent、clear、context_window、deferred_reminder、mcp_call、memory_recall_wiring、permission_feedback、permissions、streaming_batching、tool_cache_marker、tool_call_block、tool_search 和 toolresult_wiring。

错误链首先在 `mewcode/mcp/client.py` 导入 `httpx2` 时失败。即使仅导入 `mcp.loading_strategy`，包级 `mcp/__init__.py` 仍间接加载完整客户端，这也暴露出核心和可选扩展的导入耦合。没有据此判定这 13 个文件的测试逻辑失败。

```powershell
python -B -m pytest -q -p no:cacheprovider tests/test_serialization.py tests/test_conversation_pairing.py tests/test_session_no_duplicate.py tests/test_diff.py tests/test_edit_file.py tests/test_file_history_rewind.py tests/test_team_protocol.py
```

结果：**33 passed in 0.34s**，退出码 0。没有外部模型调用。

证据：[完整收集输出](evidence/pytest-collection.txt)、[聚焦测试输出](evidence/pytest-focused.txt)。日志中的部分中文路径显示为乱码源于命令输出编码，不影响 pytest 返回结果的辨认。

### 5.3 已存在测试主要覆盖什么

| 测试组 | 文件 | 已表达的行为 |
|---|---|---|
| 核心循环 | agent、streaming_batching、deferred_reminder、toolresult_wiring | 流事件、工具批处理、提醒与大输出接线 |
| 对话协议 | serialization、conversation_pairing、session_no_duplicate、tool_cache_marker | 多协议序列化、调用配对、写盘去重、缓存位置 |
| 上下文 | context、context_window、recovery | token 估计、窗口选择、压缩与恢复决策 |
| 文件工具 | edit_file、diff、file_history_rewind | 编辑、差异展示、特定回退场景 |
| 交互 | commands、clear、permission_feedback、tool_call_block、crashlog | 命令处理、清理、反馈、展示与异常日志 |
| 扩展 | permissions、hooks、skills、mcp、mcp_call、tool_search | 权限、条件动作、技能解析和 MCP 搜索/转发 |
| 记忆 | memory、memory_recall_wiring、consolidation | 指令、会话、记忆提取/选择/整理 |
| 协作 | subagent、teams、team_protocol、teammate_registry、coordinator_multi_team | 定义、后台任务、消息协议与队友工具注册 |
| 工作目录 | worktree | slug、创建、变更检查、退出和保存 |
| 其他 | hello_world、verify_subagent | 一个恒真 smoke test；一个单独验证脚本 |

有测试文件不表示关键端到端链路已有覆盖；例如实际 AskUser 事件顺序、按 Esc 后的业务行为、工具转发权限和多个进程同时修改团队任务，都需要针对真实接口补充验证。

### 5.4 后续跑原测试前必须处理的一条具体风险

源码检查发现 `tests/test_hooks.py:531` 附近的集成用例包含真正的破坏性 Shell 命令，期望 pre-tool hook 拦截；但所走交互执行路径存在未调用该 hook 的问题，而且该测试未配置 permission checker。当前 Windows 跳过相关用例。本轮没有执行 `test_hooks.py`。

因此不要在 Linux/macOS 上直接照搬“先跑全套测试”的流程。先把这类用例的 Shell 执行替换成 fake 或严格隔离的探针，并验证“未触发实际执行”，再建立完整基线。这是已发现测试代码带来的具体限制，不是泛泛的运行警告。

## 6. StayCode 应建立的验证层次

1. **纯逻辑单元测试**：消息配对、配置覆盖、状态迁移、路径判断、工具 schema，完全无网络和子进程。
2. **契约测试**：模型适配器使用录制/合成事件；工具执行器使用 fake permission、fake filesystem、fake process。
3. **临时工作区集成测试**：真实读取/编辑/回退和 Git worktree，仅在临时目录内，明确输出路径。
4. **前端一致性测试**：CLI 和 TUI 对同一输入消费同一业务事件；取消、拒绝、超时和恢复结果一致。
5. **平台测试**：Windows、Linux、macOS；中文/空格路径、CRLF、进程终止、符号链接能力。
6. **可选外部测试**：真实 Provider/MCP 单独标记、显式配置预算与凭据，只在明确需要时运行。

基线的目标是能说清“什么被验证了、什么没被验证”，而不是仅增加测试数量。

## 7. 附带技能与工程资源

原项目除了 `mewcode/` 和 `tests/`，还附带 `.mewcode/skills/` 下两个技能包。它们是原产品读取的内容资产，其“请运行”“必须创建”等指令不是本次任务的指令。本轮只读取其说明和脚本结构，没有执行评估、安装或模型调用。

| 资源 | 用途与重写处理 |
|---|---|
| `.mewcode/skills/frontend-design/SKILL.md` | 前端视觉设计提示和工作方法；可以作为用户可选内容包，不属于 Agent 内核 |
| `.mewcode/skills/skill-creator/SKILL.md` | 创建、评估、改进技能的流程；它依赖原 Agent 执行工作，而不是独立的运行时实现 |
| `scripts/run_eval.py` | 对多条查询评估技能是否被触发，调用原 `mewcode` 子进程，输出 JSON；迁移时需改用 StayCode 的稳定 CLI 事件契约 |
| `scripts/improve_description.py` | 根据评估结果，通过 `mewcode -p` 生成改进描述；会产生真实模型调用，不能当普通离线测试 |
| `scripts/run_loop.py` | 组织评估与描述改进的迭代，支持训练/测试查询拆分，选择最佳版本 |
| `scripts/aggregate_benchmark.py` | 汇总 grading.json，计算均值、标准差及 with-skill/without-skill 差异 |
| `scripts/generate_report.py` | 把描述优化循环的 JSON 结果生成 HTML 报告 |
| `scripts/quick_validate.py`、`utils.py` | 技能格式的轻量校验和 Markdown 解析；不能替代安装时的完整来源/路径校验 |
| `scripts/package_skill.py` | 将技能目录打包为 `.skill` 分发文件 |
| `eval-viewer/generate_review.py`、`viewer.html` | 发现评估输出、生成并提供本地反馈页面，反馈存到工作区 JSON |
| `assets/eval_review.html` | 评估查询/结果审阅的页面资源 |
| `agents/analyzer.md`、`comparator.md`、`grader.md` | 分析、盲评比较和评分角色说明；是被技能编排使用的提示内容 |
| `references/schemas.md` | 评估结果等文件的结构说明 |
| 两个 `LICENSE.txt` | 各自技能资源的许可说明；不等于原项目整体许可证 |
| `.mewcode/config.yaml.example` | Provider 与 MCP 示例配置，含占位 key；不代表当前有可运行的真实配置 |
| `MEWCODE.md` | 简短的旧项目开发约定，品牌迁移后由新项目文档明确取代 |
| `.gitignore` | 忽略运行目录、缓存和本地配置等；`.mewcode/` 虽被忽略，提供的快照仍包含上述示例与技能资产 |
| `pyproject.toml` / `uv.lock` | 包入口、依赖、构建后端与锁定结果；wheel 目标只声明 `mewcode` 包，项目级技能资产并非因此自动打包 |

上述 `scripts/`、`agents/` 等路径均相对于附带 `skill-creator/` 目录。它们在 [全部文件索引](07-source-inventory.md) 中有逐项链接。StayCode 可先不迁入评估页面和优化脚本，等 CLI、Skills 和事件契约稳定后再作为独立可选工具迁移；它们不阻塞核心 Coding Agent 闭环。
