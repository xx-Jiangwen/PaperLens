# Design System Specification: The Academic Editorial

## 1. Overview & Creative North Star
**Creative North Star: "The Digital Curator"**

This design system rejects the cluttered, utility-first aesthetic of traditional academic software in favor of a high-end editorial experience. It is designed to feel like a premium physical monograph—quiet, authoritative, and expensive. 

We break the "template" look by utilizing **intentional asymmetry** and **tonal layering**. Rather than boxing content into rigid grids with visible lines, we use expansive white space and subtle shifts in surface luminance to guide the eye. The interface does not compete with the research; it frames it. The result is a "scholarly minimalist" environment where the user’s focus is treated as a finite, precious resource.

---

### 2. Colors: Tonal Depth & The "No-Line" Rule
The palette is rooted in the "Apple-esque" philosophy of light and air, but refined for deep focus.

| Role | Token | Value | Application |
| :--- | :--- | :--- | :--- |
| **Background** | `surface-container-lowest` | `#FFFFFF` | Primary canvas for reading and deep focus. |
| **Surface** | `surface` | `#F9F9FB` | The base "tabletop" on which sheets of content sit. |
| **Secondary Surface**| `surface-container` | `#EEEEF0` | For utility bars, sidebars, and grouped metadata. |
| **Primary Accent** | `primary-container` | `#0066CC` | Focused actions, active states, and scholarly highlights. |
| **Main Text** | `on_surface` | `#1D1D1F` | High-contrast, deep black for maximum legibility. |
| **Secondary Text** | `on_surface_variant` | `#414753` | Metadata, captions, and non-essential information. |

#### **The "No-Line" Rule**
Designers are strictly prohibited from using 1px solid borders to section off UI areas. Boundaries must be defined through:
*   **Background Shifts:** A `surface-container-low` section sitting on a `surface` background.
*   **Tonal Transitions:** Using depth to define where one thought ends and another begins.

#### **Surface Hierarchy & Nesting**
Treat the UI as a series of physical layers. 
*   **Level 0:** `surface` (#F9F9FB) - The absolute base.
*   **Level 1:** `surface-container-lowest` (#FFFFFF) - Floating sheets (cards/reading panes) that "lift" off the base.
*   **Level 2:** `surface-container-high` (#E8E8EA) - Inset elements (search bars, code blocks) within a sheet.

#### **Glassmorphism & Texture**
For floating navigation or overlays (like a "Tools" menu over a PDF), use `surface-container-lowest` with **70% opacity and a 20px backdrop blur**. This creates a "frosted glass" effect that keeps the user grounded in their primary text while providing temporary utility.

---

### 3. Typography: The Editorial Voice
We use a dual-font strategy to balance modern precision with scholarly warmth.

*   **Headlines (Manrope):** Chosen for its geometric clarity and unique "high-end" terminals. Use `display-lg` (3.5rem) for chapter titles to create a bold, editorial entrance.
*   **Reading/UI (Inter):** Chosen for its immense legibility at small sizes. The tall x-height makes it the workhorse for body text and labels.

**Hierarchy Strategy:**
*   **Primary Focus:** Use `headline-md` (Manrope, 1.75rem) with `-0.02em` tracking for a tight, professional look.
*   **Body Content:** Use `body-lg` (Inter, 1rem) with a generous `1.6` line-height. Academic reading requires "breathing room" between lines to reduce cognitive load.

---

### 4. Elevation & Depth: Tonal Layering
Traditional shadows are often a crutch for poor layout. In this system, we favor **Tonal Layering**.

*   **The Layering Principle:** To "elevate" a card, do not reach for a shadow first. Place a `#FFFFFF` (`surface-container-lowest`) card on a `#F3F3F5` (`surface-container-low`) background. The luminance difference provides a natural, soft lift.
*   **Ambient Shadows:** If a floating element (like a modal) requires a shadow, it must be "Ambient":
    *   `blur: 40px`, `y: 10px`, `color: rgba(26, 28, 29, 0.06)`. 
    *   The shadow is never grey; it is a tinted version of the text color at ultra-low opacity.
*   **The Ghost Border Fallback:** If accessibility requires a border (e.g., in high-contrast situations), use `outline-variant` at **15% opacity**. It should feel like a suggestion of a line, not a boundary.

---

### 5. Components
All components utilize the **xl (1.5rem / 24px)** or **lg (1rem / 16px)** roundedness scale to feel approachable and organic.

*   **The Reading Card:** Never uses a border. Uses `surface-container-lowest` and an `8.5` (spacing-24) internal padding.
*   **Action Buttons:** 
    *   *Primary:* `primary-container` (#0066CC) background with `on_primary` text. Use a subtle gradient from `primary` to `primary-container` for a "jewel" effect.
    *   *Tertiary:* Ghost style. Only `on_surface` text. No background until hover (then use `surface-container-low`).
*   **Navigation Rails:** Vertical, docked to the left. No dividing line; separate from the main content area via a `surface` to `surface-container-lowest` transition.
*   **Scholarly Chips:** Used for "Citations" or "Tags." Use `surface-container-highest` with `label-md` text. Border radius must be `full` (pill shape).
*   **Input Fields:** `surface-container-high` background. No border. On focus, a 2px `primary` "Ghost Border" appears at 30% opacity.
*   **The "Paper" Sidebar:** A persistent area for notes using `surface-container-low`. It should feel like a margin in a textbook.

---

### 6. Do's and Don'ts

**Do:**
*   **Do** use asymmetrical margins. A wider left margin for text can create a sophisticated "editorial" feel.
*   **Do** use iconography from the SF Symbols library style—consistent line weights (Regular or Medium) and rounded caps.
*   **Do** use `spacing-16` (5.5rem) between major sections to let the layout "breathe."

**Don't:**
*   **Don't** use pure black (#000000) for text. Always use `on_surface` (#1D1D1F) to avoid eye strain.
*   **Don't** use standard "AI" sparkles or glowing gradients. If an intelligent feature is present, represent it with the same clean, minimalist typography as the rest of the app.
*   **Don't** use divider lines to separate list items. Use `spacing-3` (1rem) of white space or a very subtle background shift on hover.