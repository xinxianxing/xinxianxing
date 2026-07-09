# 信先行实用卡片 - 2026-07-09

> 从 43 条内容中筛选出 7 条教程/案例/技巧。

---

1. [提示词教你如何将来源融入议论文](#item-1) · TUTORIAL · Score: 7.0 / 10
2. [将 8 个月的 AI 聊天记录挖掘成提示词画像](#item-2) · TUTORIAL · Score: 7.0 / 10
3. [针对 AI 概览的 5 阶段 SEO 博客提示词管道](#item-3) · TUTORIAL · Score: 7.0 / 10
4. [用指令防止 AI 乱改代码](#item-4) · PRODUCTIVITY_TIP · Score: 7.0 / 10
5. [编写 AI Agent 技能的 5 条原则](#item-5) · TUTORIAL · Score: 7.0 / 10
6. [提示词实验室：告诉 AI 如何思考，而非写什么](#item-6) · TUTORIAL · Score: 6.0 / 10
7. [两阶段学术审稿系统：先诊断后改写](#item-7) · TUTORIAL · Score: 6.0 / 10

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1ur5fpv" markdown="1">
<a id="item-1"></a>
## [提示词教你如何将来源融入议论文](https://www.reddit.com/r/PromptEngineering/comments/1ur5fpv/this_prompt_takes_your_sources_and_shows_you/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 这是一个提示词模板，教你如何将引用来源自然地融入议论文段落中，而不是生硬地堆砌。

**具体怎么做**:
- 将以下提示词粘贴到ChatGPT、Claude等AI中：
- 在提示词中填入你的学科、来源列表（含关键主张）和主题句。
- AI会展示三种整合模式：a) 改写+归属；b) 短引+分析；c) 信号短语+综合。
- AI还会提供分析句模板，如“这表明/说明……”。

**适合谁/适用场景**: `学生写议论文`, `学术写作新手`, `需要提升论证质量的人`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 提示词效果取决于 AI 模型和输入质量；不同 AI 可能输出有差异。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1ur5fpv/this_prompt_takes_your_sources_and_shows_you/)

reddit · r/PromptEngineering · /u/Neat_Translator1865 · 7月8日 20:58

**背景**: 在学术写作中，有效的论证需要将来源融入自己的推理中，而不是将其作为孤立的证据堆砌。许多学生难以掌握这一技能，常常写出像引用列表一样的段落。提示词工程涉及为 AI 模型编写指令以产生所需输出，该提示词旨在充当来源整合的导师。

**标签**: `#学生写议论文`, `#学术写作新手`, `#需要提升论证质量的人`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uqu6wz" markdown="1">
<a id="item-2"></a>
## [将 8 个月的 AI 聊天记录挖掘成提示词画像](https://www.reddit.com/r/PromptEngineering/comments/1uqu6wz/i_mined_8_months_of_my_ai_chats_into_a_prompt/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 通过分析自己与 AI 的聊天记录，提取个人对话模式，生成一个提示词画像，让 AI 更了解你的偏好和习惯。

**具体怎么做**:
- 从Claude或Codex等工具的磁盘日志中提取自己写的消息（排除工具输出和错误信息），得到约1656个会话、近300万token的原始文本。
- 将文本分块，让20个不同的AI代理分别读取不同片段，每个代理分析你的决策方式、卡点、语言习惯、常要求修复的内容等模式。
- 汇总所有代理的分析结果，找出重叠的模式（例如多个代理都指出你经常拒绝某类建议）。
- 将重叠的模式整理成一个简短的提示词画像，在每次与AI对话前让AI读取该画像。

**适合谁/适用场景**: `重度AI用户`, `提示词工程师`, `希望提升AI对话效率的人`, `想了解自己使用AI习惯的人`

**效果或数据**: 未提供具体数据，但作者提到 15 个不同代理阅读不同月份的数据后得出了高度一致的结论。

**可信度/风险提示**: 该方法需要用户有大量聊天记录（约 300 万 token），且需要一定的技术能力从磁盘提取日志；分析结果可能受代理理解偏差影响。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uqu6wz/i_mined_8_months_of_my_ai_chats_into_a_prompt/)

reddit · r/PromptEngineering · /u/BiosRios · 7月8日 14:24

**背景**: Claude 和 Codex 是 AI 编程助手，会在本地磁盘存储会话日志。提示词画像是一组指令，用于告知 AI 模型用户的偏好和沟通风格，帮助 AI 定制回复。挖掘聊天记录来创建此类画像是一种利用个人数据实现 AI 个性化的新颖方法。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://mcpmarket.com/tools/skills/session-log-analytics">Session Logs: Claude Code Skill for AI Conversation History</a></li>
<li><a href="https://github.com/wondercoms/codex-logs">GitHub - wondercoms/codex-logs · GitHub</a></li>

</ul>
</details>

**标签**: `#重度AI用户`, `#提示词工程师`, `#希望提升AI对话效率的人`, `#想了解自己使用AI习惯的人`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uqpmcn" markdown="1">
<a id="item-3"></a>
## [针对 AI 概览的 5 阶段 SEO 博客提示词管道](https://www.reddit.com/r/PromptEngineering/comments/1uqpmcn/just_built_a_5stage_seo_blog_writing_prompt/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个由 5 个阶段组成的提示词管道，用于生成同时针对传统搜索引擎和 AI 概览（如 Google AI Overviews、ChatGPT、Perplexity 等）进行优化的 SEO 博客文章。

**具体怎么做**:
- 阶段1：研究与搜索意图分析——分析关键词的搜索意图、实体、People Also Ask问题、AI概览机会等。
- 阶段2：SEO大纲——基于研究结果生成结构化大纲，包含标题、子标题、实体和内部链接建议。
- 阶段3：撰写完整文章——根据大纲生成全文，确保内容覆盖所有关键实体和问题。
- 阶段4：专业审计——对文章进行SEO、GEO、AEO、EEAT等方面的审计，检查可读性、内部链接和内容质量。
- 阶段5：优化与最终QA——根据审计结果进行优化，并执行最终质量检查，确保文章符合所有要求。

**适合谁/适用场景**: `内容营销人员`, `SEO专家`, `博客作者`, `希望内容在AI搜索中排名的人`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该管道基于个人经验构建，效果可能因行业、关键词和 AI 模型版本而异。需要自行测试和调整。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uqpmcn/just_built_a_5stage_seo_blog_writing_prompt/)

reddit · r/PromptEngineering · /u/Comfortable_War2683 · 7月8日 11:13

**背景**: SEO（搜索引擎优化）传统上专注于在 Google 搜索结果中排名。然而，随着 AI 驱动的搜索工具（如 Google AI Overviews、ChatGPT 和 Perplexity）的兴起，出现了新的优化范式：AEO（答案引擎优化）用于直接答案，GEO（生成引擎优化）用于被生成式 AI 引用的内容。EEAT（经验、专业、权威、信任）和语义/实体 SEO 等概念帮助搜索引擎理解内容的上下文和关系。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.smoothfusion.com/blog/post/the-new-language-of-search-seo-aeo-geo-in-2026">The New Language of Search: SEO, AEO, GEO, SEO 2.O and Beyond in 2026</a></li>
<li><a href="https://www.searchenginepeople.com/blog/geo-vs-aeo-vs-seo-whats-the-difference-and-how-to-optimize-for-all-three.html">GEO vs AEO vs SEO: What’s the Difference and How to Optimize for All Three</a></li>
<li><a href="https://moz.com/blog/ai-overviews-optimization-whiteboard-friday">Optimizing for AI Overviews — Whiteboard Friday - Moz</a></li>

</ul>
</details>

**标签**: `#内容营销人员`, `#SEO专家`, `#博客作者`, `#希望内容在AI搜索中排名的人`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uqp6s8" markdown="1">
<a id="item-4"></a>
## [用指令防止 AI 乱改代码](https://www.reddit.com/r/PromptEngineering/comments/1uqp6s8/the_most_annoying_thing_about_building_with_ai_is/)

**栏目分类**: `PRODUCTIVITY_TIP`

**一句话简介**: 在 AI 编程会话开始时设置几条固定指令，让 AI 只修改你明确要求的部分，避免它擅自改动其他功能。

**具体怎么做**:
- 在会话开始时，设置以下三条指令并命名：
- 1. Frozen：所有现有功能视为固定，只修改明确要求的代码，其他部分保持不变。
- 2. Minimal：做出满足请求的最小改动，保持其他部分不变；如果无法做到，先暂停并解释原因。
- 3. Changes-only：只显示与上一版本不同的部分，而不是整个文件。
- 在后续请求中，通过名称引用这些指令，例如“使用Frozen模式修改函数X”。

**适合谁/适用场景**: `使用AI辅助编程的开发者`, `需要维护大型代码库的团队`, `希望减少AI引入意外bug的人`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 指令效果可能因 AI 模型和上下文长度而异，需要多次测试调整；对于复杂重构任务，严格限制可能降低 AI 的灵活性。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uqp6s8/the_most_annoying_thing_about_building_with_ai_is/)

reddit · r/PromptEngineering · /u/Professional-Rest138 · 7月8日 10:51

**背景**: 像 GPT-4 这样的 AI 编程助手常常会生成超出用户请求范围的代码修改，导致回归问题。开发者可以通过在会话开始时提供明确约束来缓解这一问题，正如该用户的方法所示。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.freecodecamp.org/chinese/news/how-to-become-an-expert-in-ai-assisted-coding-a-handbook-for-developers/">如何成为 AI 辅助编程专家 - 开发者手册</a></li>
<li><a href="https://deepseek.csdn.net/686380a3080e555a88cbc7fb.html">一份让AI能更好的基于现有代码进行修改的准则_人工智能_春秋一剑-DeepSeek技术社区</a></li>

</ul>
</details>

**标签**: `#使用AI辅助编程的开发者`, `#需要维护大型代码库的团队`, `#希望减少AI引入意外bug的人`

</section>

---

<section class="action-card" data-card-id="twitter:tweet:2074732405743624650" markdown="1">
<a id="item-5"></a>
## [编写 AI Agent 技能的 5 条原则](https://twitter.com/dotey/status/tweet-2074732405743624650)

**栏目分类**: `TUTORIAL`

**一句话简介**: 基于 SkillsBench 测试结果，总结编写 AI Agent Skill 的 5 条关键原则，帮助用户避免常见错误，提升技能效果。

**具体怎么做**:
- 1. 不要完全依赖 AI 自生成 Skill：人指挥 AI 写 Skill 效果更好，人类专家策划的 Skill 显著提升通过率，而模型自生成的 Skill 平均比无 Skill 基线低 1.3 个点。
- 2. 聚焦核心，小而精：只包含 2-3 个文件，范围明确，避免大而全的百科全书式技能。
- 3. 控制技能数量：加载过多 Skill 会占用上下文，反而降低智能体表现。
- 4. 针对不同平台测试：Skill 虽通用，但不同 Agent 或模型（如 Codex、Claude、GLM）能力有差异，需针对性测试并写兼容说明。
- 5. 瞄准模型薄弱领域：优先在模型表现差的领域（如医疗保健、制造业）编写 Skill，提升效果更显著。

**适合谁/适用场景**: `AI Agent 开发者`, `提示词工程师`, `希望优化 AI 工具效率的普通用户`, `需要编写或改进 AI Skill 的团队`

**效果或数据**: SkillsBench 测试显示：专家策划的 Skill 显著提升通过率；模型自生成的 Skill 平均比无 Skill 基线低 1.3 个点；在医疗保健领域提升 51.9 分，制造业紧随其后，软件工程仅提升 4.5 分。

**可信度/风险提示**: 部分结论基于特定测试（SkillsBench），不同场景和模型可能结果不同；原文作者指出文章存在不严谨之处，如 AI 写 Skill 并非完全不可行，需结合人工引导。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://twitter.com/dotey/status/tweet-2074732405743624650)

twitter · 宝玉 · 7月8日 05:48

**背景**: AI Agent 技能是模块化的指令或工具，用于增强 AI 代理执行特定任务的能力。SkillsBench 是一个基准测试，用于评估此类技能在不同领域的有效性。文章批评了依赖 AI 自己生成技能的常见做法，认为人类引导能带来更好的结果。

**社区讨论**: 作者承认第一条原则不够严谨，指出如果提供适当的上下文，AI 可以编写技能，最佳方法是人类引导 AI 编写技能。社区普遍同意其他原则，尤其是小而精的技能的价值以及测试的必要性。

**标签**: `#AI Agent 开发者`, `#提示词工程师`, `#希望优化 AI 工具效率的普通用户`, `#需要编写或改进 AI Skill 的团队`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1urf1iw" markdown="1">
<a id="item-6"></a>
## [提示词实验室：告诉 AI 如何思考，而非写什么](https://www.reddit.com/r/PromptEngineering/comments/1urf1iw/prompt_lab_001/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 通过对比 10 种提示词写法，发现让 ChatGPT 先思考再写作能显著提升输出质量。

**具体怎么做**:
- 1. 不要直接告诉AI写什么内容（如“写一篇关于学习AI的领英帖子”），而是告诉它如何思考（如“先找出读者最大的误解，然后围绕纠正误解来写”）。
- 2. 在提示词中加入“思考步骤”指令，例如：“在写作之前，先分析目标读者的常见误区，再基于此构建帖子结构。”
- 3. 避免使用模糊的修饰词（如“吸引人的”“有经验的”），而是给出具体的思考框架。

**适合谁/适用场景**: `内容创作者`, `营销人员`, `使用ChatGPT生成文本的普通用户`

**效果或数据**: 未提供具体数据，但作者声称“一个微小的改变产生了显著更强的结果”。

**可信度/风险提示**: 实验基于单一任务（领英帖子），结果可能因任务类型而异；未提供量化指标，主观性较强。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1urf1iw/prompt_lab_001/)

reddit · r/PromptEngineering · /u/Matthuesviewfinder · 7月9日 03:48

**背景**: 许多用户直接让 AI 生成内容，结果往往很泛泛。通过增加自我评估步骤，模型可以识别并修正自身弱点，从而产生更连贯、更吸引人的文本。

**标签**: `#内容创作者`, `#营销人员`, `#使用ChatGPT生成文本的普通用户`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1ur6d8f" markdown="1">
<a id="item-7"></a>
## [两阶段学术审稿系统：先诊断后改写](https://www.reddit.com/r/PromptEngineering/comments/1ur6d8f/i_built_a_twostage_academic_review_system_for/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个用于学术论文的两阶段审稿提示词工作流，先进行诊断分析，再按规则进行最小化改写。

**具体怎么做**:
- 阶段一：分析。使用提示词对文本进行诊断性审查，检查清晰度与逻辑推进、衔接与过渡、结构一致性、术语使用、潜在矛盾、学术语气，不修改原文。
- 阶段二：修订。在分析完成后，按以下规则进行改写：最小化措辞改动、保留作者风格、学术去人称化、优化连接词、标准化术语。

**适合谁/适用场景**: `学术写作者`, `研究生`, `论文编辑`, `需要保留个人风格的学术文本审校`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 提示词的具体内容未公开，复现需自行构建；效果取决于提示词设计质量。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1ur6d8f/i_built_a_twostage_academic_review_system_for/)

reddit · r/PromptEngineering · /u/Dai2santos · 7月8日 21:31

**背景**: 学术编辑常面临两个极端：要么改写过度改变作者风格，要么只做表面修改而忽略结构问题。这种两阶段工作流旨在将深度分析与保守修改相结合，可适用于学位论文、研究报告等长篇文档。

**标签**: `#学术写作者`, `#研究生`, `#论文编辑`, `#需要保留个人风格的学术文本审校`

</section>

---

