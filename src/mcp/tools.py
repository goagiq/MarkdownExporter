"""MCP Tool Manager for dynamic tool management."""

from typing import Dict, List, Any, Callable, Optional
from pathlib import Path

from ..core.processor import MarkdownProcessor
from ..core.converters import WordConverter, PDFConverter, HTMLConverter


class MCPToolManager:
    """Dynamic MCP Tool Management System."""
    
    def __init__(self, output_dir: Path = Path("results")):
        """Initialize MCP tool manager.
        
        Args:
            output_dir: Output directory for converted files
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.processor = MarkdownProcessor(remove_unicode=True, remove_emoji=True)
        self._setup_default_tools()
    
    def _setup_default_tools(self):
        """Setup default MCP tools."""
        self.register_tool(
            "convert_markdown_to_word",
            self._convert_markdown_to_word,
            "Convert markdown content to Word document",
            {"content": "str", "output_filename": "str"}
        )
        
        self.register_tool(
            "convert_markdown_to_pdf",
            self._convert_markdown_to_pdf,
            "Convert markdown content to PDF document",
            {"content": "str", "output_filename": "str"}
        )
        
        self.register_tool(
            "convert_markdown_to_html",
            self._convert_markdown_to_html,
            "Convert markdown content to HTML document",
            {"content": "str", "output_filename": "str"}
        )
        
        self.register_tool(
            "process_markdown_file",
            self._process_markdown_file,
            "Process a markdown file and return cleaned content",
            {"file_path": "str"}
        )
        
        self.register_tool(
            "list_available_tools",
            self._list_available_tools,
            "List all available MCP tools",
            {}
        )
    
    def register_tool(
        self,
        name: str,
        func: Callable,
        description: str,
        parameters: Dict[str, str]
    ):
        """Register a new MCP tool.
        
        Args:
            name: Tool name
            func: Tool function
            description: Tool description
            parameters: Tool parameters schema
        """
        self.tools[name] = {
            "function": func,
            "description": description,
            "parameters": parameters,
            "enabled": True
        }
    
    def unregister_tool(self, name: str):
        """Unregister an MCP tool.
        
        Args:
            name: Tool name
        """
        if name in self.tools:
            del self.tools[name]
    
    def enable_tool(self, name: str):
        """Enable an MCP tool.
        
        Args:
            name: Tool name
        """
        if name in self.tools:
            self.tools[name]["enabled"] = True
    
    def disable_tool(self, name: str):
        """Disable an MCP tool.
        
        Args:
            name: Tool name
        """
        if name in self.tools:
            self.tools[name]["enabled"] = False
    
    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        """Get tool information.
        
        Args:
            name: Tool name
            
        Returns:
            Tool information or None if not found
        """
        return self.tools.get(name)
    
    def get_enabled_tools(self) -> List[str]:
        """Get list of enabled tools.
        
        Returns:
            List of enabled tool names
        """
        return [name for name, tool in self.tools.items() if tool["enabled"]]
    
    def execute_tool(self, name: str, **kwargs) -> Any:
        """Execute an MCP tool.
        
        Args:
            name: Tool name
            **kwargs: Tool parameters
            
        Returns:
            Tool execution result
        """
        tool = self.tools.get(name)
        if not tool:
            raise ValueError(f"Tool {name} not found")
        
        if not tool["enabled"]:
            raise ValueError(f"Tool {name} is disabled")
        
        return tool["function"](**kwargs)
    
    # Tool implementations
    def _convert_markdown_to_word(self, content: str, output_filename: str) -> Dict[str, Any]:
        """Convert markdown content to Word document.
        
        Args:
            content: Markdown content
            output_filename: Output filename
            
        Returns:
            Conversion result
        """
        try:
            # Process content
            processed_content = self.processor.process_content(content)
            
            # Convert to Word
            converter = WordConverter(self.output_dir)
            output_path = self.output_dir / output_filename
            
            success = converter.convert(processed_content, output_path)
            
            if success:
                return {
                    "success": True,
                    "output_file": str(output_path),
                    "file_size": output_path.stat().st_size
                }
            else:
                return {"success": False, "error": "Conversion failed"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _convert_markdown_to_pdf(self, content: str, output_filename: str) -> Dict[str, Any]:
        """Convert markdown content to PDF document.
        
        Args:
            content: Markdown content
            output_filename: Output filename
            
        Returns:
            Conversion result
        """
        try:
            # Process content
            processed_content = self.processor.process_content(content)
            
            # Convert to PDF
            converter = PDFConverter(self.output_dir)
            output_path = self.output_dir / output_filename
            
            success = converter.convert(processed_content, output_path)
            
            if success:
                return {
                    "success": True,
                    "output_file": str(output_path),
                    "file_size": output_path.stat().st_size
                }
            else:
                return {"success": False, "error": "Conversion failed"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _convert_markdown_to_html(self, content: str, output_filename: str) -> Dict[str, Any]:
        """Convert markdown content to HTML document.
        
        Args:
            content: Markdown content
            output_filename: Output filename
            
        Returns:
            Conversion result
        """
        try:
            # Process content
            processed_content = self.processor.process_content(content)
            
            # Convert to HTML
            converter = HTMLConverter(self.output_dir)
            output_path = self.output_dir / output_filename
            
            success = converter.convert(processed_content, output_path)
            
            if success:
                return {
                    "success": True,
                    "output_file": str(output_path),
                    "file_size": output_path.stat().st_size
                }
            else:
                return {"success": False, "error": "Conversion failed"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _process_markdown_file(self, file_path: str) -> Dict[str, Any]:
        """Process a markdown file and return cleaned content.
        
        Args:
            file_path: Path to markdown file
            
        Returns:
            Processing result
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return {"success": False, "error": f"File not found: {file_path}"}
            
            # Process file
            processed_content = self.processor.process_file(path)
            
            return {
                "success": True,
                "content": processed_content,
                "content_length": len(processed_content)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _list_available_tools(self) -> Dict[str, Any]:
        """List all available MCP tools.
        
        Returns:
            Tool information
        """
        tools_info = {}
        for name, tool in self.tools.items():
            tools_info[name] = {
                "description": tool["description"],
                "parameters": tool["parameters"],
                "enabled": tool["enabled"]
            }
        
        return {
            "success": True,
            "tools": tools_info,
            "enabled_count": len(self.get_enabled_tools()),
            "total_count": len(self.tools)
        }
