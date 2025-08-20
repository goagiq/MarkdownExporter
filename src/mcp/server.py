"""MCP Server implementation with streamable HTTP protocol."""

import asyncio
import json
from typing import Dict, List, Any, Optional
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware


class MCPServer:
    """MCP Server with streamable HTTP protocol support."""
    
    def __init__(self, port: int = 8500):
        """Initialize MCP server.
        
        Args:
            port: Server port number
        """
        self.port = port
        self.app = FastAPI(title="MCP Server", version="1.0.0")
        self.tools: Dict[str, Any] = {}
        self._setup_routes()
        self._setup_middleware()
    
    def _setup_middleware(self):
        """Setup CORS middleware."""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def _setup_routes(self):
        """Setup API routes."""
        
        @self.app.get("/")
        async def root():
            """Root endpoint."""
            return {"message": "MCP Server is running", "port": self.port}
        
        @self.app.get("/health")
        async def health():
            """Health check endpoint."""
            return {"status": "healthy", "tools_count": len(self.tools)}
        
        @self.app.post("/mcp")
        async def mcp_endpoint(request: Request):
            """MCP streamable HTTP endpoint."""
            return StreamingResponse(
                self._handle_mcp_request(request),
                media_type="text/event-stream",
                headers={
                    "Accept": "application/json, text/event-stream",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                }
            )
        
        @self.app.get("/tools")
        async def list_tools():
            """List available MCP tools."""
            return {"tools": list(self.tools.keys())}
        
        @self.app.post("/tools/{tool_name}")
        async def call_tool(tool_name: str, request: Request):
            """Call a specific MCP tool."""
            if tool_name not in self.tools:
                return {"error": f"Tool {tool_name} not found"}
            
            try:
                body = await request.json()
                result = await self._execute_tool(tool_name, body)
                return {"result": result}
            except Exception as e:
                return {"error": str(e)}
    
    async def _handle_mcp_request(self, request: Request):
        """Handle MCP streamable HTTP request."""
        try:
            body = await request.json()
            method = body.get("method")
            params = body.get("params", {})
            
            if method == "tools/list":
                yield f"data: {json.dumps({'tools': list(self.tools.keys())})}\n\n"
            
            elif method == "tools/call":
                tool_name = params.get("name")
                tool_params = params.get("arguments", {})
                
                if tool_name in self.tools:
                    result = await self._execute_tool(tool_name, tool_params)
                    yield f"data: {json.dumps({'result': result})}\n\n"
                else:
                    yield f"data: {json.dumps({'error': f'Tool {tool_name} not found'})}\n\n"
            
            else:
                yield f"data: {json.dumps({'error': f'Unknown method: {method}'})}\n\n"
                
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    async def _execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """Execute an MCP tool.
        
        Args:
            tool_name: Name of the tool to execute
            params: Tool parameters
            
        Returns:
            Tool execution result
        """
        tool = self.tools.get(tool_name)
        if not tool:
            raise ValueError(f"Tool {tool_name} not found")
        
        if asyncio.iscoroutinefunction(tool):
            return await tool(**params)
        else:
            return tool(**params)
    
    def register_tool(self, name: str, func: callable):
        """Register an MCP tool.
        
        Args:
            name: Tool name
            func: Tool function
        """
        self.tools[name] = func
    
    def unregister_tool(self, name: str):
        """Unregister an MCP tool.
        
        Args:
            name: Tool name
        """
        if name in self.tools:
            del self.tools[name]
    
    def start(self, host: str = "0.0.0.0"):
        """Start the MCP server.
        
        Args:
            host: Server host address
        """
        uvicorn.run(
            self.app,
            host=host,
            port=self.port,
            log_level="info"
        )
    
    async def start_async(self, host: str = "0.0.0.0"):
        """Start the MCP server asynchronously.
        
        Args:
            host: Server host address
        """
        config = uvicorn.Config(
            self.app,
            host=host,
            port=self.port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()
