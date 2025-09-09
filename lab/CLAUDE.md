# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains premium marketing website prototypes, specifically focused on creating Apple-style product showcase websites. The primary project is the LAB SEVEN battery system website for Labrador Field Systems, built as a sophisticated single-page application.

## Architecture

### Design System
The codebase implements a premium design system with:

- **CSS Custom Properties**: Centralized color palette using CSS variables in `:root`
  - Primary brand colors: `--primary-orange` (#FF6B35) to `--accent-gold` (#F4B942)
  - Semantic color tokens for text, backgrounds, and borders
  - Gradient definitions: `--gradient-primary` and `--gradient-secondary`

- **Typography Scale**: Systematic font sizing from 12px to 112px with precise letter-spacing
  - Font stack: Inter/Poppins with system fallbacks
  - Weight scale: 400, 500, 600, 700, 800

- **Spacing System**: Consistent 140px section padding with proportional margins
  - Card padding: 40-60px
  - Icon sizing: 96px, 120px, 140px scale

### Component Architecture

**Navigation**: Fixed glassmorphism header with:
- Backdrop blur effects
- Scroll-triggered background changes
- Hover animations with gradient underlining

**Hero Section**: Large-scale typography with:
- 96px headlines with gradient text treatments
- Staggered animation system
- Parallax product imagery

**Feature Blocks**: Split-screen layout pattern:
- Content/visual pairs with reversible direction
- Large statistic displays (112px font-weight 800)
- Glassmorphism visual containers

**Interactive Elements**:
- Custom button system with shimmer animations
- Hover effects using `transform: translateY()` and box-shadows
- Card lift interactions with gradient border highlights

### Animation System

- **Intersection Observer**: Scroll-triggered animations with staggered delays
- **Cubic Bezier Easing**: `cubic-bezier(0.4, 0, 0.2, 1)` for premium feel
- **Hover States**: Multi-property transitions (transform, box-shadow, background)
- **Loading Animations**: Progressive revelation with 150ms delays

## Development Workflow

### Testing
Open HTML files directly in browser - no build process required:
```bash
open lab-seven-battery.html
```

### Structure
- Single-file applications with embedded CSS and JavaScript
- Self-contained with no external dependencies
- Responsive design with mobile-first breakpoints at 768px, 1024px

### Code Organization
CSS follows this order:
1. CSS Custom Properties (`:root`)
2. Base styles and resets  
3. Component styles (navigation → hero → content sections → footer)
4. Responsive media queries
5. Animation keyframes

JavaScript features:
- Intersection Observer for scroll animations
- Smooth scroll polyfill
- Enhanced hover effects
- Parallax scrolling implementation

## Key Files

- `lab-seven-battery.html`: Main Labrador Field Systems product website (1,600+ lines)
- `macbook-air-replica.html`: Apple MacBook Air website replica for reference
- `.claude/settings.local.json`: Claude Code permissions allowing Apple.com WebFetch

## Design Principles

The codebase follows premium web design patterns:
- High contrast typography (800 font-weight headlines)
- Generous whitespace with 140px section padding
- Sophisticated color gradients avoiding flat colors
- Micro-interactions on all interactive elements
- Glassmorphism effects with backdrop-filter
- Professional animation timing (0.3-0.4s transitions)

Content structure maintains Apple-style information hierarchy while establishing unique brand identity through color, typography, and interaction design.