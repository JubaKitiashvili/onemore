# Animation & Motion Rules

Comprehensive rules for animation libraries. Follow these when building UI with any of these tools.

---

## 1. Framer Motion (Motion)

### Core API

```jsx
// motion component — the building block
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.4, ease: [0.25, 0.1, 0.25, 1] }}
/>

// whileHover / whileTap — gesture animations
<motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} />

// whileInView — viewport-triggered
<motion.div whileInView={{ opacity: 1 }} viewport={{ once: true, margin: "-100px" }} />

// layout — animate layout changes automatically
<motion.div layout />
```

### Variants (reusable animation states)

```jsx
const variants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4 } },
  exit: { opacity: 0, y: -20 }
};

<motion.div variants={variants} initial="hidden" animate="visible" exit="exit" />
```

### AnimatePresence (exit animations)

```jsx
// REQUIRED: wrap conditional renders for exit animations
<AnimatePresence mode="wait">
  {show && <motion.div key="unique" exit={{ opacity: 0 }} />}
</AnimatePresence>
```

### Rules

- **ALWAYS** use `key` prop on children inside `AnimatePresence`
- **ALWAYS** set `mode="wait"` when swapping between components (prevents overlap)
- **PREFER** variants over inline animation objects for reusability
- **PREFER** `whileInView` with `viewport={{ once: true }}` for scroll reveals (no re-trigger)
- **NEVER** animate `width`/`height` directly — use `layout` prop or `scale` transform instead
- **NEVER** put heavy computation inside `useMotionValue` transforms
- **PREFER** spring transitions for interactive elements: `{ type: "spring", stiffness: 300, damping: 30 }`
- **PREFER** tween with cubic-bezier for scroll-linked: `{ ease: [0.25, 0.1, 0.25, 1] }`
- **USE** `useAnimate` for imperative sequences, `useMotionValue` + `useTransform` for derived values
- **AVOID** re-renders: `style={{ x: motionValue }}` doesn't trigger React re-render, `animate={{ x }}` does

### Performance

- `layout` animations use FLIP — fast but avoid on large lists (>50 items)
- `layoutId` for shared element transitions between routes
- `useTransform` chains are computed outside React render cycle — prefer these for continuous values
- Set `willChange: "transform"` on frequently animated elements

---

## 2. GSAP + ScrollTrigger + @gsap/react

### Core API

```javascript
// Basic tween
gsap.to(".box", { x: 100, duration: 1, ease: "power2.out" });
gsap.from(".box", { opacity: 0, y: 50, duration: 0.8 });
gsap.fromTo(".box", { opacity: 0 }, { opacity: 1, duration: 0.6 });

// Timeline
const tl = gsap.timeline({ defaults: { duration: 0.5, ease: "power2.out" } });
tl.from(".title", { y: 30, opacity: 0 })
  .from(".subtitle", { y: 20, opacity: 0 }, "-=0.3")  // overlap by 0.3s
  .from(".cta", { scale: 0.8, opacity: 0 }, "-=0.2");

// Stagger
gsap.from(".card", { y: 40, opacity: 0, stagger: 0.1, duration: 0.6 });
```

### ScrollTrigger

```javascript
// Basic scroll-triggered animation
gsap.to(".parallax-bg", {
  y: -200,
  ease: "none",
  scrollTrigger: {
    trigger: ".section",
    start: "top bottom",     // trigger-top hits viewport-bottom
    end: "bottom top",       // trigger-bottom hits viewport-top
    scrub: true              // link to scroll position
  }
});

// Pinned section with scrub
gsap.timeline({
  scrollTrigger: {
    trigger: ".hero",
    pin: true,
    start: "top top",
    end: "+=1000",           // pin for 1000px of scroll
    scrub: 1,                // smooth 1s catch-up
    snap: { snapTo: "labels", duration: 0.3 }
  }
})
.addLabel("start")
.to(".hero-text", { opacity: 0, y: -50 })
.addLabel("middle")
.from(".hero-image", { scale: 1.2 })
.addLabel("end");
```

### React Integration (@gsap/react)

```jsx
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(useGSAP, ScrollTrigger);

function Section() {
  const container = useRef();
  const tl = useRef();

  useGSAP(() => {
    // All GSAP code goes inside useGSAP — auto-cleanup guaranteed
    tl.current = gsap.timeline({
      scrollTrigger: {
        trigger: container.current,
        start: "top 80%",
        toggleActions: "play none none reverse"
      }
    });
    tl.current.from(".card", { y: 40, opacity: 0, stagger: 0.15 });
  }, { scope: container }); // scope limits selector queries to container

  return <div ref={container}>...</div>;
}
```

### Rules

- **ALWAYS** use `useGSAP` hook in React — NEVER `useEffect` + manual cleanup
- **ALWAYS** call `gsap.registerPlugin(ScrollTrigger)` before any ScrollTrigger usage
- **ALWAYS** set `scope` option in `useGSAP` to limit DOM queries to component
- **ALWAYS** use `contextSafe()` for event handler animations inside `useGSAP`
- **NEVER** use CSS selectors without scope in React — will leak across components
- **PREFER** `scrub: 1` over `scrub: true` for smoother scroll-linked animations
- **PREFER** `toggleActions: "play none none reverse"` for enter/leave behavior
- **PREFER** `.from()` for reveal animations, `.to()` for exit animations
- **USE** `ease: "none"` for parallax, `ease: "power2.out"` for reveals
- **USE** labels + snap for multi-step pinned sections
- **AVOID** `pin: true` on mobile unless tested — can cause scroll jank
- **STORE** timelines in `useRef` to prevent re-creation on renders
- **MATCH MEDIA** for responsive animations:
  ```javascript
  ScrollTrigger.matchMedia({
    "(min-width: 768px)": () => { /* desktop animations */ },
    "(max-width: 767px)": () => { /* mobile animations */ }
  });
  ```

### Performance

- `will-change: transform` on pinned elements
- Use `fastScrollEnd: true` on ScrollTrigger for better mobile perf
- `gsap.ticker.lagSmoothing(0)` disables lag smoothing if you need frame-accurate
- Batch ScrollTrigger refreshes: `ScrollTrigger.config({ limitCallbacks: true })`
- Kill ScrollTriggers on route change in SPA: `ScrollTrigger.getAll().forEach(t => t.kill())`

---

## 3. Three.js + React Three Fiber (R3F) + Drei

### Three.js Core

```javascript
// Scene setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // cap at 2x
renderer.setSize(width, height);

// Animation loop
renderer.setAnimationLoop((time) => {
  mesh.rotation.y = time * 0.001;
  renderer.render(scene, camera);
});

// CRITICAL: dispose on unmount
renderer.dispose();
geometry.dispose();
material.dispose();
texture.dispose();
```

### React Three Fiber (R3F)

```jsx
import { Canvas, useFrame, useThree } from "@react-three/fiber";

function Scene() {
  return (
    <Canvas
      camera={{ position: [0, 0, 5], fov: 50 }}
      dpr={[1, 2]}                    // responsive pixel ratio
      gl={{ antialias: true, alpha: true }}
      style={{ position: "absolute", top: 0, left: 0 }}
    >
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 5, 5]} />
      <RotatingBox />
    </Canvas>
  );
}

function RotatingBox() {
  const meshRef = useRef();

  useFrame((state, delta) => {
    // delta = time since last frame — frame-rate independent
    meshRef.current.rotation.y += delta * 0.5;
    meshRef.current.position.y = Math.sin(state.clock.elapsedTime) * 0.3;
  });

  return (
    <mesh ref={meshRef}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="royalblue" />
    </mesh>
  );
}
```

### Drei Helpers

```jsx
import { Float, Text3D, Environment, MeshDistortMaterial, Stars, Html } from "@react-three/drei";

// Float — auto floating animation
<Float speed={2} rotationIntensity={1} floatIntensity={0.5}>
  <mesh><sphereGeometry /><meshStandardMaterial /></mesh>
</Float>

// Environment — instant PBR lighting
<Environment preset="sunset" />  // city, dawn, forest, lobby, night, park, studio, sunset, warehouse

// MeshDistortMaterial — animated distortion
<mesh>
  <sphereGeometry args={[1, 64, 64]} />
  <MeshDistortMaterial distort={0.4} speed={2} color="#8B5CF6" />
</mesh>

// Stars — particle starfield
<Stars radius={100} depth={50} count={5000} factor={4} fade speed={1} />

// Html — DOM overlay in 3D
<Html position={[0, 1, 0]} center distanceFactor={10}>
  <div className="label">Hello 3D</div>
</Html>
```

### Rules

- **ALWAYS** dispose geometry, material, and texture on unmount (R3F does this automatically for declared components)
- **ALWAYS** cap `dpr` at `[1, 2]` — higher is wasteful
- **ALWAYS** use `delta` from `useFrame` for frame-rate independent animation
- **NEVER** create new objects inside `useFrame` — causes GC pressure every frame
- **NEVER** set state in `useFrame` — triggers React re-render every frame
- **PREFER** `useRef` + direct mutation over React state for 3D object properties
- **PREFER** `instancedMesh` for >100 identical objects (10,000+ is fine)
- **USE** `Suspense` with `fallback` for async model/texture loading
- **USE** `useLoader.preload()` for critical assets
- **USE** `frameloop="demand"` + `invalidate()` for static scenes (saves battery)
- **AVOID** real-time shadows unless needed — expensive on mobile
- **AVOID** post-processing on mobile — use simpler materials instead

### Performance Budget

- **Triangle count:** <100k for mobile, <500k for desktop
- **Draw calls:** <50 for mobile, <200 for desktop
- **Textures:** max 2048x2048, prefer compressed (KTX2/Basis)
- **Target:** 60fps on mid-range devices
- **Monitor:** `renderer.info.render` for draw calls, `renderer.info.memory` for GPU memory

### ResourceTracker Pattern

```javascript
class ResourceTracker {
  constructor() { this.resources = new Set(); }
  track(resource) {
    if (resource.dispose || resource instanceof THREE.Object3D)
      this.resources.add(resource);
    return resource;
  }
  dispose() {
    for (const resource of this.resources) {
      if (resource instanceof THREE.Object3D && resource.parent)
        resource.parent.remove(resource);
      if (resource.dispose) resource.dispose();
    }
    this.resources.clear();
  }
}
```

---

## 4. Lottie

### Core API

```javascript
import lottie from "lottie-web";

const anim = lottie.loadAnimation({
  container: document.getElementById("lottie"),
  renderer: "svg",          // "svg" | "canvas" | "html"
  loop: true,
  autoplay: true,
  path: "/animations/hero.json",
  // OR: animationData: importedJSON
});

// Control
anim.play();
anim.pause();
anim.stop();
anim.setSpeed(1.5);
anim.goToAndStop(30, true);    // frame 30
anim.playSegments([0, 60], true); // play frames 0-60
anim.setDirection(-1);          // reverse

// Events
anim.addEventListener("complete", () => { /* ... */ });
anim.addEventListener("loopComplete", ({ currentLoop }) => { /* ... */ });
anim.addEventListener("enterFrame", ({ currentTime }) => { /* ... */ });

// CRITICAL: destroy when done
anim.destroy();
```

### React (lottie-react)

```jsx
import Lottie from "lottie-react";
import animationData from "./animation.json";

<Lottie
  animationData={animationData}
  loop={true}
  autoplay={true}
  style={{ width: 200, height: 200 }}
  onComplete={() => {}}
/>
```

### Rules

- **ALWAYS** call `anim.destroy()` on unmount — prevents memory leaks and orphaned DOM nodes
- **ALWAYS** use `renderer: "svg"` for quality, `"canvas"` only for many simultaneous animations
- **PREFER** `animationData` (imported JSON) over `path` (network request) for critical animations
- **PREFER** `playSegments` for micro-interactions (hover states, button feedback)
- **AVOID** `enterFrame` listener unless necessary — fires every frame, expensive
- **AVOID** Lottie for simple transitions — CSS/Framer Motion is lighter
- **USE** Lottie for: complex After Effects animations, icon animations, loading states, illustrations
- **KEEP** JSON files small: <50KB for micro-animations, <200KB for hero animations
- **LAZY LOAD** non-critical Lottie animations with `Suspense` or `IntersectionObserver`

---

## 5. CSS Scroll-Driven Animations

### Scroll Progress Timeline

```css
/* Anonymous scroll timeline — element's own scroller */
.progress-bar {
  animation: grow-width linear;
  animation-timeline: scroll();           /* nearest scroll ancestor */
}

@keyframes grow-width {
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}

/* Named scroll timeline — specific scroller */
.scroll-container {
  scroll-timeline: --main block;          /* name + axis */
}

.animated-child {
  animation: slide-up linear;
  animation-timeline: --main;
}
```

### View Progress Timeline (viewport-triggered)

```css
/* Animate as element scrolls into/out of viewport */
.reveal-card {
  animation: fade-in linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;   /* during entry phase */
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* With inset — trigger zone adjustment */
.reveal-stagger {
  animation: slide-up linear both;
  animation-timeline: view(block 20% 20%);
}

/* Named view timeline */
.tracked-element {
  view-timeline: --card-reveal block;
}

.animated-by-tracked {
  animation-timeline: --card-reveal;
  animation-range: contain 0% contain 100%;
}
```

### Animation Range Values

```
entry    — element entering the scrollport
exit     — element exiting the scrollport
contain  — element fully contained in scrollport
cover    — from first entry edge to last exit edge
```

### Rules

- **ALWAYS** set `animation-duration: 1ms` for Firefox compatibility (auto doesn't work yet)
- **ALWAYS** use `animation-fill-mode: both` with scroll-driven animations
- **PREFER** `view()` over JavaScript IntersectionObserver for simple reveal animations
- **PREFER** CSS scroll-driven over GSAP ScrollTrigger for lightweight parallax/reveals
- **USE** GSAP ScrollTrigger when you need: pinning, snapping, complex timelines, callbacks
- **USE** `animation-range` to precisely control when animation plays relative to viewport
- **TEST** browser support — Chrome 115+, Firefox 110+ (with flag), Safari not yet supported
- **PROVIDE** fallback for unsupported browsers:
  ```css
  @supports (animation-timeline: view()) {
    .reveal { animation: fade-in linear both; animation-timeline: view(); }
  }
  @supports not (animation-timeline: view()) {
    .reveal { opacity: 1; } /* static fallback */
  }
  ```
- **COMBINE** with `prefers-reduced-motion`:
  ```css
  @media (prefers-reduced-motion: reduce) {
    * { animation-timeline: auto !important; }
  }
  ```

---

## 6. SVG Animation & Filters

### Path Drawing Animation

```css
.draw-path {
  stroke-dasharray: 1000;         /* total path length */
  stroke-dashoffset: 1000;        /* hide initially */
  animation: draw 2s ease-out forwards;
}

@keyframes draw {
  to { stroke-dashoffset: 0; }
}
```

```javascript
// Dynamic: get exact path length
const path = document.querySelector("path");
const length = path.getTotalLength();
path.style.strokeDasharray = length;
path.style.strokeDashoffset = length;
```

### SVG Filters — Noise & Grain (Apple-like texture)

```html
<svg width="0" height="0">
  <filter id="noise">
    <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch" />
    <feColorMatrix type="saturate" values="0" />
    <feBlend in="SourceGraphic" mode="multiply" />
  </filter>
</svg>

<style>
  .textured { filter: url(#noise); }
  /* OR as overlay */
  .noise-overlay::before {
    content: "";
    position: absolute;
    inset: 0;
    filter: url(#noise);
    opacity: 0.05;
    pointer-events: none;
    mix-blend-mode: overlay;
  }
</style>
```

### SVG Filter — Glass Blur

```html
<filter id="glass-blur">
  <feGaussianBlur in="SourceGraphic" stdDeviation="10" />
</filter>
```

### SVG Filter — Displacement / Distortion

```html
<filter id="distort">
  <feTurbulence type="turbulence" baseFrequency="0.02" numOctaves="3" result="turbulence" />
  <feDisplacementMap in="SourceGraphic" in2="turbulence" scale="20" />
</filter>
```

### Rules

- **ALWAYS** get actual path length with `getTotalLength()` — don't hardcode
- **ALWAYS** set `pointer-events: none` on SVG filter overlays
- **PREFER** `mix-blend-mode: overlay` for noise textures at 3-8% opacity
- **PREFER** `feTurbulence type="fractalNoise"` for organic textures, `"turbulence"` for distortion
- **KEEP** `baseFrequency` low (0.01-0.1) for subtle effects, higher for aggressive noise
- **USE** `stitchTiles="stitch"` to prevent visible seams in tiled noise
- **AVOID** SVG filters on large areas on mobile — GPU expensive
- **ANIMATE** feTurbulence `baseFrequency` with GSAP for morphing effects (not CSS — SVG attributes need JS)

---

## 7. Modern CSS Color (oklch, oklab, color-mix)

### oklch — Perceptually Uniform Colors

```css
:root {
  /* oklch(lightness chroma hue) */
  --brand-primary: oklch(0.65 0.25 265);    /* vibrant blue */
  --brand-hover:   oklch(0.55 0.25 265);    /* same hue, darker */
  --brand-light:   oklch(0.85 0.10 265);    /* same hue, lighter, less saturated */

  /* Gradient WITHOUT banding (unlike hsl) */
  --gradient: linear-gradient(
    in oklch,
    oklch(0.7 0.25 300),    /* purple */
    oklch(0.7 0.25 200)     /* teal — smooth hue transition */
  );
}
```

### color-mix — Dynamic Color Manipulation

```css
:root {
  --brand: oklch(0.65 0.25 265);
  --brand-10: color-mix(in oklch, var(--brand) 10%, transparent);
  --brand-50: color-mix(in oklch, var(--brand) 50%, white);
  --brand-dark: color-mix(in oklch, var(--brand) 80%, black);
}

/* Hover overlay */
.card:hover {
  background: color-mix(in oklch, var(--brand) 8%, var(--surface));
}
```

### light-dark() — Theme Function

```css
:root {
  color-scheme: light dark;
  --text: light-dark(oklch(0.2 0 0), oklch(0.95 0 0));
  --surface: light-dark(oklch(0.98 0 0), oklch(0.15 0 0));
  --border: light-dark(oklch(0.85 0 0), oklch(0.3 0 0));
}
```

### Rules

- **ALWAYS** use `oklch` for design systems — perceptually uniform, predictable
- **ALWAYS** specify `in oklch` in gradients to prevent muddy mid-tones:
  ```css
  /* BAD */  linear-gradient(blue, yellow)           /* goes through gray */
  /* GOOD */ linear-gradient(in oklch, blue, yellow)  /* vibrant through green */
  ```
- **PREFER** `color-mix(in oklch, ...)` over sass `darken()`/`lighten()`
- **PREFER** `light-dark()` over `@media (prefers-color-scheme)` for simple toggles
- **USE** consistent lightness values for color harmony:
  ```css
  --blue:   oklch(0.65 0.25 265);
  --green:  oklch(0.65 0.20 155);
  --red:    oklch(0.65 0.25 25);
  /* Same L=0.65: they look equally prominent */
  ```
- **KEEP** chroma (C) below 0.3 — higher values may be out of sRGB gamut
- **FALLBACK** for older browsers:
  ```css
  .element {
    color: #3b82f6;                         /* fallback */
    color: oklch(0.65 0.25 265);            /* modern */
  }
  ```

---

## 8. View Transitions API

### Same-Document (SPA)

```javascript
// Basic transition
document.startViewTransition(() => {
  updateDOM(); // your DOM changes
});

// With transition classes for direction
async function navigate(url, isBack = false) {
  if (isBack) document.documentElement.classList.add("back-transition");

  const transition = document.startViewTransition(() => updateDOM(url));

  try {
    await transition.finished;
  } finally {
    document.documentElement.classList.remove("back-transition");
  }
}
```

### CSS Styling

```css
/* Name specific elements for independent transitions */
.hero-image { view-transition-name: hero; }
.page-title { view-transition-name: title; }

/* Custom animation for specific element */
::view-transition-old(hero) {
  animation: 0.3s ease-out shrink;
}
::view-transition-new(hero) {
  animation: 0.3s ease-in grow;
}

/* Default crossfade timing */
::view-transition-group(root) {
  animation-duration: 0.3s;
}

/* Back navigation — slide right */
.back-transition::view-transition-old(root) {
  animation: 0.3s ease-out slide-to-right;
}
.back-transition::view-transition-new(root) {
  animation: 0.3s ease-in slide-from-left;
}
```

### Cross-Document (MPA)

```css
/* In both pages */
@view-transition { navigation: auto; }

/* Source page */
.card { view-transition-name: card-hero; }

/* Destination page */
.hero-banner { view-transition-name: card-hero; }
```

### Rules

- **ALWAYS** use `view-transition-name` for elements that should animate independently
- **ALWAYS** ensure `view-transition-name` is unique per page — duplicates break transitions
- **ALWAYS** provide fallback: `if (!document.startViewTransition) { updateDOM(); return; }`
- **PREFER** short durations (200-400ms) — transitions should feel instant
- **PREFER** `mode: "wait"` equivalent via `transition.ready` / `transition.finished` promises
- **USE** for: page transitions, list reordering, image gallery, tab switching
- **AVOID** for: continuous animations, scroll-linked effects, micro-interactions
- **COMBINE** with `prefers-reduced-motion`:
  ```css
  @media (prefers-reduced-motion: reduce) {
    ::view-transition-group(*) { animation-duration: 0.01s; }
  }
  ```

---

## 9. Web Animations API (WAAPI)

### Core API

```javascript
// element.animate() — the foundation
const animation = element.animate(
  [
    { transform: "translateY(0)", opacity: 1 },
    { transform: "translateY(-20px)", opacity: 0 }
  ],
  {
    duration: 400,
    easing: "cubic-bezier(0.25, 0.1, 0.25, 1)",
    fill: "forwards",
    delay: 100
  }
);

// Control
animation.pause();
animation.play();
animation.reverse();
animation.cancel();
animation.finish();

// Promises
await animation.finished;

// Playback rate
animation.playbackRate = 2;
animation.updatePlaybackRate(0.5); // smooth rate change
```

### Stagger Pattern

```javascript
document.querySelectorAll(".card").forEach((card, i) => {
  card.animate(
    [
      { opacity: 0, transform: "translateY(30px)" },
      { opacity: 1, transform: "translateY(0)" }
    ],
    {
      duration: 500,
      delay: i * 80,
      fill: "forwards",
      easing: "cubic-bezier(0.25, 0.1, 0.25, 1)"
    }
  );
});
```

### Rules

- **PREFER** WAAPI over CSS animations when you need: JS control, promises, dynamic values, playback rate
- **PREFER** CSS `@keyframes` for static, declarative animations
- **ALWAYS** use `fill: "forwards"` if you want the end state to persist
- **ALWAYS** `await animation.finished` before triggering dependent animations
- **USE** `animation.cancel()` for cleanup on unmount
- **USE** `composite: "add"` to layer animations on the same element
- **AVOID** in React — prefer Framer Motion. WAAPI is best for vanilla JS/Web Components
- **COMBINE** with `IntersectionObserver` for scroll-triggered reveals:
  ```javascript
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.animate([...], { duration: 500, fill: "forwards" });
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });
  ```

---

## 10. Animation Performance Rules

### GPU Compositing — What's Cheap vs Expensive

```
CHEAP (GPU-composited, no layout/paint):
  ✅ transform (translate, scale, rotate, skew)
  ✅ opacity
  ✅ filter (blur, brightness, etc.)
  ✅ clip-path (with will-change)

EXPENSIVE (triggers layout and/or paint):
  ❌ width, height, top, left, right, bottom
  ❌ margin, padding, border-width
  ❌ font-size, line-height
  ❌ box-shadow (paint only, but still expensive)
```

### will-change

```css
/* DO: set before animation starts */
.about-to-animate { will-change: transform, opacity; }

/* DON'T: set on everything */
* { will-change: transform; } /* ❌ wastes GPU memory */

/* DO: remove after animation ends */
element.addEventListener("transitionend", () => {
  element.style.willChange = "auto";
});
```

### Layout Thrashing Prevention

```javascript
// BAD — forces layout on every iteration
elements.forEach(el => {
  const height = el.offsetHeight;     // read → force layout
  el.style.height = height * 2 + "px"; // write → invalidate layout
});

// GOOD — batch reads, then batch writes
const heights = elements.map(el => el.offsetHeight); // all reads
elements.forEach((el, i) => {
  el.style.height = heights[i] * 2 + "px";           // all writes
});

// BEST — use requestAnimationFrame
function animate() {
  // reads
  const rect = element.getBoundingClientRect();
  // writes in next frame
  requestAnimationFrame(() => {
    element.style.transform = `translateX(${rect.x}px)`;
  });
}
```

### content-visibility

```css
/* Offscreen sections skip rendering entirely */
.section {
  content-visibility: auto;
  contain-intrinsic-size: auto 500px; /* estimated height */
}
```

### Web Vitals Impact

```
CLS (Cumulative Layout Shift):
  - NEVER animate layout properties (width, height, margin)
  - ALWAYS set explicit dimensions on animated elements
  - USE transform instead of top/left for position changes

INP (Interaction to Next Paint):
  - KEEP animation callbacks under 50ms
  - USE requestAnimationFrame, not setTimeout for visual updates
  - DEFER non-critical animations with requestIdleCallback

LCP (Largest Contentful Paint):
  - DON'T animate LCP elements on load — show them immediately
  - DEFER hero animations until after LCP fires
  - PRELOAD critical animation assets (Lottie JSON, 3D models)
```

### requestAnimationFrame Patterns

```javascript
// Correct RAF loop with cleanup
let rafId;
function loop(time) {
  // animation logic using time
  rafId = requestAnimationFrame(loop);
}
rafId = requestAnimationFrame(loop);

// Cleanup
cancelAnimationFrame(rafId);

// Throttled RAF (e.g., for scroll handlers)
let ticking = false;
window.addEventListener("scroll", () => {
  if (!ticking) {
    requestAnimationFrame(() => {
      updateAnimation();
      ticking = false;
    });
    ticking = true;
  }
});
```

### prefers-reduced-motion (MANDATORY)

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

```javascript
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
if (prefersReducedMotion.matches) {
  // skip GSAP/Three.js/Lottie animations
  gsap.globalTimeline.timeScale(100); // effectively instant
}
```

---

## 11. GLSL Basics (for Three.js custom effects)

### Vertex Shader

```glsl
varying vec2 vUv;
varying float vElevation;

uniform float uTime;
uniform float uFrequency;
uniform float uAmplitude;

void main() {
  vUv = uv;
  vec3 pos = position;

  // Wavy displacement
  float elevation = sin(pos.x * uFrequency + uTime) * uAmplitude;
  elevation += sin(pos.y * uFrequency * 0.8 + uTime * 1.2) * uAmplitude * 0.5;
  pos.z += elevation;

  vElevation = elevation;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
```

### Fragment Shader

```glsl
varying vec2 vUv;
varying float vElevation;

uniform vec3 uColor1;
uniform vec3 uColor2;
uniform float uTime;

void main() {
  // Gradient based on elevation
  float mixFactor = (vElevation + 0.5) * 0.5;
  vec3 color = mix(uColor1, uColor2, mixFactor);

  // Add subtle shimmer
  color += 0.05 * sin(vUv.x * 20.0 + uTime * 2.0);

  gl_FragColor = vec4(color, 1.0);
}
```

### R3F Usage

```jsx
function GradientMesh() {
  const meshRef = useRef();
  const uniforms = useRef({
    uTime: { value: 0 },
    uFrequency: { value: 3.0 },
    uAmplitude: { value: 0.15 },
    uColor1: { value: new THREE.Color("#667eea") },
    uColor2: { value: new THREE.Color("#764ba2") },
  });

  useFrame((state) => {
    uniforms.current.uTime.value = state.clock.elapsedTime;
  });

  return (
    <mesh ref={meshRef}>
      <planeGeometry args={[4, 4, 64, 64]} />
      <shaderMaterial
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={uniforms.current}
      />
    </mesh>
  );
}
```

### Common Noise Functions

```glsl
// Simple 2D noise (include in shaders)
float random(vec2 st) {
  return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453);
}

// Smooth noise
float noise(vec2 st) {
  vec2 i = floor(st);
  vec2 f = fract(st);
  float a = random(i);
  float b = random(i + vec2(1.0, 0.0));
  float c = random(i + vec2(0.0, 1.0));
  float d = random(i + vec2(1.0, 1.0));
  vec2 u = f * f * (3.0 - 2.0 * f); // smoothstep
  return mix(a, b, u.x) + (c - a) * u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
}
```

### Rules

- **ALWAYS** use `uniforms` for values that change (time, mouse, scroll) — never hardcode
- **ALWAYS** update uniforms in `useFrame`, not React state
- **NEVER** allocate new `THREE.Color`/`THREE.Vector` objects in `useFrame`
- **PREFER** `smoothstep` over `mix` for organic transitions
- **USE** `varying` to pass data from vertex to fragment shader
- **KEEP** fragment shaders simple — they run per-pixel at 60fps
- **PROFILE** shader complexity with `renderer.info.programs`
- **COMMON PATTERNS:** noise for organic textures, `sin(uTime)` for pulsing, `mix()` for gradients, `step()`/`smoothstep()` for hard/soft edges

---

## Quick Reference: When to Use What

| Need | Use |
|------|-----|
| React component animation | Framer Motion |
| Scroll-linked complex timeline | GSAP + ScrollTrigger |
| Scroll-linked simple reveal | CSS `animation-timeline: view()` |
| 3D scene / particles / effects | Three.js + R3F + Drei |
| Complex After Effects animation | Lottie |
| Page/route transitions | View Transitions API |
| Vanilla JS animation control | WAAPI |
| Noise/grain texture | SVG filters |
| Path drawing animation | SVG stroke-dasharray |
| Custom 3D effects | GLSL shaders |
| Color system / gradients | oklch + color-mix |
| Simple hover/focus | CSS transitions (no library needed) |

## Universal Rules

1. **prefers-reduced-motion** — ALWAYS respected, in every library
2. **GPU-only properties** — only animate `transform`, `opacity`, `filter`, `clip-path`
3. **Clean up** — destroy/dispose/cancel on unmount, always
4. **Frame-rate independence** — use `delta` time, never assume 60fps
5. **Mobile-first** — test on real devices, reduce complexity on mobile
6. **Progressive enhancement** — animations enhance, never block content
7. **No layout animation** — never animate width, height, top, left, margin, padding
8. **Lazy load** — defer non-critical animations until after LCP
