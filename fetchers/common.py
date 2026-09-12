"""API별 fetcher가 공유하는 타입 + 집계 로직.

실API로 교체할 때도 이 파일은 그대로 두고 fetchers/*.py 세 개만 바꾸면 된다.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TrendSignal:
    source: str
    raw: float          # 소스 고유 단위 (기사 수, 지수, 랭크 등)
    normalized: float   # 0~100, 소스 간 비교 가능하게 맞춘 값


# ponytail: 가중치는 감으로 잡은 값. 실 API 응답을 모으면 실측 분포로 재보정할 것.
WEIGHTS = {"naver_news": 0.30, "datalab": 0.45, "youtube_trend": 0.25}


def aggregate(signals: list[TrendSignal]) -> float:
    return sum(s.normalized * WEIGHTS[s.source] for s in signals)


def classify(score: float) -> str:
    if score >= 70:
        return "폭발적 화제"
    if score >= 40:
        return "화제"
    if score >= 15:
        return "보통"
    return "관심없음"
