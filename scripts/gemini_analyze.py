#!/usr/bin/env python3
"""
OneMore Video Analyzer — Multi-Provider
Supports Google Gemini and OpenAI GPT-4o for video analysis.
Uses only stdlib — no pip dependencies required.

Usage:
  python3 gemini_analyze.py <video_path> <provider:api_key> <output_dir> [model]

  provider:api_key examples:
    gemini:AIzaSy...     — Google Gemini
    openai:sk-...        — OpenAI GPT-4o

  model (optional): override model selection
    gemini-3.1-pro-preview, gemini-3.1-flash, gpt-4o, etc.
"""

import json
import sys
import os
import time
import base64
import urllib.request
import urllib.error
import mimetypes

# === MODEL PRIORITY ===
GEMINI_MODELS = [
    "gemini-2.5-flash",          # default — fast, cheap, good quality
    "gemini-2.5-pro",            # premium — best available quality
    "gemini-2.0-flash",          # fallback
]

OPENAI_MODEL = "gpt-4o"

GEMINI_UPLOAD_URL = "https://generativelanguage.googleapis.com/upload/v1beta/files"

# === ANALYSIS PROMPT ===
ANALYSIS_PROMPT = """You are a senior front-end engineer reverse-engineering a web page or mobile app from a screen recording video. Analyze this video and produce a structured implementation blueprint.

The video shows a web page being scrolled OR a mobile app being used. Every visual change is caused by: scroll position change, viewport entry, user interaction, or time-based animation.

Your job is to REVERSE-ENGINEER THE IMPLEMENTATION — not describe what things look like.

Analyze and return a JSON object with this exact structure:

{
  "page_type": "web_scroll | mobile_app | prototype_walkthrough",
  "title": "Short descriptive title of what this page/app is",
  "objective": "One sentence: what to build and what it should feel like",

  "visual_architecture": {
    "theme": "dark | light | mixed",
    "background_color": "#hex",
    "typography": {
      "heading_font": "font-family string",
      "body_font": "font-family string",
      "hero_size": "px value",
      "body_size": "px value"
    },
    "color_tokens": {
      "bg": "#hex",
      "surface": "#hex",
      "text_primary": "#hex",
      "text_secondary": "#hex",
      "accent": "#hex"
    },
    "sections": [
      {
        "name": "Section name",
        "description": "One line description",
        "height": "estimated height (100vh, auto, etc)",
        "key_feature": "What makes this section notable"
      }
    ]
  },

  "animations": [
    {
      "name": "Descriptive animation name",
      "trigger": "scroll-linked | scroll-triggered | interaction | time-based | gesture-driven",
      "description": "What happens in one sentence",
      "target": "CSS selector or element description",
      "properties": {
        "property_name": {"from": "start value", "to": "end value"}
      },
      "duration_ms": 0,
      "delay_ms": 0,
      "stagger_ms": 0,
      "easing": "cubic-bezier or named easing or spring config",
      "scroll_model": "scrubbed | one-shot | continuous | null"
    }
  ],

  "interactions": [
    {
      "name": "Interaction name",
      "gesture": "tap | drag | swipe | long-press | pan",
      "target": "What element is interactive",
      "behavior": "What happens when user interacts",
      "implementation": "Specific API or approach (PanGestureHandler, onPress, etc.)"
    }
  ],

  "layer_system": [
    {
      "layer": 0,
      "content": "What's on this layer",
      "scroll_rate": 0.0,
      "notes": "Additional info"
    }
  ],

  "section_transitions": [
    {
      "from_section": "Section A",
      "to_section": "Section B",
      "mechanism": "hard-cut | gradient-blend | color-match-reveal | parallax-reveal | crossfade | scale-reveal | shared-element-morph",
      "details": "How the transition works"
    }
  ],

  "hover_states": [
    {
      "target": "Element description",
      "effect": "What changes on hover/press",
      "properties": {"property": "value"},
      "duration_ms": 0,
      "easing": "easing value"
    }
  ],

  "tech_stack": {
    "framework": "Recommended framework",
    "styling": "CSS approach",
    "animation_library": "GSAP | Framer Motion | Reanimated | CSS | etc",
    "additional_deps": ["list of specific packages needed"],
    "smooth_scroll": "Lenis | null",
    "reason": "Why this stack"
  },

  "accessibility": {
    "reduced_motion_strategy": "How to handle prefers-reduced-motion",
    "contrast_notes": "Any contrast concerns",
    "touch_targets": "Minimum sizes"
  }
}

CRITICAL RULES — Be SPECIFIC with values:
- "scale(0.92 → 1.0)" not "scales up"
- "cubic-bezier(0.25, 0.1, 0.25, 1)" not "smooth"
- "translateY(20px → 0)" not "slides up"
- "spring(mass: 1, stiffness: 100, damping: 12)" not "spring animation"
- "300ms" not "fast"
- "#1d1d1f" not "dark"

CRITICAL RULES — Detection:
- NEVER default to "no animations" for marketing/product landing pages — they almost always have scroll-linked effects.
- If a full-bleed image has dark borders that shrink → scroll-linked scale(0.9x → 1.0) + border-radius change
- If text fades in as section enters → scroll-triggered opacity + translateY stagger
- If text disappears while image stays → scroll-linked opacity fade on text layer
- If background moves slower than foreground → parallax (estimate the rate)
- If an element has a non-rectangular shape → SVG path, clip-path, or custom shape
- If user's finger/cursor drags something → gesture-driven animation (PanGestureHandler, drag)
- If numbers animate → spring counter or interpolated value
- Check for: parallax, scroll-linked scale, text stagger, sticky sections, color-match transitions, SVG shapes, gesture interactions, shared element transitions

Respond with ONLY the JSON object, no markdown code blocks, no explanation.
"""


def get_mime_type(video_path: str) -> str:
    """Detect correct MIME type for video file."""
    ext = os.path.splitext(video_path)[1].lower()
    mime_map = {
        ".mp4": "video/mp4",
        ".mov": "video/quicktime",
        ".webm": "video/webm",
        ".avi": "video/x-msvideo",
        ".mkv": "video/x-matroska",
        ".gif": "image/gif",
    }
    return mime_map.get(ext, mimetypes.guess_type(video_path)[0] or "video/mp4")


# === GEMINI PROVIDER ===

def gemini_upload(video_path: str, api_key: str) -> str:
    """Upload video to Gemini Files API, return file URI."""
    mime_type = get_mime_type(video_path)
    file_size = os.path.getsize(video_path)
    display_name = os.path.basename(video_path)

    headers = {
        "X-Goog-Upload-Protocol": "resumable",
        "X-Goog-Upload-Command": "start",
        "X-Goog-Upload-Header-Content-Length": str(file_size),
        "X-Goog-Upload-Header-Content-Type": mime_type,
        "Content-Type": "application/json",
    }
    metadata = json.dumps({"file": {"display_name": display_name}}).encode()
    req = urllib.request.Request(
        f"{GEMINI_UPLOAD_URL}?key={api_key}", data=metadata, headers=headers, method="POST"
    )
    resp = urllib.request.urlopen(req)
    upload_url = resp.headers.get("X-Goog-Upload-URL")
    if not upload_url:
        raise RuntimeError("Failed to get upload URL from Gemini API")

    with open(video_path, "rb") as f:
        video_data = f.read()

    headers2 = {
        "Content-Length": str(file_size),
        "X-Goog-Upload-Offset": "0",
        "X-Goog-Upload-Command": "upload, finalize",
    }
    req2 = urllib.request.Request(upload_url, data=video_data, headers=headers2, method="PUT")
    resp2 = urllib.request.urlopen(req2)
    result = json.loads(resp2.read().decode())
    file_uri = result["file"]["uri"]
    file_name = result["file"]["name"]

    for _ in range(30):
        check_url = f"https://generativelanguage.googleapis.com/v1beta/{file_name}?key={api_key}"
        check_resp = urllib.request.urlopen(urllib.request.Request(check_url))
        status = json.loads(check_resp.read().decode())
        if status.get("state") == "ACTIVE":
            return file_uri
        if status.get("state") == "FAILED":
            raise RuntimeError(f"Video processing failed: {status}")
        time.sleep(2)

    raise RuntimeError("Video processing timed out (60s)")


def gemini_analyze(file_uri: str, api_key: str, mime_type: str, model_override: str = None) -> dict:
    """Send video to Gemini, try models in priority order. Returns parsed JSON."""
    models = [model_override] if model_override else GEMINI_MODELS

    for model in models:
        generate_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        gen_config = {"temperature": 0.1}

        payload = {
            "contents": [
                {
                    "parts": [
                        {"file_data": {"mime_type": mime_type, "file_uri": file_uri}},
                        {"text": ANALYSIS_PROMPT},
                    ]
                }
            ],
            "generationConfig": gen_config,
        }

        data = json.dumps(payload).encode()
        headers = {"Content-Type": "application/json"}
        req = urllib.request.Request(
            f"{generate_url}?key={api_key}", data=data, headers=headers, method="POST"
        )

        try:
            print(f"  Trying: {model}...", file=sys.stderr)
            resp = urllib.request.urlopen(req, timeout=180)
            result = json.loads(resp.read().decode())
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            print(f"  Success: {model}", file=sys.stderr)
            return _parse_json_response(text), model
        except urllib.error.HTTPError as e:
            if e.code in (429, 400, 404):
                error_body = e.read().decode()[:200] if e.fp else ""
                print(f"  Failed: {model} (HTTP {e.code}) — {error_body[:100]}", file=sys.stderr)
                continue
            raise

    raise RuntimeError(f"All Gemini models exhausted: {', '.join(models)}")


# === OPENAI PROVIDER ===

def openai_analyze(video_path: str, api_key: str, model_override: str = None) -> dict:
    """Extract frames from video and send to OpenAI GPT-4o via Chat Completions API."""
    import subprocess
    import tempfile

    model = model_override or OPENAI_MODEL

    # Extract frames as base64 images (GPT-4o doesn't accept raw video via Chat Completions)
    with tempfile.TemporaryDirectory() as tmpdir:
        # Extract 1 frame per second at 512px width
        subprocess.run([
            "ffmpeg", "-i", video_path, "-vf", "fps=1,scale=512:-1",
            "-q:v", "2", f"{tmpdir}/frame_%03d.jpg"
        ], capture_output=True)

        # Collect frames as base64
        image_parts = []
        for fname in sorted(os.listdir(tmpdir)):
            if fname.endswith(".jpg"):
                with open(os.path.join(tmpdir, fname), "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                image_parts.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{b64}", "detail": "high"}
                })

    if not image_parts:
        raise RuntimeError("Failed to extract frames from video for OpenAI analysis")

    print(f"  Extracted {len(image_parts)} frames for GPT-4o", file=sys.stderr)

    # Build Chat Completions payload
    content = image_parts + [{"type": "text", "text": ANALYSIS_PROMPT + "\n\nRespond with ONLY the JSON object, no markdown or explanation."}]

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "temperature": 0.1,
        "max_tokens": 8192,
    }

    data = json.dumps(payload).encode()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions", data=data, headers=headers, method="POST"
    )

    print(f"  Trying: {model}...", file=sys.stderr)
    resp = urllib.request.urlopen(req, timeout=180)
    result = json.loads(resp.read().decode())

    text = result["choices"][0]["message"]["content"]
    print(f"  Success: {model}", file=sys.stderr)
    return _parse_json_response(text), model


# === SHARED UTILITIES ===

def _parse_json_response(text: str) -> dict:
    """Parse JSON from model response, handling markdown wrapping."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        if "```json" in text:
            return json.loads(text.split("```json")[1].split("```")[0].strip())
        elif "```" in text:
            return json.loads(text.split("```")[1].split("```")[0].strip())
        raise


def analysis_to_build_prompt(analysis: dict, model_used: str = "unknown") -> str:
    """Convert structured JSON to build-prompt.md format."""
    lines = []
    va = analysis.get("visual_architecture", {})
    tokens = va.get("color_tokens", {})
    typo = va.get("typography", {})
    tech = analysis.get("tech_stack", {})

    lines.append(f"# Build Prompt: {analysis.get('title', 'Untitled')}")
    lines.append(f"*Analyzed by: {model_used}*")
    lines.append("")
    lines.append("## Objective")
    lines.append(analysis.get("objective", ""))
    lines.append("")

    # 1. Visual Architecture
    lines.append("## 1. Visual Architecture")
    lines.append(f"- **Theme:** {va.get('theme', 'dark')} — background {va.get('background_color', '#000')}")
    lines.append(f"- **Typography:** Heading: {typo.get('heading_font', 'system-ui')}, Body: {typo.get('body_font', 'system-ui')}")
    lines.append("- **Sections:**")
    for i, sec in enumerate(va.get("sections", []), 1):
        lines.append(f"  {i}. **{sec.get('name', '')}** — {sec.get('description', '')} (height: {sec.get('height', 'auto')})")
    lines.append("")

    # 2. Key Animation Effects
    lines.append("## 2. Key Animation Effects")
    for i, anim in enumerate(analysis.get("animations", []), 1):
        lines.append(f"### Effect {i}: {anim.get('name', '')}")
        lines.append(f"- **Trigger:** {anim.get('trigger', 'unknown')}")
        lines.append(f"- **What happens:** {anim.get('description', '')}")
        props = anim.get("properties", {})
        if props:
            prop_strs = []
            for k, v in props.items():
                if isinstance(v, dict):
                    prop_strs.append(f"`{k}: {v.get('from', '?')} → {v.get('to', '?')}`")
                else:
                    prop_strs.append(f"`{k}: {v}`")
            lines.append(f"- **Properties:** {', '.join(prop_strs)}")
        timing_parts = []
        if anim.get("duration_ms"): timing_parts.append(f"{anim['duration_ms']}ms")
        if anim.get("stagger_ms"): timing_parts.append(f"stagger {anim['stagger_ms']}ms")
        if anim.get("easing"): timing_parts.append(anim["easing"])
        if timing_parts:
            lines.append(f"- **Timing:** {', '.join(timing_parts)}")
        if anim.get("scroll_model"):
            lines.append(f"- **Scroll model:** {anim['scroll_model']}")
        lines.append("")

    # 2b. Interactions (if present)
    interactions = analysis.get("interactions", [])
    if interactions:
        lines.append("## 2b. Gesture Interactions")
        for inter in interactions:
            lines.append(f"### {inter.get('name', '')}")
            lines.append(f"- **Gesture:** {inter.get('gesture', '')}")
            lines.append(f"- **Target:** {inter.get('target', '')}")
            lines.append(f"- **Behavior:** {inter.get('behavior', '')}")
            lines.append(f"- **Implementation:** {inter.get('implementation', '')}")
            lines.append("")

    # 3. Technical Stack
    lines.append("## 3. Technical Stack")
    lines.append(f"- **Framework:** {tech.get('framework', 'Vanilla HTML/CSS/JS')}")
    lines.append(f"- **Styling:** {tech.get('styling', 'CSS')}")
    lines.append(f"- **Animation:** {tech.get('animation_library', 'CSS')}")
    deps = tech.get("additional_deps", [])
    if deps:
        lines.append(f"- **Dependencies:** {', '.join(deps)}")
    if tech.get("smooth_scroll"):
        lines.append(f"- **Smooth scroll:** {tech['smooth_scroll']}")
    lines.append(f"- **Reason:** {tech.get('reason', '')}")
    lines.append("")

    # 4. Component Details + Hover States
    lines.append("## 4. Component Details")
    for hover in analysis.get("hover_states", []):
        lines.append(f"### {hover.get('target', 'Element')}")
        lines.append(f"- **Hover/Press:** {hover.get('effect', '')}")
        props = hover.get("properties", {})
        if props:
            lines.append(f"- **Properties:** {', '.join(f'`{k}: {v}`' for k, v in props.items())}")
        if hover.get("duration_ms"):
            lines.append(f"- **Duration:** {hover['duration_ms']}ms {hover.get('easing', '')}")
        lines.append("")

    # Layer system
    layers = analysis.get("layer_system", [])
    if layers:
        lines.append("### Parallax Layer System")
        for layer in layers:
            lines.append(f"- **Layer {layer.get('layer', '?')}:** {layer.get('content', '')} — scroll rate {layer.get('scroll_rate', '?')}x")
        lines.append("")

    # Section transitions
    transitions = analysis.get("section_transitions", [])
    if transitions:
        lines.append("### Section Transitions")
        for t in transitions:
            lines.append(f"- **{t.get('from_section', '')} → {t.get('to_section', '')}:** {t.get('mechanism', '')} — {t.get('details', '')}")
        lines.append("")

    # 5. Design Tokens
    lines.append("## 5. Design Tokens")
    lines.append("```css")
    lines.append(":root {")
    for key, val in tokens.items():
        lines.append(f"  --color-{key.replace('_', '-')}: {val};")
    lines.append("}")
    lines.append("```")
    lines.append("")

    # 6. Sample Animation Logic
    lines.append("## 6. Sample Animation Logic")
    lines.append("*(Code should be generated based on the effects and tech stack above)*")
    lines.append("")

    # 7. Accessibility
    a11y = analysis.get("accessibility", {})
    lines.append("## 7. Accessibility")
    lines.append(f"- **Reduced motion:** {a11y.get('reduced_motion_strategy', 'Disable animations, show content statically')}")
    lines.append(f"- **Contrast:** {a11y.get('contrast_notes', 'Verify WCAG AA compliance')}")
    lines.append(f"- **Touch targets:** {a11y.get('touch_targets', '44px minimum')}")
    lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 4:
        print("Usage: gemini_analyze.py <video_path> <provider:api_key> <output_dir> [model]", file=sys.stderr)
        print("  provider: gemini | openai", file=sys.stderr)
        print("  example: python3 gemini_analyze.py video.mp4 gemini:AIzaSy... ./output", file=sys.stderr)
        sys.exit(1)

    video_path = sys.argv[1]
    provider_key = sys.argv[2]
    output_dir = sys.argv[3]
    model_override = sys.argv[4] if len(sys.argv) > 4 else None

    if not os.path.isfile(video_path):
        print(f"ERROR: Video file not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    # Parse provider:key
    if ":" not in provider_key:
        # Legacy format — assume Gemini
        provider, api_key = "gemini", provider_key
    else:
        provider, api_key = provider_key.split(":", 1)

    os.makedirs(output_dir, exist_ok=True)
    mime_type = get_mime_type(video_path)

    try:
        if provider == "gemini":
            print("Uploading video to Gemini...", file=sys.stderr)
            file_uri = gemini_upload(video_path, api_key)
            print(f"Upload complete: {file_uri}", file=sys.stderr)

            print("Analyzing...", file=sys.stderr)
            analysis, model_used = gemini_analyze(file_uri, api_key, mime_type, model_override)

        elif provider == "openai":
            print("Analyzing with OpenAI...", file=sys.stderr)
            analysis, model_used = openai_analyze(video_path, api_key, model_override)

        else:
            print(f"ERROR: Unknown provider '{provider}'. Use 'gemini' or 'openai'.", file=sys.stderr)
            sys.exit(1)

        print(f"Analysis complete (model: {model_used}).", file=sys.stderr)

        # Write raw JSON
        json_path = os.path.join(output_dir, "analysis.json")
        with open(json_path, "w") as f:
            json.dump(analysis, f, indent=2)
        print(f"Raw JSON: {json_path}", file=sys.stderr)

        # Write build-prompt.md
        build_prompt = analysis_to_build_prompt(analysis, model_used)
        prompt_path = os.path.join(output_dir, "build-prompt.md")
        with open(prompt_path, "w") as f:
            f.write(build_prompt)
        print(f"Build prompt: {prompt_path}", file=sys.stderr)

        # Print success for agent detection
        print("GEMINI_SUCCESS")
        print(json_path)

    except urllib.error.HTTPError as e:
        error_body = e.read().decode()[:500] if e.fp else ""
        print(f"ERROR: API HTTP {e.code}: {error_body}", file=sys.stderr)
        print("GEMINI_FAILED")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        print("GEMINI_FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
