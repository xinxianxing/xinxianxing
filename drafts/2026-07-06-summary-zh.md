---
layout: default
title: "信先行 Action Cards: 2026-07-06 (ZH)"
date: 2026-07-06
lang: zh
---

> 从 15 条内容中筛选出 6 条教程/案例/技巧。

---

1. [设计令牌解决 AI 网站千篇一律问题](#item-1) · TUTORIAL · Score: 8.0 / 10
2. [决策笔记：LLM 代理的新模式](#item-2) · TUTORIAL · Score: 7.0 / 10
3. [学术论文人性化改写提示词](#item-3) · TUTORIAL · Score: 7.0 / 10
4. [用好 Claude Code Fable 5 的三个秘诀](#item-4) · TUTORIAL · Score: 7.0 / 10
5. [精简提示词让 AI 输出更佳](#item-5) · PRODUCTIVITY_TIP · Score: 6.0 / 10
6. [提示词改动提升 SEO 内容质量](#item-6) · TUTORIAL · Score: 6.0 / 10

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uoqcef" markdown="1">
<a id="item-1"></a>
## [设计令牌解决 AI 网站千篇一律问题](https://www.reddit.com/r/PromptEngineering/comments/1uoqcef/the_generic_ai_website_look_is_a_solved_problem/)

**栏目分类**: `TUTORIAL`

**一句话简介**: Anthropic 官方文档指出，AI 生成网站看起来千篇一律的原因是“分布收敛”，解决方案不是更好的提示词，而是使用具体的设计令牌。

**具体怎么做**:
- 1. 识别问题：AI生成网站时，如果视觉设计描述过于模糊（如“现代”、“有创意”），模型会从训练数据分布的中心采样，导致输出趋同于最常见的SaaS模板。
- 2. 避免使用形容词提示：像“让它现代一点”或“有创意”这类提示仍然不够具体，模型只会从同一通用簇中采样附近点。
- 3. 使用设计令牌（Design Tokens）：提供具体的视觉参数，如字体、颜色、间距、圆角等，消除不确定性。例如指定“字体: Inter, 颜色: #333背景 #fff, 主色: #6C63FF, 卡片圆角: 8px, 间距: 24px”。
- 4. 将设计令牌作为系统提示的一部分，或通过结构化输出（如JSON）传递给模型。

**适合谁/适用场景**: `使用AI生成前端界面的开发者`, `希望避免AI输出同质化设计的UI设计师`, `提示工程师`, `需要快速生成定制化网站原型的人`

**效果或数据**: 未提供具体数据，但引用 Anthropic 官方文档说明该方法是经过验证的。

**可信度/风险提示**: 该方法基于 Anthropic 的官方文档，可靠性较高。但实际效果取决于设计令牌的详细程度和模型对令牌的遵循能力。

**实用度评分**: Score: 8.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uoqcef/the_generic_ai_website_look_is_a_solved_problem/)

reddit · r/PromptEngineering · /u/Professional-Rest138 · 7月6日 07:27

**背景**: 设计令牌是视觉设计属性（颜色、排版、间距）的标准化命名值，是设计系统中的单一事实来源。AI 模型中的分布收敛是指当提示词不够具体时，模型会默认采用训练数据中最常见的模式——因此产生千篇一律的 SaaS 风格。基于形容词的提示词如“现代”或“创意”仍然不够具体，无法摆脱这种收敛。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://grokipedia.com/page/Design_tokens">Design tokens</a></li>
<li><a href="https://design.dev/guides/design-systems/">Design Systems & Design Tokens Explained — design.dev</a></li>
<li><a href="https://m3.material.io/foundations/design-tokens/overview">Design tokens – Material Design 3</a></li>

</ul>
</details>

**社区讨论**: Reddit 帖子获得强烈正面反响，评论者一致认为设计令牌比调整提示词更有效。一些人分享了额外技巧，例如将设计令牌文件用作系统提示或与 Figma 等工具集成。少数人指出该方法需要前期投入，但能带来一致性回报。

**标签**: `#使用AI生成前端界面的开发者`, `#希望避免AI输出同质化设计的UI设计师`, `#提示工程师`, `#需要快速生成定制化网站原型的人`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uormlv" markdown="1">
<a id="item-2"></a>
## [决策笔记：LLM 代理的新模式](https://www.reddit.com/r/PromptEngineering/comments/1uormlv/new_ai_pattern_decision_notes_for_llm_agents/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一种轻量级决策记录模式，帮助 AI 代理在行动前回顾历史判断，避免偏离目标。

**具体怎么做**:
- 1. 创建一个 decision-notes/ 目录，用于存储代理的过往决策记录。
- 2. 每条决策笔记包含：决策内容、依据证据、以及明确的“何时重新审视”触发条件。
- 3. 在代理执行工具前，先检查决策笔记，确认当前行动是否与之前人类认可的决策一致。
- 4. 如果新行动与历史决策冲突，代理应标记冲突而非盲目执行。

**适合谁/适用场景**: `使用LLM代理进行自动化工作流的开发者`, `需要长期稳定执行任务的AI代理场景`, `希望减少系统提示词膨胀和代理漂移的团队`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该模式来自网络分享，尚未经过大规模验证；实施效果取决于代理的复杂度和决策笔记的维护质量。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uormlv/new_ai_pattern_decision_notes_for_llm_agents/)

reddit · r/PromptEngineering · /u/Latter-Hospital-4883 · 7月6日 08:43

**背景**: LLM 代理通常依赖向量数据库或维基来获取知识，但缺乏追踪自身过去判断的机制，导致行为随时间不一致。系统提示词膨胀是指将过多指令塞入提示词中，而代理漂移则指逐渐偏离预期目标。决策笔记旨在提供一种轻量级、人类可读的代理推理记录。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f">llm-wiki · GitHub</a></li>
<li><a href="https://www.nickjensen.co/posts/agent-how-to-write-architecture-decision-records">AI Agent for Architecture Decision Records | Nick Jensen</a></li>
<li><a href="https://www.getmaxim.ai/articles/a-comprehensive-guide-to-preventing-ai-agent-drift-over-time/">A Comprehensive Guide to Preventing AI Agent Drift Over Time</a></li>

</ul>
</details>

**社区讨论**: Reddit 帖子作者分享了该模式，并询问其他人是否构建过类似系统，使用 markdown 还是结构化数据库。讨论可能探讨了简单性与可扩展性之间的权衡，一些用户可能主张采用更结构化的方法，如图数据库。

**标签**: `#使用LLM代理进行自动化工作流的开发者`, `#需要长期稳定执行任务的AI代理场景`, `#希望减少系统提示词膨胀和代理漂移的团队`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uo6fww" markdown="1">
<a id="item-3"></a>
## [学术论文人性化改写提示词](https://www.reddit.com/r/PromptEngineering/comments/1uo6fww/the_ultimate_humanizer_prompt_for_students/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个用于将 AI 生成的学术文本改写成更像人类手笔的提示词，通过刻意制造结构不对称和写作摩擦来避免 AI 痕迹。

**具体怎么做**:
- 将以下系统指令复制到ChatGPT或其他AI对话工具中：
- 指令内容：你是一名分析能力强的大学高年级学生，正在撰写高分课程论文。你的写作在智力上严谨、分析上深刻，但具有真实人类思维在键盘上组织想法时产生的有机结构不对称和“草稿摩擦”。你的文笔干净、清晰、专注，完全避免AI文本生成典型的无菌、优化、均匀平衡的布局。你的任务是彻底重写提供的文本，使其成为人类撰写的草稿。保持绝对的技术准确性，但将句法从语义中解耦，以注入真实、非线性的人类足迹。关键重写约束（违反任何一条即失败）：约束1：解耦结构波动性——不允许句子或段落长度与文本的语义功能匹配。在论文的整个时间线上随机变化写作节奏：独立句子、复杂复合句、片段句、列表、过渡句等。约束2：非对称论点展开——避免对称的论点结构。论点可以突然出现、被质疑、被部分撤回，然后再重新审视。约束3：引入“草稿摩擦”——包括偶尔的措辞调整、冗余、自我纠正或轻微的口语化表达。
- 将需要改写的AI生成文本粘贴到对话中，AI会按照指令输出人性化版本。

**适合谁/适用场景**: `学生`, `需要提交学术论文的人`, `希望避免AI检测工具的人`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 提示词效果取决于 AI 模型和原始文本质量；过度使用可能导致逻辑混乱；部分学校可能禁止使用 AI 辅助写作。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uo6fww/the_ultimate_humanizer_prompt_for_students/)

reddit · r/PromptEngineering · /u/True-Yesterday-6274 · 7月5日 16:25

**背景**: AI 生成的文本通常表现出均匀的句子长度、可预测的过渡和过度使用的流行词，使其容易被 AI 分类器检测到。“写作摩擦”指的是人类写作中的自然不完美之处，如句子长度变化和偶尔别扭的措辞，该提示词旨在模仿这些特征。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://docsbot.ai/prompts/education/academic-essay-humanizer">Academic Essay Humanizer - AI Prompt</a></li>
<li><a href="https://phrasly.ai/blog/prompt-to-humanize-ai-text/">The Best Prompts to Humanize AI Text (2026 Guide)</a></li>
<li><a href="https://aceessay.ai/en/essay-humanizer">Free Essay Humanizer - Bypass AI Detectors & No... - Ace Essay</a></li>

</ul>
</details>

**标签**: `#学生`, `#需要提交学术论文的人`, `#希望避免AI检测工具的人`

</section>

---

<section class="action-card" data-card-id="twitter:tweet:2074019009226322078" markdown="1">
<a id="item-4"></a>
## [用好 Claude Code Fable 5 的三个秘诀](https://twitter.com/dotey/status/tweet-2074019009226322078)

**栏目分类**: `TUTORIAL`

**一句话简介**: Claude Code 团队成员分享的使用 Fable 5 模型的新工作方式：将模型视为思维伙伴、设定目标并提供验证方法、更大胆地尝试。

**具体怎么做**:
- 1. 把 Claude 当作思维伙伴：在实施前尽早让 Claude 参与，例如先写一个小的需求规范，让 Claude 就实施方案对你进行“面试提问”，或让它提出多个发展方向并制作 HTML 原型。
- 2. 提供上下文而非仅约束条件：例如不说“保持简单”，而是说“这个功能是实验，可能一个月后删掉，不要构建丢弃起来会心疼的东西”。
- 3. 设定目标并提供验证方法：使用 /goal 指令让 Claude 持续工作直至完成，使用 workflows 功能让 Claude 验证其工作。

**适合谁/适用场景**: `使用 Claude Code 的开发者`, `希望提升 AI 辅助编程效率的程序员`, `需要处理复杂、长时间运行任务的 AI 用户`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法基于 Claude Code 团队成员的分享，但具体效果因人而异，需要用户自行尝试和调整。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://twitter.com/dotey/status/tweet-2074019009226322078)

twitter · 宝玉 · 7月6日 06:33

**背景**: Claude Fable 5 是 Anthropic 在 FrontierBench 上得分最高的模型，擅长长周期推理和陌生工具的使用。Claude Code 是一款集成在终端中的 AI 编程助手。/goal 命令设定一个完成条件，Claude 会持续工作直至达成，无需用户每一步都提示。动态工作流允许 Claude 通过并行子代理执行任务并自行检查工作。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.anthropic.com/claude/fable">Claude Fable \ Anthropic</a></li>
<li><a href="https://code.claude.com/docs/en/goal">Keep Claude working toward a goal - Claude Code Docs</a></li>
<li><a href="https://claude.com/blog/introducing-dynamic-workflows-in-claude-code">Introducing dynamic workflows | Claude by Anthropic</a></li>

</ul>
</details>

**标签**: `#使用 Claude Code 的开发者`, `#希望提升 AI 辅助编程效率的程序员`, `#需要处理复杂、长时间运行任务的 AI 用户`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uoxi5c" markdown="1">
<a id="item-5"></a>
## [精简提示词让 AI 输出更佳](https://www.reddit.com/r/PromptEngineering/comments/1uoxi5c/i_stopped_making_my_prompts_longer_and_the/)

**栏目分类**: `PRODUCTIVITY_TIP`

**一句话简介**: 一位用户发现，减少提示词中的指令、规则和示例，只保留目标和上下文，AI 输出变得更清晰、更可用。

**具体怎么做**:
- 移除提示词中多余的指令、规则和示例
- 只保留核心目标和必要的上下文信息
- 测试精简后的提示词，观察输出质量变化

**适合谁/适用场景**: `提示词工程师`, `AI工具使用者`, `希望提升AI输出质量的人`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该技巧基于个人经验，效果可能因模型和任务而异，建议用户自行测试。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uoxi5c/i_stopped_making_my_prompts_longer_and_the/)

reddit · r/PromptEngineering · /u/Chemical-Spite-3203 · 7月6日 13:33

**背景**: 提示词工程通常涉及编写包含明确指令和示例的详细提示词，以引导 AI 行为。然而，过于复杂的提示词可能引入干扰或限制模型的创造力，导致输出不够自然或重复。这一经验表明，极简方法有时可能更有效。

**标签**: `#提示词工程师`, `#AI工具使用者`, `#希望提升AI输出质量的人`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uos4us" markdown="1">
<a id="item-6"></a>
## [提示词改动提升 SEO 内容质量](https://www.reddit.com/r/PromptEngineering/comments/1uos4us/one_prompt_change_completely_changed_the_quality/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 通过改变提示词策略，让 AI 先思考主题再写作，从而生成深度更强、编辑更少的 SEO 内容。

**具体怎么做**:
- 不要直接要求AI“写一篇SEO文章”，而是先让模型思考主题，理解深层概念后再开始写作。
- 提示词中强调先分析主题的细节、权衡和实际见解，而非仅关注关键词。

**适合谁/适用场景**: `内容创作者`, `SEO从业者`, `使用AI生成文章的写手`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法基于个人经验，效果可能因主题和模型而异；需要自行测试调整。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uos4us/one_prompt_change_completely_changed_the_quality/)

reddit · r/PromptEngineering · /u/Comfortable_War2683 · 7月6日 09:13

**背景**: 面向 SEO 的提示词工程涉及编写精确指令，以生成既满足人类可读性又符合搜索引擎要求的内容。像 ChatGPT Search 和 Perplexity 这样的 AI 搜索引擎现在优先考虑展示专业知识并提供简洁答案的内容。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.linkedin.com/pulse/prompt-engineering-seo-friendly-content-writing-ultimate-aritra-bose-t0acc">Prompt Engineering for SEO Friendly Content Writing: The Ultimate...</a></li>
<li><a href="https://www.texta.ai/glossary/ai-search/prompt-engineering-seo">Prompt Engineering for SEO : Definition and Guide | Texta</a></li>
<li><a href="https://loudscale.com/blog/best-chatgpt-prompts-seo-marketing/">Best ChatGPT Prompts for SEO & Marketing... | LoudScale</a></li>

</ul>
</details>

**社区讨论**: 该 Reddit 帖子获得了积极反响，作者指出提示词工程对内容质量的影响比更换 AI 模型更大，并邀请其他人分享自己的提示词。

**标签**: `#内容创作者`, `#SEO从业者`, `#使用AI生成文章的写手`

</section>

---