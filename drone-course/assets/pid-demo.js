document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('pid-chart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const ids = ['kp', 'ki', 'kd'];
  const inputs = Object.fromEntries(ids.map(id => [id, document.getElementById(id)]));
  const labels = Object.fromEntries(ids.map(id => [id, document.getElementById(id + '-value')]));
  const metrics = document.getElementById('pid-metrics');
  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
  function simulate() {
    const kp = +inputs.kp.value, ki = +inputs.ki.value, kd = +inputs.kd.value;
    ids.forEach(id => labels[id].textContent = (+inputs[id].value).toFixed(id === 'kd' ? 4 : 3));
    const dt = .002, n = 1500, j = .02, damping = .006, motorTau = .025;
    const target = 10 * Math.PI / 180;
    let angle = 0, rate = 0, torque = 0, integral = 0, dFilt = 0, prevRate = 0;
    const points = [];
    let peak = -Infinity, held = 0;
    for (let k = 0; k <= n; k++) {
      const t = k * dt, angleSp = t >= .4 ? target : 0;
      const rateSp = clamp(4 * (angleSp - angle), -2, 2);
      const error = rateSp - rate;
      const rawD = -(rate - prevRate) / dt;
      prevRate = rate;
      dFilt += (1 - Math.exp(-2 * Math.PI * 30 * dt)) * (rawD - dFilt);
      const iCandidate = clamp(integral + ki * error * dt, -.1, .1);
      const tentative = kp * error + iCandidate + kd * dFilt;
      if (!((tentative > .25 && error > 0) || (tentative < -.25 && error < 0))) integral = iCandidate;
      const torqueCmd = clamp(kp * error + integral + kd * dFilt, -.25, .25);
      torque += (torqueCmd - torque) * dt / motorTau;
      rate += (torque - damping * rate) / j * dt;
      angle += rate * dt;
      points.push([t, angle * 180 / Math.PI]);
      if (t >= .4) peak = Math.max(peak, angle * 180 / Math.PI);
      if (t >= 2.5) held = angle * 180 / Math.PI;
    }
    const w = canvas.width, h = canvas.height, left = 54, right = 18, top = 24, bottom = 40;
    const x = t => left + t / 3 * (w - left - right);
    const y = deg => h - bottom - (deg + 2) / 18 * (h - top - bottom);
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#f9fcff'; ctx.fillRect(0, 0, w, h);
    ctx.font = '13px system-ui'; ctx.textAlign = 'right';
    for (let deg = 0; deg <= 15; deg += 5) {
      ctx.beginPath(); ctx.moveTo(left, y(deg)); ctx.lineTo(w - right, y(deg));
      ctx.strokeStyle = '#dae5ef'; ctx.stroke(); ctx.fillStyle = '#5b7087';
      ctx.fillText(deg + '°', left - 8, y(deg) + 4);
    }
    ctx.textAlign = 'center';
    for (let t = 0; t <= 3.01; t += .5) {
      ctx.fillStyle = '#5b7087'; ctx.fillText(t.toFixed(1) + 's', x(t), h - 12);
    }
    ctx.beginPath(); ctx.moveTo(x(0), y(0)); ctx.lineTo(x(.4), y(0));
    ctx.lineTo(x(.4), y(10)); ctx.lineTo(x(3), y(10));
    ctx.strokeStyle = '#d47a2c'; ctx.lineWidth = 2; ctx.setLineDash([7, 5]); ctx.stroke(); ctx.setLineDash([]);
    ctx.beginPath(); points.forEach(([t, deg], i) => i ? ctx.lineTo(x(t), y(deg)) : ctx.moveTo(x(t), y(deg)));
    ctx.strokeStyle = '#1265a8'; ctx.lineWidth = 3; ctx.stroke();
    ctx.fillStyle = '#1265a8'; ctx.textAlign = 'left'; ctx.fillText('Góc thực', w - 165, top + 10);
    ctx.fillStyle = '#d47a2c'; ctx.fillText('Mục tiêu', w - 165, top + 30);
    metrics.textContent = `Đỉnh: ${peak.toFixed(2)}° · Góc cuối 3 s: ${held.toFixed(2)}° · Mục tiêu: 10°`;
  }
  ids.forEach(id => inputs[id].addEventListener('input', simulate));
  simulate();
});
