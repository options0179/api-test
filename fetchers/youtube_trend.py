"""YouTube 인기 급상승(Trending) mock fetcher.

실API 붙일 때: fetch() 시그니처만 유지하고 내부를 YouTube Data API의
videos.list(chart=mostPopular) 결과에서 키워드 매칭 랭크 조회로 바꾸면 된다.
"""
from __future__ import annotations

import random

from .common import TrendSignal

SOURCE = "youtube_trend"


def fetch(keyword: str, true_buzz: float) -> TrendSignal:
    # 실API 특성 가정: 급상승 목록(1~50위)에 아예 없으면 0점 — 연속값이 아니라
    # on/off에 가까운 신호라 낮은 화제도 구간에서는 정보가 거의 없다.
    if true_buzz + random.gauss(0, 20) < 40:
        return TrendSignal(SOURCE, raw=0, normalized=0)
    rank = max(1, round(50 - true_buzz * 0.5 + random.gauss(0, 5)))
    normalized = max(0, 100 - rank * 2)
    return TrendSignal(SOURCE, rank, normalized)
