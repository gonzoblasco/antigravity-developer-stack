#!/usr/bin/env python3
"""
Tool Schema Validator

Validates JSON Schema for AI agent tools against best practices.
This script exemplifies the error handling and output structure patterns
taught in the agent-tool-builder skill.

Usage:
    python validate_tool_schema.py path/to/schema.json
    python validate_tool_schema.py --self-check  # Validate this script's principles
"""

import json
import sys
from typing import Dict, List, Any
from pathlib import Path


class ValidationResult:
    """Structured validation result following best practices."""
    
    def __init__(self):
        self.valid = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.suggestions: List[str] = []
    
    def add_error(self, message: str):
        """Add critical error (makes schema invalid)."""
        self.valid = False
        self.errors.append(message)
    
    def add_warning(self, message: str):
        """Add warning (best practice violation but not invalid)."""
        self.warnings.append(message)
    
    def add_suggestion(self, message: str):
        """Add improvement suggestion."""
        self.suggestions.append(message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Return structured dict for easy consumption."""
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "suggestions": self.suggestions
        }
    
    def print_report(self):
        """Print human-readable report."""
        if self.valid and not self.warnings and not self.suggestions:
            print("✅ Schema is valid and follows all best practices!")
            return
        
        if self.errors:
            print("\n❌ ERRORS (must fix):")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS (should fix):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if self.suggestions:
            print("\n💡 SUGGESTIONS (nice to have):")
            for suggestion in self.suggestions:
                print(f"  - {suggestion}")
        
        if self.valid:
            print("\n✅ Schema is valid but has improvement opportunities")
        else:
            print("\n❌ Schema validation failed")


def validate_tool_schema(schema: Dict[str, Any]) -> ValidationResult:
    """
    Validate a tool schema against best practices.
    
    Args:
        schema: Tool schema dict (should have 'name', 'description', 'inputSchema')
    
    Returns:
        ValidationResult with errors, warnings, and suggestions
    """
    result = ValidationResult()
    
    # Check required top-level fields
    if "name" not in schema:
        result.add_error("Schema missing required field 'name'")
    
    if "description" not in schema:
        result.add_error("Schema missing required field 'description'")
    else:
        validate_description(schema["description"], result)
    
    if "inputSchema" not in schema:
        result.add_error("Schema missing required field 'inputSchema'")
    else:
        validate_input_schema(schema["inputSchema"], result)
    
    return result


def validate_description(description: str, result: ValidationResult):
    """Validate tool description quality."""
    word_count = len(description.split())
    
    if word_count < 20:
        result.add_error(
            f"Description is too short ({word_count} words, minimum 20). "
            "Should specify: what it does, input format, output format, and possible errors."
        )
    
    if word_count > 150:
        result.add_warning(
            f"Description is very long ({word_count} words, recommended < 150). "
            "Consider moving details to field descriptions or documentation."
        )
    
    # Check for key elements
    has_action = any(verb in description.lower() for verb in 
                     ["search", "create", "update", "delete", "validate", "process", 
                      "fetch", "retrieve", "send", "execute", "analyze"])
    
    if not has_action:
        result.add_warning(
            "Description should start with an action verb (e.g., 'Searches', 'Creates', 'Validates')"
        )
    
    has_input_info = any(word in description.lower() for word in 
                         ["accept", "require", "take", "input", "parameter"])
    
    if not has_input_info:
        result.add_suggestion("Description should mention what inputs it accepts")
    
    has_output_info = any(word in description.lower() for word in 
                          ["return", "output", "provide", "result"])
    
    if not has_output_info:
        result.add_suggestion("Description should specify what it returns")
    
    has_error_info = any(word in description.lower() for word in 
                         ["throw", "error", "fail", "exception"])
    
    if not has_error_info:
        result.add_suggestion("Description should mention possible errors/exceptions")


def validate_input_schema(input_schema: Dict[str, Any], result: ValidationResult):
    """Validate input schema structure and properties."""
    
    if input_schema.get("type") != "object":
        result.add_warning("Input schema type should be 'object' for clarity")
    
    properties = input_schema.get("properties", {})
    
    if not properties:
        result.add_warning("Input schema has no properties defined")
        return
    
    required = input_schema.get("required", [])
    
    # Validate each property
    for prop_name, prop_schema in properties.items():
        validate_property(prop_name, prop_schema, prop_name in required, result)
    
    # Check if too many required fields
    if len(required) > 5:
        result.add_warning(
            f"Many required fields ({len(required)}). Consider which are truly necessary."
        )


def validate_property(
    name: str, 
    schema: Dict[str, Any], 
    is_required: bool, 
    result: ValidationResult,
    path: str = ""
):
    """Validate individual property schema."""
    full_path = f"{path}.{name}" if path else name
    
    # Check for description
    if "description" not in schema:
        result.add_error(f"Property '{full_path}' missing description")
    
    # Check type specificity
    prop_type = schema.get("type")
    
    if not prop_type:
        result.add_error(f"Property '{full_path}' missing type")
        return
    
    # Warn about 'any' type
    if prop_type == "any":
        result.add_warning(
            f"Property '{full_path}' uses 'any' type. Consider specific type or union."
        )
    
    # Check for constraints on strings
    if prop_type == "string":
        if "enum" not in schema and "pattern" not in schema:
            if "minLength" not in schema and "maxLength" not in schema:
                result.add_suggestion(
                    f"String property '{full_path}' has no constraints (enum/pattern/length). "
                    "Consider adding validation."
                )
        
        # Check if enum would be better than free string
        if "description" in schema and any(word in schema["description"].lower() 
                                          for word in ["one of", "either", "options"]):
            result.add_suggestion(
                f"Property '{full_path}' description suggests limited options. "
                "Consider using 'enum' instead of free string."
            )
    
    # Check for constraints on numbers
    if prop_type in ["number", "integer"]:
        if "minimum" not in schema and "maximum" not in schema:
            result.add_suggestion(
                f"Numeric property '{full_path}' has no min/max constraints. "
                "Consider adding sensible bounds."
            )
    
    # Check for defaults on optional fields
    if not is_required and "default" not in schema and prop_type in ["string", "number", "integer", "boolean"]:
        result.add_suggestion(
            f"Optional property '{full_path}' has no default value. "
            "Consider providing a sensible default."
        )
    
    # Check arrays
    if prop_type == "array":
        if "items" not in schema:
            result.add_error(f"Array property '{full_path}' missing 'items' specification")
        
        if "minItems" not in schema and "maxItems" not in schema:
            result.add_suggestion(
                f"Array property '{full_path}' has no size constraints. "
                "Consider adding minItems/maxItems for safety."
            )
    
    # Check nested objects (avoid deep nesting)
    if prop_type == "object":
        nested_props = schema.get("properties", {})
        
        if nested_props:
            depth = len(path.split(".")) if path else 0
            
            if depth >= 2:
                result.add_warning(
                    f"Deep nesting detected at '{full_path}' (level {depth}). "
                    "Consider flattening the schema."
                )
            
            # Recursively validate nested properties
            nested_required = schema.get("required", [])
            for nested_name, nested_schema in nested_props.items():
                validate_property(
                    nested_name, 
                    nested_schema, 
                    nested_name in nested_required, 
                    result,
                    full_path
                )


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python validate_tool_schema.py <schema.json>")
        print("       python validate_tool_schema.py --self-check")
        sys.exit(1)
    
    if sys.argv[1] == "--self-check":
        print("🔍 Self-check: This script follows these principles:\n")
        print("✅ Structured error output (ValidationResult class)")
        print("✅ Clear error messages with context and suggestions")
        print("✅ Distinction between errors, warnings, and suggestions")
        print("✅ Helper functions for readability")
        print("✅ Type hints for clarity")
        print("✅ Comprehensive docstrings")
        print("\n💡 This structure is what the agent-tool-builder skill teaches!")
        return
    
    schema_path = Path(sys.argv[1])
    
    if not schema_path.exists():
        print(f"❌ Error: File not found: {schema_path}")
        print("\nSuggestion: Verify the file path is correct")
        sys.exit(1)
    
    try:
        with open(schema_path) as f:
            schema = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {schema_path}")
        print(f"   {str(e)}")
        print("\nSuggestion: Validate JSON syntax using a JSON validator")
        sys.exit(1)
    
    result = validate_tool_schema(schema)
    result.print_report()
    
    sys.exit(0 if result.valid else 1)


if __name__ == "__main__":
    main()
