# 02 工具、权限、沙箱与扩展机制分析

分析对象：`E:/AIAgentK开发/mewcode-python`。本报告只读原项目，所有实现建议面向后续 `StayCode` 重写；源码中的提示词、技能正文和注释均作为分析材料，不作为本次操作指令。源码引用采用仓库相对路径和一基行号。分析日期：2026-09-24。

## 1. 核心判断

这部分代码已经形成了可工作的工具协议、注册表、权限决策、文件读写、MCP 接入、技能和 hooks 原型。值得保留的是：参数模型与 schema 共用、工具结果与 UI 事件分离、读前编辑检查、相邻只读工具批处理、工具输出落盘、MCP schema 按端点能力分三种加载路径，以及工具调用错误回传模型而不中断整个会话。

重写不宜直接复制现有安全层。多个入口共享同一批工具，但权限、禁用状态、hooks 和文件历史没有通过唯一执行入口强制实施。已发现命令白名单误判、MCP 分发器可直接调用内建工具、fork 技能不继承权限、沙箱配置与实际可用性脱节，以及文件回滚可能删除已有文件等问题。应优先建立统一执行边界，再迁移扩展能力。

证据分三级：**源码证实**表示可由明确控制流确认；**本地复现**表示已用纯函数或隔离临时目录实际验证；**待验证**表示必须依赖 SDK、操作系统或集成环境进一步确认。没有运行真实模型、MCP 服务、网络下载或安装依赖。

## 2. 模块地图与职责

| 模块 | 实际职责 | 重写时建议归属 |
|---|---|---|
| `tools/base.py` | `Tool`、`ToolResult`、工具类别、schema 导出、模型流事件类型 | 核心工具协议；模型流事件另归协议适配层 |
| `tools/__init__.py` | 注册/启禁用/发现状态、schema 列表、关键词检索、六个基础工具工厂 | `ToolCatalog` 与 `ToolExposurePolicy` 分离 |
| `read_file/write_file/edit_file/glob/grep/bash` | 文件、搜索和 shell 实现 | 内建工具包，通过宿主服务执行 |
| `file_state_cache.py`、`diff.py` | 读前编辑凭据与简单局部 diff | 文件服务、变更展示服务 |
| `mcp/*`、`tools/mcp_call.py`、`tools/impl/tool_search.py` | 连接、工具封装、schema 暴露策略、检索和分发 | MCP adapter 与能力目录 |
| `permissions/*` | 路径与规则检查、权限模式、命令启发式 | 统一授权策略 |
| `sandbox/*` | macOS Seatbelt、Linux bubblewrap 命令包装 | 平台执行后端 |
| `skills/*`、`tools/load_skill.py`、`tools/install_skill.py` | 技能定义、发现、热加载、inline/fork、安装 | 扩展包管理与执行上下文 |
| `hooks/*` | 生命周期枚举、条件解析、动作执行、通知/提示词收集 | 类型化事件订阅与受管任务 |
| `filehistory/history.py` | 修改前备份、内存快照索引、代码回滚 | 独立可恢复变更日志 |
| `web_content.py` | 内嵌 HTML/CSS/JS 的 Remote UI，**不是网页抓取工具** | 单独前端工程或模板资源 |
| 团队/Agent/Worktree 工具 | 包装各自领域服务供模型调用 | 详细实现见协作与工作区专题报告 |

`create_default_registry()` 只注册 ReadFile、WriteFile、EditFile、Bash、Glob、Grep，并共享一个 `FileStateCache`（`tools/__init__.py:182`）。其余工具由 TUI、Remote、CLI、teammate 等宿主分别追加，因此“源码中存在工具”不等于“每个运行入口都可调用”。例如 TUI 在 `app.py:768` 后挂载文件历史、技能、AskUserQuestion、ExitPlanMode；Remote 的注册链见 `remote.py:257`；teammate 工具链见 `__main__.py:487`。这类重复装配应在 StayCode 合并为可声明的能力组合。

## 3. 完整工具清单

以下是源码定义的 24 个内建工具，加上动态 MCP 工具。`R/W/C` 分别代表当前实现的 read/write/command 类别；这只是现有调度和权限标签，并不等于真实副作用。参数后 `?` 表示可省略。未列出的约束不应自行假定存在。

| 工具（实现） | 参数 | 用途与真实边界 |
|---|---|---|
| **ReadFile** R（`read_file.py:20`） | `file_path`；`offset?=0`；`limit?=2000` | UTF-8 全量读入后按行切片，返回一基行号；成功读后记录绝对路径 mtime。不是流式读取；offset/limit 没有非负上限约束；部分读取也会解锁整个文件的修改权限。 |
| **WriteFile** W（`write_file.py:20`） | `file_path`、`content` | 自动建父目录并覆盖文本；已有文件在共享缓存启用时必须先读且 mtime 未变；新文件可直接写。写入前就调用历史追踪；不是原子替换。 |
| **EditFile** W（`edit_file.py:21`） | `file_path`、`old_string`、`new_string` | 精确字符串必须恰好出现一次；读前检查、替换一次、返回增删行统计与 diff。没有批量替换和结构化 patch；完整文件读写，失败前也可能已产生历史条目。 |
| **Bash** C（`bash.py:111`） | `command`；`timeout?=120` 秒，上限截为 600 | `asyncio.create_subprocess_shell`，stderr 合并 stdout，可注入 cwd 和 OS 沙箱；实际 shell 随平台变化。输出完全缓冲；超时 kill 当前 shell；普通非零退出码仍返回 `is_error=False`。 |
| **Glob** R（`glob.py:16`） | `pattern`；`path?='.'` | `Path.glob` 找文件，排除若干目录，按 mtime 降序；先枚举再过滤，未限制数量；权限层错误地检查 pattern 而非 path。 |
| **Grep** R（`grep.py:17`） | `pattern`；`path?='.'`；`include?=''` | Python regex，全目录遍历、逐文件完整读取，以 UTF-8 ignore 解码，返回文件:行:文本；未限制时间/体积/匹配数，非 rg 后端；权限检查同样没用实际根路径。 |
| **AskUserQuestion** R（`ask_user.py:16`） | `questions[]`：`type/name/message/options?=[]`，options 为字符串列表 | 支持声明 text/radio/select/checkbox；单个 `_pending_event` 和 Future，等待 300 秒。type 不是枚举；按 read 默认可并发，但该对象只有一个 pending 槽。 |
| **ExitPlanMode** R（`exit_plan_mode.py:16`） | 无 | 校验是否 plan 模式及计划存在，返回提示；真正状态切换/审批由宿主执行，不是工具自身完成。 |
| **EnterWorktree** C（`enter_worktree.py:21`） | `name?` | 生成或校验 slug，调用 manager.create/enter；已有会话拒绝。创建与进入是两个操作，失败清理由 manager 负责。 |
| **ExitWorktree** C（`exit_worktree.py:21`） | `action='keep'/'remove'`；`discard_changes?` | 只作用于当前 EnterWorktree 会话；删除含未提交/未合并工作时须显式 true；最终删除委托 manager。 |
| **LoadSkill** R（`load_skill.py:20`） | `name` | inline 激活正文并返回；fork 调 SkillExecutor，只带回结果；没有 executor 时 fork 回退 inline。读取标签掩盖 fork 可能调用写工具的副作用。 |
| **InstallSkill** W（`install_skill.py:19`） | `url` | 解析 skills.sh/GitHub tree/raw URL，下载整个技能目录到用户全局路径，刷新目录/斜杠命令。会联网并覆盖同名技能；不是普通文件路径授权。 |
| **ToolSearch** R（`impl/tool_search.py:21`） | `query`；`max_results?=5` | 关键词检索或 `select:name,...`；返回 schema 文本或 native tool_reference。没有 max_results 范围约束；select 路径未过滤 disabled。 |
| **mcp_call** C（`mcp_call.py:127`） | `server`、`tool`；`arguments?={}` | dispatch 模式统一调用入口；全名、server+短名、唯一后缀容错；递归修正部分类型。当前会绕过目标工具权限和启用检查，详见问题清单。 |
| **SyntheticOutput** R（`synthetic_output.py:15`） | `output` 为对象/数组/字符串 | JSON 输出出口；可注入 schema，但只检查顶层 object/array/string 和 required 字段，不是完整 JSON Schema validator。 |
| **Agent** C（`agent_tool.py:25`） | `prompt`、`description`；`subagent_type?/model?/run_in_background?=false/name?/isolation?/plan_mode_required?=false/team_name?` | 启动一次性子 Agent 或长期 teammate；成本、权限继承、worktree 与生命周期由协作领域负责。 |
| **TeamCreate** C（`team_create.py:19`） | `team_name`；`description?=''` | 创建团队并装配团队工具/上下文；不是只读目录操作。 |
| **TeamDelete** C（`team_delete.py:19`） | `team_name` | 删除团队关联状态，具体成员和资源清理见团队专题。 |
| **SendMessage** C（`send_message.py:21`） | `to`、`content`；`type?='text'/request_id?=''/approve?` | 团队文本与审批/关闭等结构化协议消息；不是普通外部聊天连接器。 |
| **TaskCreate** C（`task_create.py:18`） | `title`；`description?=''/assignee?=''/blocks?/blocked_by?` | 创建团队共享任务和依赖关系。 |
| **TaskGet** R（`task_get.py:18`） | `task_id` | 查询任务详情及依赖。 |
| **TaskList** R（`task_list.py:18`） | `status?/assignee?` | 筛选当前团队任务。 |
| **TaskUpdate** C（`task_update.py:18`） | `task_id`；`status?/assignee?/description?/add_blocks?/add_blocked_by?` | 更新任务；状态集合 pending/in_progress/completed/blocked。 |
| **TaskStop** C（`task_stop.py:18`） | `teammate` | 停止指定 teammate，由 TeamManager 管理实际后端。 |
| **mcp__server__tool** C（`mcp/tool_wrapper.py:86`） | 服务器原始 JSON schema | 动态扩展；全部按 command 处理、默认延迟；没有利用服务器只读提示细分风险。非文本内容被简化，图片仅 MIME 占位、二进制资源仅 URI。 |

`diff.py`、`file_state_cache.py`、`base.py` 是辅助设施，不是额外模型工具。`diff.build_diff()` 通过公共首尾行定位变化，不是通用最小差异算法；最多显示 200 行，增删统计仍计完整变化（`tools/diff.py:12`、`:22`）。

## 4. 从模型调用到执行、历史与 UI 的真实链路

### 4.1 目录、schema 与结果协议

`Tool` 要求 name、description、params_model、execute；`get_schema()` 调 Pydantic 导出 input_schema。`ToolResult` 保存 output、is_error，以及可选 content_blocks。structured blocks 目前主要承载 native MCP 检索返回的 tool_reference；人类可读 output 仍给 UI/日志（`tools/base.py:28`）。注册表的 get 不检查 disabled，只有 is_enabled 才检查（`tools/__init__.py:34`）；这在分发器处构成了真实缺口。

工具名称冲突时 `register()` 直接覆盖。权限属性、工具状态、schema 暴露状态分散为 category、should_defer、_disabled、_discovered 和两项 expose 开关。StayCode 应把“可发现、对模型暴露、用户授权、实际可执行、可并发”分成清晰属性，避免用单一 read/command 承担全部语义。

### 4.2 交互与非交互有三套入口

```text
LLM stream → StreamCollector → 完整 ToolCallComplete
  ├─ PermissionChecker 首次判断为 ask → deferred_tool_calls
  └─ 其余 → StreamingExecutor.submit（仅收集，不立即运行）
流结束 → assistant tool_use 入会话
  → execute_all：连续并发安全调用成批 gather；写/命令独占串行
  → _execute_single_tool_direct：存在/启用检查 → 权限 deny 检查 → 参数校验 → execute
  → ask 队列逐个 _execute_tool：权限检查 → Future 等待人工答复 → execute
  → 结果溢写/聚合预算 → ToolResultBlock 入历史 → ToolResultEvent 给 UI

非交互：_execute_tool_noninteractive
  → 存在/启用 → pre_tool hooks → 权限（ask 通常拒绝）→ 校验/执行 → post_tool hooks
```

关键源码：`agent.py:245` 分批、`:280` executor、`:679` 初次分流、`:799` 执行第一组、`:825` 最后执行 ask 组、`:914` 直接入口、`:965` 人工审批入口、`:1316` 非交互入口。部分注释仍称“流中立即执行”，但 submit 实际仅 append（`:292`），报告以实现为准。

两个入口差异尤其重要：交互链没有 pre/post tool hooks；ask 调用被全部移到其他调用之后，会改变一轮模型给出的跨组先后关系。若先请求写文件并需要审批，后请求读取同一路径且已允许，读取将先执行。direct 路径第二次权限判断只处理 deny、不处理 ask；规则在两次检查间改变时也没有统一处理。

人工 Allow Always 把 extract_content 截到前 60 字符后拼 `*` 写入本地规则（`agent.py:1023`）；这不是“只批准相同参数”的精确持久授权。没有 content 映射的工具会产生 `*`，即该工具全放行。

### 4.3 三类“缓存”不能混为一谈

1. **文件状态缓存**：同一基础 registry 的 Read/Edit/Write 共用内存 `{resolved_path: mtime_ns}`。成功 ReadFile 后记录；Edit/已有文件 Write 前比较；成功写后更新。它不是文件内容缓存，也不跨会话持久化。ReadFile 先读取后 stat，有竞争窗口；仅 mtime 无内容哈希；stat 失败在 check 中返回允许（`file_state_cache.py:28`）。
2. **权限规则解析缓存**：三份规则文件按 `(mtime_ns,size)` 缓存，单次 check 共享同一规则快照（`permissions/rules.py:104`、`:129`）。规则优先级 deny > ask > allow，但只对真正走到规则引擎的分支成立。
3. **模型提示词缓存**：MCP schema 暴露策略尽量保持 tools 数组稳定；`client.py:82` 在最后一个非延迟工具上附 cache_control，native 工具带 defer_loading 时添加 beta header（`:215`）。源码里的命中率数字属于作者注释，未在本次分析中复现实测。

### 4.4 工具输出持久化

单结果超过 50,000 字符时保存完整文本，对话保留约前 2,000 字符预览及路径；写盘失败则保留原结果（`tools/base.py:23`、`agent.py:1387`、`context/manager.py:109`）。同轮多结果还经过聚合预算，先落最大输出；读取溢写文件豁免再次溢写，防止模型读不回原文（`context/manager.py:137`、`:152`）。UI 接收的仍可为原始全文，不能把模型上下文限额当成进程内存或 UI 限额。

输出溢写是结果存档，FileHistory 是代码回滚，两者完全不同。StayCode 应分别管理生命周期、清理策略和事件索引。

## 5. 权限与沙箱

### 5.1 当前决策顺序

`PermissionChecker.check()` 顺序如下（`permissions/checker.py:63`）：

1. Plan 特例：Agent/ToolSearch/AskUserQuestion/ExitPlanMode 直接允许；匹配“计划文件”的写入直接允许。
2. “安全只读命令”直接允许。
3. 正则危险命令黑名单拒绝。
4. sandbox_enabled 且 command：分割复合命令，deny/ask 规则生效，其余自动允许。
5. read/write 类工具用 extract_content 检查受保护路径/允许根；写受保护路径直接 deny，越界通常 ask，bypass 跳过越界 ask。
6. 用户、项目、本地规则合并裁决。
7. 模式默认矩阵；必要时请求人工确认。

| 模式 | read | write | command |
|---|---|---|---|
| default | allow | ask | ask |
| acceptEdits | allow | allow | ask |
| plan | allow | ask | ask |
| bypassPermissions | allow | allow | allow |

因此 plan 本身不是不可写执行环境，仍有特例、ask 与其他早返回；不能仅依赖模式名称实现只读承诺。PathSandbox 允许 project_root、系统 temp 和 extra_allowed；路径解析支持 expanduser 和现存祖先解析，并检查 symlink 逃逸。默认保护项目 `.mewcode/config.yaml`、`permissions.local.yaml` 和 `skills/`（`permissions/sandbox.py:15`），却不包含项目 `permissions.yaml`。路径沙箱保护基于工具被报告的目标，而不是操作系统强制隔离。

规则格式为 `ToolName(glob_pattern)`，工具名精确匹配、参数内容 fnmatch。Bash 映射 command；文件工具映射 file_path；Glob/Grep 映射 pattern；mcp_call 合成 server__tool；其他工具映射空串（`permissions/rules.py:19`、`:49`）。格式非法、文件缺失或 YAML 读取失败往往视为空规则，操作侧并不区分“没有策略”和“策略损坏”。

### 5.2 OS 沙箱实际覆盖

`create_sandbox()` 仅 macOS/Linux 有实现；Windows 返回 None（`sandbox/__init__.py:45`）。

| 平台 | 后端与边界 | 需要注意 |
|---|---|---|
| macOS | sandbox-exec，允许全局读、进程执行/fork/sysctl-read；白名单可写，deny_write 限制写；network 开关 | available 仅检查可执行文件存在；SBPL 路径字符串没有额外语言转义；OS 实际兼容性未测 |
| Linux | bwrap user/pid namespace，根只读挂载、白名单 bind 可写、deny_write ro-bind；默认 unshare-net；bash -c | available 仅检查 PATH；未探测 namespace 能力；不存在的挂载目标可能失败；未实际验证 |
| Windows | 无 OS 沙箱 | Bash 实为平台 shell，POSIX command/profile 不可直接通用；配置 auto_allow 仍可能被错误启用 |

TUI 仅给 **Bash 实例**挂载 OS 沙箱，allow_write 为 work_dir 和 `/tmp`，deny_write 只两项配置文件（`app.py:749`）。但权限自动放行作用于**所有 command 类工具**，包括 MCP、Agent、团队和 worktree，它们不会因这一标志自动进入 Bash 沙箱。保护范围不一致不能用“内核兜底”解释。

## 6. MCP 连接、延迟暴露与兼容性

### 6.1 连接及工具生命周期

`MCPManager` 按配置顺序逐台创建 client、连接、list_tools、构造 wrapper，一台失败记录错误并继续（`mcp/manager.py:45`）。支持 stdio 与 Streamable HTTP；Client 使用 `mode='auto'` 协议协商，实际协议行为委托 SDK（`mcp/client.py:51`）。stdio 子进程环境只显式继承 PATH 和声明 env；HTTP headers 会替换环境变量占位。关闭通过 AsyncExitStack。

**延迟加载只指 schema 进模型上下文，不是延迟建立服务器连接或延迟启动 stdio 进程。** connect_all 启动时已经连接所有配置服务器并列工具。没有本项目层面的 connect_all 总超时或并发连接控制；SDK 的超时与分页行为需要另验。

wrapper 把服务名/工具名非法字符替换为 `_`，拼成 `mcp__server__tool`，保留原 schema 对模型发送。调用前只按顶层 schema 生成 Pydantic 类型：object→dict、array→list；enum、嵌套、oneOf/$ref 等不完整映射。direct native/eager 会经这个模型，dispatch 则绕过该模型，按完整 schema 的有限子集进行递归转换并调用 execute_raw，造成模式间参数接受范围不一致。

`MCPClient._alive` 是客户端本地标志，不是健康探测。wrapper 异常时将其置 false，下次自己 connect；manager.get_client 又可创建替代 client，但已注册 wrapper 保留旧对象引用。重连、关闭、工具目录更新的所有权应统一到 manager，避免两条重连路径。

### 6.2 三种 schema 暴露策略

`loading_strategy.py:65` 以 schema JSON 字符数 / 2.5 估 token，与上下文窗口 10% 比较；可用 `MEWCODE_MCP_LOADING=eager/native/dispatch` 强制覆盖。

| 模式 | 条件 | tools 数组 | ToolSearch 返回 | 调用方式 |
|---|---|---|---|---|
| eager | 估算 MCP schema 小于窗口 10%，或无工具 | 所有 MCP 完整 schema；隐藏检索/分发工具 | 不需要 | 直接调用 wrapper |
| native | 超阈值且 endpoint 判为官方 Anthropic | MCP schema 留在 tools，标 defer_loading；暴露 ToolSearch | tool_reference content blocks | 服务端展开后直接调用 wrapper |
| dispatch | 超阈值且其他 endpoint | 隐藏 MCP schema；暴露 ToolSearch 与 mcp_call | schema JSON 文本追加消息 | mcp_call 间接调用 |

`ToolSearch` 检索按名称完整包含 +10、描述完整包含 +5、各词命中名称 +3/描述 +1，得分降序（`tools/__init__.py:77`）；不是语义向量搜索。`select:` 精确选名；MCP 检索不设置 discovered，避免检索后改变 tools 数组。普通非 MCP deferred 工具则会被标记 discovered 并进入后续 schema。

dispatch 的 coerce_by_schema 能递归对象 properties/array items、数字字符串/布尔字符串、单键数组包装和逗号分隔字符串。它是模型容错逻辑，不是完整校验，也不能替代服务端约束。StayCode 应把规范校验与可选容错显式区分，记录每次强转并避免把含逗号的合法单字符串误拆成多个元素。

服务器 instructions 会由宿主拼入模型上下文（`app.py:1951`、`remote.py:388`）；它们属于外部服务内容，需要保留来源和权限边界，不能当作可提升本地授权的政策。

## 7. Skills：发现、执行、热更新与安装

### 7.1 格式和目录优先级

加载顺序项目 `.mewcode/skills` → 用户 `~/.mewcode/skills` → builtin，同名先到先得，当前 builtin 已为空（`skills/loader.py:36`、`:141`）。支持目录 SKILL.md、平铺 `.md`、以及 `skill.yaml + prompt.md`。Markdown parser 要求 YAML frontmatter name/description，名称小写字母开头、数字和连字符；mode inline/fork，context full/recent/none；兼容 `context: fork`（`skills/parser.py:18`、`:62`）。

目录只扫描一级入口，嵌套资源不进入工具目录。技能附带 references/scripts 是磁盘资源，不会自动解读或执行。`get_catalog()` 返回 name/description；`get()` 尝试每次重新解析正文，出错使用缓存；needs_reload 只看两个技能根目录 mtime。YAML 格式初始化时有专用解析，但热加载统一调用 Markdown parser，这是格式不一致问题。

### 7.2 inline 与 fork

inline 用 `$ARGUMENTS` 替换正文；无占位且参数非空则追加 User Request；激活后保存在 agent.active_skills，并在恢复状态记录调用。LoadSkill 工具自身没有 args 参数，模型调用和斜杠调用的参数能力不同。

fork 新建 ConversationManager，试图按 none/recent/full 复制上下文，再创建新 Agent。recent 取最近 5 条非工具正文；full 实际是每条截前 200 字的文字摘要，不是完整对话；schema 中 model 字段已解析，但 executor 沿用当前 client，没有使用 skill.model。更严重的是查询属性 `_conversation`，主 Agent 实际写入 `_current_conversation`，上下文继承链脱节（`skills/executor.py:87`、`agent.py:562`）。

fork 复用主 registry/work_dir/client，permission_checker=None，未传 hooks；它隔离的是对话对象，不是工具权限、文件系统或进程状态（`skills/executor.py:70`）。LoadSkill 却是 read 且可并发，启动的子代理可以产生写入。必须在 StayCode 明确隔离层次和父子权限上限。

### 7.3 安装机制

URL 只接受 skills.sh、github.com/tree、raw.githubusercontent.com 三类主机，统一走 GitHub Contents API。skills.sh 被映射成 main 分支的 skills/目录；tree/ref 按单路径段解释，带斜杠的 ref 未处理。递归深度上限 4、文件最多 64、总量 8 MiB、元数据单文件上限 1 MiB；拒绝 entry.name 中 `..`、`/`、`\`，跳过 symlink/submodule（`skills/install.py:20`、`:223`）。

下载先写同目录 staging，检查有 SKILL.md 或 skill.yaml，然后删除旧目录再 rename（`:280`）。它减少半下载状态，但**不是完整原子替换**：删除成功、rename 失败会丢旧版本；校验只检查 manifest 文件存在，不校验内容能被 SkillLoader 接受。默认写用户全局目录，不经过普通文件工具的 file_path 路径检查。

StayCode 应保留 staging、配额和目录校验，补上发布者/来源/ref/内容哈希记录、manifest 预验证、旧版本备份与回滚；安装授权与技能执行授权应分开。

## 8. Hooks：配置能力与实际接线

`LifecycleEvent` 定义 15 个名字：session_start/end、turn_start/end、pre/post_tool_use、pre_send/post_receive、startup/shutdown、error、compact、permission_request、file_change、command_execute（`hooks/events.py:11`）。枚举存在不代表已接入全部触发点；搜索当前宿主和 agent，后五种没有对应 run_hooks 调用。TUI 有 startup/shutdown；交互循环有 session/turn/send/receive；非交互工具入口有 pre/post_tool。

条件支持字段 tool、event、args.<顶层键>；`==`、`!=`、regex `=~`、glob `~=`；一组只支持全 AND 或全 OR，不允许混合，未实现括号/转义语法（`hooks/conditions.py:60`）。动作模板直接替换 EVENT、TOOL_NAME、FILE_PATH、MESSAGE、ERROR、TOOL_ARGS.key。

| 动作 | 实际实现 | 边界 |
|---|---|---|
| command | 模板展开后 create_subprocess_shell；超时 kill 当前进程；合并输出 | 绕过 Tool 权限/OS 沙箱，未显式 cwd；模板是原始字符串替换，参数可能变成 shell 语法 |
| prompt | 返回展开文本；一般 run_hooks 会排入待发送提示消息 | pre_tool 专门通路只记通知，没有同样收集 prompt 队列 |
| http | urlopen 放线程执行，可展开 URL/body/headers，输出截 500 字 | timeout 写死 30 秒，未用 action.timeout；读取整个 body 后才截断 |
| agent | 记录日志并返回 success=True | **尚未实现的 stub**，不能宣称已有 Agent hook |

hooks 可 once、async；once 在实际执行前标记，失败也不会重试；async 用 ensure_future 但 engine 不保留任务集合供 shutdown 取消/等待。reject 只允许 pre_tool_use，async 不允许 pre_tool_use。pre_tool 上 reject=true 在动作返回后直接拒绝，与 exit code/success 无关；动作异常被捕获则不拒绝，语义不适合作强制安全门。

适合保留 hooks 的事件扩展思想，但安全策略必须在授权层实现；自动化 hook 动作也应交给同一个 ExecutionService，明确其宿主可信度、能力范围、失败策略和审计记录。

## 9. 文件历史与回滚

`FileHistory` 在 `.mewcode/file-history/<session_id>` 存原始 bytes 备份，以绝对路径 SHA-256 前 16 位和版本号命名。索引 `_tracked`、`_snapshots` 只在内存，threading.Lock 保护；最多留 100 个快照索引，没有对应磁盘垃圾回收（`filehistory/history.py:16`、`:35`）。

真实链路是：Write/Edit **开始时** track_edit → 读取修改前 bytes 并写新版本 → 真正校验/写入 → Agent 正常结束一轮时 make_snapshot（`agent.py:764`）→ `/rewind` 选择恢复代码/会话/两者（`commands/handlers/rewind.py:57`）。Bash、MCP、hooks 和外部编辑的修改不自动纳入记录。

rewind 对目标快照的备份逐个恢复；备份文件缺失就把当前目标删掉；目标快照没有但 `_tracked` 有的文件一律删掉；随后截断快照列表并回退版本。这里缺少“原本不存在”和“尚未追踪”的区分，也缺少 missing backup 与 intentional absence 的区分。写文件时没有原子事务、外部修改冲突检查或事先预览。

本次在随机 TemporaryDirectory 内复现：

```text
场景 A：先存在 existing.txt=original → 快照 S0（尚未追踪该文件）
        → track_edit → 写 modified → 快照 S1 → rewind(S0)
结果：existing_file_survives=False（已有文件被删除）。

场景 B：existing.txt=original → track_edit → 写 modified → 轮末快照 S0
        → rewind(S0)
结果：latest_checkpoint_content=original（最新轮末检查点引用的是修改前版本）。
```

以上只操作临时文件，测试后由标准库清理。现有 `test_file_history_rewind.py` 三条用例分别覆盖新建文件删除、预先 track 的原文件恢复、新建文件最新快照保留；没有覆盖这两个真实工具生命周期。StayCode 的回滚应在文件能力稳定、可持久重建之后再开放给用户，不能直接迁移此实现。

## 10. Remote 页面与跨平台情况

`web_content.py` 是单个大字符串：样式、DOM、Markdown、WebSocket、斜杠菜单、权限/问答对话框都在其中。支持连接重试（3 秒）、ping（10 秒）、历史 replay、流文字/思考、工具状态、usage、错误和 compact 消息。工具正常结果显示截前 5,000 字符，找不到匹配工具节点的回退路径未同样截断。

Markdown 来自 CDN 的未固定版本 marked.min.js，renderMarkdown 直接 marked.parse，随后 innerHTML，未见清洗（`web_content.py:217`、`:244`、`:474`）。模型内容/服务返回内容可成为 HTML，需要先消毒再进入 DOM。这里证实的是危险数据流；浏览器可利用性未在本轮动态测试。

问答前端使用 `q.question/q.Text`、对象 options 的 label/description，回传 `question_0` 等键（`:625`、`:665`），与 AskUserQuestion 的 message/name/字符串 options 不匹配；同时 Remote 当前没有注册 AskUserQuestion，也没有 ask_user_response 后端处理（`remote.py:207` 附近消息分派、`:257` 注册链）。因此该前端能力属于未完成接线，不应当成已实现特性。

跨平台上，大部分 pathlib/asyncio/Pydantic 数据逻辑可移植，但命令语义、目录权限、字符编码、文件锁、进程终止、MCP stdio 环境和 OS sandbox 并不自动可移植。Bash 没有固定 executable；在 Windows 实际随 Python shell 后端运行，POSIX 白名单和危险正则失去一致含义。stdio 环境仅继承 PATH（`config.py:99`），是否需要 SystemRoot/ComSpec 等系统变量取决于具体服务，需列入 Windows smoke test。测试中某些 POSIX 集成路径在 Windows 被 skip，不等于已在其他平台验证通过。

## 11. 已证实问题与优先级

以下优先级是 StayCode 设计/验收排序，不表示本次修改了原项目。

| 优先级 | 问题与影响 | 源码证据/验证 |
|---|---|---|
| P0 | **安全白名单包含可写/可执行任意程序的命令**；在 deny 规则和危险检查前 allow，且同时被用于并发安全判断 | `permissions/dangerous.py:22`、`:37`；`checker.py:84`；`tools/bash.py:130`。本地只做字符串分类，sed -i、find -delete、tee、npx、env python、git branch -D 全返回 True，未执行这些命令 |
| P0 | **mcp_call 可调用非 MCP 内建工具并绕目标授权/禁用**；_resolve 首先 registry.get(tool)，execute 最后直接 target.execute | `tools/mcp_call.py:158`、`:186`；`tools/__init__.py:37`。例如传 tool=WriteFile 会返回内建工具；外层仅审核 mcp_call 的 server__tool，而非目标文件。实际是否获得外层允许取决于模式/规则/用户批准 |
| P0 | **沙箱自动允许不等于实际隔离**：配置先允许，后验证可用性；且所有 command 自动允许，只有 Bash 包装 | `app.py:729`、`:748`、`:759`；`permissions/checker.py:99`；`sandbox/__init__.py:45`。enabled=true+auto_allow=true 在 Windows/缺后端时尤其直接 |
| P0 | **fork 技能丢失权限/hook 边界**；共享主工具目录，permission_checker=None | `skills/executor.py:70`；`tools/load_skill.py:68`。不是纯对话隔离能保证的安全执行 |
| P0 | **文件回滚删除已有但晚追踪的文件；轮末检查点引用修改前版本** | `filehistory/history.py:46`、`:61`、`:125`；`agent.py:764`。两项均已临时目录复现 |
| P1 | **Glob/Grep 路径授权检查错字段**，pattern 安全不能证明 path 在允许范围 | `permissions/rules.py:24`；`checker.py:115`；`tools/glob.py:28`、`grep.py:30`。可用普通 pattern 指向外部 path |
| P1 | **交互工具 hook 未接线；ask 队列导致跨组重排** | `agent.py:914`、`:965` 对比 `:1332`/`:1375`；分流 `:684`、执行 `:801`/`:826` |
| P1 | **Plan 文件例外过宽且绕过保护**：同 basename 或字符串包含 .mewcode/plans/ 即允许 | `permissions/checker.py:76`、`:146`。路径例外在 deny_write 和显式 deny 之前 |
| P1 | **策略文件保护不完整**：项目 permissions.yaml 不在默认 deny_write；全局技能与权限文件也非该项目列表 | `permissions/sandbox.py:15`；`app.py:735`。允许写后可影响下一次规则读取；Bash 路径更不统一 |
| P1 | **持久授权自动拓宽**：截前 60 字符+通配符；空映射退化为该工具 * | `agent.py:1023`；`permissions/rules.py:59` |
| P1 | **Remote Markdown 未清洗入 DOM**，存在 HTML 注入数据流 | `web_content.py:244`、`:474`，浏览器影响待动态验证 |
| P1 | **hook command 模板原样入 shell**，缺少参数化/能力约束；配置中看似引用文件路径可被其字符串内容改变命令语义 | `hooks/models.py:73`；`hooks/executors.py:17`。不应把项目 hook 当无副作用配置 |
| P2 | **技能上下文继承属性错位、YAML 技能热加载走错 parser、model 字段未使用** | `skills/executor.py:91` 对比 `agent.py:562`；`skills/loader.py:89`/`:153`；executor 创建 Agent 的参数 |
| P2 | **安装替换非原子；只校验 manifest 存在；单文件实际长度未二次核验** | `skills/install.py:182`、`:235`、`:252`、`:308`。总量校验仍存在，但在下载进内存后执行 |
| P2 | **MCP 名称清洗可碰撞、select 可返 disabled、dispatch 后缀解析与授权服务器不一定一致** | `mcp/tool_wrapper.py:25`；`tools/__init__.py:34`/`:116`；`mcp_call.py:106`/`:170`。应解析目标后才做目标权限判断 |
| P2 | **MCP 原 schema 与本地模型语义不一致**；direct model_dump(exclude_none=True) 丢显式 null，额外参数默认可能被忽略；JSON type 数组交给字典 lookup 会报类型错误 | `mcp/tool_wrapper.py:41`、`:58`、`:129`。具体服务器 schema 兼容性需用 fixture 覆盖 |
| P2 | **普通 Bash 非零退出永不标错；超时仅杀 shell；没有输出上限/取消清理保证** | `tools/bash.py:151`、`:159`、`:181`。退出语义 helper 存在但 execute 不使用；子进程存活后果需平台复现 |
| P2 | **hooks 功能表大于实现**：agent action 是成功 stub；HTTP timeout 忽略配置；多个事件无触发点；async 任务不受统一管理 | `hooks/executors.py:63`/`:78`；`hooks/events.py:33`；`hooks/engine.py:50` |
| P2 | **hook loader 在类型检查前 entry.get**，非 mapping 条目可能抛 AttributeError 而非预期 HookConfigError | `hooks/loader.py:27`、`:38` |
| P2 | **文件修改保护存在竞态且写入非原子**；历史追踪先于参数/文件检查，失败调用也推进版本 | `tools/read_file.py:45`/`:52`；`file_state_cache.py:37`；`write_file.py:41`/`:53`；`edit_file.py:43`/`:71` |

### 待验证而未冒充结论的事项

- MCP 2.2+/httpx2 SDK 当前实际字段名（input_schema/mime_type/is_error）、协议自动协商、分页、断线资源释放和 timeout。本机缺 mcp/httpx2，未用真实服务验证；源码依赖声明见 `pyproject.toml:12`。
- native 加载是否适用于所有配置协议。decide_mode 只按 endpoint/窗口判断，没有 protocol 参数；base_url 为空会视为 Anthropic 官方，而 registry native 分支又要求 anthropic。需要 OpenAI 官方空 URL、大 schema 的集成用例。
- bwrap 在 user namespace 禁用、保护文件不存在、容器内运行的结果；Seatbelt profile 语义及特殊路径转义；macOS 实际支持情况。
- Windows shell、取消后子进程清理、并发文件竞态、符号链接和网络目录的 mtime 行为。
- Remote Markdown 注入的浏览器可利用性与最终影响，需在隔离页面/假 WebSocket 环境测试；本次没有浏览器攻击试验。

## 12. 测试现状与重写验收

已阅读/检索相关测试：`test_permissions.py`、`test_permission_feedback.py`、`test_hooks.py`、`test_skills.py`、`test_mcp.py`、`test_mcp_call.py`、`test_tool_search.py`、`test_edit_file.py`、`test_diff.py`、`test_file_history_rewind.py`、`test_toolresult_wiring.py`、`test_tool_cache_marker.py`；并追踪到 batching/deferred 提醒相关集成点。它们覆盖大量局部 happy path 和近期回归，但不能证明整个工具执行面安全一致。

根代理本轮基线结果：当前 Python 3.13.9，未安装依赖；全量收集 480 项、13 个收集错误（缺 mcp/httpx2 等链路），不能宣称全量通过。七个焦点文件 33 passed，其中本专题直接相关 diff/edit/file-history 测试通过；原始日志位于 `docs/analysis/evidence/`。本专题另外用标准库 runpy 做了白名单分类与上述两条临时目录回滚复现，未改原测试。

**测试自身需先修正副作用边界**：`tests/test_hooks.py:531` 用真实 `Bash('rm -rf /')`、未注入 PermissionChecker（`:555`），寄望 pre hook 拦截；该测试 Windows skip（`:516`）。由于交互 hook 恰好缺失，不能在 Linux/macOS 未 mock subprocess 时直接运行它。应把所有模型生成命令替换为记录调用的 fake executor，而不是用破坏性命令测试阻断。

StayCode 的重点验收用例应包括：

1. 同一工具通过 direct、batch、noninteractive、MCP dispatcher、skill fork、hook 路径执行，授权和审计结果一致；被禁工具任何路径均不可执行。
2. 显式 deny 永远优先；命令风险判断覆盖参数、复合表达式、重定向和平台 shell；判不清时不做“只读并发”优化。
3. 沙箱不可用时绝不按已隔离放行；MCP/HTTP/子代理不能借 Bash 沙箱状态获得权限。
4. 先写后读且写需批准的同轮调用保持依赖顺序；中途取消能终止任务树并写出明确未执行结果。
5. 文件读版本与写时版本一致；多字节文本、CRLF、大文件、外部改动和原子写失败得到可恢复行为。
6. 回滚区分原已存在/新建/删除/未追踪；检查点保存轮末状态，重启可恢复；备份丢失不能自动删用户文件。
7. MCP 多模式都保留 null/嵌套/额外字段的明确语义，名称碰撞拒绝，禁用/服务器授权针对已解析的真实目标。
8. hooks 每个公开事件都有接线测试；技能两种 manifest 都能热加载，fork 上下文与权限继承经过断言。
9. Remote 共享一份消息 schema；不可信 Markdown 清洗，所有问答类型端到端回传原 name。

## 13. StayCode 保留、重构和延后建议

本节按工具专题列出候选方案。最终模块命名与阶段顺序见 [重写设计](../05-staycode-rewrite-design.md) 和 [路线图](../06-rewrite-roadmap.md)；本节中的 MVP/阶段不作为另一套全项目实施计划。

### 先保留概念，重新定义边界

保留 ToolResult + 结构化事件、参数模型生成 schema、工具发现、基础六工具、读前编辑、结果溢写、目录优先级、MCP 三模式思路和可插拔生命周期事件。保留功能目标，不兼容已有缺陷。可从原实现提取纯函数作为行为对照，但不要照抄权限短路与 dispatcher。

### 第一阶段必须重构

建议形成一条宿主无关的执行服务：

```text
ToolIntent
 → 解析真实目标与规范参数
 → 检查注册/启用/能力和来源
 → 计算读写/网络/进程资源范围
 → 授权策略（deny 优先，受保护资源与父级上限）
 → 人工决定或非交互拒绝
 → 选择实际可用的执行后端
 → 受限 pre hook
 → 执行/取消/超时/输出配额
 → 文件日志提交、post hook、审计与模型结果
```

`ToolCatalog` 仅负责元信息和能力发现；`ExecutionService` 是唯一执行入口；`PermissionPolicy` 处理目标资源而非任意字符串字段；`WorkspaceFileService` 统一 cwd、规范路径、版本和原子写；`ProcessService` 区分 Windows PowerShell/cmd 与 POSIX shell，并管理进程树；`ExtensionManager` 负责 MCP/skills/hooks 来源和权限范围。UI 只消费事件、提交审批，不重复装配业务规则。

MCP dispatcher 只能解析 MCP tool handle，不能拿 registry 任意名称执行；解析完成后基于服务器身份、工具身份和资源声明再授权。fork 继承父级权限上限，允许更窄不允许更宽；共享工具实例若有 mutable pending state，应改成每调用上下文或不可变定义。

### 分阶段迁移优先级

| 阶段 | 内容 | 完成标准 |
|---|---|---|
| MVP | Read/Write/Edit/Glob/Grep、ProcessService、统一 executor、权限 UI、输出存档 | 三平台基本操作；路径与命令授权不可绕；假执行器集成测试通过 |
| 第二阶段 | MCP stdio/HTTP、schema 验证、eager+dispatch、目录检索；inline skills | 插件失败不拖垮会话；参数/禁用/授权/取消一致 |
| 第三阶段 | native MCP、fork skills、受管 hooks、可靠文件检查点 | 有可持续的契约测试和跨平台验证；失败可解释可回滚 |
| 延后 | 任意 hook shell/HTTP 自动化、在线覆盖安装技能、复杂 rewind、多宿主独立实现 Remote 问答 | 依赖来源信任、事件协议、事务日志成熟后开放 |

特别建议：暂不把“自动沙箱放行”“全功能回滚”“hook agent 动作”写入 StayCode 首版承诺。先让基础执行、授权、取消、存档与错误语义可测试，再扩大能力范围，才能避免新品牌继承旧实现的隐性风险。
