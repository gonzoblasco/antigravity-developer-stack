# Description Writing Guide

Complete guide for writing LLM-friendly tool descriptions.

> [!NOTE]
> This is a companion reference to the `agent-tool-builder` skill.
> For core principles, see the main SKILL.md.

## Table of Contents

1. [The Anatomy of a Great Description](#the-anatomy-of-a-great-description)
2. [Template Library](#template-library)
3. [Before & After Examples](#before--after-examples)
4. [Common Mistakes](#common-mistakes)
5. [Advanced Patterns](#advanced-patterns)

---

## The Anatomy of a Great Description

A complete tool description has **4 required parts**:

```
[ACTION] [WHAT] using [METHOD].
Accepts [INPUT with types and constraints].
Returns [OUTPUT structure with key fields].
Throws [ERROR_TYPE] if [CONDITION].
```

### Part 1: ACTION + WHAT

**Start with a clear action verb:**

- Searches, Creates, Updates, Deletes
- Validates, Processes, Analyzes
- Fetches, Retrieves, Sends
- Executes, Compiles, Transforms

**Specify WHAT it acts on:**

- "Searches **product database**"
- "Creates **user account**"
- "Validates **configuration**"

### Part 2: INPUT Specification

**Format:** "Accepts X (type, constraints), Y (type, constraints)"

**Examples:**

- "Accepts query (string, 1-200 chars)"
- "Accepts email (string, valid email format) and role (enum: admin|user)"
- "Accepts config (object) and schema_id (string)"

**Key elements:**

- Parameter name
- Type in parentheses
- Constraints (length, range, format)
- Optional vs required clarity

### Part 3: OUTPUT Specification

**Format:** "Returns {field: type, field: type}"

**Examples:**

- "Returns {results: array, total: int}"
- "Returns {user_id: string, created_at: string}"
- "Returns {valid: boolean, errors: array of {field, message}}"

**Key elements:**

- Structure preview
- Key field names
- Field types
- Nested structure if applicable

### Part 4: ERROR Specification

**Format:** "Throws 'ERROR_TYPE' if CONDITION"

**Examples:**

- "Throws 'invalid_email' if email format is wrong"
- "Throws 'not_found' if user doesn't exist, 'unauthorized' if no permission"
- "Throws 'service_unavailable' if database is down"

**Key elements:**

- Error type name
- Condition that triggers it
- Multiple errors separated by commas

---

## Template Library

### Search/Query Tools

```
Searches [RESOURCE] using [METHOD].
Accepts query (string, [MIN]-[MAX] chars), optional [FILTER] ([TYPE]),
and limit (int, [MIN]-[MAX], default [N]).
Returns {results: array of {[KEY_FIELDS]}, total: int, query_time_ms: int}.
Throws '[ERROR]' if [CONDITION].
```

**Example:**
"Searches product catalog using full-text search. Accepts query (string, 1-200 chars), optional category (enum: electronics|books|clothing), and limit (int, 1-100, default 20). Returns {results: array of {id, name, price, relevance}, total: int, query_time_ms: int}. Throws 'invalid_category' if category not recognized."

### CRUD Tools

**Create:**

```
Creates [RESOURCE] with provided data.
Accepts [REQUIRED_FIELDS] ([TYPES]) and optional [OPTIONAL_FIELDS] ([TYPES]).
Returns {[RESOURCE]_id: string, created_at: string}.
Throws '[ERROR]' if [CONDITION].
```

**Read:**

```
Retrieves [RESOURCE] by [IDENTIFIER].
Accepts [ID_PARAM] ([TYPE], [FORMAT]).
Returns {[KEY_FIELDS]}.
Throws 'not_found' if [RESOURCE] doesn't exist.
```

**Update:**

```
Updates [RESOURCE] with new data.
Accepts [ID_PARAM] and [UPDATE_FIELDS] (object with {[FIELDS]}).
Returns {updated: boolean, [RESOURCE]: object}.
Throws 'not_found' if [RESOURCE] doesn't exist, 'validation_error' if data invalid.
```

**Delete:**

```
Deletes [RESOURCE] by [IDENTIFIER].
Accepts [ID_PARAM] ([TYPE]).
Returns {deleted: boolean, [ID]: string}.
Throws 'not_found' if [RESOURCE] doesn't exist, 'permission_denied' if not allowed.
```

### Validation Tools

```
Validates [INPUT] against [SCHEMA/RULES].
Accepts [INPUT_PARAM] ([TYPE]) and optional [SCHEMA_PARAM] ([TYPE]).
Returns {valid: boolean, errors: array of {field: string, message: string, suggestion: string}}.
Throws '[ERROR]' if [CONDITION].
```

**Example:**
"Validates user configuration against JSON schema. Accepts config (object) and schema_id (string, default 'user_config_v1'). Returns {valid: boolean, errors: array of {field, message, suggestion}}. Throws 'schema_not_found' if schema_id doesn't exist."

### Processing/Transformation Tools

```
Processes [INPUT] to produce [OUTPUT].
Accepts [INPUT] ([TYPE], [CONSTRAINTS]) and [OPTIONS] (object with {[FIELDS]}).
Returns {result: [TYPE], metadata: object with {[FIELDS]}}.
Throws '[ERROR]' if [CONDITION].
```

**Example:**
"Processes CSV file to extract contacts. Accepts file_url (string, HTTP/HTTPS), column_mapping (object with {name, email, phone}). Returns {contacts: array of {name, email, phone}, imported_count: int, skipped_count: int}. Throws 'invalid_url' if URL malformed, 'file_too_large' if > 10MB."

### Async/Job Tools

```
Starts [OPERATION] asynchronously.
Accepts [PARAMS].
Returns {job_id: string, status: 'queued', estimated_seconds: number}.
Check status with get_job_status(job_id).
Throws '[ERROR]' if [CONDITION].
```

**Example:**
"Starts batch image processing asynchronously. Accepts image_urls (array of strings, max 100), operation (enum: resize|compress|convert), and options (object). Returns {job_id: string, status: 'queued', estimated_seconds: number}. Check progress with get_job_status(job_id). Throws 'too_many_images' if > 100 URLs."

---

## Before & After Examples

### Example 1: File Upload

❌ **Before (vague):**
"Uploads a file"

✅ **After (clear):**
"Uploads file to cloud storage. Accepts file_url (string, HTTP/HTTPS), destination_path (string, max 255 chars), and optional metadata (object). Returns {file_id: string, storage_url: string, size_bytes: int}. Throws 'invalid_url' if URL malformed, 'file_too_large' if > 100MB, 'storage_full' if quota exceeded."

**Improvements:**

- Specified WHERE (cloud storage)
- Listed all parameters with types/constraints
- Defined output structure
- Listed 3 specific error conditions

### Example 2: Data Processing

❌ **Before (generic):**
"Processes data and returns results"

✅ **After (specific):**
"Processes customer transactions to calculate daily totals. Accepts transactions (array of {amount, timestamp, category}), date_range (object with {start, end} in ISO 8601), and group_by (enum: category|hour|customer, default category). Returns {totals: array of {group, amount, count}, period: string, processed_at: string}. Throws 'invalid_date_range' if start > end, 'no_data' if no transactions in range."

**Improvements:**

- Specific action: calculate daily totals
- Detailed input structure (nested objects)
- Detailed output structure
- Specific error conditions

### Example 3: External API Call

❌ **Before (unclear):**
"Calls external API"

✅ **After (comprehensive):**
"Fetches weather data from OpenWeather API. Accepts location (string, city name or lat,lng), units (enum: metric|imperial, default metric), and optional include_forecast (boolean, default false). Returns {temperature: number, conditions: string, humidity: number, forecast?: array of {date, temp_high, temp_low}}. Throws 'location_not_found' if location invalid, 'api_key_invalid' if credentials wrong, 'rate_limit_exceeded' if quota hit."

**Improvements:**

- Named the external service
- All parameters with defaults
- Optional field marked with ?
- Multiple specific errors

### Example 4: Multi-Step Operation

❌ **Before (incomplete):**
"Deploys the service"

✅ **After (detailed):**
"Deploys application to production environment. Accepts app_id (string), version (string, semver format), environment (enum: staging|production), and optional config_overrides (object). Returns {deployment_id: string, status: 'deploying', steps: array of {name, status}, eta_seconds: number}. Monitor with get_deployment_status(deployment_id). Throws 'app_not_found' if app_id invalid, 'version_invalid' if not semver, 'dependency_missing' if required services not deployed."

**Improvements:**

- Specified destination (production environment)
- Version format specified (semver)
- Mentioned monitoring tool
- Listed dependency-related errors

### Example 5: Batch Operation

❌ **Before (ambiguous):**
"Creates multiple users"

✅ **After (clear):**
"Creates multiple user accounts in batch. Accepts users (array of {email, role, metadata}, max 100 items), send_welcome_email (boolean, default true). Returns {successes: array of {email, user_id}, failures: array of {email, error, suggestion}, total: int, success_count: int}. Throws 'batch_too_large' if > 100 users, 'invalid_batch' if array is empty."

**Improvements:**

- Specified max batch size
- Detailed output showing partial success support
- Both field-level and batch-level errors

---

## Common Mistakes

### Mistake 1: Too Short

❌ **Bad:** "Searches documents"

- Missing: method, inputs, outputs, errors
- **Word count:** 2

✅ **Good:** "Searches document database using full-text search. Accepts query (string, 1-500 chars) and optional limit (int, 1-50, default 10). Returns {results: array of {id, title, snippet, score}, total: int}. Throws 'query_too_short' if query < 3 chars."

- **Word count:** 40
- Has: method, inputs, outputs, error

### Mistake 2: Too Long

❌ **Bad:** "This tool searches through our comprehensive document database which contains various types of documents including PDFs, Word documents, and text files. It uses advanced full-text search capabilities powered by Elasticsearch version 8.x with custom analyzers for better relevance. The search algorithm considers multiple factors such as term frequency, document freshness, user permissions, and popularity metrics to rank results. You can provide a search query along with various optional filters..."

- **Word count:** 72+ and still incomplete
- **Problem:** Implementation details, not interface specification

✅ **Good:** Use the 40-word version above and move details to documentation resource

### Mistake 3: Missing Format Details

❌ **Bad:** "Accepts date parameter"

- What format? String? Object? ISO 8601?

✅ **Good:** "Accepts date (string in YYYY-MM-DD format)"

- Clear format specification

### Mistake 4: Vague Errors

❌ **Bad:** "Throws error if something goes wrong"

- Which errors? When?

✅ **Good:** "Throws 'invalid_email' if email format wrong, 'duplicate_email' if already exists, 'service_unavailable' if database down"

- Specific error types and conditions

### Mistake 5: No Examples for Complex Types

❌ **Bad:** "Accepts filter object"

- What structure? What fields?

✅ **Good:** "Accepts filters (object with optional {category: string, price_range: {min: number, max: number}, tags: array of strings})"

- Structure specified inline

---

## Advanced Patterns

### Pattern 1: Conditional Parameters

When some parameters depend on others:

"Accepts payment_method (enum: card|bank|crypto). If 'card': requires card_number (string, 16 digits) and cvv (string, 3-4 digits). If 'bank': requires account_number and routing_number. If 'crypto': requires wallet_address."

### Pattern 2: Multiple Output Formats

When tool can return different formats:

"Returns data in requested format. If format='json': {data: object, metadata: object}. If format='csv': string with CSV content. If format='xml': string with XML content."

### Pattern 3: Streaming/Progressive Results

For async operations with updates:

"Starts analysis and streams results. Initial response: {job_id: string, status: 'started'}. Progress updates via websocket: {progress: number 0-1, current_step: string, results_so_far: array}. Final result: {status: 'completed', results: array, total_time_ms: int}."

### Pattern 4: Idempotency

When repeated calls are safe:

"Creates or updates resource (idempotent). Accepts resource_id (string, optional - generates if not provided). If resource_id exists: updates and returns {updated: true, resource: object}. If new: creates and returns {created: true, resource_id: string, resource: object}."

### Pattern 5: Partial Success

For batch operations:

"Processes items in batch, continuing on errors. Returns {successes: array, failures: array with {item, error, suggestion}, total: int, success_count: int, failure_count: int}. Never throws - always returns partial results."

---

## Testing Your Descriptions

### Checklist

- [ ] Starts with action verb?
- [ ] Specifies what it acts on?
- [ ] Lists all parameters with types?
- [ ] Mentions constraints (length, range, format)?
- [ ] Describes output structure?
- [ ] Lists possible errors with conditions?
- [ ] 20-150 words?
- [ ] No implementation details?
- [ ] Examples for complex parameters?
- [ ] Can be understood without context?

### Self-Review Questions

1. **Could an LLM use this without seeing code?**
   - If no → add missing details

2. **Are all parameters explained?**
   - If no → add type and constraints for each

3. **Is the output structure clear?**
   - If no → specify key fields and types

4. **Can the LLM recover from errors?**
   - If no → specify error types and conditions

5. **Is it self-contained?**
   - If no → remove references to external docs

---

## Summary

**Good description has:**

1. ✅ Clear action + target
2. ✅ All inputs with types & constraints
3. ✅ Output structure preview
4. ✅ Specific error conditions
5. ✅ 20-150 words
6. ✅ Self-contained (no external refs needed)

**Remember:** The description IS the API documentation for the LLM. Make it complete.
