---
description: Qualitäts-Audit — Prüfung aller Regeln, Architektur und Sicherheit ohne Änderungen.
---

# /audit Workflow

## Übersicht
Systematische Prüfung des Projekts gegen alle aktiven Regeln.
Ziel: Verstöße **identifizieren und dokumentieren**, ohne sie zu beheben.

## Steps

### 1. Security-Audit (OWASP 2025)
// turbo
Prüfe das Projekt gegen die Security-Regeln (Sektion 1 in GEMINI.md):
- [ ] Keine hardcoded Secrets im Code? (`grep` nach `sk-`, `AKIA`, `ghp_`, `-----BEGIN`)
- [ ] `.env` in `.gitignore` gelistet?
- [ ] Keine PII in Logs oder Console-Output?
- [ ] Alle externen Inputs validiert (serverseitig)?
- [ ] Rate-Limiting für API-Aufrufe implementiert?
- [ ] Keine `*`-Versionen in `package.json`?
- [ ] `npm audit` zeigt keine kritischen Vulnerabilities?

### 2. Architektur-Audit
Prüfe die Separation of Concerns (Sektion 4 in GEMINI.md):
- [ ] UI-Layer frei von direkten DB-Calls?
- [ ] Backend-Services frei von React-Imports?
- [ ] DAL gibt DTOs zurück (keine rohen DB-Objekte)?
- [ ] Validierung im Backend (Zod/Pydantic), nicht nur im Client?
- [ ] Keine N+1-Queries identifizierbar?

### 3. Agent-Boundaries-Audit
Prüfe die Rollen-Matrix (Sektion 3 in GEMINI.md):
- [ ] Keine Frontend-Logik in Backend-Dateien?
- [ ] Keine Backend-Logik in UI-Komponenten?
- [ ] Shadcn `components/ui/` Dateien unverändert?

### 4. Testing-Audit
Prüfe die Testing Policy (Sektion 5 in GEMINI.md):
- [ ] Kritische Pfade (Auth, Payment) haben ≥ 95% Coverage?
- [ ] Keine flaky Tests (deterministische Mocks)?
- [ ] DB-Tests in Transaktionen oder Containern?
- [ ] Test-Naming-Konvention eingehalten?

### 5. Error-Handling-Audit
Prüfe die Error Handling Policy (Sektion 7 in GEMINI.md):
- [ ] Keine leeren `catch`-Blöcke?
- [ ] Strukturierte Fehler mit `code`, `message`, `context`?
- [ ] Retry-Logik für transiente Fehler?
- [ ] Graceful Degradation bei Service-Ausfällen?

### 6. Report erstellen
Erstelle `specs/audit-report.md` mit:
- **Datum** des Audits
- **Geprüfte Bereiche** (mit Häkchen)
- **Verstöße** (je Verstoß: Datei, Zeile, Regel, Schweregrad)
- **Empfehlungen** (priorisiert nach Schweregrad)

⚠️ **Behebe keine Verstöße selbst** — liste sie nur auf. Die Behebung erfolgt durch den zuständigen Agent.
