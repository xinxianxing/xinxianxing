"""File-backed channel registry utilities."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Mapping

from pydantic import ValidationError

from ..models import ChannelConfig, ChannelFileConfig


CHANNELS_DIR = Path("config/channels")
SUPPORTED_TEMPLATE_TYPES = {"action_card"}
SUPPORTED_SCHEDULES = {"daily_8am"}
LEGACY_SECRET_ALIASES: dict[str, tuple[str, ...]] = {
    "CHANNEL_REVIEW_FREE_WEBHOOK": ("CHANNEL_REVIEW_WEBHOOK",),
    "CHANNEL_AI_TOOLS_FREE_WEBHOOK": ("XINXIANXING_WEBHOOK_URL",),
    "CHANNEL_AI_TOOLS_PAID_WEBHOOK": ("XINXIANXING_PAID_FEISHU_URL",),
    "CHANNEL_AI_TUTORIALS_FREE_WEBHOOK": ("XINXIANXING_TUTORIAL_FEISHU_URL",),
    "CHANNEL_AI_MONETIZATION_FREE_WEBHOOK": (
        "XINXIANXING_AI_MONETIZATION_FEISHU_URL",
        "XINXIANXING_MONEY_CASE_FEISHU_URL",
    ),
    "CHANNEL_PRODUCTIVITY_TIPS_FREE_WEBHOOK": (
        "XINXIANXING_PRODUCTIVITY_TIP_FEISHU_URL",
    ),
}


@dataclass(frozen=True)
class ChannelDestination:
    """One concrete webhook destination for a logical channel."""

    destination_type: str
    secret_name: str
    webhook_url: str | None


@dataclass
class ChannelCheckResult:
    """Validation result for one file-backed channel."""

    channel: ChannelFileConfig | None
    path: Path | None
    status: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    missing_secrets: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    @property
    def can_enable(self) -> bool:
        return self.ok and not self.missing_secrets


def normalize_channel_id(channel_id: str) -> str:
    """Normalize channel ids for filenames and secret suffixes."""
    value = re.sub(r"[^a-zA-Z0-9]+", "_", channel_id.strip()).strip("_")
    return value.lower()


def secret_suffix(channel_id: str) -> str:
    """Return CHANNEL_<suffix>_... compatible suffix from a channel id."""
    return re.sub(r"[^A-Za-z0-9]+", "_", channel_id.upper()).strip("_")


def default_free_secret_name(channel_id: str) -> str:
    return f"CHANNEL_{secret_suffix(channel_id)}_FREE_WEBHOOK"


def default_paid_secret_name(channel_id: str) -> str:
    return f"CHANNEL_{secret_suffix(channel_id)}_PAID_WEBHOOK"


def channel_path(channel_id: str, channels_dir: Path = CHANNELS_DIR) -> Path:
    """Return the expected JSON path for a channel id."""
    return channels_dir / f"{normalize_channel_id(channel_id)}.json"


def load_channel_file(path: Path) -> ChannelFileConfig:
    """Load and validate one channel JSON file."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc
    try:
        return ChannelFileConfig.model_validate(raw)
    except ValidationError as exc:
        raise ValueError(f"Invalid channel config in {path}: {exc}") from exc


def list_channel_files(channels_dir: Path = CHANNELS_DIR) -> list[Path]:
    """Return all channel JSON files in stable order."""
    if not channels_dir.exists():
        return []
    return sorted(path for path in channels_dir.glob("*.json") if path.is_file())


def load_channel_file_configs(
    channels_dir: Path = CHANNELS_DIR,
) -> list[ChannelFileConfig]:
    """Load all file-backed channel configs."""
    return [load_channel_file(path) for path in list_channel_files(channels_dir)]


def write_channel_file(
    channel: ChannelFileConfig,
    channels_dir: Path = CHANNELS_DIR,
) -> Path:
    """Write one channel config to config/channels/<channel_id>.json."""
    channels_dir.mkdir(parents=True, exist_ok=True)
    path = channel_path(channel.channel_id, channels_dir)
    path.write_text(
        json.dumps(channel.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def resolve_secret_value(secret_name: str, env: Mapping[str, str]) -> str | None:
    """Return a secret value, accepting legacy self-operated secret aliases."""
    for candidate in (secret_name, *LEGACY_SECRET_ALIASES.get(secret_name, ())):
        value = env.get(candidate)
        if value:
            return value
    return None


def channel_destinations(
    channel: ChannelFileConfig,
    env: Mapping[str, str] | None = None,
) -> list[ChannelDestination]:
    """Return concrete webhook destinations for one logical channel."""
    env = env if env is not None else os.environ
    destinations: list[ChannelDestination] = []
    for destination_type, secret_name in (
        ("free", channel.free_webhook_secret_name),
        ("paid", channel.paid_webhook_secret_name),
    ):
        secret = secret_name.strip()
        if not secret:
            continue
        destinations.append(
            ChannelDestination(
                destination_type=destination_type,
                secret_name=secret,
                webhook_url=resolve_secret_value(secret, env) or f"${{{secret}}}",
            )
        )
    return destinations


def runtime_channels_from_file_config(
    channel: ChannelFileConfig,
    env: Mapping[str, str] | None = None,
) -> list[ChannelConfig]:
    """Expand one logical channel into concrete runtime webhook channels."""
    runtime: list[ChannelConfig] = []
    for destination in channel_destinations(channel, env=env):
        runtime_id = (
            channel.channel_id
            if destination.destination_type == "free"
            else f"{channel.channel_id}_{destination.destination_type}"
        )
        runtime_name = (
            channel.channel_name
            if destination.destination_type == "free"
            else f"{channel.channel_name}·会员"
        )
        runtime.append(
            ChannelConfig(
                id=runtime_id,
                name=runtime_name,
                webhook_url=destination.webhook_url,
                logical_channel_id=channel.channel_id,
                destination_type=destination.destination_type,
                description=channel.description,
                partner_name=channel.partner_name,
                category=channel.category,
                template_type=channel.template_type,
                schedule=channel.schedule,
                max_items_per_push=channel.max_items_per_push,
                dedupe_enabled=channel.dedupe_enabled,
                admin_webhook_secret_name=channel.admin_webhook_secret_name,
                content_tags=list(channel.content_tags),
                sources=list(channel.sources),
                signal_types=list(channel.signal_types),
                min_score=channel.min_score,
                active=channel.active,
            )
        )
    return runtime


def load_runtime_channels(
    *,
    channels_dir: Path = CHANNELS_DIR,
    fallback_channels: Iterable[ChannelConfig] | None = None,
    env: Mapping[str, str] | None = None,
) -> list[ChannelConfig]:
    """Load runtime channels from config/channels, falling back to data config."""
    files = list_channel_files(channels_dir)
    if not files:
        return list(fallback_channels or [])

    channels: list[ChannelConfig] = []
    for file_config in (load_channel_file(path) for path in files):
        channels.extend(runtime_channels_from_file_config(file_config, env=env))
    return channels


def find_channel_file(
    channel_id: str,
    channels_dir: Path = CHANNELS_DIR,
) -> tuple[Path | None, ChannelFileConfig | None]:
    """Find one logical channel by id."""
    target = normalize_channel_id(channel_id)
    for path in list_channel_files(channels_dir):
        channel = load_channel_file(path)
        if normalize_channel_id(channel.channel_id) == target:
            return path, channel
    return None, None


def duplicate_channel_ids(channels_dir: Path = CHANNELS_DIR) -> set[str]:
    """Return duplicate logical channel ids in the registry."""
    seen: set[str] = set()
    duplicates: set[str] = set()
    for path in list_channel_files(channels_dir):
        channel = load_channel_file(path)
        normalized = normalize_channel_id(channel.channel_id)
        if normalized in seen:
            duplicates.add(channel.channel_id)
        seen.add(normalized)
    return duplicates


def check_channel(
    channel_id: str,
    *,
    channels_dir: Path = CHANNELS_DIR,
    env: Mapping[str, str] | None = None,
    for_enable: bool = False,
) -> ChannelCheckResult:
    """Validate one channel config and list missing secrets."""
    env = env if env is not None else os.environ
    try:
        path, channel = find_channel_file(channel_id, channels_dir)
    except ValueError as exc:
        return ChannelCheckResult(
            channel=None,
            path=None,
            status="配置错误",
            errors=[str(exc)],
        )

    if channel is None or path is None:
        return ChannelCheckResult(
            channel=None,
            path=None,
            status="不存在",
            errors=[f"配置文件不存在：{channel_path(channel_id, channels_dir)}"],
        )

    result = ChannelCheckResult(
        channel=channel,
        path=path,
        status="已启用" if channel.active else "未启用",
    )

    allow_open_routing = channel.category == "review"

    if channel.channel_id in duplicate_channel_ids(channels_dir):
        result.errors.append(f"channel_id 重复：{channel.channel_id}")
    if not channel.sources and not allow_open_routing:
        result.warnings.append("sources 为空")
    if not channel.template_type:
        result.errors.append("template_type 为空")
    elif channel.template_type not in SUPPORTED_TEMPLATE_TYPES:
        result.errors.append(f"template_type 不支持：{channel.template_type}")
    if channel.schedule not in SUPPORTED_SCHEDULES:
        result.errors.append(f"schedule 不支持：{channel.schedule}")
    if channel.max_items_per_push <= 0:
        result.errors.append("max_items_per_push 必须大于 0")
    if not channel.admin_webhook_secret_name:
        result.warnings.append("admin_webhook_secret_name 为空")

    webhook_secrets = [
        channel.free_webhook_secret_name,
        channel.paid_webhook_secret_name,
    ]
    for secret_name in webhook_secrets:
        secret = secret_name.strip()
        if not secret:
            result.missing_secrets.append("<empty webhook secret name>")
        elif not resolve_secret_value(secret, env):
            result.missing_secrets.append(secret)

    require_active_ready = channel.active or for_enable
    if require_active_ready:
        if not channel.sources and not allow_open_routing:
            result.errors.append("active=true 时 sources 不能为空")
        if not channel.signal_types and not allow_open_routing:
            result.errors.append("active=true 时 signal_types 不能为空")
        if not channel.free_webhook_secret_name and not channel.paid_webhook_secret_name:
            result.errors.append("active=true 时至少需要一个 webhook secret")

    return result


def required_secret_names(channels: Iterable[ChannelFileConfig]) -> list[str]:
    """Return unique webhook/admin secret names declared by channel files."""
    names: list[str] = []
    seen: set[str] = set()
    for channel in channels:
        for name in (
            channel.free_webhook_secret_name,
            channel.paid_webhook_secret_name,
            channel.admin_webhook_secret_name,
        ):
            if name and name not in seen:
                seen.add(name)
                names.append(name)
    return names
