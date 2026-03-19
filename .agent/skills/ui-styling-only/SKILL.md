---
name: ui-styling-only
description: >
  Verbessert ausschließlich UI/Design (Spacing, Typografie, Farben, Responsiveness)
  ohne Geschäftslogik zu ändern. Nutzen für UI-Polish, Redesigns, Dark Mode,
  Layout-Fixes. Keine Refactors, keine Feature-Änderungen.
---

# UI Styling Only Skill

## Ziel
Verschönerung der Benutzeroberfläche **ohne jedes Risiko** für die Business-Logik.
Diese Skill-Anleitung sorgt dafür, dass der Agent **nur** die visuelle Oberfläche
verbessert und **keine** bestehende Logik, Datenflüsse oder Projektstruktur verändert.

## Wann dieser Skill genutzt werden soll
Nutze diesen Skill, wenn die Aufgabe Begriffe enthält wie:
- „Design verbessern", „UI polish", „schöner machen"
- „Abstände", „Layout", „Typografie", „Farben", „Dark Mode"
- „Responsiveness", „Mobile optimieren"
- „UI konsistenter", „modernisieren"
- „Barrierefreiheit verbessern" (nur visuelle Aspekte)

## Wann dieser Skill NICHT genutzt werden soll
Nicht nutzen, wenn die Aufgabe ist:
- Neue Features, neue Endpoints, neue Datenfelder
- Bugfixes in Logik, Validierung, State-Management
- Datenbank/Backend-Integration (z. B. Supabase)
- Refactoring oder Architektur-Änderungen

## Erlaubte Änderungen
✅ Erlaubt:
- CSS / Styling-Dateien (`.css`, `.scss`, `tailwind.config.*`, UI-Theme-Dateien)
- Rein visuelle Anpassungen in UI-Komponenten (`className`, Layout-Struktur, semantische HTML-Tags)
- Responsiveness (Breakpoints), Abstände, Typografie, Farben, Schatten
- Hover/Focus States, Transitions, Micro-Animations
- Barrierefreiheit im UI (Labels, Kontraste, Fokus-Ringe) — **solange keine Logik geändert wird**
- Design Tokens / CSS Custom Properties aktualisieren

## Verbotene Änderungen
❌ Verboten:
- Änderungen an Geschäftslogik, Datenlogik, API-Calls, Formular-Submit-Logik
- Änderungen an `useEffect`, `useState`, `useQuery` oder State-Management
- Refactoring (Umbenennen/Extrahieren/Verschieben von Funktionen oder Dateien)
- Änderungen an Datenstrukturen oder Server-Side Code
- Änderungen an Build-/Tooling-Setup, wenn nicht explizit gefordert

## Instruktionen

### 1. Scope-Prüfung
Bevor du eine Datei öffnest:
1. Ist es eine Styling-Datei (`.css`, `tailwind.config.*`, Theme)? → ✅ Bearbeiten
2. Ist es eine Komponente mit nur `className`-Änderungen? → ✅ Bearbeiten
3. Enthält die Änderung Logik (`useEffect`, API-Calls, Validierung)? → ❌ STOPP

### 2. Design-System beachten
- Nutze bestehende **Design Tokens** (CSS Custom Properties / Tailwind Theme).
- Erstelle keine neuen Magic Numbers — nutze das Token-System.
- Halte dich an die bestehende Farbpalette, es sei denn, ein Redesign ist explizit gewünscht.

### 3. Responsive Design
Prüfe alle Änderungen für diese Breakpoints:

| Breakpoint | Min-Width | Gerät |
|---|---|---|
| `sm` | 640px | Mobile (Landscape) |
| `md` | 768px | Tablet |
| `lg` | 1024px | Desktop |
| `xl` | 1280px | Großer Desktop |

### 4. Barrierefreiheit (WCAG 2.1 AA)
- **Kontraste:** Mindestens 4.5:1 für normalen Text, 3:1 für großen Text.
- **Fokus-Ringe:** Sichtbar für Keyboard-Navigation — niemals `outline: none` ohne Alternative.
- **Semantisches HTML:** `<button>` statt `<div onClick>`, `<nav>` statt `<div class="nav">`.
- **Labels:** Alle interaktiven Elemente brauchen `aria-label` oder sichtbare Labels.

### 5. Post-Change Review
Nach jeder Änderung prüfe:
- [ ] Mobile Ansicht korrekt?
- [ ] Dark Mode konsistent? (falls vorhanden)
- [ ] Keine Logik-Dateien verändert?
- [ ] Hover/Focus-States funktional?
- [ ] Keine neuen Magic Numbers eingeführt?
