# 信先行实用卡片 - 2026-07-18

> 从 35 条内容中筛选出 5 条教程/案例/技巧。

---

1. [六步提示词框架：一次获得高质量 AI 输出](#item-1) · TUTORIAL · Score: 7.0 / 10
2. [无代笔模式：保持 AI 面试练习的自然表达](#item-2) · TUTORIAL · Score: 7.0 / 10
3. [长文本生成中用外部时钟检查一致性](#item-3) · TUTORIAL · Score: 6.0 / 10
4. [LLM 评判技巧：先找问题再打分](#item-4) · PRODUCTIVITY_TIP · Score: 6.0 / 10
5. [Qwen3 ASR 与开源工具解决 Whisper 字幕痛点](#item-5) · TUTORIAL · Score: 6.0 / 10

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uzba2v" markdown="1">
<a id="item-1"></a>
## [六步提示词框架：一次获得高质量 AI 输出](https://www.reddit.com/r/PromptEngineering/comments/1uzba2v/i_kept_getting_mediocre_ai_outputs_until_i/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一位用户分享了自己总结的提示词标准化框架，包含六个关键步骤，帮助减少反复调整，一次获得满意输出。

**具体怎么做**:
- 1. 角色/上下文放在最前面：以“你是[具体角色]，帮助[具体用户类型]”开头，例如“你是一位资深品牌设计师，为一位没有设计背景的精品咖啡店老板评审初稿Logo”。
- 2. 明确输出要求：指定输出格式、长度、风格等（原文未提供详细步骤）。
- 3. 提供示例或参考：给出一个理想输出的例子。
- 4. 设定约束条件：说明避免什么、必须包含什么。
- 5. 分步骤引导：将复杂任务拆解为多个子步骤。
- 6. 迭代反馈：在输出后给出具体修改方向。

**适合谁/适用场景**: `日常使用AI工具的用户`, `需要稳定高质量输出的内容创作者`, `希望减少提示词调试时间的从业者`

**效果或数据**: 未提供具体数据，但作者表示使用该框架后通常一次尝试即可获得满意结果。

**可信度/风险提示**: 框架基于个人经验，效果可能因模型和任务类型而异；部分步骤原文未详细展开。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uzba2v/i_kept_getting_mediocre_ai_outputs_until_i/)

reddit · r/PromptEngineering · /u/lit_llamaa · 7月17日 20:30

**背景**: 提示词工程是设计输入以引导大型语言模型（LLM）产生期望输出的实践。许多用户因提示词模糊而得到平庸结果，需要反复调整。该框架通过分解成功提示词的共同点，旨在标准化有效的提示方法。

**标签**: `#日常使用AI工具的用户`, `#需要稳定高质量输出的内容创作者`, `#希望减少提示词调试时间的从业者`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uyrs6q" markdown="1">
<a id="item-2"></a>
## [无代笔模式：保持 AI 面试练习的自然表达](https://www.reddit.com/r/PromptEngineering/comments/1uyrs6q/how_do_you_stop_prompts_from_turning_into/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一个防止 AI 在面试练习中过度润色回答、保持自然表达风格的提示词技巧。

**具体怎么做**:
- 在提示词中明确要求AI扮演“面试练习评审者”而非“写作者”，禁止重写完整答案或使其比自然说话风格更精致。
- 要求AI只做三件事：问一个面试官可能追问的问题、指出回答中最薄弱的部分、告知缺少的细节。
- 使用类似“不要重写我的完整答案或使其比自然说话风格更精致”的约束语句。

**适合谁/适用场景**: `准备面试的求职者`, `需要练习真实表达的人`, `使用AI进行模拟面试的用户`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该技巧基于个人经验，效果可能因模型和具体场景而异；需要根据实际反馈调整提示词。

**实用度评分**: Score: 7.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uyrs6q/how_do_you_stop_prompts_from_turning_into/)

reddit · r/PromptEngineering · /u/Fragrant_Spirit2953 · 7月17日 06:33

**背景**: AI 面试练习工具常常生成过度润色的回答，口头表达时显得不自然。“无代笔模式”提示词约束模型专注于反馈和清晰度而非华丽辞藻，解决了用户希望保持真实声音的常见困扰。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://aitoolsclub.com/5-claude-ai-prompt-tricks-and-commands-that-make-it-10x-more-powerful/">5 Claude AI Prompt Tricks and Commands That Make It 10x More ...</a></li>
<li><a href="https://sureprompts.com/blog/ai-prompts-for-job-interviews">30 AI Prompts for Job Interviews: Prep, Practice, and Follow-Up (2026) | SurePrompts</a></li>

</ul>
</details>

**社区讨论**: 原帖作者指出，如果会话时间较长，模型仍会偏向“更好听”的回答，需要定期提醒。来源中未提供其他评论。

**标签**: `#准备面试的求职者`, `#需要练习真实表达的人`, `#使用AI进行模拟面试的用户`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uz4rzx" markdown="1">
<a id="item-3"></a>
## [长文本生成中用外部时钟检查一致性](https://www.reddit.com/r/PromptEngineering/comments/1uz4rzx/a_season_is_cyclic_so_you_cannot_check_it_against/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 一种避免长文本生成（如多章节小说、长代理对话）中前后矛盾的技术：对季节等循环变量，不依赖模型自身检查，而是对照外部时钟（如固定时间戳）来验证一致性。

**具体怎么做**:
- 识别长文本中需要保持一致的循环变量（如季节、时间、角色状态）。
- 不将整个历史文本回传给模型检查（成本高且注意力分散），而是为每个循环变量维护一个外部时钟或计数器。
- 在生成新内容时，将当前时钟值与历史记录中的值进行简单比较，若发现矛盾则修正或重新生成。
- 例如：为季节分配数字（1=春，2=夏，3=秋，4=冬），每经过一天增加0.01，生成时检查当前值是否与之前一致。

**适合谁/适用场景**: `长文本生成（小说、剧本、报告）`, `多步骤代理对话`, `需要长期一致性的AI应用开发者`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该方法需要额外设计外部时钟机制，可能增加实现复杂度；对于非循环变量（如角色性格）不适用。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uz4rzx/a_season_is_cyclic_so_you_cannot_check_it_against/)

reddit · r/PromptEngineering · /u/Beginning_Support_86 · 7月17日 16:34

**背景**: 长文本生成经常出现模型遗忘或矛盾早期细节的问题，尤其是在多章节小说或长代理对话中。传统方法重新读取整个上下文，token 成本高且准确性低，因为模型的注意力被稀释。所提出的技术使用结构化事实存储和外部时钟来高效检测不一致性。

**标签**: `#长文本生成（小说、剧本、报告）`, `#多步骤代理对话`, `#需要长期一致性的AI应用开发者`

</section>

---

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_1uz084z" markdown="1">
<a id="item-4"></a>
## [LLM 评判技巧：先找问题再打分](https://www.reddit.com/r/PromptEngineering/comments/1uz084z/try_this_on_your_llm_judge_ask_for_the_problems/)

**栏目分类**: `PRODUCTIVITY_TIP`

**一句话简介**: 一种提示词技巧：让 LLM 评判时先列出错误和未支持的声明，再打分，从而获得更准确的评分。

**具体怎么做**:
- 1. 准备一个已有的评判提示词，例如“给这个答案打分1-5并给出简短理由”。
- 2. 对一个听起来不错但有错误的答案运行该提示词，通常会得到高分（如4分）。
- 3. 修改提示词顺序：先要求“列出任何事实错误或未支持的声明”，然后“仅对剩余部分打分”。
- 4. 再次运行，分数通常会降低。

**适合谁/适用场景**: `需要评估LLM输出质量的人`, `提示词工程师`, `希望提高评判准确性的用户`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 该技巧基于个人经验，效果可能因模型和任务而异；需要自行测试验证。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/1uz084z/try_this_on_your_llm_judge_ask_for_the_problems/)

reddit · r/PromptEngineering · /u/Future_AGI · 7月17日 13:46

**背景**: LLM 作为评判者是一种常见的评估方法，即用一个语言模型根据评分标准对其他模型的输出进行打分。然而，这些评判者常常表现出偏见，例如偏好流畅或冗长的回答而非事实准确性。提示词工程技术，如思维链和明确的标准排序，可以减轻这些偏见。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://futureagi.com/blog/llm-judge-prompt-engineering-guide-2026/">LLM-Judge Prompt Engineering: The 2026 Engineering Guide</a></li>
<li><a href="https://mbrenndoerfer.com/writing/evaluation-prompt-engineering">Evaluation Prompt Engineering: Designing Reliable LLM Judges</a></li>
<li><a href="https://www.confident-ai.com/blog/llm-evaluation-metrics-everything-you-need-for-llm-evaluation">LLM Evaluation Metrics: The Ultimate LLM Evaluation Guide - Confident AI</a></li>

</ul>
</details>

**标签**: `#需要评估LLM输出质量的人`, `#提示词工程师`, `#希望提高评判准确性的用户`

</section>

---

<section class="action-card" data-card-id="twitter:tweet:2078003883855524314" markdown="1">
<a id="item-5"></a>
## [Qwen3 ASR 与开源工具解决 Whisper 字幕痛点](https://twitter.com/dotey/status/tweet-2078003883855524314)

**栏目分类**: `TUTORIAL`

**一句话简介**: 介绍如何用 Qwen3 ASR 配合开源工具解决 Whisper 在字幕翻译中的时间戳不准、中英文混排差、不支持发言人识别等问题。

**具体怎么做**:
- 使用 Qwen3 ASR 模型（0.6b 即可）进行语音转文字，配合 Qwen3-ForcedAligner 模型获取精准的词级时间戳。
- 对于发言人识别，使用 Pyannote + WeSpeaker 开源模型；若多人同时说话识别不准，可结合 Agent 上下文提升准确度。
- 若预算允许，可选用火山引擎豆包录音文件识别模型 2.0 等云端服务，质量高、速度快但需付费。

**适合谁/适用场景**: `字幕翻译者`, `视频创作者`, `需要语音转文字并校对时间戳的用户`, `需要识别发言人的会议记录场景`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 开源模型在多人同时说话时识别准确度有限；云端服务需额外付费；Qwen3 ASR 和 ForcedAligner 的具体配置步骤原文未提供。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://twitter.com/dotey/status/tweet-2078003883855524314)

twitter · 宝玉 · 7月17日 06:28

**背景**: Whisper 是流行的开源 ASR 模型，但存在时间戳精度和混排转录问题。Qwen3-ASR 由阿里巴巴 Qwen 团队于 2026 年 1 月发布，是支持 52 种语言的新开源 ASR 系列。Qwen3-ForcedAligner 等强制对齐模型能将文本与音频在词级别对齐，改善字幕同步。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/QwenLM/Qwen3-ASR">GitHub - QwenLM/Qwen3-ASR: Qwen3-ASR is an open-source series of ASR ...</a></li>
<li><a href="https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B">Qwen/Qwen3-ForcedAligner-0.6B · Hugging Face</a></li>
<li><a href="https://huggingface.co/pyannote/wespeaker-voxceleb-resnet34-LM">pyannote/wespeaker-voxceleb-resnet34-LM · Hugging Face</a></li>

</ul>
</details>

**标签**: `#字幕翻译者`, `#视频创作者`, `#需要语音转文字并校对时间戳的用户`, `#需要识别发言人的会议记录场景`

</section>

---

