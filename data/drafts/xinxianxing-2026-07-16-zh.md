# 信先行实用卡片 - 2026-07-16

> 从 42 条内容中筛选出 7 条教程/案例/技巧。

---

1. [15 分钟构建系统提示词测试数据集](#item-1) · TUTORIAL · Score: 8.0 / 10
2. [语音优先规则修复语音转写编辑问题](#item-2) · TUTORIAL · Score: 7.0 / 10
3. [Seedance 2.0 稳定动作提示词模式](#item-3) · TUTORIAL · Score: 7.0 / 10
4. [Claude 订阅包含云虚拟机，实现持久化编码](#item-4) · PRODUCTIVITY_TIP · Score: 7.0 / 10
5. [AI 自动评估客户定价风险](#item-5) · TUTORIAL · Score: 6.0 / 10
6. [通过 API 为 AI 代理分配真实邮箱](#item-6) · TUTORIAL · Score: 6.0 / 10
7. [保留面部特征的 AI 商务肖像提示词](#item-7) · TUTORIAL · Score: 6.0 / 10

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uxauuh" markdown="1">
<a id="item-1"></a>
## [15 分钟构建系统提示词测试数据集](https://www.reddit.com/r/PromptEngineering/comments/1uxauuh/for_a_great_system_prompt_build_a_dataset_in_15/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 通过快速构建测试数据集来优化系统提示词，避免生产环境中的失败。

**具体怎么做**:
- 列出提示词必须完成的3-5个任务，每个任务写2-3个典型用例。
- 添加你担心的输入：最长、最短、模糊、错误语言或格式的输入。
- 添加2-3个对抗性用例（试图劫持指令的输入）。
- 为每个用例写出“好”的标准（一句话即可），作为评分标准或参考答案。
- 可以用LLM生成用例变体，但需人工审查，因为会生成一些无意义内容。
- 15-20个用例足够开始，目标不是覆盖全面，而是捕捉生产环境中可能出现的失败。

**适合谁/适用场景**: `提示词工程师`, `AI应用开发者`, `需要优化系统提示词的团队`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 方法基于作者经验，效果取决于用例质量和审查；LLM 生成的变体可能包含错误，需人工审核。

**实用度评分**: Score: 8.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uxauuh/for_a_great_system_prompt_build_a_dataset_in_15/)

reddit · r/PromptEngineering · /u/Old_Organization1183 · 7月15日 16:27

**背景**: 系统提示词是给 LLM 的指令，用于定义其行为。没有测试数据集，很难知道提示词更改是否真的提升了性能。对抗性输入是故意设计的，旨在劫持提示词，针对它们进行测试对于鲁棒性至关重要。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/datasets/Naomibas/llm-system-prompts-benchmark">Naomibas/llm-system-prompts-benchmark - Hugging Face</a></li>
<li><a href="https://github.com/KazKozDev/system-prompt-benchmark">KazKozDev/system-prompt-benchmark - GitHub</a></li>
<li><a href="https://www.stingrai.io/blog/ultimate-guide-to-adversarial-inputs-in-llms">Ultimate Guide to Adversarial Inputs in LLMs</a></li>

</ul>
</details>

**标签**: `#提示词工程师`, `#AI应用开发者`, `#需要优化系统提示词的团队`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uxjgjc" markdown="1">
<a id="item-2"></a>
## [语音优先规则修复语音转写编辑问题](https://www.reddit.com/r/PromptEngineering/comments/1uxjgjc/a_simple_system_prompt_heuristic_to_fix/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个简单的系统提示词规则，让 LLM 在编辑语音转写文本时优先采用北约音标拼写，避免模型错误“修正”正确拼写。

**具体怎么做**:
- 在系统提示词中加入“语音优先”规则：
- 规则内容：将北约音标拼写（如“Golf Alpha Romeo...”）或逐字母拼写视为专有名词、姓名、序列号、代码的绝对加密锚点。
- 如果拼写出的单词与对应的音标拼写冲突，始终修正单词以匹配音标拼写。
- 永远不要改变音标字母去匹配假设的单词。

**适合谁/适用场景**: `使用语音转写工具的用户`, `需要编辑语音转写文本的LLM应用开发者`, `处理专有名词、序列号等场景的提示词工程师`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该技巧基于作者个人经验，未提供量化效果或广泛测试结果；实际效果可能因模型和具体场景而异。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uxjgjc/a_simple_system_prompt_heuristic_to_fix/)

reddit · r/PromptEngineering · /u/FractionalTotality · 7月15日 21:47

**背景**: 语音转写系统经常产生拼写错误的专有名词，因为它们依赖的声学模型可能听错不熟悉的单词。北约音标字母表是一套标准化的单词（例如“Alpha”代表 A，“Bravo”代表 B），用于无线电通信中清晰地拼出字母。用于编辑转录文本的 LLM 可能会错误地将正确拼写的音标单词“修正”为与拼写错误的转录文本匹配，而这条规则可以防止这种情况。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/NATO_phonetic_alphabet">NATO phonetic alphabet</a></li>

</ul>
</details>

**社区讨论**: 原帖作者分享了这条规则，并指出 LLM 本身从架构角度承认该方法“非常符合逻辑”。来源中没有提供其他评论。

**标签**: `#使用语音转写工具的用户`, `#需要编辑语音转写文本的LLM应用开发者`, `#处理专有名词、序列号等场景的提示词工程师`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1ux2gmu" markdown="1">
<a id="item-3"></a>
## [Seedance 2.0 稳定动作提示词模式](https://www.reddit.com/r/PromptEngineering/comments/1ux2gmu/a_few_seedance_20_prompts_that_actually_hold/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 分享三个让 Seedance 2.0 生成稳定连贯动作的提示词编写模式，避免画面变形或跳跃。

**具体怎么做**:
- 1. 使用单一连续动作，而非动作列表。例如：“一个连续镜头。一只纸船沿着雨水沟漂流，逐渐加速，在一个小瀑布处旋转一次，然后滑入平静的水面。摄像机全程跟拍，无剪辑。”
- 2. 锁定主体描述一次，之后只描述运动。例如：“一只红色折纸鹤，有折纸纹理和锋利折痕。它扇动两次翅膀，从木桌上起飞，向左转弯，落在窗台上。全程保持相同的纸张纹理和比例。”
- 3. 明确指定摄像机运动。例如：“缓慢推进到一杯咖啡上，蒸汽升腾缭绕。其他部分保持固定构图，无剪辑。”

**适合谁/适用场景**: `AI 视频生成用户`, `提示词工程师`, `使用 Seedance 2.0 创作动画或短片的人`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 这些模式基于作者个人测试，不同模型版本或参数设置下效果可能不同，需要自行尝试调整。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1ux2gmu/a_few_seedance_20_prompts_that_actually_hold/)

reddit · r/PromptEngineering · /u/Practical_Low29 · 7月15日 10:54

**背景**: Seedance 2.0 是字节跳动于 2026 年 2 月发布的文本到视频 AI 模型。它能根据文本提示生成逼真的视频片段，但常在保持主体外观一致和帧间平滑运动方面遇到困难。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Seedance_2.0">Seedance 2.0</a></li>
<li><a href="https://magichour.ai/blog/cinematic-ai-video-prompt-cookbook">Cinematic AI Video Prompt Cookbook (2026): 25 Patterns for Realistic ...</a></li>
<li><a href="https://gptprompts.ai/ai-video-prompts">AI Video Prompts: Scripts, Scenes, Camera Moves and Motion</a></li>

</ul>
</details>

**社区讨论**: 该帖子获得了积极反响，用户确认这些模式有效，并分享了额外技巧，如添加负面提示词以避免常见伪影。

**标签**: `#AI 视频生成用户`, `#提示词工程师`, `#使用 Seedance 2.0 创作动画或短片的人`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uwoh2z" markdown="1">
<a id="item-4"></a>
## [Claude 订阅包含云虚拟机，实现持久化编码](https://www.reddit.com/r/PromptEngineering/comments/1uwoh2z/your_claude_subscription_includes_cloud_computers/)

**栏目分类**: `PRODUCTIVITY_TIP`

**一句话简介**: 利用 Claude 订阅附带的云 VM，通过准备私有上下文仓库来避免每次会话从零开始，实现持久化开发环境。

**具体怎么做**:
- 创建一个私有上下文仓库，包含：仓库间关系、项目约定、重要架构决策、近期工作记录。
- 启动新Claude Code会话时，同时附加上下文仓库和相关工作仓库。
- 任务提示可以简短，因为Claude已理解环境。
- 可以启动多个调查，每个分配独立VM，关闭笔记本后从手机查看结果。

**适合谁/适用场景**: `使用Claude Code进行开发的程序员`, `需要长时间运行或并行任务的开发者`, `希望利用云资源提高效率的Claude订阅用户`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 依赖 Claude 订阅的云 VM 功能，不同订阅层级可能限制资源；上下文仓库需自行维护更新。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uwoh2z/your_claude_subscription_includes_cloud_computers/)

reddit · r/PromptEngineering · /u/MostBlood7319 · 7月14日 23:07

**背景**: Claude Code 是一种 AI 编码助手，可以在 Anthropic 管理的隔离云虚拟机中执行代码。默认情况下，每个新会话都没有任何项目上下文，用户需要每次重新附加仓库并重新解释约定。私有上下文仓库通过提供一个可复用的知识库来解决这个问题，Claude 在会话启动时加载该知识库。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://code.claude.com/docs/en/claude-code-on-the-web">Use Claude Code on the web - Claude Code Docs</a></li>
<li><a href="https://duet.so/blog/how-to-run-claude-code-in-the-cloud">Run Claude Code in the Cloud 24/7 (No Laptop Needed) | Duet Blog</a></li>
<li><a href="https://github.com/ksamaschke/claude-code-vm">GitHub - intelligentcode-ai/claude-code-vm: Deploy Claude Code and additional tools to a VM for remote development · GitHub</a></li>

</ul>
</details>

**标签**: `#使用Claude Code进行开发的程序员`, `#需要长时间运行或并行任务的开发者`, `#希望利用云资源提高效率的Claude订阅用户`

</section>

---

<section class="action-card" data-card-id="rss:feed.indiehackers.world_posts.rss?exclude=link-post:2652f896e30945e1" markdown="1">
<a id="item-5"></a>
## [AI 自动评估客户定价风险](https://feed.indiehackers.world/post/6b1fb42a0f)

**栏目分类**: `TUTORIAL`

**一句话简介**: 本文介绍如何通过 Zapier 和 OpenAI 自动分析客户使用量与收入数据，判断客户是否定价过低、有升级潜力、使用率低或存在流失风险。

**具体怎么做**:
- 1. 在Airtable中创建Users表，记录客户的使用量、收入等数据。
- 2. 在Zapier中创建Zap，触发器为Airtable中的新记录或更新记录。
- 3. 添加过滤器：仅当客户需要进一步审查时继续，例如定价风险字段显示“需要审查”或使用量每美元过高/过低。
- 4. 添加OpenAI/ChatGPT动作，发送客户的使用量和收入数据，要求AI将账户分类为定价过低、升级候选、低使用量或可能流失风险，并给出简短解释。
- 5. 添加Airtable更新记录动作，将AI的回复保存到AI推荐字段中。

**适合谁/适用场景**: `SaaS创业者`, `产品经理`, `需要评估客户定价策略的运营人员`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法依赖 Zapier 和 OpenAI API，需要一定的技术配置；AI 分类的准确性取决于输入数据的质量和提示词设计；实际效果未经验证。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://feed.indiehackers.world/post/6b1fb42a0f)

rss · Indie Hackers · 7月15日 14:55

**背景**: 许多 SaaS 公司难以根据使用量手动评估客户定价是否合理。Zapier 是一个无代码自动化平台，可连接各种应用；OpenAI 提供能分析文本数据的 AI 模型。该方法结合两者，自动化了一项常见的业务分析任务。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://mktbee.com/tools/zapier/pricing">Zapier Pricing Cost: Complete 2026 Guide | MKTBee</a></li>
<li><a href="https://openai.com/business/pricing/">Business Pricing | OpenAI</a></li>
<li><a href="https://zylo.com/blog/openai-api-pricing">OpenAI API Pricing: How to Control Costs Before They Escalate</a></li>

</ul>
</details>

**标签**: `#SaaS创业者`, `#产品经理`, `#需要评估客户定价策略的运营人员`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uxbgxc" markdown="1">
<a id="item-6"></a>
## [通过 API 为 AI 代理分配真实邮箱](https://www.reddit.com/r/PromptEngineering/comments/1uxbgxc/tool_giving_your_ai_agent_a_real_email_inbox_api/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 介绍一种使用 AgentMail API 为 AI 代理创建专用邮箱、发送邮件并通过 Webhook 接收回复的编程模式，实现线程追踪。

**具体怎么做**:
- 1. 使用AgentMail API为每个AI代理创建一个专用邮箱（POST /inboxes）。
- 2. 通过API发送外发邮件（POST /inboxes/{id}/send），获取返回的thread_id用于线程管理。
- 3. 配置Webhook接收回复，AgentMail会自动将回复关联到原线程。
- 4. 在AI代理之间传递thread_id，实现多代理间的连续对话。

**适合谁/适用场景**: `需要为AI代理配置邮件通信的开发者`, `构建多代理系统的工程师`, `希望实现邮件线程追踪的自动化场景`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 依赖第三方 API（AgentMail），需自行评估其稳定性和成本；示例代码为简化版，生产环境需完善错误处理。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uxbgxc/tool_giving_your_ai_agent_a_real_email_inbox_api/)

reddit · r/PromptEngineering · /u/AgentGuy1 · 7月15日 16:49

**背景**: 传统上，为 AI 代理提供邮件能力需要复杂的 IMAP 轮询或基于 OAuth 的 API（如 Gmail），这些并非为无头多代理系统设计。AgentMail 是一个 API 优先的邮件提供商，专为 AI 代理提供可编程的邮箱创建、原生线程追踪和 Webhook 支持。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.agentmail.to/">AgentMail | Email Inbox API for AI Agents</a></li>
<li><a href="https://www.ycombinator.com/companies/agentmail">AgentMail: Email Inboxes for AI Agents | Y Combinator</a></li>
<li><a href="https://docs.agentmail.to/inboxes">Inboxes | AgentMail | Documentation</a></li>

</ul>
</details>

**社区讨论**: 帖子作者邀请讨论多代理邮件工作流和路由层，但来源中未提供社区评论。

**标签**: `#需要为AI代理配置邮件通信的开发者`, `#构建多代理系统的工程师`, `#希望实现邮件线程追踪的自动化场景`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uwxjjv" markdown="1">
<a id="item-7"></a>
## [保留面部特征的 AI 商务肖像提示词](https://www.reddit.com/r/PromptEngineering/comments/1uwxjjv/image_preserved_prompt/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个提示词技巧，利用上传的照片生成保留面部特征的专业商务肖像，适用于个人网站或简历。

**具体怎么做**:
- 1. 上传一张自己的照片作为参考。
- 2. 使用以下提示词：'Use my uploaded photo as the reference. Preserve my facial features, hairstyle, skin tone, and overall identity. Create a realistic, professional business portrait suitable for a modern Data Analyst portfolio website. Remove the background completely and generate a transparent PNG. Show me from the waist up with a confident, approachable expression and a slight smile. Pose me at about a 15-degree angle toward the left, with my eyes looking slightly toward the viewer. Keep a relaxed posture with arms crossed or one hand in a pocket. Dress me in smart business casual clothing: a fitted navy blue shirt or charcoal blazer over a white shirt, with a clean, minimal look and no tie. Ensure the clothing looks premium and well-tailored. Use soft studio lighting.'
- 3. 在支持图像生成的AI工具中运行提示词（如DALL·E、Midjourney等）。

**适合谁/适用场景**: `需要专业头像但不想重新拍照的人`, `数据分析师或职场人士`, `制作个人作品集或简历`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 提示词效果依赖于 AI 工具的能力，可能无法完全保留面部特征；不同工具输出质量有差异。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uwxjjv/image_preserved_prompt/)

reddit · r/PromptEngineering · /u/QuirkyAd8831 · 7月15日 06:18

**背景**: 像 Stable Diffusion 和 Midjourney 这样的 AI 图像生成模型可以从文本提示词创建逼真的肖像，但常常改变面部特征。“图生图”技术使用上传的照片作为参考来保留身份，这对专业头像至关重要。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://zhuanlan.zhihu.com/p/1980899187408257984">AI生成证件照提示词大全（超全管够） - 知乎</a></li>
<li><a href="https://www.cnblogs.com/laoguanchaidao/p/19191311">如何使用 AI 制作专业证件照？（图生图超详细指南，附黄金提示词） - 哦扫地 - 博客园</a></li>

</ul>
</details>

**标签**: `#需要专业头像但不想重新拍照的人`, `#数据分析师或职场人士`, `#制作个人作品集或简历`

</section>

---

