"""Phase 3: results/raw_<api>.json을 읽어 API별 성능 지표를 계산하고
results/analysis.json + web/data.js(웹사이트가 그대로 읽을 임베디드 데이터)를 만든다.
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / "results"
WEB_DIR = Path(__file__).parent / "web"
DETECTION_THRESHOLD = 70  # 이 이상을 "화제"로 본다


def analyze_api(rows: list[dict]) -> dict:
    true_vals = [r["true_buzz"] for r in rows]
    norm_vals = [r["normalized"] for r in rows]

    correlation = statistics.correlation(true_vals, norm_vals)
    errors = [n - t for t, n in zip(true_vals, norm_vals)]
    mae = statistics.mean(abs(e) for e in errors)
    bias = statistics.mean(errors)          # 양수면 과대평가 경향, 음수면 과소평가
    noise_std = statistics.pstdev(errors)   # 값이 클수록 들쭉날쭉(신뢰도 낮음)

    buzzy = [r for r in rows if r["true_buzz"] >= DETECTION_THRESHOLD]
    quiet = [r for r in rows if r["true_buzz"] < DETECTION_THRESHOLD]
    detect_rate = (
        sum(1 for r in buzzy if r["normalized"] >= DETECTION_THRESHOLD) / len(buzzy)
        if buzzy else None
    )
    false_positive_rate = (
        sum(1 for r in quiet if r["normalized"] >= DETECTION_THRESHOLD) / len(quiet)
        if quiet else None
    )

    return {
        "n": len(rows),
        "correlation": round(correlation, 4),
        "mae": round(mae, 2),
        "bias": round(bias, 2),
        "noise_std": round(noise_std, 2),
        "detect_rate": round(detect_rate, 4) if detect_rate is not None else None,
        "false_positive_rate": round(false_positive_rate, 4) if false_positive_rate is not None else None,
    }


def main():
    apis = ["naver_news", "datalab", "youtube_trend"]
    per_api = {}
    scatter = {}
    for name in apis:
        rows = json.loads((RESULTS_DIR / f"raw_{name}.json").read_text())
        per_api[name] = analyze_api(rows)
        # 웹 산점도용: 트라이얼 전부 넘기면 무거우니 true_buzz별 평균만 넘김
        by_level: dict[int, list[float]] = {}
        for r in rows:
            by_level.setdefault(r["true_buzz"], []).append(r["normalized"])
        scatter[name] = [
            {"true_buzz": lvl, "avg_normalized": round(statistics.mean(vals), 2)}
            for lvl, vals in sorted(by_level.items())
        ]

    aggregate = json.loads((RESULTS_DIR / "aggregate_scenarios.json").read_text())

    analysis = {"per_api": per_api, "scatter": scatter, "aggregate": aggregate}

    out = RESULTS_DIR / "analysis.json"
    out.write_text(json.dumps(analysis, ensure_ascii=False, indent=2))
    print(f"wrote {out}")

    WEB_DIR.mkdir(exist_ok=True)
    data_js = WEB_DIR / "data.js"
    data_js.write_text("const ANALYSIS = " + json.dumps(analysis, ensure_ascii=False) + ";\n")
    print(f"wrote {data_js}")

    print(json.dumps(per_api, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
