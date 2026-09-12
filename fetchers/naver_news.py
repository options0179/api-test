"""Naver News mock fetcher.

실API 붙일 때: 이 파일의 fetch() 시그니처(keyword -> TrendSignal)만 유지하고
내부를 실제 뉴스 검색 API 호출(최근 24h 기사 수 집계)로 바꾸면 된다.
"""
from __future__ import annotations

import random

from .common import TrendSignal

SOURCE = "naver_news"


def fetch(keyword: str, true_buzz: float) -> TrendSignal:
    # 실API 특성 가정: 최근 24h 기사 수. 화제일수록 기사가 급증하지만
    # 언론사 보도 텀 때문에 노이즈가 크고(중대형), 반응이 다소 느리다(반영폭↓).
    count = max(0, round(true_buzz * 2 + random.gauss(0, 15)))
    normalized = min(100, count / 2)
    return TrendSignal(SOURCE, count, normalized)
