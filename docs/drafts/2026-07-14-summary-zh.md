---
layout: default
title: "信先行 Action Cards: 2026-07-14 (ZH)"
date: 2026-07-14
lang: zh
---

> 从 30 条内容中筛选出 5 条教程/案例/技巧。

---

1. [Claude 一夜将 200 张杂乱收据转为整洁电子表格](#item-1) · PRODUCTIVITY_TIP · Score: 8.0 / 10
2. [在嵌入前重写用户查询以提升 RAG 准确性](#item-2) · TUTORIAL · Score: 7.0 / 10
3. [Digita：将提示词变成菜单驱动界面](#item-3) · TUTORIAL · Score: 6.0 / 10
4. [提示工程 vs 循环工程：构建可靠 AI 工作流](#item-4) · TUTORIAL · Score: 6.0 / 10
5. [针对 Claude 模型的提示词结构技巧](#item-5) · TUTORIAL · Score: 6.0 / 10

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uv4hsd" markdown="1">
<a id="item-1"></a>
## [Claude 一夜将 200 张杂乱收据转为整洁电子表格](https://www.reddit.com/r/PromptEngineering/comments/1uv4hsd/i_gave_claude_a_folder_of_200_messy_receipts_and/)

**栏目分类**: `PRODUCTIVITY_TIP`

**一句话简介**: 通过一次性将大量文件交给 Claude 并给出详细指令，实现自动化数据提取和整理，无需实时等待。

**具体怎么做**:
- 1. 将所有待处理的文件（如收据、发票）放入一个文件夹。
- 2. 向Claude发出指令，要求它查看文件夹中的所有文件，提取指定字段（如日期、金额、商家、用途），并整理成电子表格。
- 3. 在指令中明确要求：对于不清晰或无法读取的内容，在单独列中标记，而不是猜测。
- 4. 让Claude保存结果并告知提取情况。
- 5. 第二天检查结果，仅需核实标记的少数条目。

**适合谁/适用场景**: `需要处理大量文档数据提取的职场人士`, `财务人员、会计、行政助理`, `任何有大量纸质或电子收据、发票需要整理的人`

**效果或数据**: 200 个文件原本需要一整天手动录入，一次运行完成。

**可信度/风险提示**: 依赖 Claude 的准确性和文件清晰度；复杂格式或手写内容可能影响结果；需确保 Claude 有文件夹访问权限。

**实用度评分**: Score: 8.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uv4hsd/i_gave_claude_a_folder_of_200_messy_receipts_and/)

reddit · r/PromptEngineering · /u/Professional-Rest138 · 7月13日 07:22

**背景**: Claude 是 Anthropic 开发的 AI 助手，能够处理文件并遵循复杂指令。传统的收据数据提取通常需要手动录入或专门的 OCR 工具，而 Claude 的批量处理功能可以通过自然语言提示一次性处理大量非结构化文档。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://claude.com/pricing">Plans & Pricing | Claude by Anthropic</a></li>
<li><a href="https://docs.anthropic.com/en/docs/welcome">Welcome to Claude - Anthropic</a></li>
<li><a href="https://www.docuclipper.com/blog/receipt-data-extraction/">Receipt Data Extraction: How to Pull Data from Receipts (2026)</a></li>

</ul>
</details>

**标签**: `#需要处理大量文档数据提取的职场人士`, `#财务人员、会计、行政助理`, `#任何有大量纸质或电子收据、发票需要整理的人`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uvfprk" markdown="1">
<a id="item-2"></a>
## [在嵌入前重写用户查询以提升 RAG 准确性](https://www.reddit.com/r/PromptEngineering/comments/1uvfprk/the_highestleverage_prompt_in_a_rag_pipeline_is/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 本文介绍在 RAG 多轮对话中，通过一个小型压缩提示词将对话历史转化为独立、自包含的问题，从而大幅提升检索准确率的方法。

**具体怎么做**:
- 1. 获取最近几轮的用户输入和助手回复，限制上下文长度约 300 字符，避免嵌入整个对话记录。
- 2. 使用指令提示词，要求模型将当前用户问题结合历史上下文重写为一个独立的、自包含的问题。
- 3. 将重写后的问题用于嵌入和检索，而不是直接使用原始用户输入。

**适合谁/适用场景**: `RAG 系统开发者`, `需要处理多轮对话的 AI 应用`, `希望提升检索准确率的工程师`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法依赖提示词设计，不同模型和场景效果可能不同；需要根据实际对话长度调整上下文截断策略。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uvfprk/the_highestleverage_prompt_in_a_rag_pipeline_is/)

reddit · r/PromptEngineering · /u/kumard3 · 7月13日 16:02

**背景**: 检索增强生成（RAG）结合了检索步骤（查找相关文档）和生成模型来回答问题。在多轮对话中，用户常提出依赖先前上下文的后续问题，例如在助手提到某个地点后问“那费用明细呢？”。如果不进行重写，检索器可能获取不相关的文档块，导致模型失败。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://sureprompts.com/blog/rag-prompt-engineering-guide">RAG Prompt Engineering: How to Write Prompts That Work With ...</a></li>
<li><a href="https://arxiv.org/html/2501.03468v1">mtRAG: A Multi-Turn Conversational Benchmark for Evaluating ...</a></li>
<li><a href="https://github.com/IBM/mt-rag-benchmark">GitHub - IBM/mt-rag-benchmark: Multi-Turn RAG Benchmark</a></li>

</ul>
</details>

**标签**: `#RAG 系统开发者`, `#需要处理多轮对话的 AI 应用`, `#希望提升检索准确率的工程师`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uvo2l7" markdown="1">
<a id="item-3"></a>
## [Digita：将提示词变成菜单驱动界面](https://www.reddit.com/r/PromptEngineering/comments/1uvo2l7/can_a_prompt_act_as_an_interface_instead_of_a/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个开源提示词模板，让单个提示词像菜单驱动界面一样引导用户完成重复性任务，无需每次从头设计提示词。

**具体怎么做**:
- 使用 Digita 提示词模板（MIT 协议开源），该模板定义了交互规则：每次回复末尾显示编号选项，用户选择数字后模型才执行动作。
- 保留键：8=查看上下文，9=更新上下文（重启步骤），0=新任务。任务选项不与保留键冲突。
- 用户输入非编号的自由文本时，模型将其视为新上下文并回答，然后重新打印菜单，程序状态不受中断影响。
- 可见的交互计数器在对话过长时提示，并提供便携的“延续块”以便在新对话中恢复。
- 该提示词仅使用文本，可在 ChatGPT、Claude、Gemini 等任何指令跟随模型上运行，无需 API 或账户。

**适合谁/适用场景**: `需要重复执行固定流程的 AI 用户`, `希望简化提示词设计的提示工程师`, `需要与 AI 进行多步骤交互的普通用户`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该实验基于作者个人尝试，效果可能因模型和任务复杂度而异；开源模板需自行测试适配。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uvo2l7/can_a_prompt_act_as_an_interface_instead_of_a/)

reddit · r/PromptEngineering · /u/Carrer88 · 7月13日 20:58

**背景**: 大多数提示词是为单条指令设计的，用户需要为每个新任务重写提示词。Digita 将提示词重新构想为一个持久化程序，在中断时保持状态，将偏离脚本的问题视为上下文更新而非失败。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/BjornMelin/prompt-atlas">GitHub - BjornMelin/prompt-atlas: Expert-level prompt ...</a></li>

</ul>
</details>

**标签**: `#需要重复执行固定流程的 AI 用户`, `#希望简化提示词设计的提示工程师`, `#需要与 AI 进行多步骤交互的普通用户`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uvf7cn" markdown="1">
<a id="item-4"></a>
## [提示工程 vs 循环工程：构建可靠 AI 工作流](https://www.reddit.com/r/PromptEngineering/comments/1uvf7cn/are_we_overinvesting_in_prompts_and/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 本文指出过度关注提示词而忽视验证循环是常见误区，并介绍了构建可靠多步骤 AI 工作流的五步方法。

**具体怎么做**:
- 1. 用系统可验证的方式定义“完成”标准
- 2. 设置重试次数、时间和成本的限制
- 3. 在对话之外存储进度
- 4. 将产生输出的智能体与检查输出的机制分离
- 5. 随着任务变长，保持上下文和工具聚焦

**适合谁/适用场景**: `提示工程师`, `AI应用开发者`, `构建多步骤AI工作流的人员`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 原文为个人观点，未提供实验数据或案例验证；具体实现细节需参考原文链接中的指南。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uvf7cn/are_we_overinvesting_in_prompts_and/)

reddit · r/PromptEngineering · /u/Apart_Buy5500 · 7月13日 15:43

**背景**: 提示工程专注于为 AI 模型编写指令，但对于多步骤任务，单条提示无法验证正确性或处理失败。循环工程围绕模型设计系统——定义验证、重试逻辑和状态管理——以确保可靠结果。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.linkedin.com/pulse/ai-loop-engineering-workflow-build-agent-loops-finish-peter-m-xayge">AI Loop Engineering Workflow : Build Agent Loops That Finish the Job</a></li>
<li><a href="https://www.forbes.com/sites/lanceeliot/2026/06/17/loop-engineering-is-fully-making-the-rounds-for-boosting-generative-ai-and-agentic-ai/">Loop Engineering Is Fully Making The Rounds For Boosting...</a></li>
<li><a href="https://www.analyticsvidhya.com/courses/loop-engineering/">Loop Engineering Free Course – Build Autonomous AI Agents</a></li>

</ul>
</details>

**社区讨论**: Reddit 帖子邀请开发者讨论他们更关注改进提示还是验证循环。虽然未提供具体评论，但该话题引起了智能体工作流构建者的共鸣。

**标签**: `#提示工程师`, `#AI应用开发者`, `#构建多步骤AI工作流的人员`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uuwg43" markdown="1">
<a id="item-5"></a>
## [针对 Claude 模型的提示词结构技巧](https://www.reddit.com/r/PromptEngineering/comments/1uuwg43/modelspecific_prompt_structure_matters_more_than/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 分享针对 Claude 模型有效的提示词结构技巧，包括使用结构标签和显式推理请求。

**具体怎么做**:
- 使用结构标签（如<instructions>和<transcript>）将指令与内容分开，避免混合在段落中，文档越长效果越明显。
- 在回答前加入显式推理请求，例如“在回答前，简要推理权衡、选项和理由”，可显著提升判断类输出的质量。

**适合谁/适用场景**: `使用Claude模型的提示工程师`, `需要高质量结构化输出的用户`, `处理长文档或复杂判断任务的场景`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 技巧基于 Claude 模型，可能不适用于其他模型；效果因任务复杂度而异。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uuwg43/modelspecific_prompt_structure_matters_more_than/)

reddit · r/PromptEngineering · /u/Spiritual_Frame8340 · 7月13日 00:33

**背景**: 提示工程涉及精心设计输入，以引导像 Claude 这样的大型语言模型（LLM）产生期望的输出。由于训练数据和架构的差异，不同模型可能对提示结构有不同的响应。由 Anthropic 开发的 Claude 以受益于使用类似 XML 标签和显式推理步骤的结构化提示而闻名。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview">Prompt engineering overview - Claude Platform Docs</a></li>
<li><a href="https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices">Prompting best practices - Claude Platform Docs</a></li>
<li><a href="https://github.com/anthropics/prompt-eng-interactive-tutorial">anthropics/prompt-eng-interactive-tutorial - GitHub</a></li>

</ul>
</details>

**社区讨论**: 该帖子目前没有评论，但作者表示对其他人的模型特定技巧感到好奇，并愿意分享完整的模板。

**标签**: `#使用Claude模型的提示工程师`, `#需要高质量结构化输出的用户`, `#处理长文档或复杂判断任务的场景`

</section>

---