DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>RoboCar Simulator Dashboard</title>
<style>
  body { background:#111; color:#eee; font-family: monospace; text-align:center; }
  canvas { background:#1c1c1c; border:1px solid #444; margin-top:20px; }
  #info { margin-top:12px; font-size:14px; }
  #info span { color:#4ade80; }
  h2 { color:#eee; }
</style>
</head>
<body>
  <h2>RoboCar Simulator Dashboard</h2>
  <canvas id="canvas" width="600" height="600"></canvas>
  <div id="info">Menyambung...</div>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const info = document.getElementById('info');
const SCALE = 15;
const CENTER = 300;
let trail = [];

function drawGrid() {
  ctx.strokeStyle = '#2a2a2a';
  ctx.lineWidth = 1;
  for (let i = 0; i <= 600; i += SCALE * 2) {
    ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, 600); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(600, i); ctx.stroke();
  }
  ctx.strokeStyle = '#555';
  ctx.beginPath(); ctx.moveTo(CENTER, 0); ctx.lineTo(CENTER, 600); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(0, CENTER); ctx.lineTo(600, CENTER); ctx.stroke();
}

function drawCar(x, y, heading) {
  const px = CENTER + x * SCALE;
  const py = CENTER - y * SCALE;
  const rad = -heading * Math.PI / 180;

  trail.push([px, py]);
  if (trail.length > 200) trail.shift();
  ctx.strokeStyle = '#3b82f6';
  ctx.beginPath();
  trail.forEach(([tx, ty], i) => i === 0 ? ctx.moveTo(tx, ty) : ctx.lineTo(tx, ty));
  ctx.stroke();

  ctx.save();
  ctx.translate(px, py);
  ctx.rotate(rad);
  ctx.fillStyle = '#4ade80';
  ctx.beginPath();
  ctx.moveTo(14, 0);
  ctx.lineTo(-10, -8);
  ctx.lineTo(-10, 8);
  ctx.closePath();
  ctx.fill();
  ctx.restore();
}

async function poll() {
  try {
    const res = await fetch('/state');
    const s = await res.json();
    ctx.clearRect(0, 0, 600, 600);
    drawGrid();
    drawCar(s.x, s.y, s.heading);
    info.innerHTML = `x: <span>${s.x.toFixed(2)}</span> | y: <span>${s.y.toFixed(2)}</span> | heading: <span>${s.heading.toFixed(1)}&deg;</span> | speed: <span>${s.speed}</span> | battery: <span>${s.battery.toFixed(1)}%</span>`;
  } catch (e) {
    info.textContent = 'Gagal konek ke server...';
  }
}

drawGrid();
setInterval(poll, 500);
poll();
</script>
</body>
</html>
"""
