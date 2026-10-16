# 原项目全部文件与符号索引

本表由本地文件快照生成。行数包含注释和空行；符号为顶层类/函数，帮助导航，不代替各专题的语义分析。源码在相邻的 `mewcode-python` 目录中。

## 产品 Python 文件

| 文件 | 行数 | 顶层类 / 函数（起始行） |
|---|---:|---|
| [mewcode/__init__.py](../../../mewcode-python/mewcode/__init__.py) | 6 | 包导出 / 常量 / 空标记 |
| [mewcode/__main__.py](../../../mewcode-python/mewcode/__main__.py) | 644 | `main:23`, `_run_prompt:129`, `_parse_teammate_flags:424`, `_build_teammate_registry:450`, `_run_teammate:532` |
| [mewcode/agent.py](../../../mewcode-python/mewcode/agent.py) | 1410 | `StreamText:69`, `ThinkingText:74`, `RetryEvent:79`, `ToolUseEvent:85`, `ToolResultEvent:92`, `TurnComplete:101`, `LoopComplete:106`, `UsageEvent:111`, `ErrorEvent:117`, `CompactNotification:122`, `HookEvent:131`, `PermissionResponse:138`, `PermissionReply:145`, `PermissionRequest:155`, `ThinkingBlock:182`, `LLMResponse:188`, `StreamCollector:199`, `ToolBatch:240`, `partition_tool_calls:245`, `_ToolExecResult:273`, `StreamingExecutor:280`, `Agent:358` |
| [mewcode/agents/__init__.py](../../../mewcode-python/mewcode/agents/__init__.py) | 31 | 包导出 / 常量 / 空标记 |
| [mewcode/agents/builtins/__init__.py](../../../mewcode-python/mewcode/agents/builtins/__init__.py) | 6 | 包导出 / 常量 / 空标记 |
| [mewcode/agents/fork.py](../../../mewcode-python/mewcode/agents/fork.py) | 81 | `ForkError:25`, `build_forked_messages:29` |
| [mewcode/agents/loader.py](../../../mewcode-python/mewcode/agents/loader.py) | 147 | `AgentLoader:19` |
| [mewcode/agents/notification.py](../../../mewcode-python/mewcode/agents/notification.py) | 58 | `format_task_notification:18`, `inject_task_notifications:51` |
| [mewcode/agents/parser.py](../../../mewcode-python/mewcode/agents/parser.py) | 133 | `AgentParseError:23`, `AgentDef:31`, `parse_frontmatter:46`, `_validate_agent_meta:69`, `parse_agent_file:105` |
| [mewcode/agents/task_manager.py](../../../mewcode-python/mewcode/agents/task_manager.py) | 210 | `ProgressInfo:21`, `BackgroundTask:29`, `TaskManager:42` |
| [mewcode/agents/tool_filter.py](../../../mewcode-python/mewcode/agents/tool_filter.py) | 246 | `_is_mcp_tool:101`, `resolve_agent_tools:105`, `build_teammate_tools:154`, `clone_registry_for_fork:216`, `apply_coordinator_filter:238` |
| [mewcode/agents/trace.py](../../../mewcode-python/mewcode/agents/trace.py) | 90 | `TraceNode:13`, `TraceManager:26` |
| [mewcode/app.py](../../../mewcode-python/mewcode/app.py) | 2095 | `scan_files_for_at:108`, `expand_at_refs:130`, `ChatInput:144`, `_is_subagent_tool:310`, `_tool_title:314`, `_format_detail:337`, `ToolCallBlock:378`, `_to_past_tense:454`, `ToolGroupSummary:491`, `SubAgentBlock:519`, `MewCodeApp:583` |
| [mewcode/askuser_dialog.py](../../../mewcode-python/mewcode/askuser_dialog.py) | 272 | `InlineAskUserWidget:14` |
| [mewcode/client.py](../../../mewcode-python/mewcode/client.py) | 688 | `_mark_last_user_tail_for_cache:44`, `needs_tool_search_beta:72`, `_mark_last_tool_for_cache:81`, `LLMError:103`, `AuthenticationError:107`, `RateLimitError:111`, `NetworkError:119`, `LLMClient:123`, `_supports_adaptive_thinking:137`, `AnthropicClient:146`, `OpenAIClient:351`, `OpenAICompatClient:476`, `create_client:647`, `resolve_context_window:657` |
| [mewcode/commands/__init__.py](../../../mewcode-python/mewcode/commands/__init__.py) | 30 | 包导出 / 常量 / 空标记 |
| [mewcode/commands/completion.py](../../../mewcode-python/mewcode/commands/completion.py) | 82 | `CompletionPopup:11` |
| [mewcode/commands/handlers/__init__.py](../../../mewcode-python/mewcode/commands/handlers/__init__.py) | 40 | `register_all_commands:37` |
| [mewcode/commands/handlers/clear.py](../../../mewcode-python/mewcode/commands/handlers/clear.py) | 50 | `handle_clear:12` |
| [mewcode/commands/handlers/compact.py](../../../mewcode-python/mewcode/commands/handlers/compact.py) | 49 | `handle_compact:11` |
| [mewcode/commands/handlers/help.py](../../../mewcode-python/mewcode/commands/handlers/help.py) | 54 | `_format_aliases:11`, `handle_help:17` |
| [mewcode/commands/handlers/mcp.py](../../../mewcode-python/mewcode/commands/handlers/mcp.py) | 47 | `handle_mcp:12` |
| [mewcode/commands/handlers/memory.py](../../../mewcode-python/mewcode/commands/handlers/memory.py) | 53 | `handle_memory:11` |
| [mewcode/commands/handlers/plan.py](../../../mewcode-python/mewcode/commands/handlers/plan.py) | 38 | `handle_plan:12` |
| [mewcode/commands/handlers/review.py](../../../mewcode-python/mewcode/commands/handlers/review.py) | 34 | `handle_review:20` |
| [mewcode/commands/handlers/rewind.py](../../../mewcode-python/mewcode/commands/handlers/rewind.py) | 83 | `_handle_rewind:13` |
| [mewcode/commands/handlers/sandbox.py](../../../mewcode-python/mewcode/commands/handlers/sandbox.py) | 145 | `handle_sandbox:19`, `_show_status:56`, `_enable_sandbox:77`, `_disable_sandbox:124` |
| [mewcode/commands/handlers/session.py](../../../mewcode-python/mewcode/commands/handlers/session.py) | 125 | `handle_session:12` |
| [mewcode/commands/handlers/skill.py](../../../mewcode-python/mewcode/commands/handlers/skill.py) | 109 | `handle_skill:16`, `_handle_list:38`, `_handle_info:51`, `_handle_reload:75` |
| [mewcode/commands/handlers/skill_register.py](../../../mewcode-python/mewcode/commands/handlers/skill_register.py) | 101 | `register_skill_commands:23` |
| [mewcode/commands/handlers/status.py](../../../mewcode-python/mewcode/commands/handlers/status.py) | 58 | `handle_status:16` |
| [mewcode/commands/handlers/tasks.py](../../../mewcode-python/mewcode/commands/handlers/tasks.py) | 99 | `_format_elapsed:16`, `_format_status:23`, `create_tasks_handler:28`, `create_tasks_command:91` |
| [mewcode/commands/handlers/trace.py](../../../mewcode-python/mewcode/commands/handlers/trace.py) | 82 | `_format_elapsed:16`, `_status_icon:23`, `create_trace_command:27` |
| [mewcode/commands/handlers/worktree.py](../../../mewcode-python/mewcode/commands/handlers/worktree.py) | 172 | `create_worktree_command:15`, `_handle_create:58`, `_handle_list:94`, `_handle_enter:113`, `_handle_exit:132`, `_handle_status:158` |
| [mewcode/commands/loader.py](../../../mewcode-python/mewcode/commands/loader.py) | 154 | `_split_frontmatter:26`, `_first_non_header_line:43`, `_make_prompt_handler:52`, `load_dir:71`, `_parse_command_file:91`, `load_user_commands:134` |
| [mewcode/commands/parser.py](../../../mewcode-python/mewcode/commands/parser.py) | 42 | `parse_command:11`, `complete:24` |
| [mewcode/commands/registry.py](../../../mewcode-python/mewcode/commands/registry.py) | 104 | `CommandType:13`, `UIController:19`, `CommandContext:30`, `Command:45`, `CommandRegistry:56` |
| [mewcode/config.py](../../../mewcode-python/mewcode/config.py) | 279 | `ProviderConfig:35`, `resolve_env_vars:95`, `build_child_env:99`, `MCPServerConfig:110`, `WorktreeConfig:125`, `SandboxAppConfig:132`, `AppConfig:140`, `_load_single_file:153`, `_merge_config:215`, `load_config:250` |
| [mewcode/context/__init__.py](../../../mewcode-python/mewcode/context/__init__.py) | 45 | 包导出 / 常量 / 空标记 |
| [mewcode/context/manager.py](../../../mewcode-python/mewcode/context/manager.py) | 775 | `CompactBoundary:61`, `CompactEvent:75`, `spill_dir:86`, `ensure_session_dir:93`, `cleanup_tool_results:99`, `persist_tool_result:109`, `make_persisted_preview:120`, `is_spill_readback:137`, `apply_tool_result_budget:152`, `compute_compact_threshold:196`, `extract_summary:296`, `build_compact_messages:304`, `FileReadRecord:336`, `SkillInvocationRecord:343`, `RecoveryState:349`, `_approx_tokens:393`, `_truncate_by_tokens:399`, `_first_line:410`, `build_recovery_attachment:418`, `_group_messages_by_turn:490`, `_message_tokens:503`, `_compute_keep_start_index:508`, `_align_keep_start_to_tool_pair:549`, `_prefix_too_small_to_compact:568`, `CompactCircuitBreaker:581`, `UsageAnchor:602`, `auto_compact:635` |
| [mewcode/conversation.py](../../../mewcode-python/mewcode/conversation.py) | 226 | `ToolUseBlock:13`, `ToolResultBlock:20`, `ThinkingBlock:30`, `Message:36`, `_message_chars:55`, `estimate_tokens:66`, `ConversationManager:78` |
| [mewcode/conversation_pairing.py](../../../mewcode-python/mewcode/conversation_pairing.py) | 83 | `rejected_tool_result:33`, `ensure_tool_pairing:44` |
| [mewcode/crashlog.py](../../../mewcode-python/mewcode/crashlog.py) | 58 | `record:21`, `record_exception:34`, `install:42` |
| [mewcode/driver.py](../../../mewcode-python/mewcode/driver.py) | 40 | `NoAltScreenDriver:16` |
| [mewcode/filehistory/__init__.py](../../../mewcode-python/mewcode/filehistory/__init__.py) | 8 | 包导出 / 常量 / 空标记 |
| [mewcode/filehistory/history.py](../../../mewcode-python/mewcode/filehistory/history.py) | 139 | `Backup:19`, `Snapshot:26`, `FileHistory:33` |
| [mewcode/hooks/__init__.py](../../../mewcode-python/mewcode/hooks/__init__.py) | 40 | 包导出 / 常量 / 空标记 |
| [mewcode/hooks/conditions.py](../../../mewcode-python/mewcode/hooks/conditions.py) | 102 | `Condition:17`, `ConditionGroup:43`, `ConditionParseError:56`, `_parse_single:63`, `parse_condition:77` |
| [mewcode/hooks/engine.py](../../../mewcode-python/mewcode/hooks/engine.py) | 119 | `HookNotification:18`, `HookEngine:25` |
| [mewcode/hooks/events.py](../../../mewcode-python/mewcode/hooks/events.py) | 38 | `LifecycleEvent:11` |
| [mewcode/hooks/executors.py](../../../mewcode-python/mewcode/hooks/executors.py) | 102 | `execute_command:17`, `execute_prompt:42`, `execute_http:47`, `execute_agent:78`, `execute_action:95` |
| [mewcode/hooks/loader.py](../../../mewcode-python/mewcode/hooks/loader.py) | 122 | `HookConfigError:23`, `_identify:27`, `load_hooks:32` |
| [mewcode/hooks/models.py](../../../mewcode-python/mewcode/hooks/models.py) | 91 | `Action:14`, `ActionResult:27`, `Hook:33`, `HookContext:55`, `ToolRejectedError:86` |
| [mewcode/mcp/__init__.py](../../../mewcode-python/mewcode/mcp/__init__.py) | 12 | 包导出 / 常量 / 空标记 |
| [mewcode/mcp/client.py](../../../mewcode-python/mewcode/mcp/client.py) | 127 | `MCPClient:24` |
| [mewcode/mcp/loading_strategy.py](../../../mewcode-python/mewcode/mcp/loading_strategy.py) | 138 | `McpLoadingMode:47`, `is_official_anthropic_endpoint:53`, `estimate_schema_tokens:61`, `decide_mode:65`, `measure_mcp_schema_chars:88`, `apply_mode:105`, `decide_and_apply:127` |
| [mewcode/mcp/manager.py](../../../mewcode-python/mewcode/mcp/manager.py) | 117 | `ServerInfo:20`, `ConnectResult:27`, `MCPManager:34` |
| [mewcode/mcp/tool_wrapper.py](../../../mewcode-python/mewcode/mcp/tool_wrapper.py) | 158 | `sanitize_name:25`, `mcp_tool_name_prefix:30`, `build_mcp_tool_name:37`, `_build_params_model:41`, `_json_type_to_python:58`, `_extract_text:70`, `MCPToolWrapper:86` |
| [mewcode/memory/__init__.py](../../../mewcode-python/mewcode/memory/__init__.py) | 62 | 包导出 / 常量 / 空标记 |
| [mewcode/memory/auto_memory.py](../../../mewcode-python/mewcode/memory/auto_memory.py) | 596 | `get_auto_mem_path:48`, `get_user_auto_mem_path:61`, `is_auto_mem_path:76`, `ensure_memory_dir_exists:88`, `MemoryFile:99`, `parse_frontmatter:107`, `_cut_to_bytes:141`, `truncate_entrypoint_content:156`, `_format_size:197`, `build_memory_prompt:210`, `_build_entrypoint_section:232`, `_build_memory_lines:244`, `MemoryManager:313`, `_load_dir:543`, `_extract_field:574`, `_clear_dir:580` |
| [mewcode/memory/consolidation.py](../../../mewcode-python/mewcode/memory/consolidation.py) | 356 | `MemoryConsolidator:34`, `_lock_path:181`, `_read_last_consolidated_at:185`, `_try_acquire_lock:194`, `_rollback_lock:226`, `_is_process_running:239`, `_list_sessions_since:262`, `_build_consolidation_prompt:279` |
| [mewcode/memory/instructions.py](../../../mewcode-python/mewcode/memory/instructions.py) | 219 | `_parse_include:22`, `_resolve_include:40`, `process_includes:52`, `_find_git_root:124`, `_project_instruction_dirs:136`, `load_instructions:159` |
| [mewcode/memory/recall.py](../../../mewcode-python/mewcode/memory/recall.py) | 375 | `MemoryHeader:56`, `RelevantMemory:66`, `RecallResult:72`, `memory_age_days:93`, `memory_age:99`, `memory_freshness_text:109`, `parse_frontmatter:126`, `scan_memory_files:164`, `_read_memory_header:193`, `format_memory_manifest:233`, `find_relevant_memories:256`, `_select_relevant_memories:299`, `_extract_json_object:335`, `render_reminder:355` |
| [mewcode/memory/session.py](../../../mewcode-python/mewcode/memory/session.py) | 501 | `_tool_uses_to_dicts:36`, `_tool_results_to_dicts:47`, `SessionRecord:59`, `_message_to_keep_dict:156`, `make_compact_boundary:168`, `parse_compact_boundary:185`, `records_to_messages:223`, `SessionMeta:249`, `Session:294`, `ResumeResult:346`, `generate_session_summary:357`, `_generate_session_id:394`, `SessionManager:400` |
| [mewcode/permission_dialog.py](../../../mewcode-python/mewcode/permission_dialog.py) | 132 | `InlinePermissionWidget:28` |
| [mewcode/permissions/__init__.py](../../../mewcode-python/mewcode/permissions/__init__.py) | 27 | 包导出 / 常量 / 空标记 |
| [mewcode/permissions/checker.py](../../../mewcode-python/mewcode/permissions/checker.py) | 158 | `Decision:23`, `PermissionChecker:28` |
| [mewcode/permissions/dangerous.py](../../../mewcode-python/mewcode/permissions/dangerous.py) | 64 | `is_safe_command:37`, `DangerousCommandDetector:50` |
| [mewcode/permissions/modes.py](../../../mewcode-python/mewcode/permissions/modes.py) | 33 | `PermissionMode:17`, `mode_decide:32` |
| [mewcode/permissions/rules.py](../../../mewcode-python/mewcode/permissions/rules.py) | 178 | `Rule:30`, `parse_rule:42`, `extract_content:49`, `_load_rules_file:65`, `RuleEngine:89`, `evaluate_rules:161` |
| [mewcode/permissions/sandbox.py](../../../mewcode-python/mewcode/permissions/sandbox.py) | 117 | `PathSandbox:12` |
| [mewcode/plan_dialog.py](../../../mewcode-python/mewcode/plan_dialog.py) | 121 | `PlanChoice:16`, `InlinePlanWidget:29` |
| [mewcode/prompts.py](../../../mewcode-python/mewcode/prompts.py) | 369 | `PromptSection:17`, `EnvironmentContext:24`, `PromptBuilder:36`, `detect_environment:169`, `environment_section:202`, `build_plan_mode_exit_reminder:278`, `build_plan_mode_reentry_reminder:286`, `build_plan_mode_reminder:293`, `build_system_prompt:321`, `build_environment_context:346` |
| [mewcode/remote.py](../../../mewcode-python/mewcode/remote.py) | 787 | `RemoteServer:72` |
| [mewcode/sandbox/__init__.py](../../../mewcode-python/mewcode/sandbox/__init__.py) | 61 | `SandboxConfig:22`, `Sandbox:33`, `create_sandbox:47` |
| [mewcode/sandbox/bwrap.py](../../../mewcode-python/mewcode/sandbox/bwrap.py) | 71 | `BwrapSandbox:21` |
| [mewcode/sandbox/seatbelt.py](../../../mewcode-python/mewcode/sandbox/seatbelt.py) | 81 | `_build_profile:24`, `SeatbeltSandbox:70` |
| [mewcode/serialization.py](../../../mewcode-python/mewcode/serialization.py) | 157 | `build_anthropic_messages:16`, `build_openai_input:67`, `build_chat_completion_messages:106`, `build_messages:152` |
| [mewcode/session_dialog.py](../../../mewcode-python/mewcode/session_dialog.py) | 155 | `_format_size:16`, `_relative_time:24`, `InlineResumeWidget:39` |
| [mewcode/skills/__init__.py](../../../mewcode-python/mewcode/skills/__init__.py) | 24 | 包导出 / 常量 / 空标记 |
| [mewcode/skills/builtins/__init__.py](../../../mewcode-python/mewcode/skills/builtins/__init__.py) | 6 | 包导出 / 常量 / 空标记 |
| [mewcode/skills/executor.py](../../../mewcode-python/mewcode/skills/executor.py) | 121 | `SkillExecutor:22` |
| [mewcode/skills/install.py](../../../mewcode-python/mewcode/skills/install.py) | 320 | `SkillSource:39`, `InstallReport:50`, `parse_skill_url:62`, `_ContentEntry:134`, `_parse_entries:145`, `_list_contents:162`, `_fetch_blob:185`, `_walk_and_download:211`, `_has_skill_manifest:252`, `_validate_skill_name:257`, `user_skills_root:269`, `install_skill:280` |
| [mewcode/skills/loader.py](../../../mewcode-python/mewcode/skills/loader.py) | 213 | `SkillLoader:26` |
| [mewcode/skills/parser.py](../../../mewcode-python/mewcode/skills/parser.py) | 132 | `SkillParseError:22`, `SkillDef:27`, `parse_frontmatter:38`, `resolve_mode_and_context:61`, `_validate_meta:77`, `parse_skill_file:99`, `substitute_arguments:121` |
| [mewcode/teammate_tree.py](../../../mewcode-python/mewcode/teammate_tree.py) | 68 | `TeammateTree:14` |
| [mewcode/teams/__init__.py](../../../mewcode-python/mewcode/teams/__init__.py) | 35 | 包导出 / 常量 / 空标记 |
| [mewcode/teams/backend_detect.py](../../../mewcode-python/mewcode/teams/backend_detect.py) | 65 | `BackendDetectionError:13`, `detect_backend_from_env:17`, `detect_backend:31`, `detect_pane_backend:51` |
| [mewcode/teams/coordinator.py](../../../mewcode-python/mewcode/teams/coordinator.py) | 237 | `get_coordinator_system_prompt:11`, `get_coordinator_reminder:211`, `get_coordinator_user_context:226` |
| [mewcode/teams/mailbox.py](../../../mewcode-python/mewcode/teams/mailbox.py) | 220 | `MailboxMessage:26`, `Mailbox:66`, `create_message:206` |
| [mewcode/teams/manager.py](../../../mewcode-python/mewcode/teams/manager.py) | 332 | `TeamError:32`, `TeamManager:36` |
| [mewcode/teams/models.py](../../../mewcode-python/mewcode/teams/models.py) | 172 | `BackendType:19`, `TeammateInfo:26`, `_sanitize_name:65`, `AgentTeam:72`, `teams_base_dir:150`, `resolve_team_dir:159`, `unique_team_name:164` |
| [mewcode/teams/progress.py](../../../mewcode-python/mewcode/teams/progress.py) | 113 | `random_verb:39`, `ToolActivity:44`, `_describe:54`, `TeammateProgress:74` |
| [mewcode/teams/protocol.py](../../../mewcode-python/mewcode/teams/protocol.py) | 114 | `new_request_id:42`, `shutdown_request:50`, `shutdown_response:60`, `plan_approval_request:72`, `plan_approval_response:81`, `request_id_of:93`, `is_shutdown_request:98`, `approved:109` |
| [mewcode/teams/registry.py](../../../mewcode-python/mewcode/teams/registry.py) | 44 | `AgentNameRegistry:10` |
| [mewcode/teams/shared_task.py](../../../mewcode-python/mewcode/teams/shared_task.py) | 135 | `SharedTask:14`, `SharedTaskStore:33` |
| [mewcode/teams/spawn.py](../../../mewcode-python/mewcode/teams/spawn.py) | 45 | `shell_quote:11`, `build_teammate_cli:25` |
| [mewcode/teams/spawn_inprocess.py](../../../mewcode-python/mewcode/teams/spawn_inprocess.py) | 303 | `_is_shutdown_request:32`, `_create_idle_notification:37`, `_inject_pending_messages:45`, `_wait_for_next_prompt_or_shutdown:56`, `_plan_mode_active:92`, `_read_plan_for_review:97`, `_run_plan_approval:106`, `InProcessTeammateHandle:141`, `spawn_inprocess_teammate:174` |
| [mewcode/teams/spawn_iterm2.py](../../../mewcode-python/mewcode/teams/spawn_iterm2.py) | 84 | `ITermPaneInfo:16`, `ITermSpawnError:20`, `spawn_iterm2_teammate:24`, `kill_pane:67` |
| [mewcode/teams/spawn_tmux.py](../../../mewcode-python/mewcode/teams/spawn_tmux.py) | 73 | `TmuxPaneInfo:15`, `TmuxSpawnError:20`, `_run_tmux:24`, `spawn_tmux_teammate:36`, `send_keys_to_pane:55`, `kill_pane:63` |
| [mewcode/teams/transcript.py](../../../mewcode-python/mewcode/teams/transcript.py) | 97 | `_serialize_conversation:15`, `_deserialize_conversation:41`, `save_transcript:72`, `load_transcript:87` |
| [mewcode/tools/__init__.py](../../../mewcode-python/mewcode/tools/__init__.py) | 200 | `ToolRegistry:16`, `create_default_registry:182` |
| [mewcode/tools/agent_tool.py](../../../mewcode-python/mewcode/tools/agent_tool.py) | 715 | `AgentToolParams:25`, `AgentTool:80` |
| [mewcode/tools/ask_user.py](../../../mewcode-python/mewcode/tools/ask_user.py) | 80 | `QuestionItem:15`, `AskUserParams:25`, `AskUserEvent:31`, `AskUserTool:43` |
| [mewcode/tools/base.py](../../../mewcode-python/mewcode/tools/base.py) | 130 | `ToolResult:29`, `Tool:39`, `TextDelta:82`, `ToolCallStart:87`, `ToolCallDelta:93`, `ToolCallComplete:98`, `ThinkingDelta:105`, `ThinkingComplete:110`, `StreamEnd:116` |
| [mewcode/tools/bash.py](../../../mewcode-python/mewcode/tools/bash.py) | 182 | `_extract_last_command_name:37`, `_interpret_exit_code:67`, `_exit_code_hint:98`, `Params:111`, `Bash:116` |
| [mewcode/tools/diff.py](../../../mewcode-python/mewcode/tools/diff.py) | 83 | `DiffResult:16`, `build_diff:22` |
| [mewcode/tools/edit_file.py](../../../mewcode-python/mewcode/tools/edit_file.py) | 84 | `Params:20`, `EditFile:26` |
| [mewcode/tools/enter_worktree.py](../../../mewcode-python/mewcode/tools/enter_worktree.py) | 71 | `EnterWorktreeParams:20`, `EnterWorktreeTool:31` |
| [mewcode/tools/exit_plan_mode.py](../../../mewcode-python/mewcode/tools/exit_plan_mode.py) | 53 | `ExitPlanModeParams:15`, `ExitPlanModeTool:19` |
| [mewcode/tools/exit_worktree.py](../../../mewcode-python/mewcode/tools/exit_worktree.py) | 116 | `ExitWorktreeParams:19`, `ExitWorktreeTool:33` |
| [mewcode/tools/file_state_cache.py](../../../mewcode-python/mewcode/tools/file_state_cache.py) | 52 | `FileStateCache:11` |
| [mewcode/tools/glob.py](../../../mewcode-python/mewcode/tools/glob.py) | 46 | `Params:15`, `Glob:20` |
| [mewcode/tools/grep.py](../../../mewcode-python/mewcode/tools/grep.py) | 61 | `Params:16`, `Grep:22` |
| [mewcode/tools/impl/__init__.py](../../../mewcode-python/mewcode/tools/impl/__init__.py) | 6 | 包导出 / 常量 / 空标记 |
| [mewcode/tools/impl/tool_search.py](../../../mewcode-python/mewcode/tools/impl/tool_search.py) | 118 | `ToolSearchParams:20`, `ToolSearchTool:25` |
| [mewcode/tools/install_skill.py](../../../mewcode-python/mewcode/tools/install_skill.py) | 89 | `InstallSkillParams:17`, `InstallSkillTool:27` |
| [mewcode/tools/load_skill.py](../../../mewcode-python/mewcode/tools/load_skill.py) | 86 | `LoadSkillParams:19`, `LoadSkill:23` |
| [mewcode/tools/mcp_call.py](../../../mewcode-python/mewcode/tools/mcp_call.py) | 210 | `_coerce_scalar:52`, `coerce_by_schema:74`, `permission_content:106`, `McpCallParams:127`, `McpCallTool:143` |
| [mewcode/tools/read_file.py](../../../mewcode-python/mewcode/tools/read_file.py) | 60 | `Params:19`, `ReadFile:25` |
| [mewcode/tools/send_message.py](../../../mewcode-python/mewcode/tools/send_message.py) | 169 | `SendMessageParams:21`, `SendMessageTool:33` |
| [mewcode/tools/synthetic_output.py](../../../mewcode-python/mewcode/tools/synthetic_output.py) | 67 | `SyntheticOutputParams:15`, `SyntheticOutputTool:19` |
| [mewcode/tools/task_create.py](../../../mewcode-python/mewcode/tools/task_create.py) | 66 | `TaskCreateParams:18`, `TaskCreateTool:26` |
| [mewcode/tools/task_get.py](../../../mewcode-python/mewcode/tools/task_get.py) | 59 | `TaskGetParams:18`, `TaskGetTool:22` |
| [mewcode/tools/task_list.py](../../../mewcode-python/mewcode/tools/task_list.py) | 72 | `TaskListParams:18`, `TaskListTool:23` |
| [mewcode/tools/task_stop.py](../../../mewcode-python/mewcode/tools/task_stop.py) | 76 | `TaskStopParams:18`, `TaskStopTool:22` |
| [mewcode/tools/task_update.py](../../../mewcode-python/mewcode/tools/task_update.py) | 84 | `TaskUpdateParams:18`, `TaskUpdateTool:30` |
| [mewcode/tools/team_create.py](../../../mewcode-python/mewcode/tools/team_create.py) | 109 | `TeamCreateParams:19`, `TeamCreateTool:24` |
| [mewcode/tools/team_delete.py](../../../mewcode-python/mewcode/tools/team_delete.py) | 51 | `TeamDeleteParams:19`, `TeamDeleteTool:23` |
| [mewcode/tools/write_file.py](../../../mewcode-python/mewcode/tools/write_file.py) | 58 | `Params:19`, `WriteFile:24` |
| [mewcode/validator.py](../../../mewcode-python/mewcode/validator.py) | 269 | `lookup_model_context_window:39`, `ConfigError:49`, `validate_providers:53`, `validate_permission_mode:110`, `validate_mcp_servers:120`, `validate_hooks:159`, `validate_bool_field:168`, `validate_worktree:175`, `validate_teammate_mode:208`, `validate_sandbox:218`, `validate_config_structure:243` |
| [mewcode/web_content.py](../../../mewcode-python/mewcode/web_content.py) | 808 | 包导出 / 常量 / 空标记 |
| [mewcode/worktree/__init__.py](../../../mewcode-python/mewcode/worktree/__init__.py) | 36 | 包导出 / 常量 / 空标记 |
| [mewcode/worktree/changes.py](../../../mewcode-python/mewcode/worktree/changes.py) | 78 | `_run_git:16`, `Changes:30`, `count_worktree_changes:35`, `has_worktree_changes:58`, `CleanupResult:64`, `has_unpushed_commits:70` |
| [mewcode/worktree/cleanup.py](../../../mewcode-python/mewcode/worktree/cleanup.py) | 102 | `_is_ephemeral:30`, `cleanup_stale_worktrees:34`, `start_stale_cleanup_task:89` |
| [mewcode/worktree/integration.py](../../../mewcode-python/mewcode/worktree/integration.py) | 42 | `generate_worktree_name:29`, `build_worktree_notice:37` |
| [mewcode/worktree/manager.py](../../../mewcode-python/mewcode/worktree/manager.py) | 312 | `WorktreeError:31`, `WorktreeManager:35` |
| [mewcode/worktree/models.py](../../../mewcode-python/mewcode/worktree/models.py) | 31 | `Worktree:13`, `WorktreeSession:23` |
| [mewcode/worktree/session.py](../../../mewcode-python/mewcode/worktree/session.py) | 66 | `_session_path:19`, `save_worktree_session:23`, `load_worktree_session:46` |
| [mewcode/worktree/setup.py](../../../mewcode-python/mewcode/worktree/setup.py) | 135 | `perform_post_creation_setup:22`, `_copy_local_configs:36`, `_setup_git_hooks:48`, `_create_symlinks:74`, `_copy_ignored_files:89` |
| [mewcode/worktree/slug.py](../../../mewcode-python/mewcode/worktree/slug.py) | 35 | `validate_slug:14`, `flatten_slug:34` |

## 测试文件

函数数按 AST 统计，不含参数化展开；`verify_subagent.py` 是单独验证脚本。

| 文件 | 行数 | test_ 函数数 |
|---|---:|---:|
| [tests/conftest.py](../../../mewcode-python/tests/conftest.py) | 26 | 0 |
| [tests/test_agent.py](../../../mewcode-python/tests/test_agent.py) | 576 | 18 |
| [tests/test_clear.py](../../../mewcode-python/tests/test_clear.py) | 139 | 3 |
| [tests/test_commands.py](../../../mewcode-python/tests/test_commands.py) | 479 | 42 |
| [tests/test_consolidation.py](../../../mewcode-python/tests/test_consolidation.py) | 334 | 10 |
| [tests/test_context.py](../../../mewcode-python/tests/test_context.py) | 679 | 51 |
| [tests/test_context_window.py](../../../mewcode-python/tests/test_context_window.py) | 240 | 18 |
| [tests/test_conversation_pairing.py](../../../mewcode-python/tests/test_conversation_pairing.py) | 64 | 5 |
| [tests/test_coordinator_multi_team.py](../../../mewcode-python/tests/test_coordinator_multi_team.py) | 106 | 2 |
| [tests/test_crashlog.py](../../../mewcode-python/tests/test_crashlog.py) | 62 | 2 |
| [tests/test_deferred_reminder.py](../../../mewcode-python/tests/test_deferred_reminder.py) | 97 | 3 |
| [tests/test_diff.py](../../../mewcode-python/tests/test_diff.py) | 55 | 5 |
| [tests/test_edit_file.py](../../../mewcode-python/tests/test_edit_file.py) | 46 | 2 |
| [tests/test_file_history_rewind.py](../../../mewcode-python/tests/test_file_history_rewind.py) | 73 | 3 |
| [tests/test_hello_world.py](../../../mewcode-python/tests/test_hello_world.py) | 10 | 1 |
| [tests/test_hooks.py](../../../mewcode-python/tests/test_hooks.py) | 570 | 50 |
| [tests/test_mcp.py](../../../mewcode-python/tests/test_mcp.py) | 318 | 21 |
| [tests/test_mcp_call.py](../../../mewcode-python/tests/test_mcp_call.py) | 451 | 45 |
| [tests/test_memory.py](../../../mewcode-python/tests/test_memory.py) | 796 | 54 |
| [tests/test_memory_recall_wiring.py](../../../mewcode-python/tests/test_memory_recall_wiring.py) | 87 | 2 |
| [tests/test_permission_feedback.py](../../../mewcode-python/tests/test_permission_feedback.py) | 227 | 8 |
| [tests/test_permissions.py](../../../mewcode-python/tests/test_permissions.py) | 834 | 61 |
| [tests/test_recovery.py](../../../mewcode-python/tests/test_recovery.py) | 74 | 5 |
| [tests/test_serialization.py](../../../mewcode-python/tests/test_serialization.py) | 127 | 9 |
| [tests/test_session_no_duplicate.py](../../../mewcode-python/tests/test_session_no_duplicate.py) | 100 | 4 |
| [tests/test_skills.py](../../../mewcode-python/tests/test_skills.py) | 483 | 38 |
| [tests/test_streaming_batching.py](../../../mewcode-python/tests/test_streaming_batching.py) | 235 | 11 |
| [tests/test_subagent.py](../../../mewcode-python/tests/test_subagent.py) | 792 | 61 |
| [tests/test_team_protocol.py](../../../mewcode-python/tests/test_team_protocol.py) | 70 | 5 |
| [tests/test_teammate_registry.py](../../../mewcode-python/tests/test_teammate_registry.py) | 88 | 2 |
| [tests/test_teams.py](../../../mewcode-python/tests/test_teams.py) | 843 | 63 |
| [tests/test_tool_cache_marker.py](../../../mewcode-python/tests/test_tool_cache_marker.py) | 68 | 6 |
| [tests/test_tool_call_block.py](../../../mewcode-python/tests/test_tool_call_block.py) | 52 | 5 |
| [tests/test_tool_search.py](../../../mewcode-python/tests/test_tool_search.py) | 321 | 11 |
| [tests/test_toolresult_wiring.py](../../../mewcode-python/tests/test_toolresult_wiring.py) | 159 | 3 |
| [tests/test_worktree.py](../../../mewcode-python/tests/test_worktree.py) | 361 | 45 |
| [tests/verify_subagent.py](../../../mewcode-python/tests/verify_subagent.py) | 509 | 0 |

## 元数据、样式与附带资源

以下覆盖非产品代码、非测试的其余文件。附带 Skills 是给原 Agent 使用的内容资产；其指令不是本次分析任务的上级指令。

| 文件 | 大小（字节） | 用途 |
|---|---:|---|
| [.gitignore](../../../mewcode-python/.gitignore) | 222 | 项目辅助文件 |
| [.mewcode/config.yaml.example](../../../mewcode-python/.mewcode/config.yaml.example) | 1077 | 示例配置，无真实凭据 |
| [.mewcode/skills/frontend-design/LICENSE.txt](../../../mewcode-python/.mewcode/skills/frontend-design/LICENSE.txt) | 10173 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [.mewcode/skills/frontend-design/SKILL.md](../../../mewcode-python/.mewcode/skills/frontend-design/SKILL.md) | 4438 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [.mewcode/skills/skill-creator/agents/analyzer.md](../../../mewcode-python/.mewcode/skills/skill-creator/agents/analyzer.md) | 10376 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [.mewcode/skills/skill-creator/agents/comparator.md](../../../mewcode-python/.mewcode/skills/skill-creator/agents/comparator.md) | 7287 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [.mewcode/skills/skill-creator/agents/grader.md](../../../mewcode-python/.mewcode/skills/skill-creator/agents/grader.md) | 9049 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [.mewcode/skills/skill-creator/assets/eval_review.html](../../../mewcode-python/.mewcode/skills/skill-creator/assets/eval_review.html) | 7058 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [.mewcode/skills/skill-creator/eval-viewer/generate_review.py](../../../mewcode-python/.mewcode/skills/skill-creator/eval-viewer/generate_review.py) | 16991 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [.mewcode/skills/skill-creator/eval-viewer/viewer.html](../../../mewcode-python/.mewcode/skills/skill-creator/eval-viewer/viewer.html) | 46307 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [.mewcode/skills/skill-creator/LICENSE.txt](../../../mewcode-python/.mewcode/skills/skill-creator/LICENSE.txt) | 11345 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [.mewcode/skills/skill-creator/references/schemas.md](../../../mewcode-python/.mewcode/skills/skill-creator/references/schemas.md) | 12052 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [.mewcode/skills/skill-creator/scripts/__init__.py](../../../mewcode-python/.mewcode/skills/skill-creator/scripts/__init__.py) | 159 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [.mewcode/skills/skill-creator/scripts/aggregate_benchmark.py](../../../mewcode-python/.mewcode/skills/skill-creator/scripts/aggregate_benchmark.py) | 14940 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [.mewcode/skills/skill-creator/scripts/generate_report.py](../../../mewcode-python/.mewcode/skills/skill-creator/scripts/generate_report.py) | 13338 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [.mewcode/skills/skill-creator/scripts/improve_description.py](../../../mewcode-python/.mewcode/skills/skill-creator/scripts/improve_description.py) | 11362 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [.mewcode/skills/skill-creator/scripts/package_skill.py](../../../mewcode-python/.mewcode/skills/skill-creator/scripts/package_skill.py) | 4527 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [.mewcode/skills/skill-creator/scripts/quick_validate.py](../../../mewcode-python/.mewcode/skills/skill-creator/scripts/quick_validate.py) | 4237 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [.mewcode/skills/skill-creator/scripts/run_eval.py](../../../mewcode-python/.mewcode/skills/skill-creator/scripts/run_eval.py) | 11767 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [.mewcode/skills/skill-creator/scripts/run_loop.py](../../../mewcode-python/.mewcode/skills/skill-creator/scripts/run_loop.py) | 14092 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [.mewcode/skills/skill-creator/scripts/utils.py](../../../mewcode-python/.mewcode/skills/skill-creator/scripts/utils.py) | 1867 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [.mewcode/skills/skill-creator/SKILL.md](../../../mewcode-python/.mewcode/skills/skill-creator/SKILL.md) | 30491 | 附带 Skill 说明、评估脚本、资源或技能许可 |
| [mewcode/agents/builtins/explore.md](../../../mewcode-python/mewcode/agents/builtins/explore.md) | 878 | 内置子 Agent 角色定义 |
| [mewcode/agents/builtins/general-purpose.md](../../../mewcode-python/mewcode/agents/builtins/general-purpose.md) | 589 | 内置子 Agent 角色定义 |
| [mewcode/agents/builtins/plan.md](../../../mewcode-python/mewcode/agents/builtins/plan.md) | 776 | 内置子 Agent 角色定义 |
| [mewcode/agents/builtins/verification.md](../../../mewcode-python/mewcode/agents/builtins/verification.md) | 1243 | 内置子 Agent 角色定义 |
| [mewcode/styles.tcss](../../../mewcode-python/mewcode/styles.tcss) | 3302 | Textual 样式 |
| [MEWCODE.md](../../../mewcode-python/MEWCODE.md) | 113 | 原项目开发约定，分析材料 |
| [pyproject.toml](../../../mewcode-python/pyproject.toml) | 597 | 包信息、运行依赖、CLI入口与构建配置 |
| [uv.lock](../../../mewcode-python/uv.lock) | 201359 | 锁定依赖及分发包哈希 |

## 可复核快照

文件总数：208。完整路径、字节数与 SHA-256 见 [source-manifest.json](evidence/source-manifest.json)。不包含外部主目录中的配置、会话或凭据；没有读取这些内容。
