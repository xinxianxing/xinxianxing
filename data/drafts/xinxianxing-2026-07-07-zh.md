# 信先行实用卡片 - 2026-07-07

> 从 31 条内容中筛选出 7 条教程/案例/技巧。

---

1. [提示词三要素框架：人物、地点、事物](#item-1) · TUTORIAL · Score: 7.0 / 10
2. [Flux 与 Stable Diffusion 的提示词写法差异](#item-2) · TUTORIAL · Score: 7.0 / 10
3. [设计令牌解决 AI 网站千篇一律问题](#item-3) · TUTORIAL · Score: 7.0 / 10
4. [Anthropic 工程师分享最大化 Fable 5 效率的技巧](#item-4) · TUTORIAL · Score: 7.0 / 10
5. [免费可视化 LLM 成本计算器对比 OpenAI、Claude、Gemini](#item-5) · TOOL · Score: 6.0 / 10
6. [Claude.md 指令文件：减少 AI 幻觉的提示词](#item-6) · TUTORIAL · Score: 6.0 / 10
7. [停止 AI 打地鼠：提示词强迫根本原因分析](#item-7) · TUTORIAL · Score: 6.0 / 10

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1up6mrr" markdown="1">
<a id="item-1"></a>
## [提示词三要素框架：人物、地点、事物](https://www.reddit.com/r/PromptEngineering/comments/1up6mrr/the_3slot_framework_i_use_for_every_prompt_person/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个简单的提示词框架，通过固定人物、地点、事物三个槽位来快速生成精准的提示词。

**具体怎么做**:
- 在写任何提示词前，先强制填充三个槽位：人物（主体或AI扮演的角色）、地点（场景或上下文）、事物（要生成的对象或任务）。
- 例如图像提示词：“一位老渔夫（人物），在雾蒙蒙的黎明码头（地点），修补一张破网（事物）”。
- 例如写作提示词：“你是一名专利审查员（人物），正在审阅一家小型机器人初创公司的申请（地点/上下文），总结前三大风险（事物）”。
- 三个槽位确定后，再添加风格、语气或约束条件即可。

**适合谁/适用场景**: `提示词工程师`, `AI绘画用户`, `需要撰写结构化提示词的任何人`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 框架简单有效，但实际效果取决于用户对三个要素的精准定义，复杂任务可能需要更多细节。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1up6mrr/the_3slot_framework_i_use_for_every_prompt_person/)

reddit · r/PromptEngineering · /u/viper2045 · 7月6日 18:55

**背景**: 提示词工程是精心设计 AI 模型输入以获得期望输出的实践。存在许多框架，如 BROKE 和 COAST，但像这样简单的基于槽位的方法降低了初学者的门槛。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://juejin.cn/post/7349542148734451731">Prompt工程全攻略：15+Prompt 框 架 一网打尽（BROKE、COAST...</a></li>
<li><a href="https://www.autolab.cloud/blog/google-official-gemini-prompt-guide-complete-analysis-part-1">Google Gemini 提 示 詞指南：掌握AI溝通技巧， 提 升生產力</a></li>

</ul>
</details>

**社区讨论**: 该 Reddit 帖子获得了积极反响，用户们分享了类似的基于槽位的方法，并讨论了变体，例如添加第四个槽位用于风格或语气。

**标签**: `#提示词工程师`, `#AI绘画用户`, `#需要撰写结构化提示词的任何人`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1up6a6f" markdown="1">
<a id="item-2"></a>
## [Flux 与 Stable Diffusion 的提示词写法差异](https://www.reddit.com/r/PromptEngineering/comments/1up6a6f/flux_wants_prose_sd_wants_weighted_tags_what/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 本文解释了为什么同一个提示词在 Stable Diffusion 和 Flux 中效果不同，并给出了各自的优化写法。

**具体怎么做**:
- Stable Diffusion (SD1.5/SDXL)：使用加权、逗号分隔的标签，如“portrait of a female alchemist, dramatic studio lighting, (renaissance oil painting:1.3), intricate golden jewelry, bokeh background”。注意 token 顺序：主体放在前面，风格修饰在后。负面提示词有效，如“blurry, low quality, deformed hands, extra fingers”。
- Flux：使用自然语言描述，避免加权标签和关键词堆砌。例如：“A young alchemist stands in her candlelit study, golden jewelry catching the warm light, painted in the style of a renaissance oil portrait...”

**适合谁/适用场景**: `AI 绘画用户`, `提示词工程师`, `希望在不同模型间迁移提示词的人`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 不同模型版本（如 SD1.5 vs SDXL）内部也有差异，建议实际测试。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1up6a6f/flux_wants_prose_sd_wants_weighted_tags_what/)

reddit · r/PromptEngineering · /u/El_Kasual · 7月6日 18:43

**背景**: Stable Diffusion（SD1.5/SDXL）使用 CLIP 文本编码器，将提示词处理为加权 token 序列，token 顺序和强调很重要。Flux 使用 T5 文本编码器，这是一种基于 transformer 的语言模型，能理解自然语言结构，因此更擅长解释完整句子。Midjourney 采用自然语言加参数的混合方式。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://artpromptsgenerator.org/flux-vs-midjourney-vs-stable-diffusion/">Flux vs Midjourney vs Stable Diffusion : Prompting</a></li>
<li><a href="https://www.runcomfy.com/comfyui-nodes/ComfyUI_ADV_CLIP_emb">Advanced CLIP Text Encode detailed guide | ComfyUI</a></li>

</ul>
</details>

**社区讨论**: 帖子作者分享了自己的挫败感和实用技巧，并邀请其他人提交提示词进行重构。社区反响积极，用户赞赏清晰的解释并分享了自己的经验。

**标签**: `#AI 绘画用户`, `#提示词工程师`, `#希望在不同模型间迁移提示词的人`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uoqcef" markdown="1">
<a id="item-3"></a>
## [设计令牌解决 AI 网站千篇一律问题](https://www.reddit.com/r/PromptEngineering/comments/1uoqcef/the_generic_ai_website_look_is_a_solved_problem/)

**栏目分类**: `TUTORIAL`

**一句话简介**: Anthropic 官方文档指出，AI 生成网站看起来千篇一律的原因是“分布收敛”，解决方法不是更好的提示词，而是使用具体的设计令牌。

**具体怎么做**:
- 1. 识别问题：AI生成网站时，如果视觉设计描述过于模糊（如“现代”、“创意”），模型会从训练数据中采样最常见的样式，导致千篇一律的SaaS模板。
- 2. 解决方法：使用具体的设计令牌（Design Tokens）代替形容词。例如，指定具体的颜色值（#hex）、字体名称、间距、圆角大小等。
- 3. 示例：不要写“现代风格”，而是写“主色：#1a73e8，字体：Inter，标题字号：32px，卡片圆角：12px”。
- 4. 原理：设计令牌消除了模糊性，模型无法“偷懒”回到默认分布，从而生成更独特的设计。

**适合谁/适用场景**: `使用AI生成前端界面的开发者`, `希望避免AI生成同质化设计的UI设计师`, `提示词工程师`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法基于 Anthropic 官方文档，但实际效果可能因模型版本和具体令牌定义而异。需要用户自行测试和调整令牌值。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uoqcef/the_generic_ai_website_look_is_a_solved_problem/)

reddit · r/PromptEngineering · /u/Professional-Rest138 · 7月6日 07:27

**背景**: 设计令牌是存储视觉设计属性（如颜色、间距）的命名实体，作为可复用的变量，构成设计系统的原子构建块。当 AI 模型收到未明确指定的指令时，会从其训练数据中最常见的模式中采样，导致输出千篇一律，这种现象称为分布收敛。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.cnblogs.com/yujiawen/p/17030364.html">Design Token 模型详解 - 喻佳文 - 博客园</a></li>
<li><a href="https://m3.material.io/foundations/design-tokens/overview">Design tokens – Material Design 3</a></li>
<li><a href="https://baoyu.ai/translations/improving-frontend-design-through-skills">借助 Skills 提升前端设计 | Claude | 宝玉的 分 享</a></li>

</ul>
</details>

**社区讨论**: Reddit 帖子获得了积极反响，评论者一致认为设计令牌是实用的解决方案，并分享了避免 AI 设计同质化的其他技巧。

**标签**: `#使用AI生成前端界面的开发者`, `#希望避免AI生成同质化设计的UI设计师`, `#提示词工程师`

</section>

---

<section class="action-card" data-card-id="twitter:tweet:2074255513353642090" markdown="1">
<a id="item-4"></a>
## [Anthropic 工程师分享最大化 Fable 5 效率的技巧](https://twitter.com/dotey/status/tweet-2074255513353642090)

**栏目分类**: `TUTORIAL`

**一句话简介**: Anthropic Claude Code 工程师 Thariq Shihipar 在 AI Engineer World's Fair 演讲中分享了如何通过减少约束、盲区扫描和多原型对比等方法，充分发挥 Fable 5 模型的能力。

**具体怎么做**:
- 1. 解除模型束缚：减少系统提示词中的详细指令和示例，只提供上下文而不给约束，让模型自由发挥。
- 2. 盲区扫描：让模型在动手前先通读相关代码，找出潜在问题。
- 3. 多原型对比：让模型一口气生成四个风格完全不同的原型，通过对比发现自己的偏好。
- 4. 让模型提问：通过模型提问挖掘你脑中未写下的细节。
- 5. 参考代码地图：给模型一段其他系统的代码作为参考，比写规格说明书更高效。
- 6. 记录决策点：让模型在执行过程中记录每个偏离预期的决策点，事后复盘。
- 7. 反向考核：让模型反过来考你，确保你理解它做了什么。

**适合谁/适用场景**: `AI 开发者`, `使用 Claude Code 或类似 AI 编程工具的工程师`, `希望提升 AI 模型使用效率的技术人员`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 演讲内容基于 Fable 5 模型，其他模型可能不适用；减少系统提示词的方法需要模型本身能力足够强。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://twitter.com/dotey/status/tweet-2074255513353642090)

twitter · 宝玉 · 7月6日 22:13

**背景**: Fable 5 是 Anthropic 最新的前沿模型，专为自主、长时间运行的代理任务而设计。'能力悬余'的概念表明模型已具备当前接口未能利用的能力，减少约束可以释放这些能力。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://cursor.com/docs/models/claude-fable-5">Claude Fable 5 | Cursor Docs</a></li>
<li><a href="https://newsletter.pragmaticengineer.com/p/how-claude-code-is-built">How Claude Code is built - by Gergely Orosz</a></li>
<li><a href="https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns">A Field Guide to Claude Fable: Finding Your Unknowns | Claude</a></li>

</ul>
</details>

**社区讨论**: 未提供社区讨论，但演讲引起了开发者的共鸣，他们赞赏从微观管理 AI 转向将其视为思维伙伴的转变，尽管有些人表达了对手动编码的怀念。

**标签**: `#AI 开发者`, `#使用 Claude Code 或类似 AI 编程工具的工程师`, `#希望提升 AI 模型使用效率的技术人员`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1upjaxw" markdown="1">
<a id="item-5"></a>
## [免费可视化 LLM 成本计算器对比 OpenAI、Claude、Gemini](https://www.reddit.com/r/PromptEngineering/comments/1upjaxw/i_built_a_free_visual_llm_calculator_to_compare/)

**栏目分类**: `TOOL`

**一句话简介**: 一个免费的交互式工具，用于直观对比 GPT-4o、Claude 3.5 Sonnet 和 Gemini 1.5 Pro 的 API 调用成本。

**具体怎么做**:
- 访问 https://neutraloverdrive.com/tools/token-calculator/
- 使用滑块调整输入和输出 token 数量
- 工具自动计算每千次和每百万次运行的成本，并支持多模型并排对比

**适合谁/适用场景**: `AI 应用开发者`, `Prompt 工程师`, `需要估算 API 预算的团队或个人`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 工具由个人开发者构建，模型价格可能随官方更新而变动，建议使用时核对最新定价。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1upjaxw/i_built_a_free_visual_llm_calculator_to_compare/)

reddit · r/PromptEngineering · /u/brancpa · 7月7日 03:25

**背景**: 像 GPT-4o、Claude 和 Gemini 这样的大语言模型通过 API 按 token（约 0.75 个单词）收费。开发者在构建需要多次调用 LLM 的应用时，需要准确估算成本，但不同模型和提供商的定价各异，手动计算非常繁琐。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.grammarly.com/blog/ai/what-is-gpt-4o/">GPT - 4 o 101: What It Is and How It Works | Grammarly</a></li>
<li><a href="https://www.anthropic.com/news/claude-3-5-sonnet">Introducing Claude 3.5 Sonnet \ Anthropic</a></li>
<li><a href="https://ai.google.dev/gemini-api/docs/pricing">Gemini Developer API pricing | Gemini API | Google AI for Developers</a></li>

</ul>
</details>

**社区讨论**: 该 Reddit 帖子暂无评论，因此没有社区讨论内容。

**标签**: `#AI 应用开发者`, `#Prompt 工程师`, `#需要估算 API 预算的团队或个人`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uozuko" markdown="1">
<a id="item-6"></a>
## [Claude.md 指令文件：减少 AI 幻觉的提示词](https://www.reddit.com/r/PromptEngineering/comments/1uozuko/this_my_gold_claudemd_instructions_file/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个可粘贴到 Claude.md 或任何 LLM 指令框中的提示词，旨在通过强制来源验证来减少 AI 的虚构回答。

**具体怎么做**:
- 将提供的指令文件内容复制到 Claude.md 或 LLM 的 instructions 框中。
- 指令核心原则：LLM 是知识管道，不是知识源头；每个事实必须有来源，输出前必须追溯来源。
- 操作循环：解析来源 → 验证 → 按风险缩放 → 推理约束 → 输出前检查 → 反馈。
- 禁止行为：不基于虚构知识行动，不存储虚构知识，不用自信语言填补缺失事实。

**适合谁/适用场景**: `需要高准确性的 AI 应用开发者`, `使用 Claude 或其他 LLM 进行事实性任务的人`, `希望减少 AI 幻觉的提示工程师`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该提示词依赖用户严格执行来源验证，实际效果可能因模型和任务而异；未提供测试数据或对比结果。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uozuko/this_my_gold_claudemd_instructions_file/)

reddit · r/PromptEngineering · /u/Financial_Tailor7944 · 7月6日 15:01

**背景**: 像 Claude 这样的 LLM 可能会生成听起来合理但不正确的信息，这被称为幻觉或虚构。检索增强生成（RAG）和思维链提示等技术有助于减少这种情况，而 Claude.md 文件提供了一种项目特定的配置来指导模型行为。这个提示词是一个自定义指令，可以粘贴到 Claude.md 或任何 LLM 的指令框中，以强制执行严格的来源验证。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://apidog.com/blog/claude-md/">How to Use claude . md for AI Coding: Guide for Dev Teams</a></li>
<li><a href="https://www.humanlayer.dev/blog/writing-a-good-claude-md">Writing a good CLAUDE . md | HumanLayer Blog</a></li>
<li><a href="https://claudelog.com/faqs/what-is-claude-md/">What is CLAUDE . md in Claude Code | ClaudeLog</a></li>

</ul>
</details>

**标签**: `#需要高准确性的 AI 应用开发者`, `#使用 Claude 或其他 LLM 进行事实性任务的人`, `#希望减少 AI 幻觉的提示工程师`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uoyzoc" markdown="1">
<a id="item-7"></a>
## [停止 AI 打地鼠：提示词强迫根本原因分析](https://www.reddit.com/r/PromptEngineering/comments/1uoyzoc/stop_the_ai_whackamole_a_simple_prompt_that/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个提示词技巧，让 AI 在技术故障排查时不再盲目尝试命令，而是先分析根本原因。

**具体怎么做**:
- 原文未提供详细步骤，但核心思路是：在提示词中要求AI先进行系统分析，列出可能的原因和证据，再提出解决方案。
- 例如，可以添加指令：“在提出任何命令之前，请先分析问题的根本原因，并解释你的推理过程。”

**适合谁/适用场景**: `技术故障排查者`, `Linux系统管理员`, `使用AI进行复杂问题解决的用户`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法基于作者经验，效果可能因 AI 模型和具体问题而异，需要用户自行测试调整。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uoyzoc/stop_the_ai_whackamole_a_simple_prompt_that/)

reddit · r/PromptEngineering · /u/Signal_Care6558 · 7月6日 14:30

**背景**: 大型语言模型以线性序列逐 token 生成文本，这使得它们容易出现“打地鼠”行为——提供一连串建议而不评估根本原因。它们缺乏对之前会话的持久记忆，并且在复杂故障排查所需的分支逻辑上存在困难。所提出的提示词模板提供了一个可重复使用的上下文，引导模型遵循诊断工作流程。

**标签**: `#技术故障排查者`, `#Linux系统管理员`, `#使用AI进行复杂问题解决的用户`

</section>

---

