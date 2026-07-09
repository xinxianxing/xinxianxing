# 信先行实用卡片 - 2026-07-10

> 从 48 条内容中筛选出 8 条教程/案例/技巧。

---

1. [用户用 Claude Fable 优化 526 条提示词库](#item-1) · TUTORIAL · Score: 7.0 / 10
2. [视频提示词不是文本提示词：核心区别](#item-2) · TUTORIAL · Score: 7.0 / 10
3. [将 24 个 B2B 提示词转化为可复用的 Agent 技能](#item-3) · TUTORIAL · Score: 7.0 / 10
4. [ChatGPT 找出每年 2400 美元的隐形支出](#item-4) · PRODUCTIVITY_TIP · Score: 7.0 / 10
5. [AI 视频提示词结构实验：动作优先 vs 主体优先](#item-5) · TUTORIAL · Score: 7.0 / 10
6. [通过写提示词的游戏学习提示工程](#item-6) · TOOL · Score: 7.0 / 10
7. [Vibe Coding 代码审查：小功能优于大模块](#item-7) · PRODUCTIVITY_TIP · Score: 7.0 / 10
8. [无代码线索路由系统自动生成个性化邮件](#item-8) · TUTORIAL · Score: 6.0 / 10

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1us0vdm" markdown="1">
<a id="item-1"></a>
## [用户用 Claude Fable 优化 526 条提示词库](https://www.reddit.com/r/PromptEngineering/comments/1us0vdm/used_claude_fable_to_strengthen_my_prompt_library/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一位用户分享如何用 Anthropic 的新模型 Claude Fable 对已有提示词库进行重写和优化，提升提示词质量。

**具体怎么做**:
- 收集现有提示词库（如营销、工程类别的提示词）。
- 将整个库输入Claude Fable模型，要求其重写薄弱提示词，使其更强、更具体。
- 对重写后的提示词进行审查，删除或编辑不符合要求的条目。
- 示例：使用“评分与优化”提示词，从清晰度、具体性、上下文完整性、输出就绪性四个维度对提示词评分（1-10），并给出理由。
- 示例：使用“模糊→大师提示词”提示词，将模糊指令转化为完整、可复用的提示词，包含具体任务、模型需要的上下文、输出格式和三个好输出示例。

**适合谁/适用场景**: `提示词工程师`, `AI应用开发者`, `需要优化提示词库的团队或个人`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法依赖于 Claude Fable 模型的能力，不同模型效果可能不同；提示词库的质量和规模会影响结果。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1us0vdm/used_claude_fable_to_strengthen_my_prompt_library/)

reddit · r/PromptEngineering · /u/Emergency-Jelly-3543 · 7月9日 19:45

**背景**: 提示词工程涉及设计输入查询以从大语言模型（LLM）获得期望输出。Claude Fable 是 Anthropic 的最新模型，以其强大的长程推理和编码性能著称，适合用于重写和优化提示词。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.anthropic.com/claude/fable">Claude Fable \ Anthropic</a></li>
<li><a href="https://www.anthropic.com/news/claude-fable-5-mythos-5">Claude Fable 5 and Claude Mythos 5 \ Anthropic</a></li>
<li><a href="https://www.ibm.com/think/topics/prompt-engineering-techniques">Prompt Engineering Techniques | IBM</a></li>

</ul>
</details>

**标签**: `#提示词工程师`, `#AI应用开发者`, `#需要优化提示词库的团队或个人`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1urua1g" markdown="1">
<a id="item-2"></a>
## [视频提示词不是文本提示词：核心区别](https://www.reddit.com/r/PromptEngineering/comments/1urua1g/video_prompting_is_not_text_prompting_heres_why/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 解释视频提示词与文本提示词的核心区别，并提供编写有效视频提示词的关键技巧。

**具体怎么做**:
- 理解视频模型预测的是下一帧，而非下一个词，因此提示词必须描述运动、物理和空间变化。
- 使用时间副词（如缓慢地、快速地、逐渐地、突然地）来控制运动速度。
- 描述动作序列和细节，例如“猫跳上垫子，前爪前伸，轻轻落地，尾巴甩动”而非仅“猫在垫子上”。

**适合谁/适用场景**: `AI视频生成用户`, `提示词工程师`, `内容创作者`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 技巧基于个人经验，不同视频模型可能表现有差异，需自行测试调整。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1urua1g/video_prompting_is_not_text_prompting_heres_why/)

reddit · r/PromptEngineering · /u/Brave-Round-3573 · 7月9日 15:53

**背景**: 像 PixVerse、Runway 和 Kling 这样的文本到视频 AI 模型根据文本提示生成视频。与预测下一个 token 的文本模型不同，视频模型预测下一帧，因此提示词需要描述运动、物理和时间动态。有效的视频提示词是一项新兴技能，与文本提示词截然不同。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://venice.ai/blog/the-complete-guide-to-ai-video-prompt-engineering">The Complete Guide to AI Video Prompt Engineering</a></li>
<li><a href="https://www.genaintel.com/guides/ai-prompt-engineering-video-generation-guide">AI Prompt Engineering for Video Generation: Complete Guide with Examples | GenAIntel Guides</a></li>

</ul>
</details>

**标签**: `#AI视频生成用户`, `#提示词工程师`, `#内容创作者`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1urq980" markdown="1">
<a id="item-3"></a>
## [将 24 个 B2B 提示词转化为可复用的 Agent 技能](https://www.reddit.com/r/PromptEngineering/comments/1urq980/i_turned_24_recurring_b2b_prompts_into_reusable/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一位用户将 24 个用于 B2B 线索研究和业务数据处理的提示词转化为可复用的 Agent 技能，并开源了代码。

**具体怎么做**:
- 识别重复出现的提示词模式，例如：按ICP评估公司、标准化不一致的职位头衔、研究公司时不编造缺失信息、识别差距后再下结论、保守审查可能的重复记录、使用明确标准对公司和人群进行细分。
- 将每个模式转化为独立的Agent技能，每个技能包含明确的责任、输入、决策规则、工作流步骤和预期输出。
- 将技能集合发布到GitHub仓库：https://github.com/spiralcrew-ou/profilespider-agent-skills

**适合谁/适用场景**: `B2B销售和营销人员`, `提示词工程师`, `需要自动化线索研究和数据处理的团队`, `希望将重复性提示词标准化的开发者`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该技能集为个人项目，未经大规模验证；实际效果取决于具体业务场景和数据质量。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1urq980/i_turned_24_recurring_b2b_prompts_into_reusable/)

reddit · r/PromptEngineering · /u/cryptoteams · 7月9日 13:25

**背景**: 在 B2B 销售中，理想客户画像（ICP）是对最适合某产品或服务的公司类型的详细描述。Agent Skills 是模块化的能力，通过专业知识和工作流程扩展 AI 代理的功能，通常定义在 SKILL.md 文件中。该项目将 Agent Skills 概念应用于标准化常见的 B2B 研究和数据处理任务。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://agentskills.io/home">Agent Skills Overview - Agent Skills</a></li>
<li><a href="https://learn.microsoft.com/en-us/agent-framework/agents/skills">Agent Skills | Microsoft Learn</a></li>
<li><a href="https://www.salesforce.com/sales/ideal-customer-profile/">Ideal Customer Profiles (ICPs): Benefits & How to Create | Salesforce</a></li>

</ul>
</details>

**社区讨论**: 作者询问这些技能是否算得上真正可复用的领域技能，还是仍然过于接近结构化的提示词模板，并邀请提示词工程师提供反馈。

**标签**: `#B2B销售和营销人员`, `#提示词工程师`, `#需要自动化线索研究和数据处理的团队`, `#希望将重复性提示词标准化的开发者`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1urm0u9" markdown="1">
<a id="item-4"></a>
## [ChatGPT 找出每年 2400 美元的隐形支出](https://www.reddit.com/r/PromptEngineering/comments/1urm0u9/i_gave_chatgpt_everything_i_earn_and_spend_and/)

**栏目分类**: `PRODUCTIVITY_TIP`

**一句话简介**: 通过将个人收支数据粘贴给 ChatGPT，让它找出被忽略的订阅、重复付费、涨价项目等，快速发现可节省的年度开支。

**具体怎么做**:
- 导出或整理所有收入、支出、订阅和定期扣款记录，以文本形式粘贴给ChatGPT。
- 使用提示词：'请分析所有数据，找出：1. 几乎没用或忘记的订阅；2. 不同形式的重复付费；3. 悄悄涨价的费用；4. 难以当面辩护的支出；5. 节省最多且不影响生活的三项削减。并计算年度总节省。'
- 重点关注第4项（难以辩护的支出），重新审视消费选择。

**适合谁/适用场景**: `个人理财者`, `希望减少不必要开支的人`, `使用AI进行财务分析的用户`

**效果或数据**: 作者称 ChatGPT 在一分钟内找出了每年 2400 美元的隐形支出。

**可信度/风险提示**: 结果依赖于用户提供数据的完整性和准确性；ChatGPT 可能遗漏某些项目或产生误判；实际节省需用户自行核实并执行削减。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1urm0u9/i_gave_chatgpt_everything_i_earn_and_spend_and/)

reddit · r/PromptEngineering · /u/Professional-Rest138 · 7月9日 10:11

**背景**: 许多人都有定期订阅和扣费项目，时间一长就容易忘记。AI 语言模型能够解析交易文本并识别模式或异常，因此可用于财务审计。

**标签**: `#个人理财者`, `#希望减少不必要开支的人`, `#使用AI进行财务分析的用户`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1url4wq" markdown="1">
<a id="item-5"></a>
## [AI 视频提示词结构实验：动作优先 vs 主体优先](https://www.reddit.com/r/PromptEngineering/comments/1url4wq/i_generated_47_useless_ai_video_clips_before/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一位用户通过 47 次实验对比了两种 AI 视频提示词结构，发现“动作优先”的提示词命中率远高于“主体优先”。

**具体怎么做**:
- 确定目标场景（如“咖啡店早晨，温馨氛围，人们在用笔记本工作”）
- 编写“主体优先”提示词：先描述主体再描述动作（如“一家咖啡店，晨光，人们在用笔记本，温馨氛围”）
- 编写“动作优先”提示词：先描述镜头运动再描述场景细节（如“缓慢推入咖啡店，晨光洒在木桌上，杯子冒热气，柔和的阴影”）
- 分别用AI视频工具生成，对比成功率

**适合谁/适用场景**: `AI视频创作者`, `提示词工程师`, `希望提升AI视频生成质量的人`

**效果或数据**: 主体优先命中率 2/10，动作优先命中率 6/10。原文未提供具体工具名称。

**可信度/风险提示**: 实验基于个人经验，不同工具和场景可能结果不同；提示词结构并非唯一影响因素。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1url4wq/i_generated_47_useless_ai_video_clips_before/)

reddit · r/PromptEngineering · /u/Feeling_Till_7418 · 7月9日 09:22

**背景**: AI 视频生成模型需要结构化的提示词才能生成连贯的运动和场景。与文本模型不同，视频模型需要明确的运动提示和具体名词，以避免出现多余肢体或漂浮物体等伪影。常见的提示词公式包括指定镜头运动、场景和细节。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://zhuanlan.zhihu.com/p/708946093">史上最全的AI视频生成提示词 - 知乎</a></li>
<li><a href="https://help.aliyun.com/zh/model-studio/text-to-video-prompt">文生视频或图生视频提示词Prompt使用指南-大模型服务平台百炼(Model Studio)-阿里云帮助中心</a></li>
<li><a href="https://zhuanlan.zhihu.com/p/1966886626169946484">打造影视级AI视频的秘诀：Wan2.2 视频生成—提示词指南 - 知乎</a></li>

</ul>
</details>

**标签**: `#AI视频创作者`, `#提示词工程师`, `#希望提升AI视频生成质量的人`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1urh5n0" markdown="1">
<a id="item-6"></a>
## [通过写提示词的游戏学习提示工程](https://www.reddit.com/r/PromptEngineering/comments/1urh5n0/built_a_game_where_you_actually_write_prompts/)

**栏目分类**: `TOOL`

**一句话简介**: 一个免费在线游戏，通过 10 个关卡让玩家实际编写提示词，由 AI 评估是否使用了正确的提示技巧，帮助巩固提示工程技能。

**具体怎么做**:
- 访问 thepromptgame.vercel.app
- 从零样本基础开始，逐关挑战，每关是一个特定的提示工程任务
- 编写提示词，真实LLM响应，另一个AI评估是否使用了正确技巧
- 每关每天有5次尝试机会，迫使你在提交前思考
- 最终挑战：编写一个包含分类、提取和格式化的单次提示词管道

**适合谁/适用场景**: `提示工程初学者`, `希望实践而非被动学习提示技巧的人`, `想测试自己提示工程水平的人`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 游戏由个人开发者构建，评估 AI 的准确性未经验证；免费使用，但可能存在限制或未来收费。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1urh5n0/built_a_game_where_you_actually_write_prompts/)

reddit · r/PromptEngineering · /u/git_blame_nobody · 7月9日 05:36

**背景**: 提示工程是为生成式 AI 模型设计输入指令以产生期望输出的实践。常见技巧包括零样本、少样本、思维链和角色分配。该游戏旨在让学习这些技巧变得更有趣、更有效。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Zero-shot_prompting">Zero-shot prompting</a></li>

</ul>
</details>

**标签**: `#提示工程初学者`, `#希望实践而非被动学习提示技巧的人`, `#想测试自己提示工程水平的人`

</section>

---

<section class="action-card" data-card-id="twitter:tweet:2075261703411904826" markdown="1">
<a id="item-7"></a>
## [Vibe Coding 代码审查：小功能优于大模块](https://twitter.com/dotey/status/tweet-2075261703411904826)

**栏目分类**: `PRODUCTIVITY_TIP`

**一句话简介**: 针对 AI 生成代码量过大难以审查的问题，提出借鉴敏捷开发中的持续集成思想，通过小功能点迭代来降低审查负担。

**具体怎么做**:
- 将需求拆解为小功能点或小 bug 修复，每次只让 AI 完成一个小的变更。
- 每次变更后立即验证功能并审查代码，确保质量。
- 配合自动化测试，保证每次小变更后系统整体稳定。
- 避免一次让 AI 生成大量代码，否则难以验收和审查。

**适合谁/适用场景**: `使用 AI 编程工具（如 Cursor、Copilot）的开发者`, `需要审查 AI 生成代码的团队`, `希望提高代码质量和可维护性的程序员`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法基于传统软件工程经验，适用于有一定代码审查能力的开发者；对于完全依赖 AI 的新手，拆解任务可能仍有难度。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://twitter.com/dotey/status/tweet-2075261703411904826)

twitter · 宝玉 · 7月9日 16:52

**背景**: Vibe Coding 是由 Andrej Karpathy 于 2025 年 2 月提出的术语，指开发者几乎不审查就接受 AI 生成代码的 AI 辅助软件开发。传统的瀑布式开发因集成规模大、频率低而难以稳定，催生了敏捷开发的持续集成实践。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Vibe_coding">Vibe coding</a></li>

</ul>
</details>

**标签**: `#使用 AI 编程工具（如 Cursor、Copilot）的开发者`, `#需要审查 AI 生成代码的团队`, `#希望提高代码质量和可维护性的程序员`

</section>

---

<section class="action-card" data-card-id="rss:feed.indiehackers.world_posts.rss?exclude=link-post:5806cb050daeb7f8" markdown="1">
<a id="item-8"></a>
## [无代码线索路由系统自动生成个性化邮件](https://feed.indiehackers.world/post/8cde06d030)

**栏目分类**: `TUTORIAL`

**一句话简介**: 本文介绍如何用无代码方式构建一个线索路由系统，根据线索来源或特征自动发送不同风格的邮件模板。

**具体怎么做**:
- 1. 定义路由规则：例如根据线索的'Route'字段（Self-serve guide 或 Founder reply）决定邮件模板。
- 2. 使用无代码工具（如Zapier、Make）连接表单或CRM，获取线索详情。
- 3. 设置条件分支：如果Route为'Self-serve guide'，则发送包含感谢语和指南链接的邮件，并邀请回复；如果Route为'Founder reply'，则提及用户需求，询问当前使用工具，仅当面向企业时添加日历链接。
- 4. 邮件模板需满足：简单语言、不超过100词、不承诺功能、不提供折扣、不编造产品细节、不提及AI。

**适合谁/适用场景**: `创业者`, `小团队`, `营销人员`, `需要自动化线索跟进的人`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 需要根据实际业务调整路由规则和邮件内容；无代码工具可能有使用限制或费用。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://feed.indiehackers.world/post/8cde06d030)

rss · Indie Hackers · 7月9日 15:52

**背景**: 线索路由是根据预定义规则将新线索分配给合适的销售人员或自动化工作流的过程。无代码工具允许非技术用户通过可视化界面而非编写代码来构建此类自动化。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.conferbot.com/zh/industries/real-estate-chatbots">房地产聊天机器人| AI智能获客| Conferbot (2026)</a></li>

</ul>
</details>

**标签**: `#创业者`, `#小团队`, `#营销人员`, `#需要自动化线索跟进的人`

</section>

---

