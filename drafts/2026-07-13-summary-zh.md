---
layout: default
title: "信先行 Action Cards: 2026-07-13 (ZH)"
date: 2026-07-13
lang: zh
---

> 从 19 条内容中筛选出 4 条教程/案例/技巧。

---

1. [两个提示约束修复长文本生成漂移](#item-1) · TUTORIAL · Score: 8.0 / 10
2. [AGENTS.md 配置指南：为 AI 编码助手设定项目规则](#item-2) · TUTORIAL · Score: 6.0 / 10
3. [媒体偏见检测的生产级提示词系统](#item-3) · TUTORIAL · Score: 6.0 / 10
4. [AI 代理通过 Git 历史时间旅行调试](#item-4) · TOOL · Score: 6.0 / 10

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uuef62" markdown="1">
<a id="item-1"></a>
## [两个提示约束修复长文本生成漂移](https://www.reddit.com/r/PromptEngineering/comments/1uuef62/two_prompt_constraints_that_fixed_most_of_my/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 分享两个提示词约束，解决长文本生成中模型引入无关角色和情节漂移的问题。

**具体怎么做**:
- 1. 角色名册（Roster）：在系统提示中维护一个固定角色列表，包含每个角色的姓名、身份和关键特征，并明确告诉模型“只能使用列表中已有的角色，不得创建新角色”。
- 2. 节拍门控（Beat Gating）：将故事大纲拆分为一系列“节拍”（beat），每个节拍描述一个关键事件或场景。在生成每个章节时，只提供当前节拍和前一两个节拍的内容，并指示模型必须严格遵循当前节拍，不得提前引入后续节拍的内容。

**适合谁/适用场景**: `需要生成长篇文本的AI用户`, `小说作者`, `内容创作者`, `使用LLM进行多章节写作的场景`

**效果或数据**: 作者使用该方案成功生成了 28 章约 8 万字的完整小说，解决了角色漂移和情节偏离问题。

**可信度/风险提示**: 该方法适用于长文本分块生成场景，但效果可能因模型和任务复杂度而异。需要根据具体故事调整角色名册和节拍粒度。

**实用度评分**: Score: 8.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uuef62/two_prompt_constraints_that_fixed_most_of_my/)

reddit · r/PromptEngineering · /u/Beginning_Support_86 · 7月12日 12:41

**背景**: 使用 LLM 进行长文本生成常出现连贯性问题，因为将整个手稿作为上下文输入成本过高。用户的流水线仅使用简短的状态摘要和之前的章节，导致模型丢失早期内容，从而出现角色漂移和情节提前解决。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://blog.laozhang.ai/zh/posts/nano-banana-pro-face-consistency-guide">Nano Banana Pro 人脸一致性完全指南：2026年AI... | LaoZhang AI Blog</a></li>
<li><a href="https://www.mianshiya.com/question/1991796944900497410">如何在 提 示 词 中设置 约 束 条件和输出要求？ - 面试鸭 | 2026...</a></li>

</ul>
</details>

**社区讨论**: 用户询问是否有比完整重读一遍更简洁的跨章节矛盾解决方案。来源中未提供其他评论。

**标签**: `#需要生成长篇文本的AI用户`, `#小说作者`, `#内容创作者`, `#使用LLM进行多章节写作的场景`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uus1gq" markdown="1">
<a id="item-2"></a>
## [AGENTS.md 配置指南：为 AI 编码助手设定项目规则](https://www.reddit.com/r/PromptEngineering/comments/1uus1gq/my_agentsmd_if_you_want_to_see_it_i_like_looking/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 分享一个用于 AI 编码助手的 AGENTS.md 配置文件，指导 AI 遵循项目约定、避免重复造轮子。

**具体怎么做**:
- 在项目根目录创建 AGENTS.md 文件，写入指令：优先使用成熟库、官方 SDK 和平台 API，避免手写客户端、解析器、协议处理等常见基础设施。
- 要求 AI 在修改代码前先广泛阅读现有代码，遵循已有模式，保持变更范围聚焦，不混入重构。
- 如果必须自定义实现，需说明原因并保持代码小巧、经过测试、独立。
- 子目录可放置局部 AGENTS.md 覆盖全局规则。

**适合谁/适用场景**: `使用 AI 编码助手（如 Cursor、Copilot）的开发者`, `希望规范 AI 生成代码质量的团队`, `需要减少重复造轮子的项目`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 配置效果取决于 AI 助手的理解能力，不同模型对 AGENTS.md 的遵循程度可能不同。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uus1gq/my_agentsmd_if_you_want_to_see_it_i_like_looking/)

reddit · r/PromptEngineering · /u/earonesty · 7月12日 21:26

**背景**: AGENTS.md 是一个放置在仓库根目录的 Markdown 文件，为 AI 编码代理提供持久的、项目特定的操作指南。它源于 AI 软件开发生态系统的协作努力，包括 OpenAI Codex、Cursor 和 Google 的 Jules。代理会自动读取目录树中最近的 AGENTS.md，允许子项目拥有定制的指令。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/agentsmd/agents.md">GitHub - agentsmd/agents.md: AGENTS.md — a simple, open format for guiding coding agents</a></li>
<li><a href="https://agents.md/">AGENTS.md</a></li>
<li><a href="https://www.augmentcode.com/guides/how-to-build-agents-md">How to Build Your AGENTS.md (2026): The Context File That Makes AI Coding Agents Actually Work | Augment Code</a></li>

</ul>
</details>

**标签**: `#使用 AI 编码助手（如 Cursor、Copilot）的开发者`, `#希望规范 AI 生成代码质量的团队`, `#需要减少重复造轮子的项目`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uus0md" markdown="1">
<a id="item-3"></a>
## [媒体偏见检测的生产级提示词系统](https://www.reddit.com/r/PromptEngineering/comments/1uus0md/my_productiongrade_prompt_for_media_bias/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一套用于检测新闻客观性和媒体偏见的结构化提示词系统，基于情报分析方法论，通过五维度评分和指令-数据分离来减少幻觉。

**具体怎么做**:
- 1. 设计五维度客观性评分标准：事实准确性、来源归因、平衡框架、利益冲突、透明度，每个维度1-5分。
- 2. 采用指令与数据分离模式：将所有指令文本与动态输入数据（主题、时间窗口、关注角度）隔离，防止LLM注意力稀释。
- 3. 实现红旗检测机制：自动标记可疑表述或潜在偏见信号。
- 4. 设置硬约束：要求LLM严格遵循评分规则，禁止输出未在输入中明确支持的评价。
- 5. 原文未提供完整提示词模板，但描述了核心设计模式。

**适合谁/适用场景**: `新闻研究者`, `事实核查人员`, `信息素养教育者`, `对媒体偏见敏感的普通读者`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法依赖 LLM 的推理能力，不同模型效果可能有差异；原文未提供完整提示词和测试结果，复现需要自行补充细节。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uus0md/my_productiongrade_prompt_for_media_bias/)

reddit · r/PromptEngineering · /u/blobxiaoyao · 7月12日 21:25

**背景**: 大语言模型常常难以区分指令和数据，导致幻觉和有偏见的输出。受情报分析方法论启发的结构化提示技术，通过定义明确的输出格式和推理步骤，旨在提高可靠性。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2403.06833">[2403.06833] Can LLMs Separate Instructions From Data? And What Do We Even Mean By That?</a></li>
<li><a href="https://www.alphaxiv.org/overview/2511.20836v3">Structured Prompts Improve Evaluation of Language Models | alphaXiv</a></li>
<li><a href="https://www.linkedin.com/pulse/structured-prompting-getting-llms-think-like-engineers-priya-raja-7hdef">Structured Prompting : Getting LLMs to Think Like Engineers</a></li>

</ul>
</details>

**标签**: `#新闻研究者`, `#事实核查人员`, `#信息素养教育者`, `#对媒体偏见敏感的普通读者`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1utyh4t" markdown="1">
<a id="item-4"></a>
## [AI 代理通过 Git 历史时间旅行调试](https://www.reddit.com/r/PromptEngineering/comments/1utyh4t/built_a_skill_that_teaches_ai_agents_to/)

**栏目分类**: `TOOL`

**一句话简介**: 一个开源工具，让 AI 代理能够回溯 Git 历史到指定时间点，分析旧版本代码以定位 bug 根因。

**具体怎么做**:
- 1. 克隆仓库：git clone https://github.com/MeherBhaskar/temporal-debug-skill
- 2. 在AI代理中集成该技能，使其能执行shell命令
- 3. 向代理提供时间描述（如“3小时前”、“v2.4.1”），技能会解析为精确commit SHA
- 4. 技能自动创建隔离的git worktree快照，代理在只读模式下分析历史代码
- 5. 分析完成后自动清理worktree，返回根因报告（含commit引用）

**适合谁/适用场景**: `AI代理开发者`, `需要调试历史版本bug的开发者`, `使用AI代理进行代码审查或调试的团队`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 依赖 git 环境，需要代理能运行 shell 命令；时间描述解析可能不准确；仅适用于 Git 管理的项目。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1utyh4t/built_a_skill_that_teaches_ai_agents_to/)

reddit · r/PromptEngineering · /u/Puzzled_Camera_7805 · 7月11日 23:06

**背景**: Git worktree 是 Git 的一个功能，允许同一仓库有多个工作目录，从而可以同时在不同分支上工作。Agentic skills 是可复用的指令集，用于扩展 AI 编码助手的能力。该工具结合了这两个概念，赋予 AI 代理时间调试能力。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://git-scm.com/docs/git-worktree">Git - git-worktree Documentation</a></li>
<li><a href="https://grokipedia.com/page/Git_worktree">Git worktree</a></li>

</ul>
</details>

**标签**: `#AI代理开发者`, `#需要调试历史版本bug的开发者`, `#使用AI代理进行代码审查或调试的团队`

</section>

---