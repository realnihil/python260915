const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const W = canvas.width;
const H = canvas.height;
const scoreEl = document.getElementById('score');
const highScoreEl = document.getElementById('highScore');
const bombsEl = document.getElementById('bombs');
const lifeStatusEl = document.getElementById('lifeStatus');
const startPanel = document.getElementById('startPanel');
const gameOverPanel = document.getElementById('gameOverPanel');
const startButton = document.getElementById('startButton');
const restartButton = document.getElementById('restartButton');
const finalScore = document.getElementById('finalScore');

const keys = {};
const audio = { context: null };
let state = 'ready';
let lastTime = 0;
let score = 0;
let highScore = Number(localStorage.getItem('sky-front-high-score') || 0);
let bombs = 2;
let lives = 3;
let spawnTimer = 0;
let shotTimer = 0;
let scroll = 0;
let player;
let bullets = [];
let enemyBullets = [];
let enemies = [];
let particles = [];
let terrain = [];

highScoreEl.textContent = String(highScore).padStart(6, '0');

function setupAudio() {
  if (!audio.context) audio.context = new (window.AudioContext || window.webkitAudioContext)();
  if (audio.context.state === 'suspended') audio.context.resume();
}

function tone(frequency, duration, type = 'square', volume = 0.035, slide = 0) {
  if (!audio.context) return;
  const oscillator = audio.context.createOscillator();
  const gain = audio.context.createGain();
  oscillator.type = type;
  oscillator.frequency.setValueAtTime(frequency, audio.context.currentTime);
  oscillator.frequency.linearRampToValueAtTime(frequency + slide, audio.context.currentTime + duration);
  gain.gain.setValueAtTime(volume, audio.context.currentTime);
  gain.gain.exponentialRampToValueAtTime(.001, audio.context.currentTime + duration);
  oscillator.connect(gain).connect(audio.context.destination);
  oscillator.start();
  oscillator.stop(audio.context.currentTime + duration);
}

function resetGame() {
  score = 0;
  bombs = 2;
  lives = 3;
  scroll = 0;
  spawnTimer = 0;
  shotTimer = 0;
  bullets = [];
  enemyBullets = [];
  enemies = [];
  particles = [];
  terrain = Array.from({ length: 16 }, (_, i) => ({ x: i * 36, y: 570 + Math.random() * 65, w: 15 + Math.random() * 30 }));
  player = { x: W / 2, y: H - 105, w: 28, h: 42, invincible: 0 };
  updateHud();
}

function startGame() {
  setupAudio();
  resetGame();
  state = 'playing';
  startPanel.classList.add('hidden');
  gameOverPanel.classList.add('hidden');
  tone(440, .08, 'sawtooth', .04, 240);
}

function endGame() {
  state = 'gameover';
  finalScore.textContent = String(score).padStart(6, '0');
  gameOverPanel.classList.remove('hidden');
  tone(180, .35, 'sawtooth', .05, -120);
  if (score > highScore) {
    highScore = score;
    localStorage.setItem('sky-front-high-score', highScore);
    highScoreEl.textContent = String(highScore).padStart(6, '0');
  }
}

function updateHud() {
  scoreEl.textContent = String(score).padStart(6, '0');
  bombsEl.textContent = '●'.repeat(bombs) + '○'.repeat(2 - bombs);
  lifeStatusEl.textContent = '●'.repeat(lives) + '○'.repeat(3 - lives);
}

function shoot() {
  if (shotTimer > 0) return;
  bullets.push({ x: player.x, y: player.y - 23, vy: -560, r: 3, color: '#ffe083' });
  shotTimer = .16;
  tone(680, .045, 'square', .025, -220);
}

function bomb() {
  if (bombs <= 0) return;
  bombs -= 1;
  enemies.forEach(enemy => { enemy.hp -= 2; burst(enemy.x, enemy.y, '#f0b323', 8); });
  enemyBullets = [];
  tone(90, .4, 'sawtooth', .06, 360);
  updateHud();
}

function spawnEnemy() {
  const heavy = Math.random() < .22;
  enemies.push({ x: 38 + Math.random() * (W - 76), y: -35, w: heavy ? 42 : 32, h: heavy ? 48 : 35, vy: 62 + Math.random() * 40, hp: heavy ? 3 : 1, maxHp: heavy ? 3 : 1, type: heavy ? 'bomber' : 'fighter', fire: 1 + Math.random() * 2 });
}

function burst(x, y, color, amount = 12) {
  for (let i = 0; i < amount; i++) {
    const angle = Math.random() * Math.PI * 2;
    const speed = 35 + Math.random() * 150;
    particles.push({ x, y, vx: Math.cos(angle) * speed, vy: Math.sin(angle) * speed, life: .35 + Math.random() * .4, color, size: 2 + Math.random() * 3 });
  }
}

function hitPlayer() {
  if (player.invincible > 0) return;
  lives -= 1;
  player.invincible = 2;
  burst(player.x, player.y, '#e65a3d', 22);
  tone(120, .2, 'sawtooth', .06, -50);
  updateHud();
  if (lives <= 0) endGame();
}

function overlaps(a, b) {
  return Math.abs(a.x - b.x) < (a.w + (b.r || b.w)) * .5 && Math.abs(a.y - b.y) < (a.h + (b.r || b.h)) * .5;
}

function update(dt) {
  scroll = (scroll + dt * 90) % 720;
  shotTimer = Math.max(0, shotTimer - dt);
  player.invincible = Math.max(0, player.invincible - dt);
  const directionX = (keys.ArrowRight || keys.d ? 1 : 0) - (keys.ArrowLeft || keys.a ? 1 : 0);
  const directionY = (keys.ArrowDown || keys.s ? 1 : 0) - (keys.ArrowUp || keys.w ? 1 : 0);
  player.x = Math.max(24, Math.min(W - 24, player.x + directionX * 250 * dt));
  player.y = Math.max(70, Math.min(H - 35, player.y + directionY * 220 * dt));
  if (keys[' '] || keys.Spacebar) shoot();
  spawnTimer -= dt;
  if (spawnTimer <= 0) { spawnEnemy(); spawnTimer = .8 + Math.random() * .75; }

  bullets.forEach(bullet => { bullet.y += bullet.vy * dt; });
  bullets = bullets.filter(bullet => bullet.y > -20);
  enemyBullets.forEach(bullet => { bullet.y += bullet.vy * dt; });
  enemyBullets = enemyBullets.filter(bullet => bullet.y < H + 20);

  enemies.forEach(enemy => {
    enemy.y += enemy.vy * dt;
    enemy.fire -= dt;
    if (enemy.fire <= 0 && enemy.y > 0) {
      enemyBullets.push({ x: enemy.x, y: enemy.y + enemy.h / 2, vy: 190, r: 4 });
      enemy.fire = 1.4 + Math.random() * 1.8;
    }
  });

  bullets.forEach(bullet => enemies.forEach(enemy => {
    if (enemy.hp > 0 && overlaps(bullet, enemy)) {
      bullet.y = -100;
      enemy.hp -= 1;
      burst(bullet.x, bullet.y, '#f0b323', 5);
      tone(260, .04, 'square', .018, 100);
      if (enemy.hp <= 0) { score += enemy.type === 'bomber' ? 300 : 100; burst(enemy.x, enemy.y, '#e65a3d', 18); updateHud(); }
    }
  }));
  enemyBullets.forEach(bullet => { if (overlaps(bullet, player)) bullet.y = H + 100, hitPlayer(); });
  enemies.forEach(enemy => { if (enemy.hp > 0 && overlaps(enemy, player)) enemy.hp = 0, burst(enemy.x, enemy.y, '#e65a3d', 16), hitPlayer(); });
  enemies = enemies.filter(enemy => enemy.hp > 0 && enemy.y < H + 70);
  particles.forEach(p => { p.x += p.vx * dt; p.y += p.vy * dt; p.life -= dt; });
  particles = particles.filter(p => p.life > 0);
}

function drawBackground() {
  const gradient = ctx.createLinearGradient(0, 0, 0, H);
  gradient.addColorStop(0, '#0b4f67'); gradient.addColorStop(.58, '#168e9b'); gradient.addColorStop(1, '#f0b323');
  ctx.fillStyle = gradient; ctx.fillRect(0, 0, W, H);
  ctx.globalAlpha = .25;
  for (let i = 0; i < 9; i++) { const y = (i * 105 + scroll) % (H + 120) - 60; ctx.fillStyle = i % 2 ? '#e8e3d5' : '#0b6578'; ctx.fillRect(0, y, W, 18); }
  ctx.globalAlpha = 1;
  terrain.forEach((piece, i) => { const y = (piece.y + scroll * .38) % (H + 100) - 80; ctx.fillStyle = i % 3 === 0 ? '#d5c99e' : '#337f72'; ctx.beginPath(); ctx.moveTo(piece.x, y + 42); ctx.lineTo(piece.x + piece.w / 2, y); ctx.lineTo(piece.x + piece.w, y + 42); ctx.closePath(); ctx.fill(); });
}

function drawPlayer() {
  if (player.invincible > 0 && Math.floor(player.invincible * 10) % 2 === 0) return;
  ctx.save(); ctx.translate(player.x, player.y); ctx.shadowColor = '#ffe083'; ctx.shadowBlur = 12;
  ctx.fillStyle = '#e8e3d5'; ctx.beginPath(); ctx.moveTo(0, -26); ctx.lineTo(8, -7); ctx.lineTo(25, 13); ctx.lineTo(7, 9); ctx.lineTo(0, 21); ctx.lineTo(-7, 9); ctx.lineTo(-25, 13); ctx.lineTo(-8, -7); ctx.closePath(); ctx.fill();
  ctx.fillStyle = '#e65a3d'; ctx.beginPath(); ctx.moveTo(0, -24); ctx.lineTo(4, 10); ctx.lineTo(0, 19); ctx.lineTo(-4, 10); ctx.closePath(); ctx.fill();
  ctx.fillStyle = '#087f82'; ctx.beginPath(); ctx.ellipse(0, -8, 5, 9, 0, 0, Math.PI * 2); ctx.fill(); ctx.restore();
}

function drawEnemy(enemy) {
  ctx.save(); ctx.translate(enemy.x, enemy.y); ctx.fillStyle = enemy.type === 'bomber' ? '#4c4940' : '#33443e'; ctx.strokeStyle = '#d4a44d'; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(0, enemy.h * .55); ctx.lineTo(6, 5); ctx.lineTo(12, -enemy.h * .42); ctx.lineTo(4, -enemy.h * .3); ctx.lineTo(0, -enemy.h * .55); ctx.lineTo(-4, -enemy.h * .3); ctx.lineTo(-12, -enemy.h * .42); ctx.lineTo(-6, 5); ctx.closePath(); ctx.fill(); ctx.stroke();
  ctx.fillStyle = '#b24c32'; ctx.fillRect(-3, -3, 6, 9); ctx.fillStyle = '#e8e3d5'; ctx.fillRect(-enemy.w * .5, -2, enemy.w, 4); ctx.restore();
}

function draw() {
  drawBackground();
  bullets.forEach(b => { ctx.fillStyle = b.color; ctx.fillRect(b.x - 2, b.y - 10, 4, 15); });
  enemyBullets.forEach(b => { ctx.fillStyle = '#e65a3d'; ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2); ctx.fill(); });
  enemies.forEach(drawEnemy); drawPlayer();
  particles.forEach(p => { ctx.globalAlpha = Math.max(0, p.life * 2); ctx.fillStyle = p.color; ctx.fillRect(p.x, p.y, p.size, p.size); }); ctx.globalAlpha = 1;
}

function loop(time) {
  const dt = Math.min(.033, (time - lastTime) / 1000 || 0); lastTime = time;
  if (state === 'playing') update(dt); else { scroll = (scroll + dt * 25) % 720; }
  draw(); requestAnimationFrame(loop);
}

window.addEventListener('keydown', event => { keys[event.key] = true; if ([' ', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(event.key)) event.preventDefault(); if (event.key.toLowerCase() === 'b' && state === 'playing') bomb(); });
window.addEventListener('keyup', event => { keys[event.key] = false; });
startButton.addEventListener('click', startGame); restartButton.addEventListener('click', startGame);
resetGame(); requestAnimationFrame(loop);
