---
description: Feature sicher hinzufügen — von Planung über DB-Gate bis Testing-Gate.
---

# /add-feature Workflow

## Übersicht
Strukturierter Ablauf für das sichere Hinzufügen eines neuen Features.
Stellt sicher, dass Planung, Agent-Zuständigkeiten und Tests eingehalten werden.

## Steps

### 1. Rules laden
// turbo
Lade und prüfe die relevanten Regeln:
- `code-ownership` (Sektion 6 in GEMINI.md)
- `architecture-separation-of-concerns` (Sektion 4 in GEMINI.md)
- `agent-roles-matrix` (Sektion 3 in GEMINI.md)

### 2. Feature planen
Erstelle `specs/feature-plan.md` mit:
- **Was:** Feature-Beschreibung (User Story / Akzeptanzkriterien)
- **UI:** Welche Komponenten/Seiten werden geändert oder neu erstellt?
- **API:** Welche Endpoints/Server Actions werden benötigt?
- **DB:** Werden Schema-Änderungen benötigt? (→ Schritt 3)
- **Tests:** Welche Tests müssen geschrieben werden?

### 3. DB-Gate (falls Schema-Änderung nötig)
Falls das Feature eine Datenbank-Änderung erfordert:
1. Trigger Workflow `/db-request`
2. Warte auf Freigabe durch DB-Agent
3. Erst nach „Ready"-Meldung weiter mit Schritt 4

⚠️ **Ohne DB-Freigabe kein Code gegen neue Schema-Felder schreiben.**

### 4. Implementierung
Parallele Arbeit nach Agent-Zuständigkeit:

| Agent | Aufgabe |
|---|---|
| **Backend Agent** | API Routes, Server Actions, Business-Logik |
| **Frontend Agent** | UI-Komponenten, Client State, Layout |

- Backend-Agent baut API/Actions.
- Frontend-Agent baut UI (gegen Mocks oder fertige API).
- Jeder Agent bleibt in seiner Swimlane (→ Rollen-Matrix).

### 5. Testing-Gate
// turbo
Bevor das Feature als „fertig" gilt:
1. Unit-Tests für neue Business-Logik → ✅ Grün
2. Integration-Tests für neue API Routes → ✅ Grün
3. E2E-Test für den neuen User Flow → ✅ Grün

⚠️ **Nur wenn alle Tests grün sind → Feature ist fertig.**

### 6. Review & Merge
- Code-Review durch den User oder zweiten Agent
- Prüfe Compliance mit allen Always-On-Regeln
- Merge nur nach bestandenem Testing-Gate
