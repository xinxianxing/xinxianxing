---
layout: default
title: "信先行 Action Cards: 2026-07-22 (ZH)"
date: 2026-07-22
lang: zh
---

> 从 26 条内容中筛选出 7 条教程/案例/技巧。

---

1. [如何让 GPT-4o 写出承包商风格](#item-1) · TUTORIAL · Score: 7.0 / 10
2. [防止 AI 编造 Bug 证据的提示词模式](#item-2) · TUTORIAL · Score: 7.0 / 10
3. [用一个提示词把 ChatGPT 从写作工具变成辅导老师](#item-3) · TUTORIAL · Score: 7.0 / 10
4. [大纲提示词决定幻灯片质量](#item-4) · TUTORIAL · Score: 7.0 / 10
5. [API 返回 200 但任务失败：验证 AI Agent 完成度](#item-5) · TUTORIAL · Score: 7.0 / 10
6. [最小线索提示词检验真实知识](#item-6) · TUTORIAL · Score: 7.0 / 10
7. [Jinja2 模板的三项解析时安全检查](#item-7) · PRODUCTIVITY_TIP · Score: 6.0 / 10

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1v2uke0" markdown="1">
<a id="item-1"></a>
## [如何让 GPT-4o 写出承包商风格](https://www.reddit.com/r/PromptEngineering/comments/1v2uke0/how_i_got_gpt4o_to_write_like_a_contractor_not_a/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一位创始人分享了让 AI 输出像真实承包商报价而非管理咨询风格的具体方法。

**具体怎么做**:
- 1. 用真实示例代替风格指令：给 AI 提供 3-4 个真实承包商报价截图，而不是告诉它“写得不正式”。
- 2. 将结构和内容分离：先让 AI 列出报价的各个部分（如工时、材料、总价），再填充具体内容。
- 3. 使用角色设定和约束：在系统提示中明确指定 AI 扮演的角色（如“你是一名有20年经验的承包商”）并限制输出格式。

**适合谁/适用场景**: `需要生成行业特定文本的开发者`, `希望 AI 输出更接地气的创业者`, `使用 AI 撰写报价、提案或合同的人`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法基于个人经验，效果可能因行业和具体用例而异；需要提供高质量的示例才能获得最佳结果。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1v2uke0/how_i_got_gpt4o_to_write_like_a_contractor_not_a/)

reddit · r/PromptEngineering · /u/Upbeat_Exam5410 · 7月21日 20:39

**背景**: 像 GPT-4o 这样的大型语言模型通常基于正式、专业的文本训练，导致默认输出咨询式语气。提示工程技术如提供示例和分离任务可以引导输出达到期望风格。这对需要清晰直接报价的服务承包商尤其相关。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://towardsdatascience.com/how-to-write-expert-prompts-for-chatgpt-gpt-4-and-other-language-models-23133dc85550/">How to Write Expert Prompts for ChatGPT (GPT-4) and Other Language Models | Towards Data Science</a></li>
<li><a href="https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide">GPT-4.1 Prompting Guide</a></li>
<li><a href="https://4idiotz.com/tech/artificial-intelligence/prompt-engineering-best-practices-gpt-4o/">prompt engineering best practices GPT-4o - 4idiotz</a></li>

</ul>
</details>

**社区讨论**: Reddit 帖子获得了积极反响，评论者赞赏这些实用技巧并分享了类似经验。一些人讨论了两步生成与单提示方法的权衡，另一些人则强调了领域特定示例对微调的重要性。

**标签**: `#需要生成行业特定文本的开发者`, `#希望 AI 输出更接地气的创业者`, `#使用 AI 撰写报价、提案或合同的人`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1v2r5oh" markdown="1">
<a id="item-2"></a>
## [防止 AI 编造 Bug 证据的提示词模式](https://www.reddit.com/r/PromptEngineering/comments/1v2r5oh/a_prompt_pattern_for_stopping_ai_from_inventing/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一种提示词约束方法，要求 AI 在修复 Bug 前对每个重要声明标注状态（观察、验证、推断、未知），从而避免编造证据。

**具体怎么做**:
- 在提示词中要求AI对每个重要声明标注为：OBSERVED（直接来自报告或工具输出）、VERIFIED（独立复现或确认）、INFERRED（基于证据的推断）、UNKNOWN（缺失或未测试的事实）。
- 禁止AI声称复现、根因、测试成功或生产行为，除非标注为VERIFIED。
- 在提出修复前，要求AI：重述预期与实际行为；列出最少缺失事实；生成复现步骤或非复现矩阵；对比失败路径与一个工作控制；以条件+机制+证据形式陈述最小支持原因；提出最小修复和回归不变性。
- 如果所需事实不可用，要求AI询问或标记结论为不确定。

**适合谁/适用场景**: `软件开发者`, `Bug分类人员`, `使用AI辅助调试的工程师`, `需要提高AI输出可审查性的场景`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法需要用户自行编写提示词并测试效果；实际效果可能因模型和任务复杂度而异。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1v2r5oh/a_prompt_pattern_for_stopping_ai_from_inventing/)

reddit · r/PromptEngineering · /u/RobeertIV · 7月21日 18:38

**背景**: Bug 分类是审查、评估和优先处理报告的软件缺陷的过程。用于调试的 AI 模型有时会产生幻觉或编造证据，导致错误的修复。该提示词模式通过强制模型明确标注每个声明的状态来缓解这一问题。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.atlassian.com/agile/software-development/bug-triage">Bug Triage: Definition, Examples, and Best Practices | Atlassian | Atlassian</a></li>
<li><a href="https://www.browserstack.com/guide/bug-triage-process">Bug Triage: What, Why and How to perform? | BrowserStack</a></li>
<li><a href="https://dev.to/naysmith/the-prompt-pattern-that-made-ai-coding-actually-work-3c88">The Prompt Pattern That Made AI Coding Actually... - DEV Community</a></li>

</ul>
</details>

**标签**: `#软件开发者`, `#Bug分类人员`, `#使用AI辅助调试的工程师`, `#需要提高AI输出可审查性的场景`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1v2oglo" markdown="1">
<a id="item-3"></a>
## [用一个提示词把 ChatGPT 从写作工具变成辅导老师](https://www.reddit.com/r/PromptEngineering/comments/1v2oglo/stop_letting_chatgpt_be_an_ai_writing_tool_for/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个提示词，让 ChatGPT 从代写作业的 AI 工具变成引导你学习的辅导老师。

**具体怎么做**:
- 将以下提示词输入ChatGPT：'You are my tutor, not my ghostwriter. I'm learning [topic]. Never write my assignment or give me paragraphs I can paste. Explain the core idea once, simply. Then ask me to explain it back. When I'm wrong, don't fix it. Ask a question that makes me find the gap. Keep going until I can teach it to you.'
- 将[topic]替换为你正在学习的具体主题。
- 按照ChatGPT的引导，先听它解释核心概念，然后用自己的话复述，回答它提出的问题，直到你能教会它为止。

**适合谁/适用场景**: `学生（尤其是本科生）`, `自学新知识的人`, `希望深入理解而非应付作业的学习者`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法需要学习者主动参与，效果取决于个人投入程度；ChatGPT 的引导质量可能因模型版本和主题而异。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1v2oglo/stop_letting_chatgpt_be_an_ai_writing_tool_for/)

reddit · r/PromptEngineering · /u/FormalSad2143 · 7月21日 17:05

**背景**: 目前许多学生使用 ChatGPT 等 AI 直接生成作业答案，绕过了学习过程。这种做法引发伦理担忧，并可能导致毕业生缺乏实际解决问题的能力。该提示词将 AI 的角色从捷径转变为学习伙伴。

**标签**: `#学生（尤其是本科生）`, `#自学新知识的人`, `#希望深入理解而非应付作业的学习者`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1v2nipn" markdown="1">
<a id="item-4"></a>
## [大纲提示词决定幻灯片质量](https://www.reddit.com/r/PromptEngineering/comments/1v2nipn/the_outline_prompt_decides_your_slide_deck_not/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个用于生成幻灯片大纲的提示词模板，强调先定大纲再生成内容，避免工具输出质量差的问题。

**具体怎么做**:
- 在生成幻灯片前，先运行以下大纲提示词：
- 提示词模板：'You are structuring a presentation outline. Do NOT write slide content yet. Topic: [topic] Audience: [who they are and what they already know] Goal: [the ONE thing they should do or believe after] Length: [N] slides, hard cap. Rules: - One idea per slide. If a slide has two ideas, split it. - Each slide = a short assertive headline (the takeaway, not a label) + max 3 supporting points. - No "Introduction" or "Conclusion" filler slides. Open on the stakes, close on the ask. - Order the slides as an argument, each one earning the next. Output a numbered list: slide number, headline, 3 bullets max.'
- 将生成的提纲粘贴到任何幻灯片生成工具中，即可获得结构清晰的初稿。

**适合谁/适用场景**: `需要制作演示文稿的职场人士`, `使用AI幻灯片生成工具但效果不佳的用户`, `希望提升幻灯片逻辑性和说服力的演讲者`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 提示词效果取决于用户对主题、受众和目标的清晰定义；不同工具对提示词的解析能力可能有差异。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1v2nipn/the_outline_prompt_decides_your_slide_deck_not/)

reddit · r/PromptEngineering · /u/East_Challenge5512 · 7月21日 16:32

**背景**: AI 幻灯片生成器常因收到模糊指令而输出杂乱无章的演示文稿。结构良好的大纲提示词充当蓝图，引导 AI 创建逻辑清晰、简洁的幻灯片，无论底层模型如何。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://yeasy.gitbook.io/prompt_engineering_guide/fu-lu/a_templates">附录 A：常用提示词模板库 | 大模型提示词工程指南 | Prompt Engineering Guide</a></li>
<li><a href="https://2slides.com/zh-CN/blog/2slides-vs-google-gemini-slides-comparison">2Slides 对比 Google Gemini 制作 幻 灯 片 ： AI ... | 2Slides 博客</a></li>
<li><a href="https://www.tinyash.com/blog/gamma-ai-presentation-guide/">Gamma AI... | 小灰灰的笔记 - AI工具分享与技术博客 | TinyAsh</a></li>

</ul>
</details>

**社区讨论**: 评论者通过自己的测试证实了这一发现，指出结构化提示词比模型升级效果更好。部分人讨论了卡片格式导出为 PPTX 的局限性。

**标签**: `#需要制作演示文稿的职场人士`, `#使用AI幻灯片生成工具但效果不佳的用户`, `#希望提升幻灯片逻辑性和说服力的演讲者`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1v2gtg4" markdown="1">
<a id="item-5"></a>
## [API 返回 200 但任务失败：验证 AI Agent 完成度](https://www.reddit.com/r/PromptEngineering/comments/1v2gtg4/my_agent_got_a_200_and_still_managed_to_fuck_up/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个 AI Agent 调用 API 返回 200 但实际业务状态错误的案例，教你如何通过定义后置条件来验证 Agent 的可靠性。

**具体怎么做**:
- 1. 在测试前明确期望的后置条件：对象是否存在、可见范围、状态、是否允许重复。
- 2. 将工作流和测试对话并排放置，检查提示词是否只描述了动作而未定义‘完成’的标准。
- 3. 使用工具（如Enter Pro's Agent Builder）时，手动验证外部系统的实际状态，不要仅依赖API返回码。
- 4. 针对并发写入和延迟问题，增加重试和状态校验逻辑。

**适合谁/适用场景**: `AI Agent开发者`, `提示词工程师`, `自动化工作流设计者`, `需要验证Agent可靠性的测试人员`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法基于个人经验，具体工具（Enter Pro's Agent Builder）可能不通用；需要用户自行调整验证步骤。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1v2gtg4/my_agent_got_a_200_and_still_managed_to_fuck_up/)

reddit · r/PromptEngineering · /u/Own_Boot_4993 · 7月21日 12:19

**背景**: AI Agent 通常通过 API 与外部系统交互，开发者传统上通过检查 HTTP 状态码（如 200）来验证成功。但这仅确认请求已接收，并不保证业务逻辑正确执行。后置条件验证是指在 Agent 操作后查询目标系统，以确认实际状态与预期一致。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.testsprite.com/blog/the-necessity-of-ai-validation-in-modern-development">The Necessity of AI Validation in Modern Development | TestSprite</a></li>
<li><a href="https://medium.com/@mitesh_shah/how-to-test-ai-agents-40c79f3ddba9">How to Test AI Agents. A practical guide to testing AI agents… | by Mitesh Shah | May, 2026 | Medium</a></li>
<li><a href="https://ai-reliability.institute/research/agentic-ai-reliability-checklist.html">Framework for Testing AI Agents: The 30-Point Agentic Reliability Enforcement Checklist | AI Reliability Institute</a></li>

</ul>
</details>

**社区讨论**: Reddit 帖子收到了分享类似经历的评论，并提出了幂等性检查、轮询最终一致性以及使用模拟系统模拟状态变化等技术。一些人强调，Agent 测试应同时包括单元级别的 API 检查和集成级别的业务状态验证。

**标签**: `#AI Agent开发者`, `#提示词工程师`, `#自动化工作流设计者`, `#需要验证Agent可靠性的测试人员`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1v29aus" markdown="1">
<a id="item-6"></a>
## [最小线索提示词检验真实知识](https://www.reddit.com/r/PromptEngineering/comments/1v29aus/this_prompt_exposes_whether_you_actually_know/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个提示词技巧，通过给出最小线索来测试你是否真正理解某个概念，而非仅仅识别它。

**具体怎么做**:
- 将以下提示词粘贴到ChatGPT、Claude、Perplexity、Gemini或NotebookLM等AI工具中：
- "Test my genuine knowledge of [TOPIC] in [SUBJECT] using the Minimum Viable Clue protocol. PROTOCOL: Ask me to recall or explain a concept, but give me the minimum possible clue — just enough that the question is fair, but not so much that it makes recall easy. For example: instead of 'Explain the process of photosynthesis,' use 'What happens when a leaf does its primary job?' After my answer, show me what a full-mark answer looks like and what I included vs. missed. Track a 'generative accuracy' score: percentage of required points I hit."
- 用你的具体主题和科目替换 [TOPIC] 和 [SUBJECT]。
- 回答AI提出的问题，然后查看AI给出的满分答案以及你的遗漏点。
- 根据生成的准确性分数（生成准确性百分比）评估自己的掌握程度。

**适合谁/适用场景**: `学生备考`, `自学者检验知识掌握度`, `需要区分“识别”与“生成”能力的学习者`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 提示词效果取决于 AI 模型和主题复杂度；生成准确性分数可能因 AI 评分标准不同而有偏差。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1v29aus/this_prompt_exposes_whether_you_actually_know/)

reddit · r/PromptEngineering · /u/Neat_Translator1865 · 7月21日 05:32

**背景**: 最小可行线索协议是一种利用测试效应（即从记忆中检索信息能强化学习）的学习方法。它与被动复习形成对比，被动复习中学生重读笔记并感到自信，但在考试条件下无法回忆细节。该协议利用 AI 以最小提示模拟主动回忆，使过程可扩展且个性化。

**标签**: `#学生备考`, `#自学者检验知识掌握度`, `#需要区分“识别”与“生成”能力的学习者`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1v2asgc" markdown="1">
<a id="item-7"></a>
## [Jinja2 模板的三项解析时安全检查](https://www.reddit.com/r/PromptEngineering/comments/1v2asgc/the_three_parsetime_checks_we_run_on_template/)

**栏目分类**: `PRODUCTIVITY_TIP`

**一句话简介**: 在 FastAPI 应用中，对用户编写的 Jinja2 模板进行三项解析时检查，防止资源耗尽攻击。

**具体怎么做**:
- 1. 检查模板中是否包含可能导致大量内存分配的模式，如 {{ ''|center(999999999) }}。
- 2. 限制模板中循环、递归或字符串操作的参数大小。
- 3. 在渲染前对模板进行静态分析，拒绝超出资源阈值的模板。

**适合谁/适用场景**: `使用 Jinja2 或类似模板引擎的开发者`, `需要防范资源耗尽攻击的 Web 应用`, `运行在内存受限环境（如 512MB 容器）中的服务`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法针对特定威胁模型（用户可编写模板），不适用于所有场景；实现细节需根据自身应用调整。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1v2asgc/the_three_parsetime_checks_we_run_on_template/)

reddit · r/PromptEngineering · /u/Parking-Kangaroo-63 · 7月21日 06:54

**背景**: Jinja2 是一个流行的 Python 模板引擎。它的 SandboxedEnvironment 能防止代码执行，但无法限制资源使用，因此像 {{ ''|center(999999999) }} 这样的模板可能分配约 1GB 内存，导致 512MB 的工作进程崩溃。这三项解析时检查在渲染前关闭了这种放大向量。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://tedboy.github.io/jinja2/off_doc.sandbox.html">2. Sandbox — Jinja2 API</a></li>
<li><a href="https://config-ninja.readthedocs.io/en/v1.6.0/jinja2/sandbox.html">jinja2.sandbox API documentation</a></li>
<li><a href="https://github.com/encode/uvicorn/issues/1226">Using UvicornWorkers in Gunicorn cause OOM on K8s · Issue #1226 · encode/uvicorn</a></li>

</ul>
</details>

**标签**: `#使用 Jinja2 或类似模板引擎的开发者`, `#需要防范资源耗尽攻击的 Web 应用`, `#运行在内存受限环境（如 512MB 容器）中的服务`

</section>

---