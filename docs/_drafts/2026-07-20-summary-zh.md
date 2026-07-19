---
layout: default
title: "信先行 Action Cards: 2026-07-20 (ZH)"
date: 2026-07-20
lang: zh
---

> 从 18 条内容中筛选出 2 条教程/案例/技巧。

---

1. [先让 AI 列出失败清单再执行任务](#item-1) · PRODUCTIVITY_TIP · Score: 7.0 / 10
2. [将 Claude Fable 5 提示提炼为 500 令牌 Markdown 引擎](#item-2) · TUTORIAL · Score: 6.0 / 10

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1v0k0b2" markdown="1">
<a id="item-1"></a>
## [先让 AI 列出失败清单再执行任务](https://www.reddit.com/r/PromptEngineering/comments/1v0k0b2/ask_ai_for_the_failure_checklist_before_asking/)

**栏目分类**: `PRODUCTIVITY_TIP`

**一句话简介**: 在执行任务前，先让 AI 列出可能出错的方式，生成验收清单，再用该清单检查最终输出，提高结果可靠性。

**具体怎么做**:
- 1. 向AI提问：“完成这个任务时，有哪些方式会让答案看起来合理但实际错误？列出5种。”
- 2. 将AI列出的失败模式转化为验收检查项。
- 3. 让AI执行原任务。
- 4. 用验收清单逐项检查AI的输出，标记并修正问题。

**适合谁/适用场景**: `需要AI生成会议纪要、研究摘要、代码、电子表格公式等内容的用户`, `希望减少AI幻觉和错误输出的场景`, `对输出质量有较高要求的任务`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法不能完全消除 AI 错误，但能帮助系统化检查；效果取决于用户能否准确识别失败模式。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1v0k0b2/ask_ai_for_the_failure_checklist_before_asking/)

reddit · r/PromptEngineering · /u/Fearless-Figure-4638 · 7月19日 07:29

**背景**: 大型语言模型（LLM）经常生成听起来自信但包含事实错误的输出，这种现象称为幻觉。传统的确定性软件验收标准不适用于 AI，因为每次运行的输出都会变化。该技术借鉴了软件测试的思路，预先定义失败模式并将其用作检查清单。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://dev.to/novaelvaris/acceptance-criteria-for-ai-tasks-a-simple-template-that-cuts-rework-3995">Acceptance Criteria for AI Tasks: A Simple Template That Cuts ...</a></li>
<li><a href="https://www.institutepm.com/knowledge-hub/ai-acceptance-criteria">Writing Acceptance Criteria for AI Features: From Vague Ideas ...</a></li>
<li><a href="https://suprmind.ai/hub/insights/ai-hallucination-prevention-methods-the-complete-stack/">AI Hallucination Prevention Methods : The Complete Stack</a></li>

</ul>
</details>

**标签**: `#需要AI生成会议纪要、研究摘要、代码、电子表格公式等内容的用户`, `#希望减少AI幻觉和错误输出的场景`, `#对输出质量有较高要求的任务`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1v0j584" markdown="1">
<a id="item-2"></a>
## [将 Claude Fable 5 提示提炼为 500 令牌 Markdown 引擎](https://www.reddit.com/r/PromptEngineering/comments/1v0j584/i_distilled_the_leaked_claude_fable_5_system/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 将 Claude Fable 5 泄露的系统提示中的核心推理框架（自验证循环、严格格式规则、高自主性约束）提炼为适用于 ChatGPT 和 Gemini 的 500 令牌 Markdown 提示模板。

**具体怎么做**:
- 从原始12万字符的Claude Fable 5系统提示中提取核心哲学：自验证循环、严格格式规则、高自主性约束。
- 剥离约60%的Anthropic内部基础设施代码（如嵌套XML标签、自定义bash环境服务器端模式）。
- 将核心逻辑翻译为通用Markdown格式，控制总令牌数在500以内。
- 将模板应用于ChatGPT或Gemini，避免直接使用原始提示导致的性能下降和工具错误。

**适合谁/适用场景**: `提示工程师`, `需要高效系统提示的AI应用开发者`, `希望优化ChatGPT或Gemini性能的用户`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该模板基于泄露内容提炼，原始提示的完整性和准确性未经官方确认；实际效果可能因模型版本而异。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1v0j584/i_distilled_the_leaked_claude_fable_5_system/)

reddit · r/PromptEngineering · /u/Velocity_Off · 7月19日 06:39

**背景**: Claude Fable 5 是 Anthropic 的前沿 AI 模型，以其高级推理能力著称。系统提示是指导 AI 行为的指令；泄露的提示通常包含专有优化。自验证循环允许模型检查自身输出中的错误，而高自主性约束鼓励主动解决问题。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/asgeirtj/system_prompts_leaks">GitHub - asgeirtj/ system _ prompts _ leaks : Extracted system prompts ...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Claude_(language_model)">Claude (AI) - Wikipedia</a></li>
<li><a href="https://one2mind.com/loop-engineering-ai-can-we-trust-self-verifying-loops/">Loop Engineering AI : Can We Trust Self - Verifying Loops ? - 2mind</a></li>

</ul>
</details>

**标签**: `#提示工程师`, `#需要高效系统提示的AI应用开发者`, `#希望优化ChatGPT或Gemini性能的用户`

</section>

---