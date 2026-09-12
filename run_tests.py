"""Phase 2: API별 mock 데이터를 여러 화제도(true_buzz) x 반복시행으로 뽑아
results/raw_<api>.json 에 저장한다. 다음 단계(analyze.py)의 입력이 된다.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

from fetchers import datalab, naver_news, youtube_trend
from fetchers.common import TrendSignal, aggregate, classify

RESULTS_DIR = Path(__file__).parent / "results"
TRUE_BUZZ_LEVELS = list(range(0, 101, 10))   # 0,10,...,100
TRIALS_PER_LEVEL = 30

FETCHERS = {
    "naver_news": naver_news.fetch,
    "datalab": datalab.fetch,
    "youtube_trend": youtube_trend.fetch,
}

# 순위 정확도용 시나리오 (aggregate 전체 파이프라인 테스트)
SCENARIOS = {
    "완전_밈": 95,
    "연예_이슈": 70,
    "일상_뉴스": 35,
    "무관심_주제": 5,
}


def run_raw_sweep(seed: int = 0) -> dict[str, list[dict]]:
    random.seed(seed)
    raw: dict[str, list[dict]] = {name: [] for name in FETCHERS}
    for true_buzz in TRUE_BUZZ_LEVELS:
        for _ in range(TRIALS_PER_LEVEL):
            for name, fetch in FETCHERS.items():
                signal = fetch("테스트키워드", true_buzz)
                raw[name].append(
                    {"true_buzz": true_buzz, "raw": signal.raw, "normalized": signal.normalized}
                )
    return raw


def run_aggregate_scenarios(seed: int = 0) -> dict:
    random.seed(seed)
    results = {}
    for kw, buzz in SCENARIOS.items():
        signals = [fetch(kw, buzz) for fetch in FETCHERS.values()]
        score = aggregate(signals)
        results[kw] = {
            "true_buzz": buzz,
            "score": score,
            "label": classify(score),
            "signals": {s.source: {"raw": s.raw, "normalized": s.normalized} for s in signals},
        }
    by_true = sorted(SCENARIOS, key=SCENARIOS.get, reverse=True)
    by_score = sorted(results, key=lambda k: results[k]["score"], reverse=True)
    return {"scenarios": results, "rank_match": by_true == by_score, "by_true": by_true, "by_score": by_score}


def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    raw = run_raw_sweep()
    for name, rows in raw.items():
        out = RESULTS_DIR / f"raw_{name}.json"
        out.write_text(json.dumps(rows, ensure_ascii=False, indent=2))
        print(f"wrote {out} ({len(rows)} rows)")

    agg = run_aggregate_scenarios()
    out = RESULTS_DIR / "aggregate_scenarios.json"
    out.write_text(json.dumps(agg, ensure_ascii=False, indent=2))
    print(f"wrote {out} (rank_match={agg['rank_match']})")
    assert agg["rank_match"], "aggregate 파이프라인이 실제 화제도 순위를 못 맞춤"


if __name__ == "__main__":
    main()
