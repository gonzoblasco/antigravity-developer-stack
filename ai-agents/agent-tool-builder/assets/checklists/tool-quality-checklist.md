# Tool Quality Checklist

Use this checklist before deploying any AI agent tool to catch common issues.

## Schema Design

### Type Specificity

- [ ] All parameters have specific types (no `any` or generic `object`)
- [ ] Used `integer` for countable items (not `number`)
- [ ] Used `enum` for finite, known choice sets
- [ ] Arrays specify `items` type
- [ ] Nested objects are kept shallow (< 3 levels)

### Descriptions

- [ ] Every field has a clear `description`
- [ ] Tool description is 20-150 words
- [ ] Descriptions are self-contained (no assumed context)
- [ ] Complex parameters include examples

### Constraints

- [ ] String parameters have `minLength`/`maxLength` or `pattern`
- [ ] Numeric parameters have `minimum`/`maximum` bounds
- [ ] Arrays have `minItems`/`maxItems` limits
- [ ] Required fields are truly necessary (not "nice to have")
- [ ] Optional fields have sensible `default` values

### Examples

- [ ] Complex/unintuitive parameters include `examples`
- [ ] Date/time fields show format examples
- [ ] Nested objects have example structures

---

## Description Writing

### Completeness

- [ ] Starts with action verb (Searches, Creates, Validates, etc.)
- [ ] Specifies WHAT it does
- [ ] Describes INPUT format and constraints
  - Example: "query (string, 1-500 chars)"
- [ ] Describes OUTPUT structure and key fields
  - Example: "Returns {results: array, total: int}"
- [ ] Mentions possible ERRORS and conditions
  - Example: "Throws 'invalid_query' if query is empty"

### Clarity

- [ ] Can be understood without external documentation
- [ ] Uses concrete terms, not vague language
- [ ] Distinguishes "must", "should", "can" appropriately
- [ ] Mentions defaults for optional parameters
- [ ] Specifies any important limits or constraints

### Length

- [ ] At least 20 words (minimum for clarity)
- [ ] Not more than 150 words (avoid overwhelming)
- [ ] Details moved to field descriptions if too long

---

## Error Handling

### Error Structure

- [ ] Errors returned in consistent format
- [ ] Error object includes `type` field
- [ ] Error object includes `message` field (human-readable)
- [ ] Error object includes `suggestions` array (recovery guidance)

### Error Messages

- [ ] Messages are specific, not generic
  - ❌ "Invalid input"
  - ✅ "Field 'email' must match format: user@example.com"
- [ ] Messages help LLM understand what went wrong
- [ ] Messages suggest how to fix the error
- [ ] Include field name for validation errors
- [ ] Include provided value (when safe to echo)

### Error Types

- [ ] Validation errors distinguish field-level issues
- [ ] Service errors indicate retry-ability
- [ ] Not found errors suggest alternatives
- [ ] Permission errors explain what's needed
- [ ] No silent failures (empty results vs errors distinguished)

---

## Code Implementation

### Input Validation

- [ ] Schema validation via JSON Schema
- [ ] Additional business logic validation
- [ ] Clear error messages for invalid input
- [ ] Edge cases handled (empty strings, null, etc.)
- [ ] SQL injection / XSS protection where applicable

### Core Logic

- [ ] Main functionality clearly separated
- [ ] Errors caught and converted to structured format
- [ ] Logging for debugging (info, warn, error)
- [ ] Performance considerations (timeouts, limits)
- [ ] Graceful degradation where appropriate

### Output Structure

- [ ] Matches documented schema
- [ ] Includes all promised fields
- [ ] Field types match documentation
- [ ] Success responses include `status: "success"` or similar
- [ ] Error responses use `error` object

### Documentation

- [ ] Function docstring complete
- [ ] Args documented with types
- [ ] Returns documented with structure
- [ ] Raises documented with conditions
- [ ] Examples provided for complex usage

---

## Testing

### Happy Path

- [ ] Tool works with minimal required parameters
- [ ] Tool works with all optional parameters
- [ ] Output structure matches documentation
- [ ] Common use cases tested

### Edge Cases

- [ ] Empty strings handled
- [ ] Minimum/maximum values tested
- [ ] Null/undefined optional parameters handled
- [ ] Large inputs handled (or rejected appropriately)

### Error Cases

- [ ] Invalid parameters return structured errors
- [ ] Service unavailable handled gracefully
- [ ] Timeout scenarios handled
- [ ] Error messages tested for clarity

### LLM Integration

- [ ] Test with actual LLM (not just unit tests)
- [ ] Verify LLM interprets description correctly
- [ ] Verify LLM can recover from errors
- [ ] Check token efficiency of schema + description

---

## Best Practices Checklist

### Design Decisions

- [ ] Considered: Is this one tool or should it be split?
- [ ] Considered: Should this be a tool, resource, or prompt?
- [ ] Considered: Sync vs async execution?
- [ ] Tool name is descriptive and in snake_case
- [ ] Functionality is focused (does one thing well)

### Token Optimization

- [ ] Description is concise but complete
- [ ] No redundant information in description and field descriptions
- [ ] Complex examples moved to referenced files
- [ ] Schema doesn't include unnecessary fields

### Maintainability

- [ ] Code is well-commented
- [ ] Error types are consistent across tools
- [ ] Validation logic is reusable
- [ ] Tool follows team/project conventions

---

## Pre-Deploy Validation

Run these checks before deploying:

```bash
# Validate schema
python scripts/validate_tool_schema.py your_tool_schema.json

# Run unit tests
python -m pytest tests/test_your_tool.py

# Test with real LLM
# Use baseline scenarios from implementation_plan.md
```

### Final Checks

- [ ] Schema validation passes
- [ ] All unit tests pass
- [ ] Integration tests with LLM pass
- [ ] Documentation is up to date
- [ ] Checklist items above are satisfied

---

## Common Mistakes Reference

| Mistake             | How to Fix                                         |
| ------------------- | -------------------------------------------------- |
| Vague description   | Use template: "[ACTION] [WHAT] using [METHOD]..."  |
| Missing constraints | Add min/max lengths, bounds, patterns              |
| Generic errors      | Include field name, value, specific suggestions    |
| Silent failures     | Return structured error, not empty result          |
| Deep nesting        | Flatten to < 3 levels or split into multiple tools |
| No examples         | Add examples for complex/unintuitive parameters    |
| 'any' type overuse  | Use specific types or union (oneOf)                |
| Too many tools      | Consolidate related functionality                  |

---

## Success Criteria

Your tool is ready when:

- ✅ This entire checklist is completed
- ✅ Validation script passes with no errors
- ✅ LLM can use the tool correctly in baseline scenarios
- ✅ LLM can recover from common errors
- ✅ Token usage is reasonable for the functionality

**Remember:** A well-designed tool makes agents reliable. Take the time to get it right.
