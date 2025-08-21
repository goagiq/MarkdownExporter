"""Generic markdown file converter using MCP tools."""

import requests
import base64
import json
from pathlib import Path
from typing import Optional, Dict, Any, Union
import logging

logger = logging.getLogger(__name__)


class MarkdownConverter:
    """Generic markdown file converter that uses MCP tools for conversion."""
    
    def __init__(self, mcp_url: str = "http://localhost:8001/mcp"):
        """Initialize the converter with MCP server URL.
        
        Args:
            mcp_url: URL of the MCP server endpoint
        """
        self.mcp_url = mcp_url
        self.request_id = 0
    
    def _get_next_id(self) -> int:
        """Get next request ID."""
        self.request_id += 1
        return self.request_id
    
    def _make_mcp_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to the MCP server.
        
        Args:
            method: MCP method name
            params: Request parameters
            
        Returns:
            Response data
            
        Raises:
            Exception: If the request fails
        """
        request_data = {
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": method,
            "params": params
        }
        
        try:
            response = requests.post(self.mcp_url, json=request_data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if "error" in result:
                raise Exception(f"MCP error: {result['error']}")
            
            return result.get("result", {})
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to connect to MCP server at {self.mcp_url}: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response from MCP server: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")
    
    def convert_file(self, 
                    input_file: Union[str, Path], 
                    output_format: str, 
                    output_file: Optional[Union[str, Path]] = None) -> Path:
        """Convert a markdown file to the specified format.
        
        Args:
            input_file: Path to the input markdown file
            output_format: Output format ('word', 'pdf', 'html')
            output_file: Optional output file path. If not provided, will be generated.
            
        Returns:
            Path to the generated output file
            
        Raises:
            Exception: If conversion fails
        """
        input_path = Path(input_file)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Read the markdown content
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            raise Exception(f"Failed to read input file {input_path}: {e}")
        
        # Determine output file path
        if output_file is None:
            output_dir = Path("results")
            output_dir.mkdir(exist_ok=True)
            
            if output_format == "word":
                extension = ".docx"
            elif output_format == "pdf":
                extension = ".pdf"
            elif output_format == "html":
                extension = ".html"
            else:
                raise ValueError(f"Unsupported output format: {output_format}")
            
            output_file = output_dir / f"{input_path.stem}{extension}"
        else:
            output_file = Path(output_file)
            output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert using MCP tools
        tool_name = f"convert_markdown_to_{output_format}"
        
        logger.info(f"Converting {input_path} to {output_format} format...")
        
        try:
            result = self._make_mcp_request("tools/call", {
                "name": tool_name,
                "arguments": {"content": content}
            })
            
            # Handle the response based on format
            if output_format in ["word", "pdf"]:
                # Binary data is base64 encoded
                content_result = result.get("content", [])
                if isinstance(content_result, list):
                    for item in content_result:
                        if item.get("type") == "data":
                            binary_data = base64.b64decode(item["data"])
                            with open(output_file, 'wb') as f:
                                f.write(binary_data)
                            logger.info(f"✅ {output_format.title()} document saved: {output_file} ({len(binary_data)} bytes)")
                            return output_file
                
                raise Exception(f"No binary data found in {output_format} conversion response")
                
            elif output_format == "html":
                # HTML content is text
                content_result = result.get("content", [])
                if isinstance(content_result, list):
                    for item in content_result:
                        if item.get("type") == "text":
                            html_content = item["text"]
                            with open(output_file, 'w', encoding='utf-8') as f:
                                f.write(html_content)
                            logger.info(f"✅ HTML document saved: {output_file} ({len(html_content)} characters)")
                            return output_file
                
                raise Exception("No text content found in HTML conversion response")
                
        except Exception as e:
            raise Exception(f"Failed to convert {input_path} to {output_format}: {e}")
    
    def convert_to_all_formats(self, 
                              input_file: Union[str, Path], 
                              output_dir: Optional[Union[str, Path]] = None) -> Dict[str, Path]:
        """Convert a markdown file to all supported formats.
        
        Args:
            input_file: Path to the input markdown file
            output_dir: Optional output directory. Defaults to 'results'
            
        Returns:
            Dictionary mapping format names to output file paths
            
        Raises:
            Exception: If any conversion fails
        """
        input_path = Path(input_file)
        if output_dir is None:
            output_dir = Path("results")
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(exist_ok=True)
        
        results = {}
        formats = ["word", "pdf", "html"]
        extensions = {"word": ".docx", "pdf": ".pdf", "html": ".html"}
        
        for format_name in formats:
            try:
                output_file = output_dir / f"{input_path.stem}{extensions[format_name]}"
                result_path = self.convert_file(input_file, format_name, output_file)
                results[format_name] = result_path
                logger.info(f"✅ Successfully converted to {format_name}: {result_path}")
            except Exception as e:
                logger.error(f"❌ Failed to convert to {format_name}: {e}")
                raise
        
        return results
    
    def list_available_tools(self) -> list:
        """List available tools from the MCP server.
        
        Returns:
            List of available tool names
        """
        try:
            result = self._make_mcp_request("tools/list", {})
            tools = result.get("tools", [])
            return [tool.get("name") for tool in tools]
        except Exception as e:
            logger.error(f"Failed to list tools: {e}")
            return []
