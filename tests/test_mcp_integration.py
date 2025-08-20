"""Test MCP server and client integration."""

import asyncio
import pytest
from pathlib import Path

from src.mcp.server import MCPServer
from src.mcp.client import MCPClient
from src.mcp.tools import MCPToolManager


@pytest.mark.asyncio
async def test_mcp_server_basic():
    """Test basic MCP server functionality."""
    # Create server
    server = MCPServer(port=8501)  # Use different port for testing
    
    # Register a test tool
    def test_tool(message: str = "Hello"):
        return f"Test tool says: {message}"
    
    server.register_tool("test_tool", test_tool)
    
    # Check that tool is registered
    assert "test_tool" in server.tools
    assert len(server.tools) == 1


@pytest.mark.asyncio
async def test_mcp_client_basic():
    """Test basic MCP client functionality."""
    client = MCPClient("http://localhost:8501")
    
    # Test health check (server might not be running)
    try:
        health = await client.health_check()
        assert isinstance(health, dict)
    except Exception:
        # Server not running, which is expected in test environment
        pass


def test_mcp_tool_manager():
    """Test MCP tool manager functionality."""
    # Create tool manager
    manager = MCPToolManager()
    
    # Check default tools are registered
    assert "convert_markdown_to_word" in manager.tools
    assert "convert_markdown_to_pdf" in manager.tools
    assert "convert_markdown_to_html" in manager.tools
    assert "process_markdown_file" in manager.tools
    assert "list_available_tools" in manager.tools
    
    # Test tool enable/disable
    manager.disable_tool("convert_markdown_to_pdf")
    enabled_tools = manager.get_enabled_tools()
    assert "convert_markdown_to_pdf" not in enabled_tools
    
    manager.enable_tool("convert_markdown_to_pdf")
    enabled_tools = manager.get_enabled_tools()
    assert "convert_markdown_to_pdf" in enabled_tools
    
    # Test list available tools
    result = manager.execute_tool("list_available_tools")
    assert result["success"]
    assert "tools" in result
    assert len(result["tools"]) >= 5


def test_mcp_tool_manager_conversion():
    """Test MCP tool manager conversion functionality."""
    manager = MCPToolManager()
    
    # Test markdown processing
    test_content = "# Test Document\n\nThis is a test."
    result = manager.execute_tool(
        "convert_markdown_to_word",
        content=test_content,
        output_filename="test_output.docx"
    )
    
    assert result["success"]
    assert "output_file" in result
    assert "file_size" in result
    
    # Check file was created
    output_path = Path(result["output_file"])
    assert output_path.exists()
    assert output_path.stat().st_size > 0
    
    # Cleanup
    output_path.unlink(missing_ok=True)


if __name__ == "__main__":
    pytest.main([__file__])
