# StayCode 品牌替换验证报告

日期：2026-09-24。本报告记录本次品牌替换检查，不代表原项目所有功能已修复或验证。

## 结果

| 检查 | 实际结果 |
|---|---|
| 源目录 | 全部 208 个文件的哈希与原快照一致，无新增或删除 |
| 复制与内容 | 208/208 文件符合品牌替换和精确页眉清理规则 |
| Python | 188 个文件语法通过；品牌归一化后的 AST 与原版一致 |
| 第三方许可 | 两份技能 LICENSE 逐字节一致 |
| 品牌残留 | 复制的产品、测试、隐藏技能及配置中无旧品牌或宣传域名残留 |
| 依赖 | 项目 `.venv` 使用原锁文件安装；依赖约束和锁定版本不变；兼容性检查通过 |
| 构建 | `dist/staycode-0.2.0-py3-none-any.whl` 构建成功；146 个包内源码及资源与目标逐字节一致 |
| CLI | `staycode --help` 与 `python -m staycode --help` 均成功，显示新命令名 |
| TUI | Textual headless 生命周期成功，标题和主题为 StayCode，输入框、Agent 与会话已初始化 |
| 路径与资源 | `.staycode/sessions` 正常创建；STAYCODE.md 加载成功；3 个内置 Agent、2 个技能正常加载 |
| 队友启动 | 生成命令使用 `-m staycode --teammate`，未启动真实队友进程 |
| 安全回归 | 11 个原有测试文件，**92 passed in 18.77s** |
| 独立审查 | 源目标差异、包资源、命名链路及文档复核未发现本次引入的问题 |

验证环境：Windows，Python 3.13.9，StayCode 0.2.0；测试使用项目 `.venv` 的锁定依赖。CLI/TUI 与测试使用独立临时工作目录及 HOME/USERPROFILE，覆盖含中文和空格的路径，不加载用户真实配置。

## 命令与证据

在项目根目录执行：

```powershell
.\.venv\Scripts\uv.exe sync --frozen --inexact
.\.venv\Scripts\uv.exe build --wheel
.\.venv\Scripts\uv.exe pip check
.\.venv\Scripts\python.exe -X utf8 -B docs\analysis\evidence\branding_startup_check.py
```

回归文件：`test_hello_world.py`、`test_conversation_pairing.py`、`test_serialization.py`、`test_session_no_duplicate.py`、`test_file_history_rewind.py`、`test_diff.py`、`test_recovery.py`、`test_team_protocol.py`、`test_context.py`、`test_edit_file.py`、`test_crashlog.py`。完整命令及输出保存在下列证据中。

- [文件映射与哈希](analysis/evidence/branding-file-map.json)
- [静态与 wheel 检查](analysis/evidence/branding-static.json)
- [依赖安装](analysis/evidence/branding-install.txt)与[构建输出](analysis/evidence/branding-build.txt)
- [CLI 帮助输出](analysis/evidence/branding-cli-help.txt)
- [启动检查结果](analysis/evidence/branding-startup.json)与[可复验脚本](analysis/evidence/branding_startup_check.py)
- [TUI 启动画面](analysis/evidence/branding-tui.svg)
- [92 项测试输出](analysis/evidence/branding-pytest.txt)

启动检查使用占位密钥、显式上下文大小、空 MCP 配置，并拦截 HTTP 客户端请求；观测到 0 次 HTTP 请求，没有提交真实模型任务。这是验证脚本，不是新增产品演示模式。

## 验证边界与执行异常

- 没有运行完整测试套件。原 hooks 和 permissions 中的真实危险命令用例、consolidation 的真实模型用例，以及可能清理用户团队目录的用例均未执行。
- 未验证真实模型生成、外部 MCP 服务、Remote 联网流程或 Linux/macOS 的 tmux/iTerm2 协作。启动成功与局部回归通过不等于这些功能均已验证。
- 原代码中版本展示不一致、权限与退出处理、技能评估脚本参数等问题仍沿用原实现，详见历史源码分析；本次没有修复这些问题。
- 首次 TUI 验证的功能断言通过，但测试框架退出没有关闭产品会话文件，Windows 随后拒绝移除临时目录。验证脚本添加测试会话关闭后复验成功，产品代码未改。[首次输出](analysis/evidence/branding-startup-initial.txt)保留用于追溯。
- 自动审批拒绝进一步删除该次残留临时目录，原因仅为 `blocked by policy`。该次用户临时目录保留；其中只有该次验证会话数据，不影响 StayCode 项目。公开文档省略本机临时目录绝对路径。

源码分析和来源说明允许保留旧品牌以保证记录准确，不属于产品残留。

## 后续：用户模型配置验证

2026-09-24，按用户请求验证其新填写的配置。上述品牌替换验证阶段的“未调用真实模型”是当时的记录；本次追加验证如下：

- 用户将配置填在 `.staycode/config.yaml.example`，该文件不被自动加载；已原样启用为 `.staycode/config.yaml`，用户填写的原文件保持不变。
- 正式配置通过程序校验及默认路径加载；协议为 `anthropic`，基础地址为 `https://api.deepseek.com/anthropic`，模型为 `deepseek-v4-pro`。该协议与地址符合 [DeepSeek 官方说明](https://api-docs.deepseek.com/guides/anthropic_api/)。
- 使用 StayCode 自身的 `create_client` 和流式解析链路发送简短验证请求，成功返回 `STAYCODE_OK`，正常 `end_turn`；耗时 1.54 秒，服务报告输入 108 tokens、输出 53 tokens。
- 验证请求临时限制输出为 2048 tokens，保留 `thinking: true`；生产配置未调整。没有向模型发送项目文件，也未允许执行工具。
- 配置中另有 1 个 MCP 服务，本次未启动或连接测试。该结果证明模型配置和基本流式调用可用，不代表完整 Agent 任务及所有扩展均已测试。
- 密钥没有进入工具输出或验证报告。只保留[脱敏验证结果](analysis/evidence/config-validation.json)。
