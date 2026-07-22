from __future__ import annotations

from scripts import build_cloudflare_site


def test_public_feedback_config_requires_both_supabase_values(monkeypatch):
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_ANON_KEY", raising=False)

    assert build_cloudflare_site.public_feedback_config() == {}


def test_public_feedback_config_exposes_only_browser_safe_values(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co/")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "sb_publishable_example")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "must-not-be-returned")

    assert build_cloudflare_site.public_feedback_config() == {
        "url": "https://example.supabase.co",
        "key": "sb_publishable_example",
    }
