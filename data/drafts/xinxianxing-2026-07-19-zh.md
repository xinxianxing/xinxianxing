# 信先行实用卡片 - 2026-07-19

> 从 32 条内容中筛选出 4 条教程/案例/技巧。

---

1. [将 SOP 作为 AI 工作流的质量层](#item-1) · TUTORIAL · Score: 7.0 / 10
2. [用 Claude 生成高保真可交互原型](#item-2) · TUTORIAL · Score: 7.0 / 10
3. [Clarify CRIT：让 AI 在行动前先确认需求的开源技能](#item-3) · TOOL · Score: 6.0 / 10
4. [使用桌面版 Codex/Claude Code 的 Computer Use 功能自动化测试](#item-4) · PRODUCTIVITY_TIP · Score: 6.0 / 10

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uzex9y" markdown="1">
<a id="item-1"></a>
## [将 SOP 作为 AI 工作流的质量层](https://www.reddit.com/r/PromptEngineering/comments/1uzex9y/i_stopped_treating_sops_like_corporate_paperwork/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 本文介绍如何将标准操作程序（SOP）从传统的公司文档转变为 AI 工作流的质量控制层，使提示词设计更简单、工作流故障更易诊断、人工审核更明确。

**具体怎么做**:
- 定义期望的输出结果和所需的输入信息。
- 在自动化之前，先记录下完整的操作步骤。
- 标记出需要人工判断的关键节点。
- 明确什么是“完成”状态。
- 只对稳定的部分进行自动化。

**适合谁/适用场景**: `构建复杂AI工作流的提示工程师`, `希望提升AI输出质量的内容创作者`, `需要标准化AI流程的团队`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法基于作者个人经验，效果可能因工作流复杂度而异；SOP 需要根据具体场景调整，并非通用模板。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uzex9y/i_stopped_treating_sops_like_corporate_paperwork/)

reddit · r/PromptEngineering · /u/Admirable-Future-633 · 7月17日 22:57

**背景**: 标准操作程序（SOP）是定义如何一致执行任务的逐步说明。在 AI 工作流中，提示词告诉模型做什么，自动化在步骤间移动数据，但两者都没有定义完整、准确的结果是什么样的。将 SOP 作为质量层，通过在自动化之前记录结果、输入、人工判断点和完成标准来填补这一空白。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://aws.amazon.com/blogs/opensource/introducing-strands-agent-sops-natural-language-workflows-for-ai-agents/">Introducing Strands Agent SOPs – Natural Language Workflows for AI Agents | AWS Open Source Blog</a></li>
<li><a href="https://www.glean.com/perspectives/how-to-implement-an-ai-content-review-workflow">How to implement an AI content review workflow</a></li>
<li><a href="https://medium.com/@danielwilliamai/sops-ai-turn-any-task-into-a-repeatable-workflow-so-you-stop-starting-from-scratch-4789e2689615">SOPs + AI: Turn Any Task Into a Repeatable Workflow (So You Stop Starting From Scratch) | by Daniel William | Medium</a></li>

</ul>
</details>

**标签**: `#构建复杂AI工作流的提示工程师`, `#希望提升AI输出质量的内容创作者`, `#需要标准化AI流程的团队`

</section>

---

<section class="action-card" data-card-id="twitter:tweet:2078388657979838830" markdown="1">
<a id="item-2"></a>
## [用 Claude 生成高保真可交互原型](https://twitter.com/dotey/status/tweet-2078388657979838830)

**栏目分类**: `TUTORIAL`

**一句话简介**: 介绍如何利用 Claude 生成高保真可交互原型，替代传统产品文档，并让 AI 根据原型实现代码。

**具体怎么做**:
- 1. 提出功能需求，让 Claude（如 Opus 4.8）生成高保真原型稿。
- 2. 反复打磨原型，直到确认设计细节。
- 3. 将确认后的原型交给 AI，让 AI 根据原型实现最终代码。

**适合谁/适用场景**: `产品经理`, `设计师`, `开发者`, `需要快速迭代产品原型的团队`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法依赖 Claude 的生成能力，不同模型效果可能有差异；原型到代码的还原度受 AI 能力影响，原文称可还原 9 成以上，但未提供具体验证数据。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://twitter.com/dotey/status/tweet-2078388657979838830)

twitter · 宝玉 · 7月18日 07:57

**背景**: 高保真原型是接近最终产品的交互式模型，通常用 HTML/CSS/JS 构建。Claude Design 是 Claude 的一个功能，可根据文本描述生成此类原型。Opus 4.8 是 Anthropic 的最新模型，以强大的智能体能力和代码生成能力著称。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://claude.com/product/design">Claude Design | Turn Ideas into Design | Claude by Anthropic</a></li>
<li><a href="https://www.anthropic.com/news/claude-opus-4-8">Introducing Claude Opus 4.8 \ Anthropic</a></li>
<li><a href="https://github.com/alchaincyf/huashu-design">GitHub - alchaincyf/huashu-design: Huashu Design · HTML ...</a></li>

</ul>
</details>

**标签**: `#产品经理`, `#设计师`, `#开发者`, `#需要快速迭代产品原型的团队`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uzgnia" markdown="1">
<a id="item-3"></a>
## [Clarify CRIT：让 AI 在行动前先确认需求的开源技能](https://www.reddit.com/r/PromptEngineering/comments/1uzgnia/i_built_a_requestrefinement_skill_for_claudellms/)

**栏目分类**: `TOOL`

**一句话简介**: 一个开源技能，让 AI 在执行请求前先判断是否存在歧义，并只问最少问题来澄清，避免盲目执行。

**具体怎么做**:
- 从GitHub仓库下载SKILL.md文件及相关参考文档。
- 将文件放入支持SKILL.md格式的工具中（如Claude项目或自定义GPT）。
- 使用时，技能会自动分析请求，若理解则直接执行，若有歧义则提出最少问题。

**适合谁/适用场景**: `提示工程师`, `需要精确输出的AI用户`, `希望减少AI幻觉和错误的人`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 开源项目，需自行测试效果；依赖支持 SKILL.md 格式的工具；可能不适用于所有场景。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uzgnia/i_built_a_requestrefinement_skill_for_claudellms/)

reddit · r/PromptEngineering · /u/Historical_Policy533 · 7月18日 00:11

**背景**: SKILL.md 是 Anthropic 创建的开源标准，用于封装可复用的 AI 代理能力，已被包括 Claude Code 和 Cursor 在内的 27 多个代理支持。Clarify CRIT 技能利用该格式提供了一个轻量级、独立的请求精炼层，可添加到任何兼容的 AI 工作流中。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://trendshift.io/repositories/85889">lanveric/ clarify - crit — GitHub trending stats & insights | Trendshift</a></li>
<li><a href="https://www.mdskills.ai/specs/skill-md">SKILL.md: The Agent Skills Format | mdskills.ai</a></li>
<li><a href="https://bibek-poudel.medium.com/the-skill-md-pattern-how-to-write-ai-agent-skills-that-actually-work-72a3169dd7ee">The SKILL.md Pattern: How to Write AI Agent Skills That Actually Work | by Bibek Poudel | Medium</a></li>

</ul>
</details>

**标签**: `#提示工程师`, `#需要精确输出的AI用户`, `#希望减少AI幻觉和错误的人`

</section>

---

<section class="action-card" data-card-id="twitter:tweet:2078481595674112362" markdown="1">
<a id="item-4"></a>
## [使用桌面版 Codex/Claude Code 的 Computer Use 功能自动化测试](https://twitter.com/dotey/status/tweet-2078481595674112362)

**栏目分类**: `PRODUCTIVITY_TIP`

**一句话简介**: 建议使用 Codex 或 Claude Code 的桌面版，借助 Computer Use 功能在交付前自动测试并修复问题，提升效率。

**具体怎么做**:
- 使用 Codex 或 Claude Code 的桌面版（Desktop 版本）
- 在交付前主动调用 Computer Use 功能进行自动化测试
- 系统会自动检测问题并修复，无需人工干预

**适合谁/适用场景**: `开发者`, `测试人员`, `使用 AI 编程工具的团队`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 依赖特定工具版本和功能，可能不适用于所有项目或环境；实际效果因项目复杂度而异。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://twitter.com/dotey/status/tweet-2078481595674112362)

twitter · 宝玉 · 7月18日 14:06

**背景**: Codex 和 Claude Code 是 AI 编程助手，可以生成和编辑代码。Computer Use 是一项扩展功能，使它们能够像人类使用鼠标和键盘一样，以视觉方式与桌面应用程序交互。这使得 AI 能够对具有图形界面的软件进行端到端测试。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/OpenCodexLabs/open-codex-computer-use/">OpenCodexLabs/open-codex-computer-use - GitHub</a></li>
<li><a href="https://code.claude.com/docs/en/computer-use">Let Claude use your computer from the CLI - Claude Code Docs</a></li>
<li><a href="https://learn.chatgpt.com/docs/computer-use">Computer Use | ChatGPT Learn</a></li>

</ul>
</details>

**标签**: `#开发者`, `#测试人员`, `#使用 AI 编程工具的团队`

</section>

---

