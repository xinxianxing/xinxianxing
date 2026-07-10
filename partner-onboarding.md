---
layout: default
title: Partner Onboarding
---

# 信先行合作方开通 SOP

这份流程用于开通一个新的合作方频道。现阶段只做飞书群推送，不做账号系统、付费系统、后台看板或复杂权限管理。

## 标准流程

1. 合作方支付 500 元开通费，可通过微信或支付宝收款。
2. 合作方在飞书创建免费群和会员群，添加群机器人，把两个 webhook 地址发给你。
3. 本地创建频道配置：

```bash
uv run horizon-channel-add \
  --channel-id ai_tools_partner_001 \
  --name "信先行·AI工具日报" \
  --partner "某某合作方" \
  --category ai_tools \
  --template action_card \
  --schedule daily_8am \
  --max-items 10 \
  --min-score 7 \
  --active false \
  --sources hackernews,reddit_artificial,twitter \
  --signal-types TUTORIAL,PRODUCTIVITY_TIP,MONEY_CASE \
  --content-tags ai,tutorial
```

4. 把 webhook 地址填进 GitHub Actions Secrets。命名规则：

```text
CHANNEL_<CHANNEL_ID大写>_FREE_WEBHOOK
CHANNEL_<CHANNEL_ID大写>_PAID_WEBHOOK
```

例如 `ai_tools_partner_001` 对应：

```text
CHANNEL_AI_TOOLS_PARTNER_001_FREE_WEBHOOK
CHANNEL_AI_TOOLS_PARTNER_001_PAID_WEBHOOK
```

5. 本地或 GitHub Actions 环境里检查配置：

```bash
uv run horizon-channel-check --channel-id ai_tools_partner_001
```

确认没有缺失配置。没有配置的 webhook secret 会被明确列出来。

6. 发送测试消息：

```bash
uv run horizon-channel-test --channel-id ai_tools_partner_001
```

让合作方在飞书群里确认收到测试消息。

7. 启用频道：

```bash
uv run horizon-channel-enable --channel-id ai_tools_partner_001
```

启用前命令会自动检查必要配置。如果 webhook secret 缺失，会拒绝启用。

8. 告知合作方：频道启用后，第二天北京时间 08:00 开始正式推送。审核群会在 06:00 收到当天全部草稿内容，便于你提前查看。

## 收费和分成说明

- 500 元开通费不退，用于覆盖信息采集和系统成本。
- 每人进群费用 99 元/年，收入 5:5 分成。
- 开通费从第一个月收入里扣除后再分成。
- 合作方负责建群、拉人和日常运营。
- 你负责信息源配置、系统维护和自动推送。

## 日常操作

停用频道但保留配置：

```bash
uv run horizon-channel-disable --channel-id ai_tools_partner_001
```

手动测试频道：

```bash
uv run horizon-channel-test --channel-id ai_tools_partner_001
```

重新检查频道：

```bash
uv run horizon-channel-check --channel-id ai_tools_partner_001
```

## 注意事项

- 频道 JSON 只保存 GitHub Secret 名称，不保存真实 webhook 地址。
- 新频道默认 `active=false`，确认测试通过后再启用。
- `active=true` 的频道会参加 08:00 定时推送。
- `content_tags` 可以被多个合作方共享。同类内容只生成一次，然后分发到所有匹配的 active 频道。
- `HORIZON_ADMIN_WEBHOOK` 只用于系统告警，不推送正式内容。
