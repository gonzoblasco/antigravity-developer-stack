"""
MCP Tool Template

Complete FastMCP tool template following agent-tool-builder best practices.
This exemplifies all the principles taught in the skill.

Usage:
    1. Copy this template
    2. Replace all [TODO] placeholders
    3. Implement core logic
    4. Test with baseline scenarios
    5. Validate with: python scripts/validate_tool_schema.py
"""

from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("my-tool-server")


@mcp.tool()
def example_search_tool(
    query: str,
    limit: int = 10,
    filters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    [TODO: Replace with your clear, complete description using this template:]
    
    Searches [WHAT] using [METHOD].
    Accepts query (string, 1-500 chars), optional limit (int, 1-100, default 10),
    and optional filters object with {field: value} pairs.
    Returns {results: array of {id, title, score}, total: int, query_time_ms: int}.
    Throws 'invalid_query' if query is empty/too long, 'service_unavailable' 
    if search service is down.
    
    Args:
        query: Search query in natural language (1-500 characters)
        limit: Maximum number of results to return (1-100, default: 10)
        filters: Optional filters as {field_name: filter_value}
    
    Returns:
        {
            "results": [
                {
                    "id": str,          # Unique identifier
                    "title": str,       # Result title
                    "content": str,     # Content snippet (first 200 chars)
                    "score": float      # Relevance score 0.0-1.0
                }
            ],
            "total": int,               # Total matching results (may exceed limit)
            "query_time_ms": int,       # Query execution time
            "filters_applied": dict     # Echo of filters used
        }
    
    Raises:
        ValueError: If query is invalid (empty, too long, malformed)
        ServiceError: If backend search service is unavailable
    
    Examples:
        >>> result = example_search_tool("machine learning", limit=5)
        >>> print(len(result["results"]))
        5
        
        >>> result = example_search_tool("python", filters={"category": "programming"})
        >>> print(result["filters_applied"])
        {'category': 'programming'}
    """
    
    # ========================================================================
    # LEVEL 1: INPUT VALIDATION
    # ========================================================================
    # Validate inputs beyond JSON Schema constraints
    # Return structured errors that help LLM recover
    
    if not query or not query.strip():
        return {
            "error": {
                "type": "validation_error",
                "field": "query",
                "message": "Query cannot be empty",
                "provided_value": query,
                "suggestions": [
                    "Provide a non-empty search query",
                    "Example: 'machine learning best practices'",
                    "Query should be 1-500 characters"
                ]
            }
        }
    
    if len(query) > 500:
        return {
            "error": {
                "type": "validation_error",
                "field": "query",
                "message": f"Query too long: {len(query)} chars (max 500)",
                "provided_value": query[:50] + "...",
                "suggestions": [
                    "Shorten the query to 500 characters or less",
                    "Focus on key search terms"
                ]
            }
        }
    
    if limit < 1 or limit > 100:
        return {
            "error": {
                "type": "validation_error",
                "field": "limit",
                "message": f"Limit {limit} out of range (1-100)",
                "provided_value": limit,
                "suggestions": [
                    "Use limit between 1 and 100",
                    "Default is 10 if not specified"
                ]
            }
        }
    
    # Validate filters if provided
    if filters:
        allowed_filter_fields = ["category", "date_range", "status"]
        invalid_fields = set(filters.keys()) - set(allowed_filter_fields)
        
        if invalid_fields:
            return {
                "error": {
                    "type": "validation_error",
                    "field": "filters",
                    "message": f"Invalid filter fields: {', '.join(invalid_fields)}",
                    "provided_value": filters,
                    "suggestions": [
                        f"Allowed filter fields: {', '.join(allowed_filter_fields)}",
                        "Remove invalid fields or use allowed ones"
                    ]
                }
            }
    
    # ========================================================================
    # LEVEL 2: CORE LOGIC
    # ========================================================================
    # Implement the actual tool functionality
    # Handle different cases and edge conditions
    
    try:
        logger.info(f"Searching for: {query[:50]}... (limit={limit})")
        
        # TODO: Replace with actual implementation
        # Example structure:
        # results = search_service.query(
        #     query=query,
        #     limit=limit,
        #     filters=filters or {}
        # )
        
        # MOCK IMPLEMENTATION - Replace this
        import time
        start_time = time.time()
        
        # Simulated results
        mock_results = [
            {
                "id": f"doc_{i}",
                "title": f"Result {i} for '{query}'",
                "content": f"This is a mock result matching '{query}'. " * 3,
                "score": 1.0 - (i * 0.1)
            }
            for i in range(min(limit, 5))
        ]
        
        query_time_ms = int((time.time() - start_time) * 1000)
        
        # ====================================================================
        # LEVEL 3: STRUCTURED RESPONSE
        # ====================================================================
        # Return well-structured output matching documented schema
        
        return {
            "results": mock_results,
            "total": len(mock_results),
            "query_time_ms": query_time_ms,
            "filters_applied": filters or {},
            "status": "success"
        }
    
    except ConnectionError as e:
        # ====================================================================
        # LEVEL 4: ERROR HANDLING
        # ====================================================================
        # Return structured errors that guide LLM to recovery
        
        logger.error(f"Search service unavailable: {e}")
        
        return {
            "error": {
                "type": "service_unavailable",
                "message": "Search service is temporarily unavailable",
                "details": str(e),
                "retry": True,
                "retry_after_seconds": 60,
                "suggestions": [
                    "Wait 60 seconds and retry the search",
                    "If problem persists, check service status",
                    "Try a simpler query in the meantime"
                ]
            }
        }
    
    except Exception as e:
        # Catch-all for unexpected errors
        logger.exception(f"Unexpected error during search: {e}")
        
        return {
            "error": {
                "type": "internal_error",
                "message": f"Unexpected error: {type(e).__name__}",
                "details": str(e),
                "suggestions": [
                    "Report this error if it persists",
                    "Try again with different parameters",
                    "Check logs for detailed error information"
                ]
            }
        }


# ============================================================================
# ADDITIONAL TOOLS - Add more tools following same pattern
# ============================================================================

@mcp.tool()
def validate_configuration(
    config: Dict[str, Any],
    schema_id: str
) -> Dict[str, Any]:
    """
    Validates user configuration against defined JSON schema.
    
    Accepts config (object) and schema_id (string).
    Returns {valid: boolean, errors: array of {field, message, suggestion}}.
    Throws 'schema_not_found' if schema_id doesn't exist.
    
    Args:
        config: Configuration object to validate
        schema_id: ID of the validation schema to use
    
    Returns:
        {
            "valid": bool,
            "errors": [
                {
                    "field": str,
                    "message": str,
                    "suggestion": str
                }
            ]
        }
    """
    # TODO: Implement following same pattern as above
    pass


# ============================================================================
# SERVER STARTUP
# ============================================================================

if __name__ == "__main__":
    # Run the MCP server
    logger.info("Starting MCP tool server...")
    mcp.run()
