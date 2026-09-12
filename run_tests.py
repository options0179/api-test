"""Phase 2 (YouTube 단일 소스로 축소): mock 데이터를 화제도(true_buzz) x 반복시행으로
뽑아 results/raw_youtube_trend.json 에 저장하고, 시나리오 4개로 전체 파이프라인
(fetch -> classify)을 검증한다.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

from fetchers import youtube_trend
from fetchers.common import classify

RESULTS_DIR = Path(__file__).parent / "results"
TRUE_BUZZ_LEVELS = list(range(0, 101, 10))   # 0,10,...,100
TRIALS_PER_LEVEL = 30

SCENARIOS = {
    "완전_밈": 95,
    "연예_이슈": 70,
    "일상_뉴스": 35,
    "무관심_주제": 5,
}


def run_raw_sweep(seed: int = 0) -> list[dict]:
    random.seed(seed)
    rows = []
    for true_buzz in TRUE_BUZZ_LEVELS:
        for _ in range(TRIALS_PER_LEVEL):
            signal = youtube_trend.fetch("테스트키워드", true_buzz)
            rows.append({"true_buzz": true_buzz, "raw": signal.raw, "normalized": signal.normalized})
    return rows


def run_scenarios(seed: int = 0) -> dict:
    random.seed(seed)
    results = {}
    for kw, buzz in SCENARIOS.items():
        signal = youtube_trend.fetch(kw, buzz)
        results[kw] = {"true_buzz": buzz, "score": signal.normalized, "label": classify(signal.normalized)}
    by_true = sorted(SCENARIOS, key=SCENARIOS.get, reverse=True)
    by_score = sorted(results, key=lambda k: results[k]["score"], reverse=True)
    return {"scenarios": results, "rank_match": by_true == by_score, "by_true": by_true, "by_score": by_score}


def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    rows = run_raw_sweep()
    out = RESULTS_DIR / "raw_youtube_trend.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2))
    print(f"wrote {out} ({len(rows)} rows)")

    agg = run_scenarios()
    out2 = RESULTS_DIR / "aggregate_scenarios.json"
    out2.write_text(json.dumps(agg, ensure_ascii=False, indent=2))
    print(f"wrote {out2} (rank_match={agg['rank_match']})")
    print(json.dumps(agg["scenarios"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
