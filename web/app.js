const API_LABELS = {
  naver_news: "Naver News",
  datalab: "DataLab",
  youtube_trend: "YouTube Trend",
};
const API_COLORS = {
  naver_news: "#5b9dff",
  datalab: "#4caf7d",
  youtube_trend: "#e0956b",
};

function fillMetricsTable() {
  const tbody = document.querySelector("#metrics-table tbody");
  for (const [api, m] of Object.entries(ANALYSIS.per_api)) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${API_LABELS[api]}</td>
      <td>${m.correlation}</td>
      <td>${m.mae}</td>
      <td>${m.bias}</td>
      <td>${m.noise_std}</td>
      <td>${(m.detect_rate * 100).toFixed(1)}%</td>
      <td>${(m.false_positive_rate * 100).toFixed(1)}%</td>
    `;
    tbody.appendChild(tr);
  }
}

function drawCorrChart() {
  const canvas = document.getElementById("corr-chart");
  const ctx = canvas.getContext("2d");
  const apis = Object.keys(ANALYSIS.per_api);
  const w = canvas.width, h = canvas.height;
  const pad = { top: 20, right: 20, bottom: 40, left: 40 };
  const plotW = w - pad.left - pad.right;
  const plotH = h - pad.top - pad.bottom;
  const barW = plotW / apis.length / 2;

  ctx.clearRect(0, 0, w, h);
  ctx.strokeStyle = "#5b6472";
  ctx.beginPath();
  ctx.moveTo(pad.left, pad.top);
  ctx.lineTo(pad.left, h - pad.bottom);
  ctx.lineTo(w - pad.right, h - pad.bottom);
  ctx.stroke();

  apis.forEach((api, i) => {
    const corr = ANALYSIS.per_api[api].correlation;
    const barH = corr * plotH; // correlation is 0~1 here
    const x = pad.left + (i + 0.5) * (plotW / apis.length) - barW / 2;
    const y = h - pad.bottom - barH;
    ctx.fillStyle = API_COLORS[api];
    ctx.fillRect(x, y, barW, barH);

    ctx.fillStyle = "#9aa2b1";
    ctx.font = "12px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(API_LABELS[api], x + barW / 2, h - pad.bottom + 16);
    ctx.fillStyle = "#e6e8ec";
    ctx.fillText(corr.toFixed(3), x + barW / 2, y - 6);
  });
}

function drawScatterChart() {
  const canvas = document.getElementById("scatter-chart");
  const ctx = canvas.getContext("2d");
  const w = canvas.width, h = canvas.height;
  const pad = { top: 20, right: 20, bottom: 40, left: 40 };
  const plotW = w - pad.left - pad.right;
  const plotH = h - pad.top - pad.bottom;
  const toX = (v) => pad.left + (v / 100) * plotW;
  const toY = (v) => h - pad.bottom - (v / 100) * plotH;

  ctx.clearRect(0, 0, w, h);
  ctx.strokeStyle = "#2a2f3a";
  ctx.beginPath();
  ctx.moveTo(pad.left, pad.top);
  ctx.lineTo(pad.left, h - pad.bottom);
  ctx.lineTo(w - pad.right, h - pad.bottom);
  ctx.stroke();

  // ideal diagonal (y = x)
  ctx.strokeStyle = "#5b6472";
  ctx.setLineDash([4, 4]);
  ctx.beginPath();
  ctx.moveTo(toX(0), toY(0));
  ctx.lineTo(toX(100), toY(100));
  ctx.stroke();
  ctx.setLineDash([]);

  for (const [api, points] of Object.entries(ANALYSIS.scatter)) {
    ctx.strokeStyle = API_COLORS[api];
    ctx.fillStyle = API_COLORS[api];
    ctx.beginPath();
    points.forEach((p, i) => {
      const x = toX(p.true_buzz);
      const y = toY(p.avg_normalized);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    ctx.stroke();
    points.forEach((p) => {
      ctx.beginPath();
      ctx.arc(toX(p.true_buzz), toY(p.avg_normalized), 3, 0, Math.PI * 2);
      ctx.fill();
    });
  }

  ctx.fillStyle = "#9aa2b1";
  ctx.font = "12px sans-serif";
  ctx.textAlign = "center";
  ctx.fillText("true_buzz →", w / 2, h - 8);
}

function fillLegend() {
  const legend = document.getElementById("scatter-legend");
  legend.innerHTML = Object.keys(API_LABELS)
    .map(
      (api) =>
        `<span><span class="swatch" style="background:${API_COLORS[api]}"></span>${API_LABELS[api]}</span>`
    )
    .join("");
}

function fillAggregate() {
  const agg = ANALYSIS.aggregate;
  document.getElementById("rank-true").textContent = agg.by_true.join(" > ");
  document.getElementById("rank-score").textContent = agg.by_score.join(" > ");
  const badge = document.getElementById("rank-match");
  badge.textContent = agg.rank_match ? "PASS — 순위 일치" : "FAIL — 순위 불일치";
  badge.classList.add(agg.rank_match ? "pass" : "fail");

  const tbody = document.querySelector("#scenario-table tbody");
  for (const [name, s] of Object.entries(agg.scenarios)) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${name}</td><td>${s.true_buzz}</td><td>${s.score.toFixed(1)}</td><td>${s.label}</td>`;
    tbody.appendChild(tr);
  }
}

function fillAcquisition() {
  const container = document.getElementById("acquisition-cards");
  for (const [api, info] of Object.entries(ANALYSIS.acquisition)) {
    const badgeClass = info.blockers.length === 0
      ? "ok"
      : info.signup_difficulty.includes("불가")
      ? "blocked"
      : "limited";
    const badgeText = info.blockers.length === 0
      ? "사용 가능"
      : info.signup_difficulty.includes("불가")
      ? "발급 불가"
      : "제한적 사용 가능";

    const card = document.createElement("div");
    card.className = "acq-card";
    card.innerHTML = `
      <h3>${API_LABELS[api] || info.label}</h3>
      <span class="badge ${badgeClass}">${badgeText}</span>
      <dl>
        <dt>비용</dt><dd>${info.cost}</dd>
        <dt>발급 난이도</dt><dd>${info.signup_difficulty}</dd>
        ${info.blockers.length > 0 ? `<dt>막힌 부분</dt><dd><ul>${info.blockers.map((b) => `<li>${b}</li>`).join("")}</ul></dd>` : ""}
        <dt>결론</dt><dd>${info.status}</dd>
      </dl>
    `;
    container.appendChild(card);
  }
}

fillMetricsTable();
drawCorrChart();
drawScatterChart();
fillLegend();
fillAggregate();
fillAcquisition();
