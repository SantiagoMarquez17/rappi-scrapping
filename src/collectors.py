from __future__ import annotations

import time
from abc import ABC, abstractmethod

from src.sample_data import build_sample_rows


class BaseCollector(ABC):
    def __init__(self, platform: str, delay_seconds: float = 1.5) -> None:
        self.platform = platform
        self.delay_seconds = delay_seconds

    def wait(self) -> None:
        time.sleep(self.delay_seconds)

    @abstractmethod
    def collect(self) -> list[dict]:
        raise NotImplementedError


class SampleCollector(BaseCollector):
    def collect(self) -> list[dict]:
        return [row for row in build_sample_rows() if row["platform"] == self.platform]


class LiveCollector(BaseCollector):
    def collect(self) -> list[dict]:
        raise NotImplementedError(
            "Live scraping should be implemented per platform with Playwright/API flows. "
            "Keep sample mode as demo fallback."
        )


def get_collectors(mode: str) -> list[BaseCollector]:
    collector_cls = SampleCollector if mode == "sample" else LiveCollector
    return [
        collector_cls("Rappi"),
        collector_cls("Uber Eats"),
        collector_cls("DiDi Food"),
    ]
