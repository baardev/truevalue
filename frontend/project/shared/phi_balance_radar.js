/**
 * PHI balance score radar (0–100% per phase, φ zone rings).
 * Call renderPhiBalanceRadar({ dataUrl, idSuffix, entity?, resolvePhases? })
 */
(function (global) {
  "use strict";

  var PHI = (1 + Math.sqrt(5)) / 2;

  function zoneFromBalance(b) {
    if (b >= 80) return "coherent";
    if (b >= 100 / PHI) return "stressed";
    if (b >= 100 * (1 - 1 / PHI)) return "failure";
    return "breakdown";
  }

  var ZONE_COLORS = {
    coherent: "#3ecf8e",
    stressed: "#f5a623",
    failure: "#ef5350",
    breakdown: "#b71c1c",
  };
  var ZONE_ABBREV = { coherent: "C", stressed: "S", failure: "F", breakdown: "B" };

  function getRawPhases(data, cfg) {
    var p = data.phases || {};
    if (cfg.resolvePhases === "lighter") {
      return p.synthetic && typeof p.synthetic === "object" ? p.synthetic : p;
    }
    if (cfg.entity != null && cfg.entity !== "") {
      return p[cfg.entity] || {};
    }
    return p;
  }

  function renderPhiBalanceRadar(cfg) {
    var dataUrl = cfg.dataUrl;
    var idSuffix = cfg.idSuffix;
    var entity = cfg.entity;

    fetch(dataUrl)
      .then(function (r) {
        return r.json();
      })
      .catch(function () {
        return null;
      })
      .then(function (data) {
        if (!data) return;

        var rawPhases = getRawPhases(data, cfg);
        var phaseMeta = data.phase_meta || {};
        var ids = Object.keys(rawPhases)
          .filter(function (k) {
            return /^\d+$/.test(k);
          })
          .sort(function (a, b) {
            return +a - +b;
          });
        if (ids.length < 3) return;

        var labels = ids.map(function (id) {
          var m = phaseMeta[id];
          var name = m && m.name ? m.name : rawPhases[id] && rawPhases[id].name ? rawPhases[id].name : "";
          if (name.length > 16) name = name.slice(0, 15) + "\u2026";
          return name ? "Ph\u202f" + id + "\n" + name : "Phase " + id;
        });
        var Bvals = ids.map(function (id) {
          return +((rawPhases[id] && rawPhases[id].balance) || 0);
        });
        var zoneKeys = ids.map(function (id, i) {
          return (rawPhases[id] && rawPhases[id].balance_zone) || zoneFromBalance(Bvals[i]);
        });
        var zoneCols = zoneKeys.map(function (z) {
          return ZONE_COLORS[z] || "#8b949e";
        });
        var zoneAbbr = zoneKeys.map(function (z) {
          return ZONE_ABBREV[z] || "?";
        });

        var canvas = document.getElementById("balance-radar-" + idSuffix);
        if (!canvas) return;
        var ctx = canvas.getContext("2d");
        var W = canvas.width,
          H = canvas.height,
          cx = W / 2,
          cy = H / 2;
        var R = Math.min(W, H) * 0.27,
          labelR = R + 56;
        var Npts = ids.length;
        var minV = 0,
          maxV = 100;

        function ang(i) {
          return (2 * Math.PI * i) / Npts - Math.PI / 2;
        }
        function pt(i, v) {
          var frac = Math.max(0, Math.min(1, (v - minV) / (maxV - minV)));
          return {
            x: cx + R * frac * Math.cos(ang(i)),
            y: cy + R * frac * Math.sin(ang(i)),
          };
        }
        function polyPath(frac) {
          ctx.beginPath();
          for (var i = 0; i < Npts; i++) {
            var x = cx + R * frac * Math.cos(ang(i)),
              y = cy + R * frac * Math.sin(ang(i));
            i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
          }
          ctx.closePath();
        }

        ctx.clearRect(0, 0, W, H);
        ctx.fillStyle = "#0d1117";
        ctx.fillRect(0, 0, W, H);

        var zones = [
          { v: 100, fill: "rgba(62,207,142,0.06)" },
          { v: 80, fill: "rgba(245,166,35,0.10)" },
          { v: 61.8, fill: "rgba(239,83,80,0.14)" },
          { v: 38.2, fill: "rgba(183,28,28,0.22)" },
        ];
        zones.forEach(function (z) {
          polyPath(z.v / 100);
          ctx.fillStyle = z.fill;
          ctx.fill();
        });

        var thresholds = [
          { v: 80, col: "#3ecf8e" },
          { v: 61.8, col: "#f5a623" },
          { v: 38.2, col: "#ef5350" },
        ];
        thresholds.forEach(function (t) {
          polyPath(t.v / 100);
          ctx.strokeStyle = t.col;
          ctx.lineWidth = 1.4;
          ctx.globalAlpha = 0.8;
          ctx.stroke();
          ctx.globalAlpha = 1;
          var lx = cx,
            ly = cy - R * (t.v / 100) - 6;
          ctx.font = "9px ui-sans-serif,system-ui,sans-serif";
          ctx.fillStyle = t.col;
          ctx.textAlign = "center";
          ctx.fillText(t.v + "%", lx, ly);
        });

        [20, 40, 60, 100].forEach(function (gv) {
          polyPath(gv / 100);
          ctx.strokeStyle = "rgba(255,255,255,0.07)";
          ctx.lineWidth = 0.8;
          ctx.stroke();
        });

        for (var si = 0; si < Npts; si++) {
          ctx.beginPath();
          ctx.moveTo(cx, cy);
          ctx.lineTo(cx + R * Math.cos(ang(si)), cy + R * Math.sin(ang(si)));
          ctx.strokeStyle = "rgba(255,255,255,0.08)";
          ctx.lineWidth = 1;
          ctx.stroke();
        }

        ctx.beginPath();
        ids.forEach(function (id, i) {
          var p = pt(i, Bvals[i]);
          i === 0 ? ctx.moveTo(p.x, p.y) : ctx.lineTo(p.x, p.y);
        });
        ctx.closePath();
        ctx.globalAlpha = 0.25;
        ctx.fillStyle = "#4fc3f7";
        ctx.fill();
        ctx.globalAlpha = 1;

        ids.forEach(function (id, i) {
          var next = (i + 1) % Npts;
          var p1 = pt(i, Bvals[i]),
            p2 = pt(next, Bvals[next]);
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.strokeStyle = zoneCols[i];
          ctx.lineWidth = 2.5;
          ctx.stroke();
        });

        ids.forEach(function (id, i) {
          var p = pt(i, Bvals[i]);
          ctx.beginPath();
          ctx.arc(p.x, p.y, 5, 0, 2 * Math.PI);
          ctx.fillStyle = zoneCols[i];
          ctx.globalAlpha = 0.95;
          ctx.fill();
          ctx.globalAlpha = 1;
        });

        ids.forEach(function (id, i) {
          var spx = cx + R * Math.cos(ang(i)),
            spy = cy + R * Math.sin(ang(i));
          ctx.beginPath();
          ctx.arc(spx, spy, 5.5, 0, 2 * Math.PI);
          ctx.fillStyle = zoneCols[i];
          ctx.globalAlpha = 0.85;
          ctx.fill();
          ctx.globalAlpha = 1;
          ctx.font = "bold 7px ui-sans-serif,system-ui,sans-serif";
          ctx.textAlign = "center";
          ctx.fillStyle = "#0d1117";
          ctx.fillText(zoneAbbr[i], spx, spy + 2.5);
        });

        ids.forEach(function (id, i) {
          var a = ang(i),
            lx = cx + labelR * Math.cos(a),
            ly = cy + labelR * Math.sin(a);
          var lines = labels[i].split("\n");
          var align = "center";
          if (Math.cos(a) > 0.25) align = "left";
          if (Math.cos(a) < -0.25) align = "right";
          ctx.textAlign = align;
          var lineH = 13,
            startY = ly - (lines.length * lineH) / 2 + lineH / 2;
          lines.forEach(function (line, li) {
            if (li === 0) {
              ctx.fillStyle = zoneCols[i];
              ctx.font = "bold 11px ui-sans-serif,system-ui,sans-serif";
            } else {
              ctx.fillStyle = "#8b949e";
              ctx.font = "10px ui-sans-serif,system-ui,sans-serif";
            }
            ctx.fillText(line, lx, startY + li * lineH);
          });
        });

        ctx.beginPath();
        ctx.arc(cx, cy, 3, 0, 2 * Math.PI);
        ctx.fillStyle = "rgba(255,255,255,0.3)";
        ctx.fill();

        var zoneCounts = { coherent: 0, stressed: 0, failure: 0, breakdown: 0 };
        zoneKeys.forEach(function (z) {
          if (zoneCounts[z] !== undefined) zoneCounts[z]++;
        });
        var avgB = (
          Bvals.reduce(function (a, b) {
            return a + b;
          }, 0) / Bvals.length
        ).toFixed(1);
        var minBi = Bvals.indexOf(Math.min.apply(null, Bvals));
        var maxBi = Bvals.indexOf(Math.max.apply(null, Bvals));

        var infoEl = document.getElementById("balance-radar-info-" + idSuffix);
        if (infoEl) {
          infoEl.innerHTML =
            '<div style="background:#f0f2f5;border-radius:8px;padding:12px 14px;font-size:12px;margin-bottom:14px;">' +
            '<div style="font-weight:700;color:#111;margin-bottom:6px;font-size:13px;">Balance Summary</div>' +
            '<div>Chain avg: <b>' +
            avgB +
            "%</b></div>" +
            "<div>Highest: <b>" +
            Math.max.apply(null, Bvals).toFixed(1) +
            "%</b> (Ph\u202f" +
            ids[maxBi] +
            ")</div>" +
            "<div>Lowest: <b>" +
            Math.min.apply(null, Bvals).toFixed(1) +
            "%</b> (Ph\u202f" +
            ids[minBi] +
            ")</div>" +
            '</div>' +
            '<div style="background:#f0f2f5;border-radius:8px;padding:12px 14px;font-size:11.5px;">' +
            '<div style="font-weight:700;color:#111;margin-bottom:8px;font-size:13px;">PHI Zone Key</div>' +
            '<table style="border-collapse:collapse;width:100%;font-size:11px;line-height:1.5;">' +
            '<thead><tr style="border-bottom:1px solid #d0d0d0;">' +
            '<th style="text-align:left;padding:0 4px 4px 0;color:#666;font-weight:600;">Zone</th>' +
            '<th style="text-align:right;padding:0 4px 4px;color:#666;font-weight:600;">Balance</th>' +
            '<th style="text-align:right;padding:0 0 4px 4px;color:#666;font-weight:600;">D/C</th>' +
            "</tr></thead><tbody>" +
            '<tr><td style="padding:4px 4px 3px 0;"><span style="display:inline-flex;align-items:center;gap:5px;"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#3ecf8e;"></span><b style="color:#3ecf8e;">C</b> Coherent <b>(' +
            zoneCounts.coherent +
            ')</b></span></td><td style="text-align:right;white-space:nowrap;padding:4px 4px 3px;">≥ 80%</td><td style="text-align:right;white-space:nowrap;padding:4px 0 3px 4px;">≤ 1.50</td></tr>' +
            '<tr><td style="padding:3px 4px 3px 0;"><span style="display:inline-flex;align-items:center;gap:5px;"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#f5a623;"></span><b style="color:#f5a623;">S</b> Stressed <b>(' +
            zoneCounts.stressed +
            ')</b></span></td><td style="text-align:right;white-space:nowrap;padding:3px 4px;">61.8–80%</td><td style="text-align:right;white-space:nowrap;padding:3px 0 3px 4px;">1.50–\u03c6 (2.24)</td></tr>' +
            '<tr><td style="padding:3px 4px 3px 0;"><span style="display:inline-flex;align-items:center;gap:5px;"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#ef5350;"></span><b style="color:#ef5350;">F</b> Failure <b>(' +
            zoneCounts.failure +
            ')</b></span></td><td style="text-align:right;white-space:nowrap;padding:3px 4px;">38.2–61.8%</td><td style="text-align:right;white-space:nowrap;padding:3px 0 3px 4px;">\u03c6\u2013\u03c6\u00b2 (2.24\u20134.24)</td></tr>' +
            '<tr><td style="padding:3px 4px 0 0;"><span style="display:inline-flex;align-items:center;gap:5px;"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#b71c1c;"></span><b style="color:#b71c1c;">B</b> Breakdown <b>(' +
            zoneCounts.breakdown +
            ')</b></span></td><td style="text-align:right;white-space:nowrap;padding:3px 4px 0;">&lt; 38.2%</td><td style="text-align:right;white-space:nowrap;padding:3px 0 0 4px;">&gt; \u03c6\u00b2 (4.24)</td></tr>' +
            "</tbody></table>" +
            "<div style=\"margin-top:8px;font-size:10.5px;color:#666;\">Polygon edge color follows each phase\'s zone. Rings mark PHI thresholds.</div>" +
            "</div>";
        }

        var stressed2 = ids.filter(function (id, i) {
          return zoneKeys[i] === "stressed";
        });
        var failure2 = ids.filter(function (id, i) {
          return zoneKeys[i] === "failure";
        });
        var breakdown2 = ids.filter(function (id, i) {
          return zoneKeys[i] === "breakdown";
        });
        var interp = [];
        interp.push(
          "<strong>Reading this chart:</strong> This chart plots only the balance score per phase on a 0–100% axis. The three coloured rings are structural thresholds derived from the golden ratio φ. A phase's position relative to the rings shows whether it is coherent, stressed, in failure, or in breakdown."
        );
        if (stressed2.length)
          interp.push(
            "<strong>Stressed phases (amber, " +
              stressed2.join(", ") +
              "):</strong> Above the 61.8% φ\u207b\u00b9 floor but below 80%. Self-sustaining; imbalance correctable from within the system."
          );
        if (failure2.length)
          interp.push(
            "<strong>Failure-zone phases (red, " +
              failure2.join(", ") +
              "):</strong> Below the 61.8% sustainability floor. Cost export; external policy or capital typically required."
          );
        if (breakdown2.length)
          interp.push(
            "<strong>Breakdown phases (dark red, " +
              breakdown2.join(", ") +
              "):</strong> Below 38.2%. Constraint dominates contribution by more than φ\u00b2:1."
          );
        if (!stressed2.length && !failure2.length && !breakdown2.length)
          interp.push(
            "<strong>All phases coherent:</strong> Every phase sits above the 80% floor."
          );

        var interpEl = document.getElementById("balance-radar-interp-" + idSuffix);
        if (interpEl) {
          var border = cfg.borderColor || "#c9922a";
          interpEl.style.borderLeftColor = border;
          interpEl.innerHTML = interp.join("<br><br>");
        }
      });
  }

  global.renderPhiBalanceRadar = renderPhiBalanceRadar;
})(typeof window !== "undefined" ? window : this);
