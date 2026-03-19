---
description: Tests ausführen, Ergebnisse verifizieren und Report erstellen.
---

# /test-verify Workflow

## Übersicht
Standardisierter Ablauf für Test-Ausführung und Verifizierung nach Code-Änderungen.
Stellt sicher, dass keine Regression eingeführt wurde.

## Steps

### 1. Test-Environment prüfen
// turbo
Vor dem Test-Lauf sicherstellen:
- [ ] Node-Module installiert (`npm ci` / `yarn install --frozen-lockfile`)
- [ ] Umgebungsvariablen gesetzt (`.env.test` vorhanden)
- [ ] Test-Datenbank erreichbar (falls Integration-Tests)
- [ ] Keine uncommitted Changes, die Tests beeinflussen könnten

### 2. Unit-Tests ausführen
// turbo
```bash
npm run test -- --coverage
# oder
npx vitest run --coverage
# oder
npx jest --coverage
```
- Erwartung: **Alle grün**
- Coverage notieren für Report

### 3. Integration-Tests ausführen
// turbo
```bash
npm run test:integration
# oder spezifisch:
npx vitest run tests/integration/
```
- Erwartung: **Alle grün**
- API-Response-Codes und Payloads prüfen

### 4. E2E-Tests ausführen (falls konfiguriert)
// turbo
```bash
npx playwright test
# oder
npx cypress run
```
- Erwartung: **Kritische Flows grün** (Login, Checkout, Onboarding)
- Screenshots bei Fehlern sichern

### 5. Ergebnisse analysieren

| Prüfpunkt | Status |
|---|---|
| Unit-Tests grün? | ✅ / ❌ |
| Integration-Tests grün? | ✅ / ❌ |
| E2E-Tests grün? | ✅ / ❌ / ⏭️ Nicht konfiguriert |
| Coverage ≥ Schwellenwert? | ✅ / ❌ |
| Neue Flaky Tests? | ✅ Keine / ⚠️ Ja (Details) |

### 6. Report erstellen
Erstelle oder aktualisiere `specs/test-report.md` mit:
- **Datum und Auslöser** (welche Änderung wurde getestet?)
- **Ergebnis-Tabelle** (Schritt 5)
- **Coverage-Zahlen** pro Modul
- **Fehlschläge** (falls vorhanden): Datei, Test-Name, Fehlermeldung
- **Empfehlung:** ✅ Merge-bereit / ❌ Nacharbeit nötig (mit Details)

### 7. Gate-Entscheidung
- **Alle grün + Coverage OK** → Feature ist merge-bereit
- **Fehlschläge vorhanden** → Zurück an den zuständigen Agent mit Fehler-Details
- **Flaky Tests** → QA-Agent soll diese stabilisieren bevor Merge
