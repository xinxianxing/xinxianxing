---
layout: default
title: "信先行 Action Cards: 2026-07-23 (ZH)"
date: 2026-07-23
lang: zh
---

> 从 24 条内容中筛选出 4 条教程/案例/技巧。

---

1. [基于 LangChain 评估的确定性提示词优化循环](#item-1) · TUTORIAL · Score: 8.0 / 10
2. [用提示词检查 PPT 标题是否经得起扫读测试](#item-2) · TUTORIAL · Score: 8.0 / 10
3. [将混乱转录稿转化为结构化演示文稿大纲的提示词](#item-3) · TUTORIAL · Score: 7.0 / 10
4. [AI 根据合作机会类型自动生成外联邮件](#item-4) · PRODUCTIVITY_TIP · Score: 6.0 / 10

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1v3s2f7" markdown="1">
<a id="item-1"></a>
## [基于 LangChain 评估的确定性提示词优化循环](https://www.reddit.com/r/PromptEngineering/comments/1v3s2f7/stop_guessing_how_to_build_a_deterministic_prompt/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 介绍一种基于 LangChain 评估的确定性提示词优化方法，通过冻结测试集、定义评分规则和自动迭代重写来提升提示词性能。

**具体怎么做**:
- 冻结测试集：准备25个固定场景（如退款政策）。
- 定义评分规则：设置权重，例如基于事实性（50%）、语气（30%）、格式（20%）。
- 使用Claude Code作为技能：读取评分，重写一个元素，重新评分，仅当分数提高时保留重写。
- 重复迭代直到达到目标分数。

**适合谁/适用场景**: `提示词工程师`, `AI应用开发者`, `需要优化提示词效果的团队`

**效果或数据**: 在一次测试中，将基线 80%的提示词在 10 分钟内提升至 98%。

**可信度/风险提示**: 该方法依赖于 LangChain 评估工具和 Claude Code，可能需要一定的技术背景；测试场景有限（25 个），实际效果可能因场景而异。

**实用度评分**: Score: 8.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1v3s2f7/stop_guessing_how_to_build_a_deterministic_prompt/)

reddit · r/PromptEngineering · /u/TrustyJalapeno · 7月22日 20:26

**背景**: 提示词工程通常依赖试错。LangChain 评估通过 LLM-as-Judge 评估器提供量化提示词性能的方法。确定性优化循环通过定义指标、构建防护机制并让代理迭代来自动化该过程。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://docs.langchain.com/oss/python/langchain/test/evals">Agent Evals - Docs by LangChain</a></li>
<li><a href="https://docs.langchain.com/langsmith/evaluation-quickstart">Evaluation quickstart - Docs by LangChain</a></li>
<li><a href="https://www.damiangalarza.com/posts/2026-04-06-autonomous-optimization-loops-with-autoresearch/">Autonomous Prompt Optimization : 28% Smaller</a></li>

</ul>
</details>

**标签**: `#提示词工程师`, `#AI应用开发者`, `#需要优化提示词效果的团队`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1v3o6c9" markdown="1">
<a id="item-2"></a>
## [用提示词检查 PPT 标题是否经得起扫读测试](https://www.reddit.com/r/PromptEngineering/comments/1v3o6c9/before_you_open_any_ai_presentation_tool_run_this/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个提示词技巧，在制作 AI 演示文稿前先用标题列表测试，确保仅靠标题就能传达完整故事。

**具体怎么做**:
- 1. 将幻灯片标题按顺序粘贴到提示词中（只贴标题，不要正文）。
- 2. 让AI执行扫读测试：仅按顺序阅读这些标题，写出它们单独讲述的段落故事。
- 3. 如果故事有缺口或不连贯，AI会指出具体位置。
- 4. 列出所有只是主题标签（如“市场概览”）而非结论（如“我们正处于即将翻三倍的市场早期”）的标题，并重写为结论。
- 5. 检查是否有单个标题承担了双重任务，应拆分为两个标题。

**适合谁/适用场景**: `PPT制作者`, `演示文稿设计者`, `需要快速传达信息的职场人士`, `使用AI辅助制作幻灯片的人`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 提示词效果取决于 AI 模型的理解能力，可能需要多次迭代；标题列表需完整且有序。

**实用度评分**: Score: 8.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1v3o6c9/before_you_open_any_ai_presentation_tool_run_this/)

reddit · r/PromptEngineering · /u/Original-Ambition643 · 7月22日 18:11

**背景**: 在演示中，许多观众只会扫读幻灯片标题，因此标题必须能独立传达核心信息。然而，常见的标题如“Q3 结果”或“我们的方法”仅仅是标签，没有提供任何见解。“扫读测试”通过隔离标题来模拟扫读者的体验，而使用没有上下文的 AI 有助于揭示作者自身知识可能会填补的信息缺口。

**社区讨论**: Reddit 帖子获得了积极反响，用户分享了其他标题测试方法，并称赞该提示词的实用性。一些评论者指出，这项技术对于团队协作制作演示文稿特别有用，因为它能在视觉设计开始前强制明确信息。

**标签**: `#PPT制作者`, `#演示文稿设计者`, `#需要快速传达信息的职场人士`, `#使用AI辅助制作幻灯片的人`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1v3p1a1" markdown="1">
<a id="item-3"></a>
## [将混乱转录稿转化为结构化演示文稿大纲的提示词](https://www.reddit.com/r/PromptEngineering/comments/1v3p1a1/copypaste_this_prompt_to_turn_a_messy_call/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个提示词，用于将会议或网络研讨会转录稿重新组织成结构化的总结演示文稿大纲，而非按对话顺序罗列。

**具体怎么做**:
- 将转录稿粘贴到AI工具中。
- 使用提供的提示词，要求AI重建内容：识别决策、未解决的问题和行动项，忽略闲聊和重复。
- 将剩余内容按4-6个主题分组，这些主题对错过会议的人有意义。
- 按先结果后推理的顺序排列主题。
- 对每个主题输出：幻灯片标题（完整句子形式的要点）和2-3个支持该要点的要点。
- 如果转录稿中决策或负责人不明确，则注明。

**适合谁/适用场景**: `需要快速整理会议纪要的职场人士`, `需要将转录稿转化为演示文稿的团队`, `希望提升AI输出质量的提示词工程师`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 提示词效果取决于转录稿质量和 AI 模型能力；可能需要调整以适应不同场景。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1v3p1a1/copypaste_this_prompt_to_turn_a_messy_call/)

reddit · r/PromptEngineering · /u/South_Video2255 · 7月22日 18:41

**背景**: 许多职场人士使用 AI 总结会议转录稿，但简单的提示词通常按发言顺序为每个主题生成一张幻灯片，包含填充内容。该提示词通过告诉模型将内容重新构建成逻辑清晰、以决策为重点的大纲，从而重新设计了任务，这对错过会议的人更有用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://promptitin.com/prompts/board-meeting-deck-outline">Board Meeting Deck Outline — Free AI Prompt Template</a></li>
<li><a href="https://www.popai.pro/ai-presentation/academy/how-to-generate-a-pitch-deck-with-ai-outline-slide-prompts.html">How to Generate a Pitch Deck with AI ( Outline Slide Prompts )</a></li>

</ul>
</details>

**社区讨论**: 原帖作者询问如何提取谁承诺了什么，并指出他们仍需手动清理这部分。来源中没有提供其他评论。

**标签**: `#需要快速整理会议纪要的职场人士`, `#需要将转录稿转化为演示文稿的团队`, `#希望提升AI输出质量的提示词工程师`

</section>

---

<section class="action-card" data-card-id="rss:feed.indiehackers.world_posts.rss?exclude=link-post:33902c51305d51d8" markdown="1">
<a id="item-4"></a>
## [AI 根据合作机会类型自动生成外联邮件](https://feed.indiehackers.world/post/d471304c36)

**栏目分类**: `PRODUCTIVITY_TIP`

**一句话简介**: 本文介绍如何根据合作机会的来源类型（如热介绍、主动请求、需要信息、拒绝），使用 AI 自动生成不同风格的邮件草稿，节省手动撰写时间。

**具体怎么做**:
- 1. 将合作机会分类为：热介绍、主动请求、需要信息、拒绝。
- 2. 对于热介绍：起草一封简洁的跟进邮件，提及介绍人，说明可能的合作，并建议一个简单的下一步。
- 3. 对于主动请求：感谢对方，回复提案，并在需要通话时附上日历预约链接。
- 4. 对于需要信息：如果是主动请求，仅询问缺失的具体信息；如果是自己发现或经介绍，起草一封简短邮件开始对话，只询问评估所需的信息，不要对对方受众或结果做无根据的声称。
- 5. 对于拒绝：如果是主动请求，起草礼貌回复说明目前不合适。

**适合谁/适用场景**: `创业者`, `商务拓展人员`, `需要处理大量合作机会的团队`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法依赖对机会来源的准确分类，且邮件模板需要根据具体业务调整；AI 生成内容需人工审核以避免不准确或不当表述。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://feed.indiehackers.world/post/d471304c36)

rss · Indie Hackers · 7月22日 13:21

**背景**: 商务拓展团队经常处理大量合作机会，每个机会都需要定制化的邮件回复。手动撰写这些邮件既耗时又不一致。通过按来源类型（热介绍、主动请求、需要信息、拒绝）对机会进行分类，AI 可以生成合适的草稿，确保及时且符合上下文的沟通。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.upcell.io/glossary/warm-introductions/">Warm Introductions — B2B Sales & Prospecting Guide - upcell</a></li>
<li><a href="https://orm-tech.com/glossary/opportunity-source/">Opportunity Source | Revenue Analytics Glossary | ORM</a></li>
<li><a href="https://www.salesforce.com/blog/small-business/prospect-vs-lead/">Prospect vs Lead vs. Sales Opportunity: The Differences</a></li>

</ul>
</details>

**标签**: `#创业者`, `#商务拓展人员`, `#需要处理大量合作机会的团队`

</section>

---