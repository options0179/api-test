"""Phase 5: DataLab + YouTube 실API로 같은 키워드 셋을 조회해서 결과를 저장한다.

뉴스 검색 API는 이 파이프라인에서 완전히 제외 — 개정된 검색 API 특약이
저장/캐싱/가공을 금지해서 이 프로젝트 용도로는 쓸 수 없음 (real_fetchers/naver_news.py 참고).
실행 전에 .env.example을 복사한 .env에 NAVER_CLIENT_ID/SECRET, YOUTUBE_API_KEY를
채워야 한다.

실데이터는 mock과 달리 "진짜 화제도(true_buzz)" 정답이 없어서, mock처럼 정확도를
못 재고 대신 (1) API가 실제로 붙는지, (2) 두 소스가 서로 비슷한 순위를 매기는지
(상호 일관성)를 확인하는 용도다.
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

from load_env import load_env

load_env()

from real_fetchers import datalab, youtube_trend  # noqa: E402  (env 로드 후 import)

RESULTS_DIR = Path(__file__).parent / "results"

# 화제도가 뚜렷이 다를 것으로 예상되는 실제 키워드 셋 (필요시 교체)
KEYWORDS = ["손흥민", "아이유", "국정감사", "장마", "펜션 예약"]


def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    call_log = {"datalab_calls": 0, "youtube_calls": 0}

    print("YouTube 트렌드 목록 조회 (1콜, 1유닛)...")
    titles = youtube_trend.fetch_trending_titles()
    call_log["youtube_calls"] += 1

    rows = []
    for kw in KEYWORDS:
        dl = datalab.fetch(kw)
        call_log["datalab_calls"] += 1
        yt = youtube_trend.fetch(kw, titles=titles)
        rows.append({
            "keyword": kw,
            "datalab_normalized": dl.normalized,
            "youtube_normalized": yt.normalized,
            "youtube_rank": yt.raw,
        })
        print(f"  {kw:10s} datalab={dl.normalized:5.1f}  youtube={yt.normalized:5.1f} (rank={yt.raw})")

    dl_vals = [r["datalab_normalized"] for r in rows]
    yt_vals = [r["youtube_normalized"] for r in rows]
    try:
        cross_source_correlation = statistics.correlation(dl_vals, yt_vals)
    except statistics.StatisticsError:
        cross_source_correlation = None  # 값 분산이 0이면 계산 불가 (표본이 너무 적거나 전부 동일)

    result = {
        "keywords": KEYWORDS,
        "rows": rows,
        "cross_source_correlation": cross_source_correlation,
        "api_calls_used": call_log,
    }
    out = RESULTS_DIR / "real_comparison.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nwrote {out}")
    print(f"이번 실행 API 호출: DataLab {call_log['datalab_calls']}콜, YouTube {call_log['youtube_calls']}콜(1유닛)")
    print(f"DataLab-YouTube 정규화값 상관계수: {cross_source_correlation}")


if __name__ == "__main__":
    main()
