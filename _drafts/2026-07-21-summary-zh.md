---
layout: default
title: "信先行 Action Cards: 2026-07-21 (ZH)"
date: 2026-07-21
lang: zh
---

> 从 28 条内容中筛选出 7 条教程/案例/技巧。

---

1. [提示词漂移导致模型对比失效](#item-1) · PRODUCTIVITY_TIP · Score: 7.0 / 10
2. [苏格拉底式提示词：把死记硬背变成真理解](#item-2) · TUTORIAL · Score: 7.0 / 10
3. [通过预提取清单避免多文档生成中的事实漂移](#item-3) · TUTORIAL · Score: 7.0 / 10
4. [顺序澄清引擎：先诊断再开方](#item-4) · TUTORIAL · Score: 7.0 / 10
5. [20 个可混搭的 ChatGPT 提示词模板（无需 GitHub）](#item-5) · TUTORIAL · Score: 6.0 / 10
6. [单人企业主 500 小时提示工程三大模板](#item-6) · TUTORIAL · Score: 6.0 / 10
7. [一周实测揭示 ChatGPT、Claude、Gemini 各自优势](#item-7) · PRODUCTIVITY_TIP · Score: 6.0 / 10

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1v1teni" markdown="1">
<a id="item-1"></a>
## [提示词漂移导致模型对比失效](https://www.reddit.com/r/PromptEngineering/comments/1v1teni/our_model_comparison_was_worthless_because_we/)

**栏目分类**: `PRODUCTIVITY_TIP`

**一句话简介**: 一个团队在对比新旧模型摘要能力时，因测试过程中反复调整提示词，导致对比结果无效，揭示了控制变量的重要性。

**具体怎么做**:
- 冻结提示词：在开始模型对比前，先确定一个固定的提示词版本，测试期间绝不修改。
- 单变量测试：每次只改变一个变量（如模型），保持其他条件（提示词、数据、评估标准）完全一致。
- 记录漂移：如果必须调整提示词，应记录每次改动，并重新运行基线模型的测试，确保对比公平。
- 使用版本控制：对提示词和测试结果进行版本管理，便于回溯和复现。

**适合谁/适用场景**: `AI工程师`, `提示词工程师`, `需要做模型选型的团队`, `进行A/B测试的开发者`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该案例基于个人经验，未提供量化数据；实际测试中完全冻结提示词可能不适用于所有场景，需根据任务灵活调整。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1v1teni/our_model_comparison_was_worthless_because_we/)

reddit · r/PromptEngineering · /u/larabyeol · 7月20日 18:16

**背景**: 提示词漂移是指由于模型更新或手动调整，提示词可靠性随时间逐渐下降。在对 LLM 进行 A/B 测试时，通过版本控制提示词并每次只改变一个因素来控制变量至关重要。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.getmaxim.ai/articles/how-to-perform-a-b-testing-with-prompts-a-comprehensive-guide-for-ai-teams/">How to Perform A/B Testing with Prompts: A Comprehensive ...</a></li>
<li><a href="https://inferensys.com/glossary/context-engineering-and-prompt-architecture/system-prompt-design/prompt-drift">Prompt Drift: Definition, Causes, and Mitigation | Inference ...</a></li>
<li><a href="https://medium.com/@amiyay.sinha/prompt-drift-the-silent-reliability-problem-in-production-llm-systems-f77cf1f714fa">Prompt Drift: The Silent Reliability Problem in Production ...</a></li>

</ul>
</details>

**标签**: `#AI工程师`, `#提示词工程师`, `#需要做模型选型的团队`, `#进行A/B测试的开发者`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1v1rygk" markdown="1">
<a id="item-2"></a>
## [苏格拉底式提示词：把死记硬背变成真理解](https://www.reddit.com/r/PromptEngineering/comments/1v1rygk/this_prompt_turns_any_fact_youve_memorised_into/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个提示词模板，让 AI 像私教一样通过连续追问“为什么”帮你从第一性原理理解任何概念。

**具体怎么做**:
- 1. 确定学科和要理解的事实或概念。
- 2. 将以下提示词填入ChatGPT、Claude等AI工具：'I am going to state a fact from [SUBJECT]: [STATE THE FACT OR CONCEPT] Do not explain it to me. Instead, interrogate me until I can explain WHY it is true from first principles. INTERROGATION PROTOCOL: Ask me only ONE question at a time Each question should ask 'why' — not 'what' When I give an answer, ask why THAT is true Continue asking why until we reach bedrock — an explanation that does not require another 'why' to be satisfying If my answer reveals a misconception, ask a question that exposes the contradiction in my own reasoning rather than telling me I am wrong After we r'（原文未完整提供，但核心是让AI一次只问一个'为什么'，直到你从基本原理解释清楚）。
- 3. 粘贴后AI会开始提问，你回答后AI继续追问，直到你无法再解释为止。

**适合谁/适用场景**: `学生`, `自学者`, `备考者`, `需要深入理解概念的知识工作者`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 提示词原文未完整给出，需自行补全；效果取决于 AI 模型对追问逻辑的遵循程度；部分 AI 可能无法严格一次只问一个问题。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1v1rygk/this_prompt_turns_any_fact_youve_memorised_into/)

reddit · r/PromptEngineering · /u/Neat_Translator1865 · 7月20日 17:25

**背景**: 苏格拉底式提问是一种通过追问来激发批判性思维、揭示假设的教学方法。第一性原理思维涉及将复杂问题分解为基本真理。这个提示词将两种方法结合起来，将表面知识转化为深层理解。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://zhuanlan.zhihu.com/p/655648168">ChatGPT提示词技术（5）：苏格拉底式提问逻辑 - 知乎</a></li>
<li><a href="https://openai-chatgpt.blog/socrates-style-prompt/">?深度思考:一个苏格拉底风格的Prompt提示词 - OpenAI-ChatGPT博客 收藏！5个超实用AI提示词模板，让Deepseek把知识嚼碎喂进你脑子！助你... Prompt一则：苏格拉底助手 | 时有所文 苏格拉底式提问（Socratic Questioning） - 思维模型详解 | 提升认知...</a></li>
<li><a href="https://zhuanlan.zhihu.com/p/1975514438833570596">第一性原理：理解世界的底层方法论（含反例大全） - 知乎</a></li>

</ul>
</details>

**标签**: `#学生`, `#自学者`, `#备考者`, `#需要深入理解概念的知识工作者`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1v1m9dr" markdown="1">
<a id="item-3"></a>
## [通过预提取清单避免多文档生成中的事实漂移](https://www.reddit.com/r/PromptEngineering/comments/1v1m9dr/how_i_structured_a_skill_to_avoid_drift_when/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一种通过强制提取事实清单来避免 LLM 在生成长对话中多个相关文档时出现事实不一致的提示工程技巧。

**具体怎么做**:
- 1. 让LLM重新阅读整个对话，并写一个“草稿清单”（scratch inventory），包含产品、技术栈、架构、约束、矛盾点、未解决问题等分类。
- 2. 基于这个清单生成所有文档（如PRD、技术栈、品牌指南、提示词），而不是直接基于原始对话。
- 3. 对于清单中的缺口，区分关键缺口和次要缺口，仅对关键缺口提问，且最多批量提出3个问题。

**适合谁/适用场景**: `需要从长对话中生成多个相关文档的提示工程师`, `使用LLM进行项目文档编写的开发者`, `希望提高多文档一致性的AI用户`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法依赖于 LLM 准确提取清单的能力，且未提供对比实验数据；实际效果可能因模型和对话长度而异。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1v1m9dr/how_i_structured_a_skill_to_avoid_drift_when/)

reddit · r/PromptEngineering · /u/Longjumping-Koala396 · 7月20日 13:55

**背景**: 事实漂移发生在 LLM 从长对话生成多个文档时缺乏单一事实来源，导致不一致。该技术引入显式提取步骤，创建所有后续文档引用的共享事实清单，类似于检索增强生成，但以对话本身作为知识库。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2404.10774">[2404.10774] MiniCheck: Efficient Fact-Checking of LLMs on ... MiniCheck: Efficient Fact-Checking of LLMs on Grounding ... Managing LLM Hallucinations in Long Document Processing 8.-9:;<9)=/ MiniCheck: Efcient Fact-Checking of LLMs on ... Verifying Facts in Patient Care Documents Generated by Large ... GitHub - Lancelot-Xie/DRIFT: Official implementation of ...</a></li>
<li><a href="https://idp-software.com/guides/prompt-engineering-document-extraction/">Prompt Engineering for Document Extraction - idp-software.com</a></li>

</ul>
</details>

**社区讨论**: Reddit 帖子获得积极反响，作者在 GitHub 上提供了完整技能和 10 阶段框架。评论者表示对多文档生成漂移的替代解决方案感兴趣。

**标签**: `#需要从长对话中生成多个相关文档的提示工程师`, `#使用LLM进行项目文档编写的开发者`, `#希望提高多文档一致性的AI用户`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1v14llq" markdown="1">
<a id="item-4"></a>
## [顺序澄清引擎：先诊断再开方](https://www.reddit.com/r/PromptEngineering/comments/1v14llq/stop_letting_chatgpt_shoot_from_the_hip_here_is_a/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个提示词框架，强制 AI 在给出建议前先进行多轮单问题发现、未知项审计和置信度检查，避免直接输出泛泛方案。

**具体怎么做**:
- 在系统提示中定义角色为世界级管理顾问，使用{{consulting_domain}}和{{advisory_tone}}两个变量。
- 设计一个顺序澄清循环：AI每次只问一个关键问题，用户回答后继续追问，直到覆盖所有未知项。
- 在循环结束后，AI进行置信度检查：列出已确认信息、仍存在的假设、建议的置信水平。
- 只有通过置信度检查后，AI才输出最终建议。

**适合谁/适用场景**: `需要深度分析的复杂领域（战略咨询、工程、文案）`, `希望获得定制化建议而非通用模板的用户`, `提示词工程师`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 框架效果取决于用户能否准确回答 AI 的澄清问题；需要多次迭代才能完善；原文未提供完整提示词模板。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1v14llq/stop_letting_chatgpt_shoot_from_the_hip_here_is_a/)

reddit · r/PromptEngineering · /u/blobxiaoyao · 7月19日 23:06

**背景**: LLM 常常在没有充分上下文的情况下生成通用回复，尤其在复杂领域。提示工程模式（如澄清模式和提示链）有助于结构化交互以提升输出质量。顺序澄清引擎通过强制一个严谨的发现过程，在这些理念基础上进行了构建。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://claudflow.com/guides/prompt-chaining-patterns.html">Prompt Chaining Patterns — Interactive Chain Builder & Code ...</a></li>
<li><a href="https://kasperjunge.github.io/posts/2023/prompting-patterns-the-clarification-pattern/">Prompting Patterns: The Clarification Pattern</a></li>
<li><a href="https://arxiv.org/abs/2302.11382">[2302.11382] A Prompt Pattern Catalog to Enhance Prompt ... Images Prompt Patterns | Generative AI | Vanderbilt University AI Agent Orchestration Patterns - Azure Architecture Center Workflow for prompt chaining - AWS Prescriptive Guidance Prompting best practices - Claude Platform Docs</a></li>

</ul>
</details>

**标签**: `#需要深度分析的复杂领域（战略咨询、工程、文案）`, `#希望获得定制化建议而非通用模板的用户`, `#提示词工程师`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1v1socu" markdown="1">
<a id="item-5"></a>
## [20 个可混搭的 ChatGPT 提示词模板（无需 GitHub）](https://www.reddit.com/r/PromptEngineering/comments/1v1socu/think_like_a_machine_heres_20_prompts_you_can_mix/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 提供 20 个无需 GitHub 访问权限的 ChatGPT 提示词模板，可混合搭配生成 101 种组合，用于审计、分析、修复等任务。

**具体怎么做**:
- 从提供的20个提示词模板中选择一个或多个，替换方括号中的占位符。
- 将替换后的提示词粘贴到ChatGPT对话中，并附上相关文件、日志或报告。
- 根据输出结果调整提示词，或组合多个模板以完成更复杂的任务。

**适合谁/适用场景**: `需要审计代码或文档的开发者`, `希望提升ChatGPT输出质量的提示工程师`, `需要分析日志或报告的数据分析师`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 提示词模板的有效性取决于输入材料的质量和占位符替换的准确性；部分模板可能需多次迭代才能获得满意结果。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1v1socu/think_like_a_machine_heres_20_prompts_you_can_mix/)

reddit · r/PromptEngineering · /u/epicskyes · 7月20日 17:51

**背景**: 提示工程是为生成式 AI 模型设计输入以产生期望输出的实践。这些模板体现了针对审计和分析等特定任务的结构化提示技术。

**标签**: `#需要审计代码或文档的开发者`, `#希望提升ChatGPT输出质量的提示工程师`, `#需要分析日志或报告的数据分析师`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1v1ob66" markdown="1">
<a id="item-6"></a>
## [单人企业主 500 小时提示工程三大模板](https://www.reddit.com/r/PromptEngineering/comments/1v1ob66/i_spent_500_hours_engineering_ai_prompts_for_my/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一位单人企业主分享了经过 500 小时测试的三个 AI 提示词模板，用于生成非机械化的客户获取、内容创作和销售文案。

**具体怎么做**:
- 1. 痛苦-激化-解决冷邮件提示：角色设为B2B文案专家，提供服务、目标受众和痛点，要求使用Pain-Agitate-Solve框架写一封不超过150字的冷邮件。
- 2. 入站线索资格认定提示：角色设为销售资格专家，提供服务定价和客户需求，要求生成资格认定问题。
- 3. 其他提示需参考原文中的完整模板，复制并填充方括号变量。

**适合谁/适用场景**: `单人企业主`, `自由职业者`, `小团队创业者`, `需要自动化客户获取和内容创作的人群`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 提示效果依赖于具体业务场景和变量填充质量；原文未提供 A/B 测试结果或转化率数据。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1v1ob66/i_spent_500_hours_engineering_ai_prompts_for_my/)

reddit · r/PromptEngineering · /u/Fluid_Onion_6056 · 7月20日 15:12

**背景**: 提示词工程是为 AI 模型编写精确指令以产生期望输出的实践。对于单人企业主，有效的提示词可以自动化内容创作、客户拓展和销售流程，起到杠杆作用。"痛点-煽动-解决"框架是一种经典的文案结构，先识别问题，放大其情感影响，然后提供解决方案。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://beomniscient.com/blog/pas-copywriting/">PAS Copywriting Framework: What Is It (+ 4 Examples)</a></li>
<li><a href="https://www.brutal-copy.com/blog/pas-framework-copywriting-guide">The PAS Framework: Write Copy That Sells Using Problem-Agitate-Solve</a></li>
<li><a href="https://www.thekiprojects.com/2025/09/why-solopreneurs-need-prompt.html?m=1">Why solopreneurs need prompt engineering and AI workflows</a></li>

</ul>
</details>

**标签**: `#单人企业主`, `#自由职业者`, `#小团队创业者`, `#需要自动化客户获取和内容创作的人群`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1v1fvrn" markdown="1">
<a id="item-7"></a>
## [一周实测揭示 ChatGPT、Claude、Gemini 各自优势](https://www.reddit.com/r/PromptEngineering/comments/1v1fvrn/i_ran_the_same_prompt_through_chatgpt_claude_and/)

**栏目分类**: `PRODUCTIVITY_TIP`

**一句话简介**: 通过一周对比测试，总结出三个主流 AI 模型在不同任务上的优势，并给出按任务选工具的分工建议。

**具体怎么做**:
- 1. 明确任务类型：快速对话、实时信息查询 → 用 ChatGPT；长文档、复杂多步指令、精细写作 → 用 Claude；需要整合 Google 账户数据（Gmail、Docs、搜索）→ 用 Gemini。
- 2. 为每个 AI 设置固定的“常驻指令”（standing instructions），避免每次重复输入相同背景和要求。
- 3. 不要用一个 AI 做所有事，根据任务特点匹配最合适的工具。

**适合谁/适用场景**: `需要频繁使用 AI 辅助工作的用户`, `希望提升 AI 输出质量的提示词工程师`, `同时使用多个 AI 工具但不知如何分工的普通人`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 结论基于个人一周测试，可能因使用场景不同而有差异；未提供量化对比数据，仅供参考。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1v1fvrn/i_ran_the_same_prompt_through_chatgpt_claude_and/)

reddit · r/PromptEngineering · /u/Professional-Rest138 · 7月20日 08:46

**背景**: ChatGPT、Claude 和 Gemini 分别是 OpenAI、Anthropic 和 Google 推出的三大主流大语言模型（LLM）。它们都经过海量文本数据训练，能执行多种语言任务，但底层架构和训练数据的不同导致各自优势各异。用户通常只选一个模型处理所有任务，但该测试表明，根据任务选择模型能获得更优结果。

**标签**: `#需要频繁使用 AI 辅助工作的用户`, `#希望提升 AI 输出质量的提示词工程师`, `#同时使用多个 AI 工具但不知如何分工的普通人`

</section>

---