"""Naver DataLab(검색어트렌드) mock fetcher.

실API 붙일 때: fetch() 시그니처만 유지하고 내부를 DataLab 검색어트렌드 API
호출(구간 내 상대 검색량 지수, 0~100)로 바꾸면 된다.
"""
from __future__ import annotations

import random

from .common import TrendSignal

SOURCE = "datalab"


def fetch(keyword: str, true_buzz: float) -> TrendSignal:
    # 실API 특성 가정: 이미 0~100으로 정규화된 상대 검색량 지수라 노이즈가
    # 적고(소형) 실제 화제도를 가장 촘촘히 반영한다.
    index = min(100, max(0, true_buzz + random.gauss(0, 10)))
    return TrendSignal(SOURCE, index, index)
