# JSON Schema Deep Dive

Extended documentation for advanced JSON Schema patterns in AI agent tools.

## Table of Contents

1. [Advanced Type Patterns](#advanced-type-patterns)
2. [Conditional Schemas](#conditional-schemas)
3. [Cross-Field Validation](#cross-field-validation)
4. [Performance Considerations](#performance-considerations)
5. [Common Patterns Library](#common-patterns-library)

---

## Advanced Type Patterns

### Union Types with oneOf

When a parameter can be **one of several** distinct types:

```json
{
  "data": {
    "oneOf": [
      {
        "type": "string",
        "description": "JSON string representation"
      },
      {
        "type": "object",
        "description": "Structured object",
        "properties": {
          "field1": { "type": "string" },
          "field2": { "type": "number" }
        }
      }
    ],
    "description": "Either a JSON string or a structured object"
  }
}
```

**Use when:**

- Parameter can be different types
- Each type has different structure
- LLM needs to choose appropriate format

**Avoid:**

- More than 3 options (confusing)
- Types that are too similar

### Intersection Types with allOf

When a parameter **must satisfy multiple** schemas:

```json
{
  "user": {
    "allOf": [
      {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "email": { "type": "string" }
        },
        "required": ["id", "email"]
      },
      {
        "properties": {
          "role": {
            "type": "string",
            "enum": ["admin", "user"]
          }
        }
      }
    ]
  }
}
```

**Use when:**

- Extending base schema
- Combining multiple constraints
- Reusing schema fragments

### anyOf for Flexible Matching

When parameter can match **one or more** schemas:

```json
{
  "filter": {
    "anyOf": [
      { "properties": { "category": { "type": "string" } } },
      { "properties": { "price_range": { "type": "object" } } },
      { "properties": { "date_after": { "type": "string" } } }
    ],
    "description": "Filter by category, price range, or date (or combinations)"
  }
}
```

**Use when:**

- Multiple optional properties
- Flexible matching needed
- Complex filter scenarios

---

## Conditional Schemas

### if/then/else Pattern

Conditional validation based on field values:

```json
{
  "type": "object",
  "properties": {
    "payment_method": {
      "type": "string",
      "enum": ["credit_card", "bank_transfer", "crypto"]
    },
    "payment_details": {
      "type": "object"
    }
  },
  "if": {
    "properties": {
      "payment_method": { "const": "credit_card" }
    }
  },
  "then": {
    "properties": {
      "payment_details": {
        "properties": {
          "card_number": { "type": "string", "pattern": "^[0-9]{16}$" },
          "cvv": { "type": "string", "pattern": "^[0-9]{3,4}$" }
        },
        "required": ["card_number", "cvv"]
      }
    }
  },
  "else": {
    "if": {
      "properties": {
        "payment_method": { "const": "bank_transfer" }
      }
    },
    "then": {
      "properties": {
        "payment_details": {
          "properties": {
            "account_number": { "type": "string" },
            "routing_number": { "type": "string" }
          },
          "required": ["account_number", "routing_number"]
        }
      }
    }
  }
}
```

**Use when:**

- Required fields depend on other fields
- Structure varies based on mode/type
- Different validation rules per case

---

## Cross-Field Validation

### Dependencies

**Simple dependencies** (field presence):

```json
{
  "properties": {
    "credit_card": { "type": "string" },
    "cvv": { "type": "string" }
  },
  "dependencies": {
    "credit_card": ["cvv"]
  }
}
```

If `credit_card` is present, `cvv` must also be present.

**Schema dependencies** (conditional schemas):

```json
{
  "dependencies": {
    "credit_card": {
      "properties": {
        "billing_address": {
          "type": "object",
          "required": ["street", "city", "zip"]
        }
      },
      "required": ["billing_address"]
    }
  }
}
```

### Property Patterns

Validate properties matching a pattern:

```json
{
  "patternProperties": {
    "^custom_field_": {
      "type": "string",
      "maxLength": 100
    }
  },
  "additionalProperties": false
}
```

Allows `custom_field_1`, `custom_field_2`, etc., all as strings ≤ 100 chars.

---

## Performance Considerations

### Schema Complexity Impact

**Token usage increases with:**

- Deep nesting (> 3 levels)
- Many properties (> 10)
- Complex conditionals
- Large descriptions

**Optimization strategies:**

1. **Flatten when possible:**

```json
// ❌ Nested (uses more tokens)
{
  "user": {
    "properties": {
      "profile": {
        "properties": {
          "bio": {"type": "string"}
        }
      }
    }
  }
}

// ✅ Flattened (more efficient)
{
  "user_bio": {"type": "string"}
}
```

2. **Group related optional params:**

```json
// ❌ Many optional top-level params
{
  "param1": {...},
  "param2": {...},
  "param3": {...}
}

// ✅ Grouped in optional object
{
  "options": {
    "type": "object",
    "properties": {
      "param1": {...},
      "param2": {...}
    }
  }
}
```

3. **Use references for repeated patterns:**

```json
{
  "$defs": {
    "address": {
      "type": "object",
      "properties": {
        "street": { "type": "string" },
        "city": { "type": "string" }
      }
    }
  },
  "properties": {
    "billing_address": { "$ref": "#/$defs/address" },
    "shipping_address": { "$ref": "#/$defs/address" }
  }
}
```

---

## Common Patterns Library

### Date/Time Patterns

```json
{
  "date": {
    "type": "string",
    "format": "date",
    "description": "Date in YYYY-MM-DD format",
    "examples": ["2024-01-15"]
  },
  "datetime": {
    "type": "string",
    "format": "date-time",
    "description": "ISO 8601 datetime",
    "examples": ["2024-01-15T10:30:00Z"]
  },
  "date_range": {
    "type": "object",
    "properties": {
      "start": { "type": "string", "format": "date-time" },
      "end": { "type": "string", "format": "date-time" }
    },
    "required": ["start", "end"]
  }
}
```

### Email/URL Patterns

```json
{
  "email": {
    "type": "string",
    "format": "email",
    "description": "Valid email address"
  },
  "url": {
    "type": "string",
    "format": "uri",
    "pattern": "^https?://",
    "description": "HTTP(S) URL"
  }
}
```

### Pagination Pattern

```json
{
  "pagination": {
    "type": "object",
    "properties": {
      "page": {
        "type": "integer",
        "minimum": 1,
        "default": 1,
        "description": "Page number (1-indexed)"
      },
      "page_size": {
        "type": "integer",
        "minimum": 1,
        "maximum": 100,
        "default": 20,
        "description": "Items per page (max 100)"
      }
    }
  }
}
```

### Sort Pattern

```json
{
  "sort": {
    "type": "object",
    "properties": {
      "field": {
        "type": "string",
        "enum": ["created_at", "updated_at", "name", "price"]
      },
      "direction": {
        "type": "string",
        "enum": ["asc", "desc"],
        "default": "desc"
      }
    },
    "required": ["field"]
  }
}
```

### Filter Pattern

```json
{
  "filters": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "field": {
          "type": "string",
          "description": "Field name to filter on"
        },
        "operator": {
          "type": "string",
          "enum": ["eq", "gt", "lt", "contains", "in"],
          "description": "Comparison operator"
        },
        "value": {
          "description": "Value to compare against"
        }
      },
      "required": ["field", "operator", "value"]
    },
    "examples": [
      [
        { "field": "category", "operator": "eq", "value": "electronics" },
        { "field": "price", "operator": "lt", "value": 500 }
      ]
    ]
  }
}
```

### Geolocation Pattern

```json
{
  "location": {
    "type": "object",
    "properties": {
      "latitude": {
        "type": "number",
        "minimum": -90,
        "maximum": 90
      },
      "longitude": {
        "type": "number",
        "minimum": -180,
        "maximum": 180
      }
    },
    "required": ["latitude", "longitude"]
  }
}
```

### File Upload Pattern

```json
{
  "file": {
    "type": "object",
    "properties": {
      "url": {
        "type": "string",
        "format": "uri",
        "description": "URL to file to process"
      },
      "mime_type": {
        "type": "string",
        "enum": ["application/pdf", "image/png", "image/jpeg"],
        "description": "File MIME type"
      },
      "size_bytes": {
        "type": "integer",
        "maximum": 10485760,
        "description": "File size in bytes (max 10MB)"
      }
    },
    "required": ["url", "mime_type"]
  }
}
```

---

## Validation Testing

### Test Your Schemas

Use these tools to validate your JSON schemas:

```bash
# Python
pip install jsonschema
python -c "from jsonschema import validate, ValidationError; ..."

# Online validators
# - https://www.jsonschemavalidator.net/
# - https://jsonschemalint.com/
```

### Example Test Cases

```python
from jsonschema import validate, ValidationError

schema = {...}  # Your schema

# Test valid input
validate({"query": "test", "limit": 10}, schema)  # Should pass

# Test invalid input
try:
    validate({"query": "", "limit": 500}, schema)
except ValidationError as e:
    print(f"Validation failed: {e.message}")
```

---

## Best Practices Summary

1. **Keep it simple:** Start with basic types, add complexity only when needed
2. **Use constraints:** min/max, patterns, enums prevent invalid data
3. **Clear descriptions:** Every field should explain its purpose
4. **Examples for complex types:** Show, don't just tell
5. **Test thoroughly:** Validate against real-world inputs
6. **Optimize for tokens:** Flatten, group, reference repeated patterns
7. **Consider LLM understanding:** Schemas guide the LLM, make them clear

---

## Further Reading

- [JSON Schema Official Spec](https://json-schema.org/specification.html)
- [Understanding JSON Schema](https://json-schema.org/understanding-json-schema/)
- [JSON Schema Validator](https://www.jsonschemavalidator.net/)
