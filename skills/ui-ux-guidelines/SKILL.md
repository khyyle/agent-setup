---
name: ui-ux-guidelines
description: >-
  Frontend UI/UX best practices for animations, timing, layout, typography, and visual design.
  Use when building or reviewing React components, CSS transitions, responsive layouts,
  interactive elements, or any user-facing frontend work.
---

# UI/UX Frontend Guidelines

Actionable rules for building polished, intuitive interfaces. Apply when implementing or reviewing any user-facing component.

## 1. Animation Timing

- User-initiated animations must complete within **300ms**
- Similar elements use identical timing values
- Context menus: no entrance animation, exit only
- Use exponential ramps for natural decay, not linear
- Linear easing only for progress indicators
- Interactive elements need `:active` scale transform (subtle, 0.95-1.05 range)
- Springs for overshoot-and-settle, not easing curves
- Stagger delays under 50ms per item
- One prominent animation at a time (staging)

### When to Use Springs vs Easing

| Scenario | Use | Why |
|----------|-----|-----|
| Drag/flick gestures | Spring | Preserves input velocity |
| Interruptible motion | Spring | Can change direction mid-flight |
| System state changes | Easing | Predictable, fixed duration |
| Entrances | ease-out | Decelerates into resting position |
| Exits | ease-in | Accelerates away |
| View transitions | ease-in-out | Smooth both ends |
| Progress/time display | linear | Represents real elapsed time |

### Duration Guide

| Interaction | Duration |
|-------------|----------|
| Press/hover feedback | 120-180ms |
| Small state changes | 180-260ms |
| User-initiated max | 300ms |
| Layout shifts | 300-500ms |

If something feels slow, shorten the duration first — don't change the curve.

### No Animation

- High-frequency interactions (typing, scrolling)
- Keyboard navigation (must be instant)
- Context menu entrance (exit animation only)

## 2. Exit Animations

- Conditional elements need an `AnimatePresence` wrapper (or equivalent)
- Exit should mirror entrance for visual symmetry
- Disable pointer events on exiting elements
- `mode="wait"` doubles perceived duration — halve your timing
- Dynamic lists need unique keys, not array index

## 3. CSS Pseudo Elements

- `::before`/`::after` require the `content` property
- Prefer pseudo-elements over extra DOM nodes for decoration
- Parent needs `position: relative` for absolute pseudo-elements
- Use negative inset on pseudo-elements for invisible hit target expansion
- Prefer View Transitions API over JS animation libraries when possible

## 4. Container Animation

- Two-div pattern: outer animated div, inner measured div — never the same element
- Guard against `bounds === 0` on initial render, fall back to `"auto"`
- Use `ResizeObserver` for measurement, not `getBoundingClientRect`
- Set `overflow: hidden` on animated container during transitions
- Use sparingly: buttons, accordions, interactive reveals
- Use callback ref (not `useRef`) for measurement hooks

## 5. Laws of UX

### Fitts's Law
- Interactive targets min **44px** (32px absolute minimum)
- Expand hit areas with invisible padding or pseudo-elements

### Hick's Law
- Minimize visible choices; use progressive disclosure
- Show what matters now, reveal complexity on demand

### Miller's Law
- Chunk data into groups of 5-9 for scannability
- Format numbers, codes, and IDs for human reading

### Doherty Threshold
- Respond within **400ms** to feel instant; under **100ms** feels real-time
- Use skeletons, optimistic UI, or progress indicators for slow operations

### Postel's Law
- Accept messy input, output clean data

### Additional Principles
- **Jakob's Law**: Use familiar patterns users know from other apps
- **Aesthetic-usability**: Visual polish increases perceived usability
- **Von Restorff**: Make important elements visually distinct from surrounding content
- **Peak-end rule**: End flows with clear success states
- **Tesler's Law**: Move complexity to the system, not the user
- **Goal gradient**: Show progress toward completion (progress bars, step indicators)

## 6. Typography

- **Tabular numbers** (`font-variant-numeric: tabular-nums`) for columns, dashboards, pricing
- **Oldstyle numbers** for body text prose
- Slashed zero in code-adjacent UIs
- `font-display: swap` to avoid invisible text during font load
- `text-wrap: balance` on headings for even line distribution
- `text-wrap: pretty` on body text to reduce orphans
- Add `letter-spacing` to uppercase and small-caps text
- Offset underlines below descenders (`text-underline-offset`)
- Disable `font-synthesis` to prevent browser-generated faux bold/italic

## 7. Visual Design

- **Concentric radius**: inner radius = outer radius minus padding (for nested rounded elements)
- **Layered shadows**: multiple box-shadows for realistic depth
- All shadows share same offset direction (single light source)
- Use neutral colors for shadows, never pure black
- Shadow size should indicate elevation consistently
- Animate shadows via pseudo-element opacity (not changing `box-shadow` directly) for performance
- Use a consistent spacing scale, not arbitrary values
- Semi-transparent borders (`border-color: rgba(...)`) adapt to any background

## 8. Responsive & Accessible

- Touch targets: min **44x44px** on mobile
- Always provide hover AND focus states for keyboard users
- Color must never be the sole indicator of state — pair with icons, text, or shape
- Contrast ratios: **4.5:1** minimum for body text, **3:1** for large text
- Respect `prefers-reduced-motion` — disable or reduce animations accordingly

## 9. Predictive Prefetching

- Trajectory prediction over hover-only; reclaims 100-200ms
- Prefetch by user intent, not viewport proximity
- Fall back gracefully on touch devices (no cursor available)
- Use selectively where latency is actually noticeable
