"""Phase 5 (YouTube 단일 소스로 축소): 실API로 고정 키워드셋의 급상승 여부를 조회한다.

Naver 뉴스검색은 개정 약관상 저장/가공 금지라 제외했고, DataLab은
developers.naver.com이 신규 발급을 막아놔서 키 자체를 못 받아 제외했다.
YouTube Data API v3만 남았다 (real_fetchers/youtube_trend.py).

실행 전에 .env.example을 복사한 .env에 YOUTUBE_API_KEY를 채워야 한다.
실데이터는 "진짜 화제도(true_buzz)" 정답이 없어서 mock처럼 정확도는 못 재고,
API가 실제로 붙어서 그럴듯한 결과를 주는지 확인하는 용도다.
"""
from __future__ import annotations

import json
from pathlib import Path

from load_env import load_env

load_env()

from real_fetchers import youtube_trend  # noqa: E402  (env 로드 후 import)

RESULTS_DIR = Path(__file__).parent / "results"

KEYWORDS = ["손흥민", "아이유", "국정감사", "장마", "펜션 예약"]


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    print("YouTube 트렌드 목록 조회 (1콜, 1유닛)...")
    titles = youtube_trend.fetch_trending_titles()

    rows = []
    for kw in KEYWORDS:
        yt = youtube_trend.fetch(kw, titles=titles)
        rows.append({"keyword": kw, "normalized": yt.normalized, "rank": yt.raw})
        print(f"  {kw:10s} normalized={yt.normalized:5.1f}  (rank={yt.raw})")

    result = {"keywords": KEYWORDS, "rows": rows, "api_calls_used": {"youtube_calls": 1}}
    out = RESULTS_DIR / "real_comparison.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nwrote {out}")
    print("이번 실행 API 호출: YouTube 1콜(1유닛)")


if __name__ == "__main__":
    main()
