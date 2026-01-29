# n8n JSON Schemas

Use these structures when generating JSON for n8n workflows.

## Workflow Structure (Base)

```json
{
  "name": "Workflow Name",
  "nodes": [
    // Array of Node Objects
  ],
  "connections": {
    // Map of Connections
  },
  "active": false,
  "settings": {},
  "tags": []
}
```

## Node Object Structure

Every node in the `nodes` array must follow this schema:

```json
{
  "parameters": {
    // Node-specific configuration (e.g., URL, HTTP method, function code)
  },
  "id": "uuid-v4", // Must be unique for each node
  "name": "Node Name", // Display name in UI
  "type": "n8n-nodes-base.nodeType", // e.g., n8n-nodes-base.httpRequest
  "typeVersion": 1,
  "position": [100, 200] // [x, y] coordinates for visual layout
}
```

## Connection Structure

Connections define the data flow between nodes.

```json
"connections": {
  "Source Node Name": {
    "main": [
      [
        {
          "node": "Target Node Name",
          "type": "main",
          "index": 0
        }
      ]
    ]
  }
}
```
