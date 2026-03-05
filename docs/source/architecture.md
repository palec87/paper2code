# Architecture

## Core Components

1. Extraction Agent: reads publication sources and returns `PaperArtifact`
   records with confidence scores.
2. Planning Agent: converts extracted evidence into `WorkflowStep` plans with
   expected intermediate outputs.
3. Reduction Strategy: shrinks large datasets into representative examples or
   mocks for fast reproducible runs.
4. Validation Engine: evaluates agreement with publication claims and metrics.
5. Missing Information Reporter: records ambiguity and missing details for
   human review.
6. Tool Registry: persists reusable tools and contracts for future papers.
7. Ontology Graph: stores scientific entities and relations for cross-paper
   reasoning.
8. Docker Delivery: captures deterministic run metadata and container entry
   points.

## Data Flow

1. Ingest publication inputs.
2. Extract artifacts.
3. Reduce data volume for MVP execution.
4. Plan executable workflow.
5. Run validation and create reports.
6. Package reproducible Docker deliverables.

## Provider Strategy

The system uses provider-agnostic interfaces for extraction and planning.
Adapters can be swapped without changing pipeline logic.

## Reproducibility Guarantees

1. Deterministic mock providers for tests.
2. Versioned run manifests.
3. Agreement reports linked to observed outputs.
