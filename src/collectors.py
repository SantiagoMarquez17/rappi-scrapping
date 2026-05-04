from __future__ import annotations

import time
from abc import ABC, abstractmethod

from src.sample_data import build_sample_rows


class BaseCollector(ABC):
    """Common interface for platform-specific data collectors."""

    def __init__(self, platform: str, delay_seconds: float = 1.5) -> None:
        self.platform = platform
        self.delay_seconds = delay_seconds

    def wait(self) -> None:
        """Throttle requests/actions when live collectors are implemented."""
        time.sleep(self.delay_seconds)

    @abstractmethod
    def collect(self) -> list[dict]:
        raise NotImplementedError


class SampleCollector(BaseCollector):
    """Reproducible collector used to validate the full analytical pipeline."""

    def collect(self) -> list[dict]:
        return [row for row in build_sample_rows() if row["platform"] == self.platform]


class LiveCollector(BaseCollector):
    """Extension point for Playwright/API collectors per platform."""

    def collect(self) -> list[dict]:
        raise NotImplementedError(
            "Live scraping should be implemented per platform with Playwright/API flows. "
            "Keep sample mode as demo fallback."
        )


def get_collectors(mode: str) -> list[BaseCollector]:
    """Factory that keeps the pipeline agnostic to the selected collection mode."""
    collector_cls = SampleCollector if mode == "sample" else LiveCollector
    return [
        collector_cls("Rappi"),
        collector_cls("Uber Eats"),
        collector_cls("DiDi Food"),
    ]
