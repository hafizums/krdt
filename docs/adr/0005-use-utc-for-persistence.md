# ADR-0005 — Persist timestamps in UTC

## Status

ACCEPTED

## Date

2026-07-24

## Context

KRDT combines sensor observations, weather events, inspections, incidents, and audit records across systems that may report local time, UTC, or ambiguous offsets. Kundasang operates in Sabah (`Asia/Kuching`, UTC+8, no daylight saving).

Mixing local time in persistence layers causes:

- incorrect ordering of observations;
- duplicate or missing hours around policy changes in other zones;
- ambiguous audit trails;
- errors in historical playback and late-arriving data handling.

`AGENTS.md` requires observation time and ingestion time to remain separate in the observation model (future gates).

## Decision

1. Persist all **timestamps in UTC** in the database, logs, and API exchange unless a future ADR defines a narrow exception.
2. Present **Kundasang-local time** to users using **`Asia/Kuching`** when local display is required.
3. In future observation models, maintain separate fields for:
   - **observation time** (when the phenomenon was measured);
   - **ingestion time** (when KRDT received the record).
4. Use UTC in structured logs during Gate 0.

APIs must document time formats (ISO 8601 with offset or `Z` for UTC).

## Consequences

### Positive

- Unambiguous ordering and comparison across sources.
- Consistent audit and correlation with external UTC-native systems.
- Clear conversion boundary at presentation layer.

### Negative

- UI and reports must explicitly convert for local operators.
- Developers must avoid `datetime.now()` without timezone in persistence code.

### Neutral

- Individual datasets may record original local time as metadata without using it as primary storage.

## Compliance

- Backend logging uses UTC timestamps in Gate 0.
- Future entity and observation schemas must use timezone-aware types end-to-end.
- Tests must cover timezone conversion and out-of-order ingestion where applicable (Gate 2+).
- Do not assume all incoming timestamps are UTC—normalize at ingestion with provenance.

## References

- `AGENTS.md` — observation and time-series rules; Sabah timezone note
- ADR-0002 — backend stack
- Gate 0 specification — logging requirements
