# 信先行实用卡片 - 2026-07-04

> 从 1 条内容中筛选出 1 条教程/案例/技巧。

---

1. [Claude Code 最佳实践：让 AI 自我验证工作成果](#item-1) · TUTORIAL · Score: 6.0 / 10

---

<section class="action-card" data-card-id="manual:url:9686dc1633cd25c6" markdown="1">
<a id="item-1"></a>
## [Claude Code 最佳实践：让 AI 自我验证工作成果](https://code.claude.com/docs/en/best-practices)

**栏目分类**: `TUTORIAL`

**一句话简介**: 介绍在 Claude Code 中通过多种方式让 AI 自动验证其工作成果，确保输出质量。

**具体怎么做**:
- 1. 在同一提示中要求 Claude 运行检查并迭代，直到通过。
- 2. 将会话中的检查条件设为 /goal 条件，每次交互后自动重新检查。
- 3. 使用 Stop hook 运行检查脚本，阻止交互结束直到检查通过（最多连续阻塞 8 次）。
- 4. 通过验证子代理或动态工作流，让另一个模型尝试反驳结果，实现交叉验证。

**适合谁/适用场景**: `使用 Claude Code 的开发者`, `需要确保 AI 输出准确性的场景`, `自动化代码审查和测试`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 这些方法需要一定的配置和脚本编写能力，且可能增加交互时间；连续阻塞机制可能影响效率。

**实用度评分**: Score: 6.0 / 10

**来源链接**: [原文](https://code.claude.com/docs/en/best-practices)

manual · Manual Add · 7月4日 08:05

**标签**: `#使用 Claude Code 的开发者`, `#需要确保 AI 输出准确性的场景`, `#自动化代码审查和测试`

</section>

---

