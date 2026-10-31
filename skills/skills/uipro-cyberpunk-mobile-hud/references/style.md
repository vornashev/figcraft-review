# Cyberpunk Mobile HUD

## No

80

## Style Category

Cyberpunk Mobile HUD

## Type

Mobile

## Keywords

cyberpunk, neon, glitch, chamfered, orbitron, jetbrains, scanlines, crt, hud, matrix, military, decker

## Primary Colors

Void #0A0A0F, Card #12121A

## Secondary Colors

Neon Green #00FF88, Neon Magenta #FF00FF, Cyber Cyan #00D4FF, Neutral Text #E0E0E0, Alert Red #FF3366, Border #2A2A3A

## Effects & Animation

Deep void background with neon radiance, chamfered 45° corners via SVG/Skia, scanline overlay, CRT flicker opacity oscillation, glitch animations (translateX ±2), neon pulses around buttons, HUD corner brackets, terminal prompt text inputs, heavy use of blurView holographic panels

## Best For

Gaming dashboards, crypto/cyberpunk apps, sci-fi companion tools, hacker OS skins, data-heavy monitoring HUDs

## Do Not Use For

Serious enterprise, health/finance requiring calm trust, minimal editorial apps

## Light Mode ✓

not-recommended

## Dark Mode ✓

supported

## Performance

cost:high|drivers:animation,large-images

## Accessibility

risk:conditional|requires:contrast-text-4.5,keyboard,visible-focus,reduced-motion

## Mobile-Friendly

native

## Conversion-Focused

✓ High

## Framework Compatibility

react-native|custom|expo

## Era/Origin

Cyber-Noir

## Complexity

High

## AI Prompt Keywords

Design a Cyberpunk Mobile HUD mobile interface using cyberpunk, neon, glitch, chamfered, orbitron, jetbrains, scanlines, crt. Prioritize clear hierarchy, safe areas, touch targets, visible focus, and reduced-motion alternatives.

## CSS/Technical Keywords

backgroundColor: '#0A0A0F', cardBg: '#12121A', accent: '#00FF88', accent2: '#FF00FF', accent3: '#00D4FF', borderColor: '#2A2A3A', destructive: '#FF3366', borderRadius: 0, chamfer via SVG path, shadowColor accent with animated radius, scanline overlay View pointerEvents='none', withRepeat glitch translateX [-2,2,0], Easing.steps(2)

## Implementation Checklist

☐ Chamfered corners used instead of radius, ☐ Scanline & CRT flicker implemented, ☐ Orbitron + JetBrains Mono typography, ☐ Neon glow shadows on primary buttons, ☐ Glitch animation on active states, ☐ Prompt-style inputs with custom cursor, ☐ HUD corner brackets implemented, ☐ Safe-area system status bar styled, ☐ Reduced motion disables glitch/flicker, ☐ Icons configured with Lucide accent color

## Design System Variables

--bg: #0A0A0F, --card: #12121A, --fg: #E0E0E0, --muted: #1C1C2E, --accent: #00FF88, --accent2: #FF00FF, --accent3: #00D4FF, --border: #2A2A3A, --destructive: #FF3366, --radius: 0px, --font-heading: Orbitron, --font-body: JetBrains Mono

## Style ID

cyberpunk-mobile-hud

## Status

supplemental

## Parent Style ID

hud-sci-fi-fui

## Preferred Mode

dark
