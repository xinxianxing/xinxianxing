# 信先行实用卡片 - 2026-07-12

> 从 29 条内容中筛选出 4 条教程/案例/技巧。

---

1. [别急着改提示词，先做好分镜表](#item-1) · TUTORIAL · Score: 7.0 / 10
2. [写出好提示词的 5 个关键要素](#item-2) · TUTORIAL · Score: 7.0 / 10
3. [简化终端 AI 智能体：无需复杂模型路由](#item-3) · PRODUCTIVITY_TIP · Score: 6.0 / 10
4. [防止 ChatGPT 在跨宇宙故事中直接命名原作](#item-4) · TUTORIAL · Score: 6.0 / 10

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1utasqj" markdown="1">
<a id="item-1"></a>
## [别急着改提示词，先做好分镜表](https://www.reddit.com/r/PromptEngineering/comments/1utasqj/stop_trying_to_fix_ai_video_prompts_build_the/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个 AI 视频创作者分享经验：与其反复修改提示词，不如先拆解脚本、制作分镜表，让每个提示词有明确目标，从而提升生成质量。

**具体怎么做**:
- 1. 将脚本拆解为一个个独立的镜头（shot），每个镜头对应一个明确的画面目标。
- 2. 为每个镜头锁定参考图（reference images），确保角色、产品、场景一致。
- 3. 基于分镜表为每个镜头单独编写提示词，而不是写一个长段落。
- 4. 使用工具（如Framia的Creative Agent）自动将脚本拆分为镜头并保持参考图在画布上。

**适合谁/适用场景**: `AI视频创作者`, `需要生成连贯AI视频的广告制作者`, `提示词工程师`, `内容创作者`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法基于个人经验，效果可能因工具和场景而异；Framia 工具的具体效果未经验证。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1utasqj/stop_trying_to_fix_ai_video_prompts_build_the/)

reddit · r/PromptEngineering · /u/ke1lle · 7月11日 05:04

**背景**: Sora、可灵、Veo 等 AI 视频生成模型能产出高质量片段，但常难以保持多镜头间的一致性，尤其对于较长的叙事。传统电影制作使用分镜表和镜头列表来规划每个场景，而许多 AI 用户跳过了这一步。Framia、SkyReels 等工具正涌现，将前期制作整合到 AI 工作流中。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://framia.pro/">Framia Pro | All-in-One Creative & Marketing Studio</a></li>
<li><a href="https://github.com/xuanyustudio/LocalMiniDrama/blob/main/README.md">LocalMiniDrama/README.md at main · xuanyustudio/LocalMiniDrama</a></li>
<li><a href="https://skyreels.ai/">SkyReels</a></li>

</ul>
</details>

**标签**: `#AI视频创作者`, `#需要生成连贯AI视频的广告制作者`, `#提示词工程师`, `#内容创作者`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1ut784q" markdown="1">
<a id="item-2"></a>
## [写出好提示词的 5 个关键要素](https://www.reddit.com/r/PromptEngineering/comments/1ut784q/the_5_things_missing_from_almost_every_bad/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个框架，教你如何通过补充目标、上下文、约束、输出格式和示例来改善 ChatGPT/Claude 的提示词，从而获得更好的输出。

**具体怎么做**:
- 1. 明确目标：写出具体期望的结果，而非模糊主题。例如，不要写“写一封营销邮件”，而要写“写一封针对30天未登录用户的重新激活邮件”。
- 2. 提供上下文：告诉模型你自己是谁、尝试过什么、以及用途等背景信息。
- 3. 设定约束：指定长度、语气、避免的内容。负面约束（如“不要使用企业行话”）比正面指令更有效。
- 4. 指定输出格式：明确要求用列表、表格、JSON或选项数量等格式，否则模型会使用最通用的默认格式。
- 5. 给出示例：展示你想要的风格，比单纯描述效果更好。

**适合谁/适用场景**: `使用ChatGPT或Claude的普通用户`, `希望提升AI输出质量的提示词工程师`, `需要写营销文案、报告、代码等内容的职场人士`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该框架基于个人经验总结，缺乏大规模验证；不同模型和任务可能需要调整。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1ut784q/the_5_things_missing_from_almost_every_bad/)

reddit · r/PromptEngineering · /u/Spiritual_Frame8340 · 7月11日 02:06

**背景**: 提示工程是设计输入给大语言模型以获取期望输出的实践。许多用户编写模糊的提示词，缺乏具体性，导致通用或不相关的回复。该框架通过用明确的目标、上下文、约束、格式和示例来构建提示词，解决了常见的缺失点。

**标签**: `#使用ChatGPT或Claude的普通用户`, `#希望提升AI输出质量的提示词工程师`, `#需要写营销文案、报告、代码等内容的职场人士`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1utnv71" markdown="1">
<a id="item-3"></a>
## [简化终端 AI 智能体：无需复杂模型路由](https://www.reddit.com/r/PromptEngineering/comments/1utnv71/you_probably_dont_need_model_routing_scripts_for/)

**栏目分类**: `PRODUCTIVITY_TIP`

**一句话简介**: 一个关于简化终端 AI 智能体模型路由的实用技巧：用单一网关让智能体自主选择模型，而不是编写复杂的路由脚本。

**具体怎么做**:
- 使用一个统一的端点（如Enter Code）作为网关，让终端智能体根据任务自主选择模型。
- 对于需要深度推理的任务，让智能体选择Claude；对于生成样板代码等简单任务，选择GPT。
- 避免编写超过200行的bash路由脚本，减少维护负担。

**适合谁/适用场景**: `开发终端AI智能体的开发者`, `希望简化模型路由逻辑的工程师`, `使用Claude和GPT等不同模型的开发者`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法依赖于智能体自主选择的能力，可能不适用于所有场景；模型更新后智能体的选择逻辑可能需要调整。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1utnv71/you_probably_dont_need_model_routing_scripts_for/)

reddit · r/PromptEngineering · /u/ke1lle · 7月11日 15:59

**背景**: 目前许多开发者编写自定义路由逻辑，根据内容将提示导向不同的 LLM（如 Claude、GPT）。这通常导致复杂且脆弱的脚本，随着新模型的出现需要频繁更新。使用网关通过将模型选择集中到智能体内部来简化架构。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://code.claude.com/docs/en/gateways">Run Claude Code through a gateway - Claude Code Docs</a></li>

</ul>
</details>

**标签**: `#开发终端AI智能体的开发者`, `#希望简化模型路由逻辑的工程师`, `#使用Claude和GPT等不同模型的开发者`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1ut7fue" markdown="1">
<a id="item-4"></a>
## [防止 ChatGPT 在跨宇宙故事中直接命名原作](https://www.reddit.com/r/PromptEngineering/comments/1ut7fue/help_me_with_my_story/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个用户求助如何让 ChatGPT 在创作包含多个虚构宇宙（如终结者、德军总部）的故事时，不通过背景角色直接说出宇宙名称，而是让每个宇宙显得全新。

**具体怎么做**:
- 在系统提示或故事设定中明确要求：禁止任何角色或叙述提及现实中的作品名称、系列名称或具体作品标题。
- 使用类似提示：'所有宇宙都应当被视为原创世界，角色不应知道他们来自哪个作品，也不应提及任何现实中的电影、游戏或小说名称。'
- 如果ChatGPT仍然出现此类问题，可以添加负面示例：'例如，不要出现“这是终结者宇宙”或“我们在德军总部2新巨像”这样的台词。'
- 在每次生成后检查输出，若仍有违规，可继续补充约束条件。

**适合谁/适用场景**: `使用ChatGPT创作跨宇宙故事的写作者`, `希望避免AI直接引用现实作品名称的创作者`, `需要保持故事沉浸感的用户`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 提示效果可能因模型版本和上下文长度而异；需要多次迭代调整提示才能稳定避免此类输出。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1ut7fue/help_me_with_my_story/)

reddit · r/PromptEngineering · /u/throwawa982y41 · 7月11日 02:16

**背景**: 提示工程是向 ChatGPT 等大型语言模型精心设计输入以获得期望输出的实践。在小说写作中，用户常需引导模型避免打破第四面墙或引用现实作品。技巧包括在系统提示中设置明确规则、使用否定指令，以及根据输出迭代优化提示。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://help.openai.com/en/articles/10032626-prompt-engineering-best-practices-for-chatgpt">Prompt engineering best practices for ChatGPT | OpenAI Help Center</a></li>
<li><a href="https://www.youtube.com/watch?v=_ZvnD73m40o">Prompt Engineering Tutorial – Master ChatGPT and LLM... - YouTube</a></li>

</ul>
</details>

**标签**: `#使用ChatGPT创作跨宇宙故事的写作者`, `#希望避免AI直接引用现实作品名称的创作者`, `#需要保持故事沉浸感的用户`

</section>

---

