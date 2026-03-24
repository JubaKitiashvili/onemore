# Visual Generation Rules — Code-Based Art

How to create rich visuals without image files. SVG illustrations, CSS art, Canvas generative graphics, and Three.js 3D scenes — all written as code.

---

## 1. SVG Illustrations

### Hero Illustrations

```svg
<!-- Abstract device mockup -->
<svg viewBox="0 0 800 600" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Screen bezel -->
  <rect x="150" y="50" width="500" height="340" rx="16" fill="#1d1d1f"/>
  <!-- Screen -->
  <rect x="162" y="62" width="476" height="316" rx="8" fill="#000"/>
  <!-- Screen content: gradient -->
  <defs>
    <linearGradient id="screen-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#667eea"/>
      <stop offset="100%" stop-color="#764ba2"/>
    </linearGradient>
  </defs>
  <rect x="162" y="62" width="476" height="316" rx="8" fill="url(#screen-grad)" opacity="0.9"/>
  <!-- UI elements on screen -->
  <rect x="185" y="85" width="120" height="12" rx="6" fill="rgba(255,255,255,0.3)"/>
  <rect x="185" y="110" width="200" height="8" rx="4" fill="rgba(255,255,255,0.15)"/>
  <rect x="185" y="130" width="160" height="8" rx="4" fill="rgba(255,255,255,0.15)"/>
  <!-- Stand -->
  <path d="M350 390 L450 390 L470 460 L330 460 Z" fill="#2c2c2e"/>
  <rect x="310" y="455" width="180" height="8" rx="4" fill="#3a3a3c"/>
</svg>
```

### Abstract Geometric Compositions

```svg
<!-- Layered circles composition -->
<svg viewBox="0 0 400 400" fill="none">
  <defs>
    <radialGradient id="g1" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#007AFF" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#007AFF" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="g2" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#5856D6" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#5856D6" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <!-- Overlapping gradient circles -->
  <circle cx="160" cy="180" r="120" fill="url(#g1)"/>
  <circle cx="240" cy="200" r="140" fill="url(#g2)"/>
  <circle cx="200" cy="160" r="80" fill="url(#g1)" opacity="0.5"/>
  <!-- Accent ring -->
  <circle cx="200" cy="200" r="100" stroke="#007AFF" stroke-width="0.5" fill="none" opacity="0.3"/>
  <circle cx="200" cy="200" r="150" stroke="#5856D6" stroke-width="0.3" fill="none" opacity="0.2"/>
</svg>
```

### Isometric UI Cards

```svg
<!-- Isometric card stack (3D effect with 2D SVG) -->
<svg viewBox="0 0 500 400" fill="none">
  <defs>
    <filter id="card-shadow">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-opacity="0.1"/>
    </filter>
  </defs>
  <!-- Back card -->
  <g transform="translate(50, 20) skewY(-5) skewX(10)">
    <rect width="300" height="180" rx="12" fill="#f5f5f7" filter="url(#card-shadow)"/>
    <rect x="20" y="20" width="80" height="8" rx="4" fill="#86868b"/>
    <rect x="20" y="40" width="180" height="6" rx="3" fill="#d1d1d6"/>
  </g>
  <!-- Middle card -->
  <g transform="translate(80, 60) skewY(-5) skewX(10)">
    <rect width="300" height="180" rx="12" fill="white" filter="url(#card-shadow)"/>
    <rect x="20" y="20" width="100" height="8" rx="4" fill="#1d1d1f"/>
    <rect x="20" y="40" width="200" height="6" rx="3" fill="#86868b"/>
    <circle cx="260" cy="30" r="16" fill="#34C759" opacity="0.2"/>
  </g>
  <!-- Front card -->
  <g transform="translate(110, 100) skewY(-5) skewX(10)">
    <rect width="300" height="180" rx="12" fill="white" filter="url(#card-shadow)"/>
    <rect x="20" y="20" width="120" height="10" rx="5" fill="#1d1d1f"/>
    <rect x="20" y="44" width="260" height="6" rx="3" fill="#86868b"/>
    <rect x="20" y="62" width="220" height="6" rx="3" fill="#d1d1d6"/>
    <!-- Mini chart -->
    <polyline points="20,140 60,120 100,130 140,100 180,110 220,80 260,90"
              stroke="#007AFF" stroke-width="2" fill="none" stroke-linecap="round"/>
  </g>
</svg>
```

### Icon Illustrations (Feature Icons)

```svg
<!-- Shield icon with gradient -->
<svg viewBox="0 0 64 64" fill="none">
  <defs>
    <linearGradient id="shield-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#34C759"/>
      <stop offset="100%" stop-color="#30D158"/>
    </linearGradient>
  </defs>
  <path d="M32 6 L54 16 V30 C54 44 44 54 32 58 C20 54 10 44 10 30 V16 L32 6Z"
        fill="url(#shield-grad)" opacity="0.15"/>
  <path d="M32 6 L54 16 V30 C54 44 44 54 32 58 C20 54 10 44 10 30 V16 L32 6Z"
        stroke="url(#shield-grad)" stroke-width="1.5" fill="none"/>
  <polyline points="22,32 28,40 42,24" stroke="#34C759" stroke-width="2.5"
            stroke-linecap="round" stroke-linejoin="round"/>
</svg>

<!-- Speed/performance icon -->
<svg viewBox="0 0 64 64" fill="none">
  <defs>
    <linearGradient id="speed-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF9500"/>
      <stop offset="100%" stop-color="#FF3B30"/>
    </linearGradient>
  </defs>
  <circle cx="32" cy="36" r="22" stroke="url(#speed-grad)" stroke-width="1.5" fill="none"
          stroke-dasharray="100 38" transform="rotate(-90 32 36)"/>
  <line x1="32" y1="36" x2="42" y2="22" stroke="url(#speed-grad)" stroke-width="2"
        stroke-linecap="round"/>
  <circle cx="32" cy="36" r="3" fill="url(#speed-grad)"/>
</svg>
```

### Rules for SVG Illustrations

- **ALWAYS** use `viewBox` — never hardcode width/height (responsive)
- **ALWAYS** use `fill="none"` on root SVG — explicit fills on children
- **PREFER** gradients (`linearGradient`, `radialGradient`) over flat fills
- **PREFER** stroke-based designs for icons (lighter, more Apple-like)
- **USE** opacity layers (0.1-0.3) for depth and atmosphere
- **USE** `filter: drop-shadow()` for elevation, not `box-shadow`
- **USE** `rx` on rects for rounded corners (match the design system)
- **KEEP** illustrations abstract/geometric — not photorealistic
- **COMPOSE** with overlapping shapes at different opacities
- **ANIMATE** with CSS: `stroke-dashoffset` for drawing, `transform` for motion

---

## 2. CSS Gradient Art

### Gradient Mesh Background

```css
/* Multi-stop gradient mesh — creates depth like Apple's hero sections */
.gradient-mesh {
  background:
    radial-gradient(ellipse 80% 50% at 20% 80%, rgba(0, 122, 255, 0.08) 0%, transparent 50%),
    radial-gradient(ellipse 60% 80% at 80% 20%, rgba(88, 86, 214, 0.06) 0%, transparent 50%),
    radial-gradient(ellipse 90% 60% at 50% 50%, rgba(175, 82, 222, 0.04) 0%, transparent 60%),
    radial-gradient(ellipse 50% 40% at 70% 70%, rgba(255, 45, 85, 0.03) 0%, transparent 40%);
  background-color: #fbfbfd;
}

/* Dark mode variant */
@media (prefers-color-scheme: dark) {
  .gradient-mesh {
    background:
      radial-gradient(ellipse 80% 50% at 20% 80%, rgba(0, 122, 255, 0.12) 0%, transparent 50%),
      radial-gradient(ellipse 60% 80% at 80% 20%, rgba(88, 86, 214, 0.10) 0%, transparent 50%),
      radial-gradient(ellipse 90% 60% at 50% 50%, rgba(175, 82, 222, 0.06) 0%, transparent 60%);
    background-color: #1d1d1f;
  }
}
```

### Aurora / Northern Lights Effect

```css
.aurora {
  position: relative;
  overflow: hidden;
}
.aurora::before {
  content: "";
  position: absolute;
  inset: -50%;
  background:
    conic-gradient(
      from 0deg at 50% 50%,
      rgba(0, 122, 255, 0.1),
      rgba(88, 86, 214, 0.08),
      rgba(175, 82, 222, 0.06),
      rgba(52, 199, 89, 0.04),
      rgba(0, 122, 255, 0.1)
    );
  filter: blur(80px);
  animation: aurora-rotate 20s linear infinite;
}

@keyframes aurora-rotate {
  to { transform: rotate(360deg); }
}

@media (prefers-reduced-motion: reduce) {
  .aurora::before { animation: none; }
}
```

### Animated Gradient Text

```css
.gradient-text {
  background: linear-gradient(
    135deg,
    #1d1d1f 0%,
    #007AFF 25%,
    #5856D6 50%,
    #AF52DE 75%,
    #1d1d1f 100%
  );
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradient-flow 6s linear infinite;
}

@keyframes gradient-flow {
  0% { background-position: 0% center; }
  100% { background-position: 200% center; }
}
```

### Glass Card

```css
.glass-card {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  box-shadow:
    0 1px 3px rgba(0, 0, 0, 0.04),
    0 4px 12px rgba(0, 0, 0, 0.06);
}

@media (prefers-color-scheme: dark) {
  .glass-card {
    background: rgba(30, 30, 30, 0.6);
    border-color: rgba(255, 255, 255, 0.08);
  }
}
```

### Floating Orbs (Ambient Background)

```css
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
  will-change: transform;
}

.orb-1 {
  width: 400px; height: 400px;
  background: rgba(0, 122, 255, 0.06);
  top: 10%; left: 20%;
  animation: drift-1 25s ease-in-out infinite alternate;
}

.orb-2 {
  width: 300px; height: 300px;
  background: rgba(88, 86, 214, 0.05);
  top: 40%; right: 15%;
  animation: drift-2 30s ease-in-out infinite alternate;
}

.orb-3 {
  width: 350px; height: 350px;
  background: rgba(175, 82, 222, 0.04);
  bottom: 20%; left: 40%;
  animation: drift-3 28s ease-in-out infinite alternate;
}

@keyframes drift-1 {
  0% { transform: translate(0, 0); }
  50% { transform: translate(30px, -40px); }
  100% { transform: translate(-20px, 20px); }
}
@keyframes drift-2 {
  0% { transform: translate(0, 0); }
  50% { transform: translate(-40px, 30px); }
  100% { transform: translate(20px, -30px); }
}
@keyframes drift-3 {
  0% { transform: translate(0, 0); }
  50% { transform: translate(25px, 25px); }
  100% { transform: translate(-30px, -20px); }
}

@media (prefers-reduced-motion: reduce) {
  .orb { animation: none; }
}
```

### Rules for CSS Gradient Art

- **ALWAYS** use low opacity (0.03-0.12) for gradient meshes — Apple never uses loud backgrounds
- **ALWAYS** provide dark mode variants with slightly higher opacity
- **PREFER** `radial-gradient(ellipse)` over circular for more organic shapes
- **USE** `conic-gradient` for rotating/aurora effects
- **USE** `filter: blur(60-120px)` on orbs — never sharp-edged
- **LAYER** 3-5 gradients for depth — single gradients look flat
- **ANIMATE** slowly (20-30s cycles) — ambient motion should be barely noticeable
- **CAP** at 3-4 orbs per section — more causes GPU strain

---

## 3. Canvas Generative Art

### Particle Constellation

```javascript
class ParticleField {
  constructor(canvas, options = {}) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.particles = [];
    this.count = options.count || 60;
    this.color = options.color || "rgba(0, 122, 255, 0.4)";
    this.lineColor = options.lineColor || "rgba(0, 122, 255, 0.06)";
    this.maxDistance = options.maxDistance || 120;
    this.speed = options.speed || 0.3;
    this.resize();
    this.init();
    this.rafId = null;
  }

  resize() {
    this.canvas.width = this.canvas.offsetWidth * window.devicePixelRatio;
    this.canvas.height = this.canvas.offsetHeight * window.devicePixelRatio;
    this.ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
  }

  init() {
    const w = this.canvas.offsetWidth;
    const h = this.canvas.offsetHeight;
    this.particles = Array.from({ length: this.count }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * this.speed,
      vy: (Math.random() - 0.5) * this.speed,
      r: Math.random() * 2 + 1,
      alpha: Math.random() * 0.5 + 0.2,
    }));
  }

  draw() {
    const w = this.canvas.offsetWidth;
    const h = this.canvas.offsetHeight;
    this.ctx.clearRect(0, 0, w, h);

    // Draw connections
    for (let i = 0; i < this.particles.length; i++) {
      for (let j = i + 1; j < this.particles.length; j++) {
        const dx = this.particles[i].x - this.particles[j].x;
        const dy = this.particles[i].y - this.particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < this.maxDistance) {
          const opacity = 1 - dist / this.maxDistance;
          this.ctx.beginPath();
          this.ctx.strokeStyle = this.lineColor.replace(/[\d.]+\)$/, `${opacity * 0.15})`);
          this.ctx.lineWidth = 0.5;
          this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
          this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
          this.ctx.stroke();
        }
      }
    }

    // Draw particles
    for (const p of this.particles) {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > w) p.vx *= -1;
      if (p.y < 0 || p.y > h) p.vy *= -1;

      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      this.ctx.fillStyle = this.color.replace(/[\d.]+\)$/, `${p.alpha})`);
      this.ctx.fill();
    }
  }

  start() {
    const loop = () => {
      this.draw();
      this.rafId = requestAnimationFrame(loop);
    };
    this.rafId = requestAnimationFrame(loop);
  }

  stop() {
    if (this.rafId) cancelAnimationFrame(this.rafId);
  }

  destroy() {
    this.stop();
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
  }
}

// Usage
const canvas = document.getElementById("particles");
const field = new ParticleField(canvas, { count: 50, color: "rgba(0, 122, 255, 0.4)" });

// Respect reduced motion
if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  field.start();
}

// Pause when tab hidden
document.addEventListener("visibilitychange", () => {
  document.hidden ? field.stop() : field.start();
});
```

### Wave / Sine Animation

```javascript
class WaveAnimation {
  constructor(canvas, options = {}) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.waves = options.waves || [
      { amplitude: 20, frequency: 0.02, speed: 0.02, color: "rgba(0, 122, 255, 0.1)" },
      { amplitude: 15, frequency: 0.03, speed: 0.015, color: "rgba(88, 86, 214, 0.08)" },
      { amplitude: 10, frequency: 0.01, speed: 0.025, color: "rgba(175, 82, 222, 0.06)" },
    ];
    this.phase = 0;
    this.resize();
  }

  resize() {
    this.canvas.width = this.canvas.offsetWidth * window.devicePixelRatio;
    this.canvas.height = this.canvas.offsetHeight * window.devicePixelRatio;
    this.ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
  }

  draw() {
    const w = this.canvas.offsetWidth;
    const h = this.canvas.offsetHeight;
    this.ctx.clearRect(0, 0, w, h);
    this.phase += 1;

    for (const wave of this.waves) {
      this.ctx.beginPath();
      this.ctx.moveTo(0, h / 2);

      for (let x = 0; x <= w; x++) {
        const y = h / 2 +
          Math.sin(x * wave.frequency + this.phase * wave.speed) * wave.amplitude +
          Math.sin(x * wave.frequency * 0.5 + this.phase * wave.speed * 1.3) * wave.amplitude * 0.5;
        this.ctx.lineTo(x, y);
      }

      this.ctx.lineTo(w, h);
      this.ctx.lineTo(0, h);
      this.ctx.closePath();
      this.ctx.fillStyle = wave.color;
      this.ctx.fill();
    }
  }

  start() {
    const loop = () => {
      this.draw();
      this.rafId = requestAnimationFrame(loop);
    };
    this.rafId = requestAnimationFrame(loop);
  }

  stop() {
    if (this.rafId) cancelAnimationFrame(this.rafId);
  }
}
```

### Data Visualization (Animated Chart)

```javascript
function drawAnimatedLineChart(canvas, data, options = {}) {
  const ctx = canvas.getContext("2d");
  const w = canvas.offsetWidth;
  const h = canvas.offsetHeight;
  const padding = options.padding || 40;
  const color = options.color || "#007AFF";
  const duration = options.duration || 1500;

  const maxVal = Math.max(...data);
  const minVal = Math.min(...data);
  const range = maxVal - minVal || 1;

  const points = data.map((val, i) => ({
    x: padding + (i / (data.length - 1)) * (w - padding * 2),
    y: h - padding - ((val - minVal) / range) * (h - padding * 2),
  }));

  let progress = 0;
  const startTime = performance.now();

  function draw(now) {
    progress = Math.min((now - startTime) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic

    ctx.clearRect(0, 0, w, h);

    // Draw line
    const drawTo = Math.floor(eased * (points.length - 1));
    ctx.beginPath();
    ctx.moveTo(points[0].x, points[0].y);

    for (let i = 1; i <= drawTo; i++) {
      ctx.lineTo(points[i].x, points[i].y);
    }

    // Interpolate partial segment
    if (drawTo < points.length - 1) {
      const frac = (eased * (points.length - 1)) - drawTo;
      const nx = points[drawTo].x + (points[drawTo + 1].x - points[drawTo].x) * frac;
      const ny = points[drawTo].y + (points[drawTo + 1].y - points[drawTo].y) * frac;
      ctx.lineTo(nx, ny);
    }

    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.stroke();

    // Area fill
    ctx.lineTo(points[Math.min(drawTo + 1, points.length - 1)].x, h - padding);
    ctx.lineTo(points[0].x, h - padding);
    ctx.closePath();
    const gradient = ctx.createLinearGradient(0, 0, 0, h);
    gradient.addColorStop(0, color + "20");
    gradient.addColorStop(1, color + "00");
    ctx.fillStyle = gradient;
    ctx.fill();

    if (progress < 1) requestAnimationFrame(draw);
  }

  requestAnimationFrame(draw);
}
```

### Rules for Canvas

- **ALWAYS** handle DPI: `canvas.width = offsetWidth * devicePixelRatio`
- **ALWAYS** call `cancelAnimationFrame` on cleanup / destroy
- **ALWAYS** pause on `visibilitychange` (tab hidden) — saves battery
- **ALWAYS** respect `prefers-reduced-motion` — show static frame instead
- **PREFER** low particle counts: 40-80 particles max
- **PREFER** subtle colors: opacity 0.05-0.4, never fully opaque
- **USE** connection lines sparingly — max distance 100-150px
- **LIMIT** canvas to background decoration — not primary content
- **RESIZE** on window resize with debounce (250ms)

---

## 4. SVG Filters & Textures

### Noise / Grain Texture

```html
<svg width="0" height="0" style="position: absolute">
  <filter id="grain">
    <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/>
    <feColorMatrix type="saturate" values="0"/>
  </filter>
</svg>

<style>
.grain-overlay::after {
  content: "";
  position: fixed;
  inset: 0;
  background: url("data:image/svg+xml,..."); /* or filter reference */
  filter: url(#grain);
  opacity: 0.03;
  pointer-events: none;
  mix-blend-mode: overlay;
  z-index: 9999;
}
</style>
```

### Glow Effect

```html
<svg width="0" height="0">
  <filter id="glow">
    <feGaussianBlur stdDeviation="3" result="blur"/>
    <feFlood flood-color="#007AFF" flood-opacity="0.3" result="color"/>
    <feComposite in="color" in2="blur" operator="in" result="glow"/>
    <feMerge>
      <feMergeNode in="glow"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
</svg>

<style>
.glow-element { filter: url(#glow); }
</style>
```

### Morphing Blob

```svg
<svg viewBox="0 0 200 200">
  <path fill="rgba(0, 122, 255, 0.1)">
    <animate
      attributeName="d"
      dur="8s"
      repeatCount="indefinite"
      values="
        M 100,50 C 130,30 170,50 180,100 C 190,150 150,180 100,170 C 50,160 20,130 30,100 C 40,70 70,70 100,50 Z;
        M 100,40 C 140,35 175,60 185,110 C 195,160 155,185 100,175 C 45,165 15,135 25,95 C 35,55 60,45 100,40 Z;
        M 100,50 C 130,30 170,50 180,100 C 190,150 150,180 100,170 C 50,160 20,130 30,100 C 40,70 70,70 100,50 Z
      "
    />
  </path>
</svg>
```

### Animated Gradient Border

```css
.gradient-border {
  position: relative;
  border-radius: 16px;
  padding: 1px; /* border thickness */
  background: conic-gradient(
    from var(--angle, 0deg),
    #007AFF, #5856D6, #AF52DE, #FF2D55, #007AFF
  );
  animation: rotate-border 4s linear infinite;
}
.gradient-border > * {
  border-radius: 15px; /* concentric: 16 - 1 = 15 */
  background: white;
}

@property --angle {
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}

@keyframes rotate-border {
  to { --angle: 360deg; }
}
```

---

## 5. CSS Device Mockups

### iPhone Frame

```css
.iphone-frame {
  width: 280px;
  height: 580px;
  border-radius: 44px;
  background: #1d1d1f;
  padding: 14px;
  position: relative;
  box-shadow:
    0 0 0 2px #3a3a3c,
    0 20px 60px rgba(0, 0, 0, 0.3);
}
.iphone-screen {
  width: 100%;
  height: 100%;
  border-radius: 34px; /* 44 - 10 (padding not exact but optical) */
  overflow: hidden;
  background: white;
}
.iphone-notch {
  position: absolute;
  top: 14px;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  height: 28px;
  background: #1d1d1f;
  border-radius: 0 0 20px 20px;
  z-index: 10;
}
```

### Browser Window Frame

```css
.browser-frame {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  border: 1px solid rgba(0, 0, 0, 0.08);
}
.browser-chrome {
  height: 40px;
  background: #f5f5f7;
  display: flex;
  align-items: center;
  padding: 0 16px;
  gap: 8px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}
.browser-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}
.browser-dot:nth-child(1) { background: #FF5F57; }
.browser-dot:nth-child(2) { background: #FFBD2E; }
.browser-dot:nth-child(3) { background: #28C840; }
.browser-url {
  flex: 1;
  height: 24px;
  background: rgba(0, 0, 0, 0.04);
  border-radius: 6px;
  margin-left: 8px;
}
.browser-content {
  /* Your screenshot / content goes here */
  aspect-ratio: 16 / 10;
  background: white;
}
```

### MacBook Frame

```css
.macbook-frame {
  position: relative;
  max-width: 800px;
}
.macbook-screen {
  border-radius: 12px 12px 0 0;
  border: 12px solid #1d1d1f;
  border-bottom: none;
  background: #000;
  aspect-ratio: 16 / 10;
  overflow: hidden;
}
.macbook-base {
  height: 14px;
  background: linear-gradient(to bottom, #c5c5c7, #b0b0b3);
  border-radius: 0 0 8px 8px;
  position: relative;
}
.macbook-base::before {
  content: "";
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 20%;
  height: 4px;
  background: #8e8e93;
  border-radius: 0 0 4px 4px;
}
```

---

## 6. Placeholder System for Real Images

When the design needs a real photo that can't be generated with code:

```html
<!-- Structured placeholder with clear intent -->
<div class="image-placeholder" data-intent="hero-product-shot"
     data-description="Dashboard screenshot showing analytics overview"
     data-aspect="16/9" data-theme="dark">
  <div class="placeholder-content">
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
      <rect x="3" y="3" width="18" height="18" rx="2"/>
      <circle cx="8.5" cy="8.5" r="1.5"/>
      <polyline points="21,15 16,10 5,21"/>
    </svg>
    <span>Product Screenshot</span>
    <span class="placeholder-size">1200 × 675px</span>
  </div>
</div>

<style>
.image-placeholder {
  aspect-ratio: attr(data-aspect);
  background: linear-gradient(135deg, #f5f5f7 0%, #e8e8ed 100%);
  border-radius: 12px;
  border: 2px dashed #d1d1d6;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #86868b;
  flex-direction: column;
  gap: 8px;
  font-size: 14px;
}
</style>
```

### Rules for Placeholders

- **ALWAYS** use `data-intent` to describe what image goes here
- **ALWAYS** specify dimensions / aspect ratio
- **ALWAYS** provide a visual placeholder (not empty space)
- **USE** gradient background that matches the design's color scheme
- **USE** a descriptive label so the user knows what to replace
- **NEVER** use external placeholder services (unsplash API, placeholder.com)

---

## Quick Reference: Visual Technique Selection

| Need | Technique | Complexity |
|------|-----------|------------|
| Hero illustration | SVG composition | Medium |
| Feature icons | SVG with gradient fills | Low |
| Background atmosphere | CSS gradient mesh + orbs | Low |
| Animated background | Canvas particles | Medium |
| Noise/grain texture | SVG feTurbulence filter | Low |
| Glass/blur effect | CSS backdrop-filter | Low |
| Device mockup | CSS shapes | Low |
| Data visualization | Canvas or SVG charts | Medium |
| 3D floating object | Three.js + R3F | High |
| Morphing shapes | SVG animate or GSAP | Medium |
| Gradient border | CSS conic-gradient + @property | Low |
| Text gradient | CSS background-clip | Low |
| Aurora effect | CSS conic-gradient + blur | Low |
| Photo placeholder | HTML + CSS placeholder component | Low |

## Universal Visual Rules

1. **No external images required** — every visual can be code
2. **Opacity restraint** — background effects: 0.03-0.12, never loud
3. **Dark mode** — every visual must work in both themes
4. **Reduced motion** — ambient animations must be pauseable
5. **GPU performance** — use `will-change`, avoid paint-heavy filters on mobile
6. **Semantic meaning** — decorative visuals: `aria-hidden="true"`, `pointer-events: none`
7. **Progressive enhancement** — content works without visuals loading
8. **Responsive SVGs** — always use `viewBox`, never fixed dimensions
