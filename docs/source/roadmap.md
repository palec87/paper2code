# Roadmap

## Vision

Translate a scientific publication into reproducible code delivered as a
Dockerized workflow with explicit agreement checks and uncertainty reporting.

## Phase 1: Foundation

1. Define typed data models for artifacts, workflow plans, agreement checks,
   missing information reports, tool records, and ontology entities.
2. Introduce provider-agnostic interfaces for extraction, planning, and
   explanation.
3. Implement a deterministic MVP pipeline scaffold with mock providers.
4. Add baseline tests for models, registry behavior, and pipeline orchestration.

## Phase 2: Extraction and Planning

1. Build extraction for full text, supplementary files, tables, and figures.
2. Add confidence scoring and uncertainty annotations for extracted items.
3. Build planning logic that maps extracted evidence to executable workflow
   steps and explicit intermediate outputs.

## Phase 3: Reduction, Validation, and Reporting

1. Add large-data reduction strategy for representative examples or mocks.
2. Implement agreement checks for numerical tolerances, workflow completeness,
   and narrative claim traceability.
3. Produce missing-information reports for reviewer handoff.

## Phase 4: Reuse and Reasoning

1. Add PostgreSQL-backed tool registry for cross-paper reuse.
2. Build ontology extraction and graph reasoning for cross-paper links.

## Phase 5: Reproducible Delivery

1. Generate Docker manifests and deterministic run artifacts.
2. Provide a single-command end-to-end run for one paper MVP.
