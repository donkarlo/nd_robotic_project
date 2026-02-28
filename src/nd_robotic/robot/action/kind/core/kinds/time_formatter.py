from __future__ import annotations


class TimeFormatter:
    def format_compact(self, total_seconds: int) -> str:
        if total_seconds < 0:
            total_seconds = 0

        days = total_seconds // 86400
        remainder = total_seconds % 86400
        hours = remainder // 3600
        remainder = remainder % 3600
        minutes = remainder // 60
        seconds = remainder % 60

        parts: list[str] = []

        if days > 0:
            parts.append(f"{days}d")
        if hours > 0 or days > 0:
            parts.append(f"{hours}h")
        if minutes > 0 or hours > 0 or days > 0:
            parts.append(f"{minutes}m")

        parts.append(f"{seconds}s")
        return " ".join(parts)
