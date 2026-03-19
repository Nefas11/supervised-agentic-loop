---
description: Dient dazu, dass Frontend/Backend Agenten eine Schema-Änderung beim DB-Agent anfordern.
---

# /db-request Workflow

## Übersicht
Strukturierter Prozess für Cross-Agent-Kommunikation bei Datenbankänderungen.
Frontend- oder Backend-Agenten dürfen das Schema **nicht selbst** ändern —
sie müssen diesen Workflow nutzen.

## Steps

### 1. Change Proposal erstellen
Der anfordernde Agent erstellt `specs/db-change-proposal.md` mit:

```markdown
# DB Change Proposal

## Anfragender Agent
<!-- Frontend Agent / Backend Agent -->

## Grund der Änderung
<!-- Warum wird die Schema-Änderung benötigt? -->

## Gewünschtes Schema
<!-- Prisma/Drizzle Syntax oder SQL -->

## Betroffene Tabellen
<!-- Liste der Tabellen, die geändert/erstellt werden -->

## RLS-Anforderungen
<!-- Welche Row Level Security Policies werden benötigt? -->

## Zeitdruck
<!-- Normal / Dringend — mit Begründung -->
```

### 2. Handover an DB-Agent
- Markiere die Proposal-Datei als bereit
- Übergabe an DB-Agent mit Verweis auf `specs/db-change-proposal.md`
- Der anfordernde Agent **wartet** — kein Code gegen neue Felder schreiben

### 3. Execution (DB-Agent)
Der DB-Agent führt aus:
1. **Review:** Prüfe Proposal auf Vollständigkeit und Sicherheit
2. **Validierung:** Prüfe auf Datenverlust-Risiko
3. **Migration:** Schema-Änderung via Prisma/Drizzle durchführen
4. **RLS:** Row Level Security Policies erstellen/anpassen
5. **Types:** TypeScript-Types regenerieren (`prisma generate` / `drizzle-kit generate`)
6. **Diff:** Schema-Diff dokumentieren

### 4. Result kommunizieren
DB-Agent meldet zurück:
- **Status:** ✅ Ready / ❌ Abgelehnt (mit Begründung)
- **Migration-Name:** z. B. `20250319_add_user_preferences`
- **Neue Types:** Pfad zu generierten Types
- **RLS-Policies:** Liste der erstellten/geänderten Policies
- **Breaking Changes:** Falls vorhanden, mit betroffenen Endpoints

### 5. Weiterarbeit
Erst nach „Ready"-Meldung darf der anfordernde Agent:
- Code gegen neue Schema-Felder schreiben
- Neue API-Endpoints implementieren
- UI-Komponenten für neue Daten erstellen
