#!/usr/bin/env python3
"""
Tool Template Generator

Generates boilerplate code for AI agent tools following best practices.
Supports MCP (FastMCP), standard functions, and Anthropic tool formats.

Usage:
    python generate_tool_template.py --name search_docs --type mcp --params "query:string,limit:int"
    python generate_tool_template.py --name validate_config --type function --params "config:object"
"""

import argparse
import json
from typing import Dict, List, Any


TOOL_TYPES = ["mcp", "function", "anthropic"]


def parse_params(params_str: str) -> Dict[str, str]:
    """
    Parse parameter string into dict.
    
    Args:
        params_str: Comma-separated "name:type" pairs
                   Example: "query:string,limit:int,filters:object"
    
    Returns:
        Dict mapping parameter names to types
    """
    if not params_str:
        return {}
    
    params = {}
    for param in params_str.split(","):
        param = param.strip()
        if ":" not in param:
            raise ValueError(
                f"Invalid parameter format: '{param}'. "
                "Expected format: 'name:type' (e.g., 'query:string')"
            )
        
        name, typ = param.split(":", 1)
        params[name.strip()] = typ.strip()
    
    return params


def generate_json_schema(
    tool_name: str, 
    params: Dict[str, str]
) -> Dict[str, Any]:
    """
    Generate JSON Schema for tool parameters.
    
    Args:
        tool_name: Tool name in snake_case
        params: Dict of {param_name: param_type}
    
    Returns:
        Complete JSON Schema dict
    """
    properties = {}
    
    for name, typ in params.items():
        prop_schema = {"type": typ}
        
        # Add description placeholder
        prop_schema["description"] = f"[TODO: Describe {name}]"
        
        # Add type-specific hints
        if typ == "string":
            prop_schema["_hint"] = "Consider adding: minLength, maxLength, enum, or pattern"
        elif typ in ["integer", "number"]:
            prop_schema["_hint"] = "Consider adding: minimum, maximum"
        elif typ == "array":
            prop_schema["items"] = {"type": "string"}
            prop_schema["_hint"] = "Specify items type and consider minItems/maxItems"
        elif typ == "object":
            prop_schema["properties"] = {}
            prop_schema["_hint"] = "Define nested properties"
        
        properties[name] = prop_schema
    
    # First parameter is typically required
    required = [list(params.keys())[0]] if params else []
    
    return {
        "name": tool_name,
        "description": "[TODO: Describe what this tool does, input format, output format, and possible errors]",
        "inputSchema": {
            "type": "object",
            "properties": properties,
            "required": required
        }
    }


def generate_mcp_code(tool_name: str, params: Dict[str, str]) -> str:
    """Generate FastMCP tool code."""
    
    # Function signature
    param_list = []
    for name, typ in params.items():
        python_type = {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
            "object": "dict",
            "array": "list"
        }.get(typ, "Any")
        
        param_list.append(f"{name}: {python_type}")
    
    # Make all but first param optional with defaults
    if len(param_list) > 1:
        for i in range(1, len(param_list)):
            name = list(params.keys())[i]
            typ = list(params.values())[i]
            default = {
                "string": '""',
                "integer": "0",
                "number": "0.0",
                "boolean": "False",
                "object": "{}",
                "array": "[]"
            }.get(typ, "None")
            param_list[i] = f"{param_list[i]} = {default}"
    
    params_str = ", ".join(param_list) if param_list else ""
    
    return f'''from fastmcp import FastMCP
from typing import Dict, Any

mcp = FastMCP("{tool_name.replace('_', '-')}")


@mcp.tool()
def {tool_name}({params_str}) -> Dict[str, Any]:
    """
    [TODO: Provide detailed description following template:]
    
    [ACTION] [WHAT] using [METHOD].
    Accepts [INPUT with types and constraints].
    Returns [OUTPUT structure with key fields].
    Throws [ERROR_TYPE] if [CONDITION].
    
    Args:
{chr(10).join(f"        {name}: [TODO: Describe {name}]" for name in params.keys())}
    
    Returns:
        {{
            "[result_field]": [type],  # TODO: Define output structure
            "status": "success"
        }}
    
    Raises:
        MCPError: If [TODO: specify error conditions]
    """
    # TODO: Input validation
    # Example:
    # if not query or len(query) > 500:
    #     raise ValueError("Query must be 1-500 characters")
    
    try:
        # TODO: Implement core logic
        result = None  # Replace with actual logic
        
        return {{
            "result": result,
            "status": "success"
        }}
    
    except Exception as e:
        # TODO: Return structured error
        return {{
            "error": {{
                "type": "operation_failed",
                "message": str(e),
                "suggestions": [
                    "Verify input parameters",
                    "[TODO: Add specific recovery suggestions]"
                ]
            }}
        }}


if __name__ == "__main__":
    # Run MCP server
    mcp.run()
'''


def generate_function_code(tool_name: str, params: Dict[str, str]) -> str:
    """Generate standard Python function code."""
    
    param_list = []
    for name, typ in params.items():
        python_type = {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
            "object": "dict",
            "array": "list"
        }.get(typ, "Any")
        param_list.append(f"{name}: {python_type}")
    
    params_str = ", ".join(param_list) if param_list else ""
    
    return f'''from typing import Dict, Any


def {tool_name}({params_str}) -> Dict[str, Any]:
    """
    [TODO: Provide detailed description following template:]
    
    [ACTION] [WHAT] using [METHOD].
    Accepts [INPUT with types and constraints].
    Returns [OUTPUT structure with key fields].
    Raises [ERROR_TYPE] if [CONDITION].
    
    Args:
{chr(10).join(f"        {name}: [TODO: Describe {name}]" for name in params.keys())}
    
    Returns:
        Dict with:
            - result: [TODO: describe result]
            - status: "success" or error dict
    
    Example:
        >>> result = {tool_name}({", ".join(f'{name}="example"' for name in list(params.keys())[:1])})
        >>> print(result["status"])
        success
    """
    # Validate inputs
    # TODO: Add validation logic
    
    try:
        # Core logic
        result = None  # TODO: Implement
        
        return {{
            "result": result,
            "status": "success"
        }}
    
    except ValueError as e:
        return {{
            "error": {{
                "type": "validation_error",
                "message": str(e),
                "suggestions": ["Check input format", "See documentation"]
            }}
        }}
    
    except Exception as e:
        return {{
            "error": {{
                "type": "operation_failed",
                "message": str(e),
                "suggestions": ["Retry the operation", "Check system status"]
            }}
        }}
'''


def generate_description_template() -> str:
    """Generate template for writing tool description."""
    return """
Tool Description Template
=========================

Fill in the placeholders below, then copy to your tool schema:

[ACTION] [WHAT] using [METHOD].
Accepts [INPUT with types and constraints].
Returns [OUTPUT structure with key fields].
Throws [ERROR_TYPE] if [CONDITION], [ERROR_TYPE2] if [CONDITION2].

Examples:
---------

Example 1 (Search):
Searches product database using full-text search. Accepts query (string, 1-200 chars), 
optional category filter (enum: electronics|books|clothing), and limit (int, 1-100, default 20). 
Returns array of {id, name, price, category, relevance_score}. Throws 'invalid_category' 
if category not recognized.

Example 2 (Validation):
Validates user configuration against defined JSON schema. Accepts config (object) and 
schema_id (string). Returns {valid: boolean, errors: array of {field, message, suggestion}}. 
Throws 'schema_not_found' if schema_id doesn't exist, 'invalid_schema' if schema is malformed.

Your Description:
-----------------
[Write your description here]
"""


def main():
    parser = argparse.ArgumentParser(
        description="Generate tool templates following best practices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --name search_docs --type mcp --params "query:string,limit:integer"
  %(prog)s --name validate_config --type function --params "config:object"
  %(prog)s --name analyze_data --type mcp --params "data:array,mode:string"
        """
    )
    
    parser.add_argument("--name", required=True, help="Tool name in snake_case")
    parser.add_argument("--type", choices=TOOL_TYPES, default="mcp", 
                       help="Type of tool to generate")
    parser.add_argument("--params", default="", 
                       help='Parameters as "name:type,name:type" (e.g., "query:string,limit:int")')
    parser.add_argument("--output", help="Output file (default: stdout)")
    
    args = parser.parse_args()
    
    try:
        params = parse_params(args.params)
    except ValueError as e:
        print(f"❌ Error: {e}")
        return 1
    
    # Generate schema
    schema = generate_json_schema(args.name, params)
    
    # Generate code
    if args.type == "mcp":
        code = generate_mcp_code(args.name, params)
    elif args.type == "function":
        code = generate_function_code(args.name, params)
    else:  # anthropic
        code = "# Anthropic tools use JSON schema format\n# See schema output below"
    
    # Generate description template
    desc_template = generate_description_template()
    
    # Output
    output = f"""
{'='*70}
Generated Tool Template: {args.name}
{'='*70}

1. JSON SCHEMA
-------------------------------------------------
{json.dumps(schema, indent=2)}

2. CODE TEMPLATE ({args.type.upper()})
-------------------------------------------------
{code}

3. DESCRIPTION TEMPLATE
-------------------------------------------------
{desc_template}

{'='*70}
Next Steps:
{'='*70}
1. Fill in all [TODO] placeholders in the code
2. Write a clear description using the template
3. Add specific validation logic for your use case
4. Test with the baseline scenarios from your skill
5. Run: python scripts/validate_tool_schema.py <your_schema.json>

✅ Remember: Good description + specific types = reliable tool
"""
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"✅ Template written to: {args.output}")
    else:
        print(output)
    
    return 0


if __name__ == "__main__":
    exit(main())
