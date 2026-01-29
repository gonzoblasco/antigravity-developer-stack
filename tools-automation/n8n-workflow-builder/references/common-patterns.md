# Common n8n Patterns & Mental Models

Use these patterns to design robust workflows.

## The Mental Model: "Trigger -> Process -> Action"

Every workflow should be conceptualized as valid data flowing through pipes.

1.  **Trigger**: "What starts this?" (Webhook, Cron, Event)
2.  **Process**: "How do I shape the data?" (Filter, Map, Split)
3.  **Action**: "What is the side effect?" (API Call, DB Write, Email)

## Common Patterns

### 1. Webhook Responder (Synchronous)

**Goal**: Receive data, process it, and return a response immediately.

- **Flow**: `Webhook` -> `Set` (Process) -> `Respond to Webhook`
- **Use Case**: API endpoints, Slash commands.

### 2. ETL (Extract, Transform, Load)

**Goal**: Fetch data, clean it, and save it.

- **Flow**: `Schedule` -> `HTTP Request` (Get Data) -> `Item Lists` (Split) -> `Set` (Clean) -> `Postgres` (Insert)
- **Use Case**: Nightly syncs, Report generation.

### 3. Error Handling (The "Let it Crash" Guard)

**Goal**: Catch failures in critical nodes.

- **Flow**: Attach an `Error Trigger` node to the workflow, or use the "Continue On Fail" setting on flaky nodes and check functionality with an `IF` node immediately after.

## Node Selection Guide

| Intent                  | Recommended Node                                |
| :---------------------- | :---------------------------------------------- |
| **Start** a workflow    | `Webhook`, `Schedule Trigger`, `Manual Trigger` |
| **Fetch** external data | `HTTP Request`                                  |
| **Logic/Decision**      | `IF`, `Switch`                                  |
| **Transform** JSON      | `Set` (Simple), `Code` (Complex)                |
| **Iterate** Array       | `Item Lists` (Split), `Loop` (Complex)          |
| **Wait**                | `Wait`                                          |
