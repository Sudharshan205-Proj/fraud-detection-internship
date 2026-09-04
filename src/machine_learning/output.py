"""Shared helpers for writing generated artifacts (CSV/PNG)."""

from __future__ import annotations

from pathlib import Path


def prepare_output_path(output_path: str | Path) -> Path:
    """Create the parent directory for an output artifact."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path