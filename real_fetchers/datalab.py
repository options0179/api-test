"""Naver DataLab 검색어트렌드 실API fetcher.

NAVER_CLIENT_ID / NAVER_CLIENT_SECRET 필요 (developers.naver.com 앱 등록).
mock 버전(fetchers/datalab.py)과 동일하게 0~100 정규화된 값을 반환해서
바로 비교 가능하게 맞춘다 — DataLab 응답의 ratio 필드가 이미 0~100이라
그대로 쓰면 된다.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import date, timedelta

from fetchers.common import TrendSignal

SOURCE = "datalab"
ENDPOINT = "https://openapi.naver.com/v1/datalab/search"


def fetch(keyword: str, days: int = 7) -> TrendSignal:
    client_id = os.environ["NAVER_CLIENT_ID"]
    client_secret = os.environ["NAVER_CLIENT_SECRET"]

    end = date.today()
    start = end - timedelta(days=days)
    body = json.dumps({
        "startDate": start.isoformat(),
        "endDate": end.isoformat(),
        "timeUnit": "date",
        "keywordGroups": [{"groupName": keyword, "keywords": [keyword]}],
    }).encode("utf-8")

    req = urllib.request.Request(ENDPOINT, data=body, method="POST", headers={
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            payload = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"DataLab API 오류 {e.code}: {e.read().decode(errors='replace')}") from e

    points = payload["results"][0]["data"]  # [{period, ratio}, ...] 최근일이 마지막
    ratio = points[-1]["ratio"] if points else 0.0
    return TrendSignal(SOURCE, raw=ratio, normalized=ratio)
