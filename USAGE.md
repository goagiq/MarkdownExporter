# Markdown Exporter - Usage Guide

This guide provides comprehensive instructions for using the Markdown Exporter with MCP integration.

## 🚀 Quick Start

### 1. Start the MCP Server

```bash
# Start the simple MCP server (recommended)
python simple_mcp_server.py
```

The server will start on `http://localhost:8001` and provide:
- MCP endpoint at `http://localhost:8001/mcp`
- Health check at `http://localhost:8001/health`
- API documentation at `http://localhost:8001/docs`

### 2. Test the Connection

```bash
# Test MCP endpoint
curl -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}'

# Test health endpoint
curl http://localhost:8001/health
```

### 3. Use the MCP Client

```python
from simple_mcp_client import SimpleMCPClient

# Create client
client = SimpleMCPClient("http://localhost:8001/mcp")

# List available tools
tools = client.list_tools()
print(f"Available tools: {[tool['name'] for tool in tools]}")

# Call a tool
result = client.call_tool("get_summary", {
    "url": "https://example.com",
    "num_sentences": 3
})
print(f"Result: {result}")
```

## 📋 Available MCP Tools

### 1. `get_summary`
Get a summary of a webpage.

**Parameters:**
- `url` (string, required): URL to summarize
- `num_sentences` (integer, optional): Number of sentences (default: 3)

**Example:**
```python
result = client.call_tool("get_summary", {
    "url": "https://example.com",
    "num_sentences": 5
})
```

### 2. `convert_markdown_to_word`
Convert markdown content to Word document.

**Parameters:**
- `content` (string, required): Markdown content to convert

**Example:**
```python
markdown_content = """# Sample Document

## Introduction
This is a sample markdown document.

### Features
- **Bold text**
- *Italic text*
- `Code snippets`

## Conclusion
This demonstrates markdown conversion.
"""

result = client.call_tool("convert_markdown_to_word", {
    "content": markdown_content
})
```

### 3. `convert_markdown_to_pdf`
Convert markdown content to PDF.

**Parameters:**
- `content` (string, required): Markdown content to convert

**Example:**
```python
result = client.call_tool("convert_markdown_to_pdf", {
    "content": "# Hello World\n\nThis is a PDF document."
})
```

### 4. `convert_markdown_to_html`
Convert markdown content to HTML.

**Parameters:**
- `content` (string, required): Markdown content to convert

**Example:**
```python
result = client.call_tool("convert_markdown_to_html", {
    "content": "# Hello World\n\nThis is an HTML document."
})
```

## 🐳 Docker Usage

### Build and Run with Docker

```bash
# Build the image
docker build -t markdownexporter .

# Run the container
docker run -p 8001:8001 -v $(pwd)/results:/app/results markdownexporter
```

### Using Docker Compose

```bash
# Start the service
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop the service
docker-compose down
```

### Docker Environment Variables

```yaml
# docker-compose.yml
environment:
  - OLLAMA_HOST=http://host.docker.internal:11434
  - OLLAMA_MODEL=llama3
  - LOG_LEVEL=INFO
  - MCP_PORT=8001
  - API_PORT=8001
```

## 🔧 Configuration

### Configuration File (`config.yaml`)

```yaml
server:
  mcp_port: 8001
  api_port: 8001
  ollama_host: "http://localhost:11434"
  ollama_model: "llama3"

conversion:
  default_format: "word"
  enable_mermaid: true
  enable_images: true
  table_alignment: "left"
  remove_unicode: true
  remove_emoji: true

logging:
  level: "INFO"
  format: "json"
  output: "stdout"

security:
  allowed_extensions: [".md", ".markdown"]
  max_file_size: "10MB"
  validate_file_types: true
```

### Environment Variables

```bash
export OLLAMA_HOST=http://localhost:11434
export OLLAMA_MODEL=llama3
export LOG_LEVEL=INFO
export MCP_PORT=8001
export API_PORT=8001
```

## 🧪 Testing

### Test Scripts

```bash
# Test MCP functionality
python test_mcp_standalone.py

# Test MCP debug
python test_mcp_debug.py

# Test MCP working functionality
python test_mcp_working.py
```

### Manual Testing

```bash
# Test MCP endpoint
curl -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}'

# Test tool call
curl -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "get_summary", "arguments": {"url": "https://example.com", "num_sentences": 2}}}'
```

## 🔍 Troubleshooting

### Common Issues

1. **Port 8001 already in use**
   ```bash
   # Find process using port 8001
   netstat -ano | findstr :8001
   
   # Kill the process
   taskkill //PID <PID> //F
   ```

2. **MCP client can't connect**
   ```bash
   # Check if server is running
   curl http://localhost:8001/health
   
   # Check server logs
   docker-compose logs markdownexporter
   ```

3. **Missing dependencies**
   ```bash
   # Install dependencies
   pip install -e .
   
   # Check virtual environment
   python -c "import requests; print('requests available')"
   ```

### Debug Mode

```bash
# Start server with debug logging
LOG_LEVEL=DEBUG python simple_mcp_server.py

# Test with verbose output
python test_mcp_debug.py
```

## 📊 Monitoring

### Health Checks

```bash
# Check server health
curl http://localhost:8001/health

# Check MCP endpoint
curl http://localhost:8001/mcp
```

### Logs

```bash
# View server logs
docker-compose logs -f markdownexporter

# View application logs
tail -f logs/app.log
```

## 🔄 Integration Examples

### Python Integration

```python
import asyncio
from simple_mcp_client import SimpleMCPClient

async def main():
    client = SimpleMCPClient("http://localhost:8001/mcp")
    
    # Initialize connection
    init_result = client.initialize()
    print(f"Initialization: {init_result}")
    
    # List tools
    tools = client.list_tools()
    print(f"Available tools: {[tool['name'] for tool in tools]}")
    
    # Convert markdown
    markdown_content = "# Hello World\n\nThis is a test document."
    result = client.call_tool("convert_markdown_to_word", {
        "content": markdown_content
    })
    print(f"Conversion result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

### JavaScript Integration

```javascript
// Using fetch API
async function callMCPTool(toolName, arguments) {
    const response = await fetch('http://localhost:8001/mcp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            jsonrpc: '2.0',
            id: 1,
            method: 'tools/call',
            params: {
                name: toolName,
                arguments: arguments
            }
        })
    });
    
    return await response.json();
}

// Example usage
callMCPTool('get_summary', {
    url: 'https://example.com',
    num_sentences: 3
}).then(result => {
    console.log('Result:', result);
});
```

### cURL Integration

```bash
#!/bin/bash

# Function to call MCP tool
call_mcp_tool() {
    local tool_name=$1
    local arguments=$2
    
    curl -X POST http://localhost:8001/mcp \
        -H "Content-Type: application/json" \
        -d "{
            \"jsonrpc\": \"2.0\",
            \"id\": 1,
            \"method\": \"tools/call\",
            \"params\": {
                \"name\": \"$tool_name\",
                \"arguments\": $arguments
            }
        }"
}

# Example usage
call_mcp_tool "get_summary" '{"url": "https://example.com", "num_sentences": 3}'
```

## 📈 Performance

### Optimization Tips

1. **Use connection pooling** for multiple requests
2. **Batch operations** when possible
3. **Monitor memory usage** for large documents
4. **Use appropriate timeouts** for long-running operations

### Benchmarks

- **Small documents** (< 1KB): ~100ms
- **Medium documents** (1-10KB): ~500ms
- **Large documents** (> 10KB): ~2-5s

## 🔐 Security

### Best Practices

1. **Use HTTPS** in production
2. **Implement authentication** for sensitive operations
3. **Validate input** before processing
4. **Limit file sizes** to prevent DoS attacks
5. **Use non-root user** in Docker containers

### Security Headers

```python
# Add security headers to your application
headers = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
}
```

## 📚 Additional Resources

- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Python-docx Documentation](https://python-docx.readthedocs.io/)
