"""MCP Client implementation using simple HTTP requests."""

import requests
import logging
from typing import Dict, List, Any, Optional

# Setup logging
logger = logging.getLogger(__name__)


class MCPClient:
    """MCP Client wrapper using simple HTTP requests."""
    
    def __init__(self, mcp_url: str = "http://localhost:8001/mcp"):
        """Initialize MCP client.
        
        Args:
            mcp_url: MCP server URL with /mcp endpoint
        """
        self.mcp_url = mcp_url
        self.request_id = 1
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def _make_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make a JSON-RPC request to the MCP server.
        
        Args:
            method: MCP method to call
            params: Method parameters
            
        Returns:
            Response from the server
        """
        request_data = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        
        self.request_id += 1
        
        try:
            response = self.session.post(self.mcp_url, json=request_data, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error making MCP request: {e}")
            return {"error": str(e)}
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        return False
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        pass
    
    def list_tools_sync(self) -> List[str]:
        """List available MCP tools synchronously.
        
        Returns:
            List of tool names
        """
        try:
            response = self._make_request("tools/list")
            if "result" in response and "tools" in response["result"]:
                return [tool["name"] for tool in response["result"]["tools"]]
            else:
                logger.error(f"Error listing tools: {response}")
                return []
        except Exception as e:
            logger.error(f"Error listing tools: {e}")
            return []
    
    def get_tools(self):
        """Get MCP tools.
        
        Returns:
            List of available tools
        """
        try:
            response = self._make_request("tools/list")
            if "result" in response and "tools" in response["result"]:
                return response["result"]["tools"]
            else:
                logger.error(f"Error getting tools: {response}")
                return []
        except Exception as e:
            logger.error(f"Error getting tools: {e}")
            return []
    
    def call_tool_sync(self, tool_name: str, **kwargs) -> Any:
        """Call an MCP tool synchronously.
        
        Args:
            tool_name: Name of the tool to call
            **kwargs: Tool parameters
            
        Returns:
            Tool execution result
        """
        try:
            params = {
                "name": tool_name,
                "arguments": kwargs
            }
            
            response = self._make_request("tools/call", params)
            
            if "result" in response and "content" in response["result"]:
                content = response["result"]["content"]
                if content and len(content) > 0:
                    return content[0].get("text", "")
            else:
                logger.error(f"Error calling tool {tool_name}: {response}")
                return {"error": "Tool call failed"}
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            return {"error": str(e)}
    
    def health_check(self) -> Dict[str, Any]:
        """Check server health by attempting to list tools.
        
        Returns:
            Health status
        """
        try:
            tools = self.list_tools_sync()
            return {
                "status": "healthy", 
                "tools_count": len(tools),
                "tools": tools
            }
        except Exception as e:
            return {"error": str(e), "status": "unhealthy"}


# Convenience function for creating client
def create_mcp_client(mcp_url: str = "http://localhost:8001/mcp") -> MCPClient:
    """Create an MCP client instance.
    
    Args:
        mcp_url: MCP server URL with /mcp endpoint
        
    Returns:
        MCP client instance
    """
    return MCPClient(mcp_url)


# Example usage following the pattern from user requirements
def create_streamable_mcp_client(mcp_url: str = "http://localhost:8001/mcp"):
    """Create an MCP client following the specified pattern.
    
    Args:
        mcp_url: MCP server URL with /mcp endpoint
        
    Returns:
        Configured MCP client
    """
    mcp_client = MCPClient(mcp_url)
    
    # Test the connection
    with mcp_client:
        # Get the tools from the MCP server
        tools = mcp_client.get_tools()
        
    return mcp_client, tools
