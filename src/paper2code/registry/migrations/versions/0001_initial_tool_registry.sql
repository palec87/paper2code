-- Initial schema migration for paper2code tool registry.

CREATE TABLE IF NOT EXISTS tool_records (
    tool_id VARCHAR(80) PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    modality VARCHAR(80) NOT NULL,
    input_contract VARCHAR(500) NOT NULL,
    output_contract VARCHAR(500) NOT NULL,
    confidence DOUBLE PRECISION NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_tool_records_modality
    ON tool_records (modality);
