"""YouTube fetcher가 쓰는 공용 타입 + 등급 분류.

Naver 뉴스/DataLab은 제외함 (뉴스 검색 API는 개정 약관상 저장/가공 금지, DataLab은
developers.naver.com 개발자센터가 신규 발급을 막아놔서 키 자체를 못 받음).
소스가 YouTube 하나뿐이라 가중합 로직은 필요 없고, 정규화값을 그대로 등급으로
나눈다.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TrendSignal:
    source: str
    raw: float          # 소스 고유 단위 (급상승 랭크 등)
    normalized: float   # 0~100


def classify(score: float) -> str:
    if score >= 70:
        return "폭발적 화제"
    if score >= 40:
        return "화제"
    if score >= 15:
        return "보통"
    return "관심없음"
