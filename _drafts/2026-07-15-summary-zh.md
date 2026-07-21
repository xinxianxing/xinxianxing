---
layout: default
title: "信先行 Action Cards: 2026-07-15 (ZH)"
date: 2026-07-15
lang: zh
---

> 从 30 条内容中筛选出 7 条教程/案例/技巧。

---

1. [LeanPrompts Studio：开源本地提示词 IDE](#item-1) · TOOL · Score: 7.0 / 10
2. [国家模拟器 AI 角色扮演提示词模板](#item-2) · TUTORIAL · Score: 7.0 / 10
3. [AI 电影制作前期准备指南发布](#item-3) · TUTORIAL · Score: 6.0 / 10
4. [AI 提示词模仿乔布斯极简风格](#item-4) · TUTORIAL · Score: 6.0 / 10
5. [将复杂提示词转化为可复用的 AI 技能](#item-5) · TUTORIAL · Score: 6.0 / 10
6. [双-sref 发现：同一参考图效果迥异](#item-6) · TUTORIAL · Score: 6.0 / 10
7. [BaoCut：Mac 上借助 Agent Skill 实现字幕转录、翻译与剪辑](#item-7) · TOOL · Score: 6.0 / 10

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uwlp6b" markdown="1">
<a id="item-1"></a>
## [LeanPrompts Studio：开源本地提示词 IDE](https://www.reddit.com/r/PromptEngineering/comments/1uwlp6b/i_got_tired_of_copypasting_prompts_and_losing/)

**栏目分类**: `TOOL`

**一句话简介**: 一款开源的本地浏览器扩展，为提示词工程提供类似 IDE 的工作空间，支持变量替换、一键插入和多模型切换。

**具体怎么做**:
- 安装LeanPrompts Studio浏览器扩展（开源免费，本地运行）。
- 在扩展界面中编写或导入提示词，使用{{变量名}}定义动态变量。
- 一键将提示词插入ChatGPT、Claude等AI工具的网页输入框。
- 自动保存提示词版本历史，可随时回退到之前的版本。

**适合谁/适用场景**: `提示词工程师`, `频繁使用多个AI模型的用户`, `需要管理大量提示词版本的用户`, `对数据隐私敏感的用户`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 工具为个人开发项目，可能存在未发现的 bug；功能依赖浏览器扩展权限，需自行评估安全性。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uwlp6b/i_got_tired_of_copypasting_prompts_and_losing/)

reddit · r/PromptEngineering · /u/UsefulAd1695 · 7月14日 21:21

**背景**: 提示词工程是设计和优化输入（提示词）以从大型语言模型（LLM）获得期望输出的过程。许多从业者在文本文件中管理提示词或在不同的 AI 聊天界面之间复制粘贴，导致效率低下和版本控制问题。类似 IDE 的环境可以集中管理、测试和版本控制提示词。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://chromewebstore.google.com/detail/leanprompts-studio-ai-pro/pbdbopolbilaemiphldmecmlppedajnd">LeanPrompts Studio - AI Prompt IDE - Chrome Web Store</a></li>
<li><a href="https://addons.opera.com/en/extensions/details/leanprompts-studio/">LeanPrompts Studio extension - Opera add-ons</a></li>

</ul>
</details>

**标签**: `#提示词工程师`, `#频繁使用多个AI模型的用户`, `#需要管理大量提示词版本的用户`, `#对数据隐私敏感的用户`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uwavg6" markdown="1">
<a id="item-2"></a>
## [国家模拟器 AI 角色扮演提示词模板](https://www.reddit.com/r/PromptEngineering/comments/1uwavg6/nation_simulator_prompt/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个用于 AI 角色扮演的详细国家模拟器提示词模板，包含初始设置和回合结构。

**具体怎么做**:
- 1. 向AI一次性提出三个问题：起始年份（公元前3000年至公元3000年）、选择真实或自定义国家、填写国家模板（名称与地区、人口、经济数据、政府与领导人、关键派系、军事、核心理想与宗教）。
- 2. 使用回合结构：AI输出上一决策的影响摘要、当前统计数据（GDP、国库、债务、通胀、军事排名等）、派系支持率、国际关系、世界快照（2-3个国际事件）、关键问题（4-6个按紧迫性排序，每个问题附带三个派系立场）。
- 3. 玩家根据这些信息做出决策，AI继续生成下一回合。

**适合谁/适用场景**: `AI角色扮演爱好者`, `游戏设计师`, `喜欢模拟策略类游戏的玩家`, `想测试AI叙事能力的提示工程师`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该提示词经过作者多次测试，但效果取决于 AI 模型的能力和一致性；不同模型可能表现差异较大。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uwavg6/nation_simulator_prompt/)

reddit · r/PromptEngineering · /u/Silly-Somewhere-7775 · 7月14日 14:50

**背景**: 国家模拟器是一种角色扮演类型，玩家管理国家的经济、政治和军事。该提示词模板构建了与 AI 的交互，以模拟现实的治理挑战，包括派系压力和不完美信息。

**标签**: `#AI角色扮演爱好者`, `#游戏设计师`, `#喜欢模拟策略类游戏的玩家`, `#想测试AI叙事能力的提示工程师`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uwjnup" markdown="1">
<a id="item-3"></a>
## [AI 电影制作前期准备指南发布](https://www.reddit.com/r/PromptEngineering/comments/1uwjnup/preparation_before_generation/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一本关于 AI 电影制作前期规划的工作流程指南，以具体故事为例展示如何将创意转化为结构化电影项目。

**具体怎么做**:
- 原文未提供详细步骤，但书中以安布罗斯·比尔斯的小说《枭河桥事件》为例，展示了从创意到成片的完整规划流程，并附有每个环节的提示词。

**适合谁/适用场景**: `电影制作人`, `创作者`, `作家`, `AI艺术家`, `希望系统化AI电影制作流程的人`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该书为付费资源（亚马逊），具体效果取决于读者是否遵循其方法；提示词可能需根据具体项目调整。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uwjnup/preparation_before_generation/)

reddit · r/PromptEngineering · /u/Winter-Routine7909 · 7月14日 20:04

**背景**: AI 电影制作涉及使用文本到视频模型等生成式 AI 工具来创作电影内容。前期制作包括故事板、剧本分解和镜头规划，但常被忽视，人们更倾向于直接生成，导致结果不一致。

**标签**: `#电影制作人`, `#创作者`, `#作家`, `#AI艺术家`, `#希望系统化AI电影制作流程的人`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uwgyry" markdown="1">
<a id="item-4"></a>
## [AI 提示词模仿乔布斯极简风格](https://www.reddit.com/r/PromptEngineering/comments/1uwgyry/ai_prompt_to_write_steve_jobsstyle_product/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个让 AI 模仿史蒂夫·乔布斯极简主义演讲风格的提示词，用于将复杂技术规格转化为情感共鸣的产品叙事。

**具体怎么做**:
- 1. 将提供的系统提示词（System Prompt）复制到ChatGPT、Claude等AI对话工具中。
- 2. 在提示词后输入你的产品名称、核心功能和技术参数。
- 3. AI会以乔布斯的口吻输出一段简洁、富有感染力、强调产品“灵魂”而非功能列表的描述。
- 4. 可根据需要调整输出长度或语气。

**适合谁/适用场景**: `产品经理`, `营销文案写手`, `创业者`, `需要撰写高端、极简风格产品描述的场景`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 提示词效果取决于 AI 模型的能力和输入的产品信息质量；乔布斯风格可能不适用于所有产品类型或品牌调性。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uwgyry/ai_prompt_to_write_steve_jobsstyle_product/)

reddit · r/PromptEngineering · /u/EQ4C · 7月14日 18:25

**背景**: 提示工程是为 GPT-4 等 AI 模型设计和优化输入指令以产生所需输出的实践。该提示词采用基于角色的方法，指示 AI 体现史蒂夫·乔布斯的沟通风格，这种风格以简洁、坚定和关注人类体验而闻名。“现实扭曲力场”是一个与乔布斯说服他人接受其愿景的能力相关的术语。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.woshipm.com/ai/5968988.html">产品经理必须懂得AI：prompts提示工程之五大经典框架 | 人人都是产品经理</a></li>
<li><a href="https://www.runoob.com/ai-agent/prompt-engineering.html">提示词工程（Prompt Engineering） | 菜鸟教程</a></li>
<li><a href="https://zhuanlan.zhihu.com/p/11470727191">Prompt提示工程从零到一：构建高质量AI提示词技巧与实战 - 知乎</a></li>

</ul>
</details>

**标签**: `#产品经理`, `#营销文案写手`, `#创业者`, `#需要撰写高端、极简风格产品描述的场景`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uwfh22" markdown="1">
<a id="item-5"></a>
## [将复杂提示词转化为可复用的 AI 技能](https://www.reddit.com/r/PromptEngineering/comments/1uwfh22/do_you_build_your_own_ai_skills_when_prompts/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 介绍如何将复杂、重复的提示词转化为可复用的 AI 技能，以提高输出质量和一致性。

**具体怎么做**:
- 识别哪些提示词会产生不一致的结果
- 将任务拆解为清晰的步骤、规则和输出格式
- 添加常见错误和边缘情况的检查
- 用不同输入测试并优化指令
- 包含实用输出而非仅推荐

**适合谁/适用场景**: `提示词工程师`, `AI工具使用者`, `需要重复执行复杂AI任务的人`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法基于个人经验，效果可能因任务复杂度而异；需要一定提示词工程基础。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uwfh22/do_you_build_your_own_ai_skills_when_prompts/)

reddit · r/PromptEngineering · /u/HiroPL4Y · 7月14日 17:34

**背景**: 提示词工程通常涉及为 AI 模型编写详细的指令。然而，复杂任务可能需要多个步骤和验证来确保可靠的结果。可复用的技能将这些步骤封装成模块化组件。

**社区讨论**: 该帖子邀请其他人分享他们自己的高级技能，表明社区对可复用提示词组件的开发感兴趣。

**标签**: `#提示词工程师`, `#AI工具使用者`, `#需要重复执行复杂AI任务的人`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uwdlhu" markdown="1">
<a id="item-6"></a>
## [双-sref 发现：同一参考图效果迥异](https://www.reddit.com/r/PromptEngineering/comments/1uwdlhu/the_reference_image_did_two_completely_different/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 介绍了一个关于 Midjourney 中参考图像（--sref）的发现：同一张图片作为普通图像提示与作为第二层--sref 值结合样式代码使用时，结果完全不同。

**具体怎么做**:
- 将参考图像作为普通图像提示（plain image prompt）使用时，成功率约12%，且出现接触漂移问题。
- 将同一参考图像作为第二层--sref值，并搭配一个数字样式代码（numeric style code）使用时，可以干净地传递风格，16/16的手势和15/16的构图保持，无构图污染。

**适合谁/适用场景**: `Midjourney用户`, `提示工程师`, `需要精确控制图像风格和构图的创作者`

**效果或数据**: 作为普通图像提示时成功率约 12%，作为第二层--sref 值时手势传递 16/16，构图传递 15/16。

**可信度/风险提示**: 该发现基于单个案例，结果可能因图像和样式代码不同而变化；需要进一步测试验证。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uwdlhu/the_reference_image_did_two_completely_different/)

reddit · r/PromptEngineering · /u/jeffbradshaw · 7月14日 16:27

**背景**: Midjourney 的--sref 参数允许用户提供参考图像来影响风格。通常，将图像作为普通提示会导致构图崩溃。双-sref 技术叠加两个--sref 值：一个数字样式代码和一个图像参考，从而实现更好的传递。

**标签**: `#Midjourney用户`, `#提示工程师`, `#需要精确控制图像风格和构图的创作者`

</section>

---

<section class="action-card" data-card-id="twitter:tweet:2077074912435433901" markdown="1">
<a id="item-7"></a>
## [BaoCut：Mac 上借助 Agent Skill 实现字幕转录、翻译与剪辑](https://twitter.com/dotey/status/tweet-2077074912435433901)

**栏目分类**: `TOOL`

**一句话简介**: BaoCut 是一个 Mac 应用，通过 Agent Skill 让 AI 助手（如 Codex、Claude Code）直接转录视频、识别说话人、润色字幕、翻译并剪辑，并提供 GUI 进行二次编辑。

**具体怎么做**:
- 1. 在 Mac 上下载并安装 BaoCut App。
- 2. 从 App 内安装对应的 Skill，或从提供的 Skill 地址安装。
- 3. 在支持 Agent Skill 的终端（如 Codex、Claude Code）中，使用命令 /baocut 转录并翻译视频：<视频 url 或路径> 触发任务。
- 4. Agent 会调用 cli 进行转录、说话人识别、润色、翻译，并实时同步进度到 GUI。
- 5. 完成后可在 GUI 中预览和人工编辑字幕。

**适合谁/适用场景**: `Mac 用户`, `需要快速转录和翻译视频字幕的内容创作者`, `希望用 AI 辅助视频剪辑的用户`, `使用 Codex 或 Claude Code 等 Agent 工具的开发者`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 仅支持 Mac；翻译速度较慢但质量不错；需要安装 App 和 Skill，依赖 Agent 环境。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://twitter.com/dotey/status/tweet-2077074912435433901)

twitter · 宝玉 · 7月14日 16:57

**背景**: Agent Skill 是一种机制，允许 Codex CLI 和 Claude Code 等 AI 编码助手通过命令行界面调用外部工具或脚本。BaoCut 利用这一点，公开了一个 CLI，代理可以用它来处理视频文件，从而可以直接从代理的聊天界面自动化字幕工作流程。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://grokipedia.com/page/Gemini_CLI_Codex_CLI_and_Claude_Code">Gemini CLI, Codex CLI, and Claude Code</a></li>

</ul>
</details>

**标签**: `#Mac 用户`, `#需要快速转录和翻译视频字幕的内容创作者`, `#希望用 AI 辅助视频剪辑的用户`, `#使用 Codex 或 Claude Code 等 Agent 工具的开发者`

</section>

---