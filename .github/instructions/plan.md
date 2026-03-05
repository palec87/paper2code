# Implementation Plan: paper2code

## Goal

Translate a scientific publication into reproducible code delivered as a
Dockerized workflow, with explicit validation against publication claims.

## MVP Scope

1. End-to-end run for one publication.
2. Provider-agnostic extraction and planning interfaces.
3. Data reduction to examples or mocks for large datasets.
4. Agreement checks and reviewer-ready gap reports.

## Workstreams

1. Extraction Agent:
Extract full text, supplementary data, tables, and figures into typed artifacts.
2. Planning Agent:
Transform artifacts into executable workflow steps and intermediate outputs.
3. Data Reduction:
Reduce large inputs while keeping claim-critical behavior.
4. Validation:
Evaluate numerical agreement, workflow completeness, and traceability.
5. Gap Reporting:
Capture missing or ambiguous publication details for review.
6. Tool Registry:
Store reusable tool contracts for future paper translations.
7. Ontology Reasoning:
Capture scientific arguments and data relations for cross-paper reasoning.
8. Docker Delivery:
Package deterministic execution into a reproducible container flow.

## Phase Plan

1. Phase 1:
Scaffold typed models, provider interfaces, pipeline orchestration, and tests.
2. Phase 2:
Implement extraction and planning logic with confidence and uncertainty signals.
3. Phase 3:
Implement reduction, agreement validation, and missing-information reports.
4. Phase 4:
Implement PostgreSQL tool registry and ontology graph integration.
5. Phase 5:
Generate Docker manifests and end-to-end reproducible run artifacts.

## Deliverables

1. Python package modules for each workstream.
2. Test suites for models, pipeline orchestration, and validation behavior.
3. Documentation pages (`roadmap`, `architecture`) linked from docs index.
4. Deterministic execution path suitable for CI and Docker packaging.