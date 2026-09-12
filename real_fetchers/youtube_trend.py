"""YouTube 인기 급상승 실API fetcher.

YOUTUBE_API_KEY 필요 (Google Cloud Console, YouTube Data API v3 활성화).
videos.list(chart=mostPopular)만 쓴다 — 1유닛/콜이라 search.list(100유닛)보다
훨씬 싸고, 하루 쿼터(기본 10,000)로 넉넉히 반복 조회 가능.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request

from fetchers.common import TrendSignal

SOURCE = "youtube_trend"
ENDPOINT = "https://www.googleapis.com/youtube/v3/videos"


def fetch_trending_titles(region_code: str = "KR", max_results: int = 50) -> list[str]:
    params = urllib.parse.urlencode({
        "part": "snippet",
        "chart": "mostPopular",
        "regionCode": region_code,
        "maxResults": max_results,
        "key": os.environ["YOUTUBE_API_KEY"],
    })
    req = urllib.request.Request(f"{ENDPOINT}?{params}")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            payload = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"YouTube API 오류 {e.code}: {e.read().decode(errors='replace')}") from e
    return [item["snippet"]["title"] for item in payload.get("items", [])]


def fetch(keyword: str, titles: list[str] | None = None) -> TrendSignal:
    # 실API 특성: 트렌드 목록에 키워드가 제목으로 매칭되는 영상이 있는지가
    # 전부라, 매칭 실패(오탈자/영문-한글 표기 차이)가 잦다 — 정밀 매칭이
    # 필요하면 태그/설명까지 봐야 하지만 POC 단계라 제목 부분일치만 본다.
    if titles is None:
        titles = fetch_trending_titles()
    for rank, title in enumerate(titles, start=1):
        if keyword.lower() in title.lower():
            normalized = max(0, 100 - rank * 2)
            return TrendSignal(SOURCE, raw=rank, normalized=normalized)
    return TrendSignal(SOURCE, raw=0, normalized=0)
