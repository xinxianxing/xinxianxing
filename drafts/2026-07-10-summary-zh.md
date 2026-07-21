---
layout: default
title: "信先行 Action Cards: 2026-07-10 (ZH)"
date: 2026-07-10
lang: zh
---

> 从 51 条内容中筛选出 8 条教程/案例/技巧。

---

1. [用户用 Claude Fable 强化 526 个提示词库](#item-1) · TUTORIAL · Score: 7.0 / 10
2. [视频提示词不是文本提示词：多数失败的原因](#item-2) · TUTORIAL · Score: 7.0 / 10
3. [将 24 个重复 B2B 提示词转化为可复用的 Agent 技能](#item-3) · TUTORIAL · Score: 7.0 / 10
4. [ChatGPT 发现每年 2400 美元隐形支出](#item-4) · PRODUCTIVITY_TIP · Score: 7.0 / 10
5. [Vibe Coding 代码审查技巧：小功能集成避免大改动](#item-5) · PRODUCTIVITY_TIP · Score: 7.0 / 10
6. [无代码线索分配系统教程](#item-6) · TUTORIAL · Score: 6.0 / 10
7. [提示工具中实时数据优于硬编码模型列表](#item-7) · PRODUCTIVITY_TIP · Score: 6.0 / 10
8. [开源工具自动化顾问的 AI 文档审查](#item-8) · TOOL · Score: 6.0 / 10

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1us0vdm" markdown="1">
<a id="item-1"></a>
## [用户用 Claude Fable 强化 526 个提示词库](https://www.reddit.com/r/PromptEngineering/comments/1us0vdm/used_claude_fable_to_strengthen_my_prompt_library/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一位用户分享使用 Anthropic 最新模型 Claude Fable 批量重写和优化其提示词库的方法，涵盖营销和工程类别。

**具体怎么做**:
- 收集或整理现有的提示词库（如营销、架构、调试、安全等类别）。
- 将整个提示词库输入Claude Fable模型，要求其重写薄弱或不够具体的提示词。
- 对重写后的提示词进行人工审核，删除或编辑不符合要求的条目。
- 示例：使用“评分与优化”提示，让模型从清晰度、特异性、上下文完整性、输出就绪性四个维度给提示词打分（1-10），并给出每个分数的理由。
- 示例：使用“模糊→大师提示”提示，将模糊的指令转化为完整的、可复用的提示词，包含具体任务、模型需要的上下文、输出格式以及三个优秀输出示例。

**适合谁/适用场景**: `提示词工程师`, `AI应用开发者`, `需要批量优化提示词库的团队`, `对提示词质量有高要求的用户`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法依赖 Claude Fable 模型的能力，不同模型效果可能不同；人工审核仍需投入时间；提示词库的初始质量会影响最终效果。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1us0vdm/used_claude_fable_to_strengthen_my_prompt_library/)

reddit · r/PromptEngineering · /u/Emergency-Jelly-3543 · 7月9日 19:45

**背景**: 提示词工程涉及设计和构造输入给大语言模型（LLM）的指令以获得期望输出。Claude Fable 5 是 Anthropic 的最新模型，擅长长程推理和编码任务，适合用于重写和优化提示词。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.anthropic.com/claude/fable">Claude Fable \ Anthropic</a></li>
<li><a href="https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5">Introducing Claude Fable 5 and Claude Mythos 5</a></li>
<li><a href="https://www.ibm.com/think/topics/prompt-engineering-techniques">Prompt Engineering Techniques | IBM</a></li>

</ul>
</details>

**标签**: `#提示词工程师`, `#AI应用开发者`, `#需要批量优化提示词库的团队`, `#对提示词质量有高要求的用户`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1urua1g" markdown="1">
<a id="item-2"></a>
## [视频提示词不是文本提示词：多数失败的原因](https://www.reddit.com/r/PromptEngineering/comments/1urua1g/video_prompting_is_not_text_prompting_heres_why/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 本文解释了视频提示词与文本提示词的核心区别，并提供了编写有效视频提示词的关键技巧。

**具体怎么做**:
- 理解视频模型预测的是下一帧，而非下一个词，因此提示词必须描述运动而非静态内容。
- 使用时间副词（如“缓慢地”“快速地”“逐渐地”“突然地”）来控制运动速度，这些词对模型有实际影响。
- 描述物理运动细节，例如“猫跳到垫子上，爪子向前伸展，轻轻落地，尾巴甩动”，而不是仅说“猫在垫子上”。

**适合谁/适用场景**: `AI视频生成用户`, `提示词工程师`, `内容创作者`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 技巧基于作者个人经验，不同视频模型可能表现不同，需自行测试验证。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1urua1g/video_prompting_is_not_text_prompting_heres_why/)

reddit · r/PromptEngineering · /u/Brave-Round-3573 · 7月9日 15:53

**背景**: 像 GPT-4 这样的文本 AI 模型预测下一个 token，专注于语言连贯性。而视频模型预测下一帧，必须理解物理、运动和空间关系。这一根本区别意味着视频提示词需要描述运动、镜头角度和光照，而不仅仅是静态场景。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://grokipedia.com/page/Prompt_engineering_for_AI_video_generators">Prompt engineering for AI video generators — Grokipedia</a></li>
<li><a href="https://venice.ai/blog/the-complete-guide-to-ai-video-prompt-engineering">The Complete Guide to AI Video Prompt Engineering</a></li>
<li><a href="https://metricsmule.com/ai/ai-video-prompt-engineering/">AI Video Prompt Engineering | metricsmule</a></li>

</ul>
</details>

**社区讨论**: Reddit 社区普遍赞同该分析，许多用户分享了自己失败的尝试，并感谢作者的数据驱动方法。一些人对提示词元素的最佳顺序有争议，但共识是运动和镜头细节至关重要。

**标签**: `#AI视频生成用户`, `#提示词工程师`, `#内容创作者`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1urq980" markdown="1">
<a id="item-3"></a>
## [将 24 个重复 B2B 提示词转化为可复用的 Agent 技能](https://www.reddit.com/r/PromptEngineering/comments/1urq980/i_turned_24_recurring_b2b_prompts_into_reusable/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一位用户将自己在 B2B 线索研究和商业数据工作流中反复使用的 24 个提示词，转化为结构化的 Agent 技能，并开源了代码库。

**具体怎么做**:
- 识别工作中重复出现的提示词模式，例如：按理想客户画像评估公司、标准化不一致的职位头衔、研究公司时不编造缺失信息、识别差距后再下结论、保守审查可能的重复记录、使用明确标准细分公司和人员等。
- 将每个模式转化为独立的Agent技能，每个技能包含：聚焦的职责、定义的输入、决策规则、工作流步骤和预期输出。
- 将技能整理成集合，发布在GitHub上供他人复用。

**适合谁/适用场景**: `B2B销售和营销人员`, `提示词工程师`, `需要自动化线索研究和数据清洗的团队`, `希望将提示词系统化、模块化的AI用户`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法需要一定的提示词工程和编程基础，复用时需根据自身业务调整技能定义和规则。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1urq980/i_turned_24_recurring_b2b_prompts_into_reusable/)

reddit · r/PromptEngineering · /u/cryptoteams · 7月9日 13:25

**背景**: Agent Skills 是一种轻量级的开放格式，用于通过专业知识和工作流程扩展 AI 代理的能力。在 B2B 场景中，线索资格认定和职位名称规范化等任务通常需要重复的提示模式，这些模式可以标准化为可复用的模块。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://agentskills.io/">Agent Skills Overview - Agent Skills</a></li>

</ul>
</details>

**社区讨论**: 作者邀请反馈，询问这些是否算作真正可复用的领域技能，还是仍然过于接近结构化的提示模板，这表明关于提示词与技能边界的讨论是开放的。

**标签**: `#B2B销售和营销人员`, `#提示词工程师`, `#需要自动化线索研究和数据清洗的团队`, `#希望将提示词系统化、模块化的AI用户`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1urm0u9" markdown="1">
<a id="item-4"></a>
## [ChatGPT 发现每年 2400 美元隐形支出](https://www.reddit.com/r/PromptEngineering/comments/1urm0u9/i_gave_chatgpt_everything_i_earn_and_spend_and/)

**栏目分类**: `PRODUCTIVITY_TIP`

**一句话简介**: 将个人收支数据粘贴给 ChatGPT，让它找出被忽略的订阅、重复付费和涨价项目，快速发现可节省的开支。

**具体怎么做**:
- 导出或整理自己的所有收入和支出记录，包括订阅和定期扣费，以文本形式粘贴给 ChatGPT。
- 要求 ChatGPT 找出以下五类问题：1. 很少使用或忘记的订阅；2. 以不同形式重复付费的项目；3. 悄悄涨价的收费；4. 难以当面辩护的支出；5. 不影响生活质量的三项最大节省。
- 让 ChatGPT 汇总如果全部执行每年能节省多少。

**适合谁/适用场景**: `想优化个人财务的普通人`, `有多个订阅和自动扣费的用户`, `希望用 AI 提高理财效率的人`

**效果或数据**: 原文称发现每年 2400 美元的隐形支出，但未提供具体数据来源或验证。

**可信度/风险提示**: 结果取决于输入数据的完整性和准确性；ChatGPT 可能遗漏或误判；实际节省需自行核实。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1urm0u9/i_gave_chatgpt_everything_i_earn_and_spend_and/)

reddit · r/PromptEngineering · /u/Professional-Rest138 · 7月9日 10:11

**背景**: 许多人拥有多个订阅和自动付款，容易忘记，导致“订阅蠕变”。AI 语言模型可以分析基于文本的交易历史，检测模式和异常，使财务审计更快、更直观。

**标签**: `#想优化个人财务的普通人`, `#有多个订阅和自动扣费的用户`, `#希望用 AI 提高理财效率的人`

</section>

---

<section class="action-card" data-card-id="twitter:tweet:2075261703411904826" markdown="1">
<a id="item-5"></a>
## [Vibe Coding 代码审查技巧：小功能集成避免大改动](https://twitter.com/dotey/status/tweet-2075261703411904826)

**栏目分类**: `PRODUCTIVITY_TIP`

**一句话简介**: 针对 AI 生成代码量过大难以审查的问题，借鉴敏捷开发中的持续集成思想，建议每次只让 AI 完成一个小功能点或修复一个小 bug，从而便于验收和审查。

**具体怎么做**:
- 将需求拆解为多个小功能点或小 bug 修复，每次只让 AI 完成一个小的变更。
- 每次变更后立即验证功能是否正确，并审查代码。
- 配合自动化测试，确保每次变更后系统整体稳定。
- 避免一次性让 AI 生成大量代码，否则难以审查且质量不可控。

**适合谁/适用场景**: `使用 AI 编程的开发者`, `需要审查 AI 生成代码的团队`, `希望提高代码质量和可维护性的程序员`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法基于传统软件工程中的持续集成实践，但需要开发者具备拆解任务和编写自动化测试的能力；对于复杂项目，小功能点的粒度需要根据实际情况调整。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://twitter.com/dotey/status/tweet-2075261703411904826)

twitter · 宝玉 · 7月9日 16:52

**背景**: Vibe Coding 是一种 AI 辅助编程实践，开发者向大语言模型描述任务并接受生成的代码，几乎不做审查。该术语由 Andrej Karpathy 于 2025 年提出。传统软件工程也面临过类似的大规模代码变更问题，因此敏捷开发中采用了持续集成（CI），主张小规模、频繁的集成。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Vibe_coding">Vibe coding</a></li>
<li><a href="https://docs.pingcode.com/ask/ask-ask/612021.html">敏 捷 性 开 发 平台是什么 – PingCode</a></li>

</ul>
</details>

**标签**: `#使用 AI 编程的开发者`, `#需要审查 AI 生成代码的团队`, `#希望提高代码质量和可维护性的程序员`

</section>

---

<section class="action-card" data-card-id="rss:feed.indiehackers.world_posts.rss?exclude=link-post:5806cb050daeb7f8" markdown="1">
<a id="item-6"></a>
## [无代码线索分配系统教程](https://feed.indiehackers.world/post/8cde06d030)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个基于路由规则自动生成个性化邮件草稿的无代码线索分配系统教程。

**具体怎么做**:
- 1. 定义线索路由规则：根据线索来源、需求或问题类型，设置不同的路由（如自助指南、创始人回复）。
- 2. 使用自动化工具（如Zapier或Make）连接表单、CRM和邮件系统，当新线索进入时触发流程。
- 3. 在自动化流程中，根据路由规则选择对应的邮件模板，并填入线索详情（姓名、用例、问题等）。
- 4. 邮件模板需遵循以下要求：使用简单语言、不超过100词、不承诺功能、不提供折扣、不编造产品细节、不提及AI。
- 5. 根据路由类型调整邮件内容：若为自助指南，感谢并发送指南链接，邀请用户遇到困难时回复；若为创始人回复，提及用户需求，询问当前使用工具，仅当面向企业时添加日历链接。

**适合谁/适用场景**: `创业者`, `小团队`, `营销人员`, `需要自动化线索跟进的人`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 系统效果取决于线索路由规则的准确性和邮件模板的适用性；自动化工具可能需要付费订阅。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://feed.indiehackers.world/post/8cde06d030)

rss · Indie Hackers · 7月9日 15:52

**背景**: 无代码线索分配系统允许企业根据预定义规则自动将线索分配给合适的团队成员，无需编写代码。本教程聚焦于邮件草拟步骤，利用路由规则定制消息内容。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.zoho.com.cn/crm/lead-management.html">销售线索管理系统 - 潜在客户管理软件 - Zoho CRM</a></li>
<li><a href="https://www.zdsztech.com/blog/what-is-no-code-clue-assignment-enterprise-efficiency-booster/">无代码线索分配是什么？企业效率提升神器！ - 支道博客</a></li>

</ul>
</details>

**标签**: `#创业者`, `#小团队`, `#营销人员`, `#需要自动化线索跟进的人`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1usgps6" markdown="1">
<a id="item-7"></a>
## [提示工具中实时数据优于硬编码模型列表](https://www.reddit.com/r/PromptEngineering/comments/1usgps6/model_choice_is_a_port_you_dont_own_heres_how/)

**栏目分类**: `PRODUCTIVITY_TIP`

**一句话简介**: 本文讨论了模型选择下拉菜单的维护陷阱，并提出了使用实时数据而非硬编码模型列表的可持续提示工程原则。

**具体怎么做**:
- 检查你的提示工具或应用中任何包含模型下拉菜单的界面。
- 选择一个已保存的模型选择，验证该模型是否仍在当前可用列表中。
- 如果模型不在列表中，确保系统能优雅地回退到推荐默认模型，而不是调用已废弃的模型ID。
- 避免在构建时硬编码模型列表，改用实时数据动态获取可用模型。

**适合谁/适用场景**: `提示工程师`, `AI应用开发者`, `需要维护模型选择功能的团队`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 文中提到的硬编码模型列表导致废弃的问题真实存在，但具体实施效果取决于应用架构和模型提供商的变化频率。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1usgps6/model_choice_is_a_port_you_dont_own_heres_how/)

reddit · r/PromptEngineering · /u/Parking-Kangaroo-63 · 7月10日 07:34

**背景**: 提示工程工具通常包含一个下拉菜单供用户选择要使用的 AI 模型。来自 OpenAI 和 Azure AI 等提供商的模型目录并非静态；模型会随时间被弃用、重命名或重新分层。在工具构建中硬编码这些列表意味着每次发布都可能提供过时或损坏的模型引用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.palantir.com/docs/foundry/model-catalog/model-deprecation">AIP Model Catalog • Model deprecation • Palantir</a></li>
<li><a href="https://learn.microsoft.com/en-gb/answers/questions/2145673/conflicting-retirement-date-for-models">Conflicting retirement date for models - Microsoft Q&A</a></li>
<li><a href="https://ofox.io/blog/openai-api-model-not-found-errors-troubleshooting/">OpenAI 404 Model Does Not Exist: All 5 Causes Fixed (2026)</a></li>

</ul>
</details>

**标签**: `#提示工程师`, `#AI应用开发者`, `#需要维护模型选择功能的团队`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1us89yh" markdown="1">
<a id="item-8"></a>
## [开源工具自动化顾问的 AI 文档审查](https://www.reddit.com/r/PromptEngineering/comments/1us89yh/cowork_skill_for_consultants_to_review_ai/)

**栏目分类**: `TOOL`

**一句话简介**: 一个开源工具，通过多维度颜色团队审查自动检查 AI 生成的提案、SOW、方案文档等，输出合规性、可行性、价格合理性等评估结果。

**具体怎么做**:
- 1. 访问GitLab仓库（http://gitlab.com/timo2026/doc-review）获取开源技能。
- 2. 将待审查的AI生成文档输入工具。
- 3. 工具运行Shipley风格的颜色团队审查，输出粉色（结构/合规）、红色（技术可行性/清晰度）、绿色（范围/价格合理性）、金色（执行决策）以及新鲜度/来源验证结果。
- 4. 根据审查发现和门控裁决进行人工复核和修改。

**适合谁/适用场景**: `咨询顾问`, `项目经理`, `需要审查AI生成技术文档的团队`, `提案和方案评审场景`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 工具为开源项目，需自行部署和测试；审查效果取决于文档质量和配置；可能无法覆盖所有行业特定要求。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1us89yh/cowork_skill_for_consultants_to_review_ai/)

reddit · r/PromptEngineering · /u/coolreddy · 7月10日 00:31

**背景**: 颜色团队审查是提案开发中的标准做法，尤其适用于政府合同，团队通过模拟不同视角（如评估者、高管）来发现问题。Shipley 方法通过特定的颜色编码门控将其形式化。然而，这些审查通常耗时，且常被视为走过场的里程碑而非质量检查点。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.hsvagi.com/ai-guides/color-team-reviews-ai-proposal-red-team-gold-team">Color Team Reviews : How AI Accelerates Red Team, Gold... | HSVAGI</a></li>
<li><a href="https://amerifusiongovcon.com/color-team-reviews-federal-proposals/">Color Team Reviews for Federal Proposals... | AmerifusionGovCon</a></li>
<li><a href="https://www.linkedin.com/pulse/color-team-reviews-broken-how-fix-them-tara-brown-xsdzc">Color Team Reviews Are Broken (And How to Fix Them)</a></li>

</ul>
</details>

**社区讨论**: 该 Reddit 帖子暂无评论，因此无社区讨论。

**标签**: `#咨询顾问`, `#项目经理`, `#需要审查AI生成技术文档的团队`, `#提案和方案评审场景`

</section>

---