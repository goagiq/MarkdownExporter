#!/usr/bin/env python3
"""
Simple MCP server implementation that properly handles the MCP protocol.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import json
import logging
import re
import os
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, Any, List

# Setup logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import conversion libraries from the integrated codebase
try:
    from src.core.converters import WordConverter, PDFConverter, HTMLConverter, CONVERSION_AVAILABLE
    CONVERSION_AVAILABLE = True
    logger.info("✅ Conversion libraries imported successfully")
except ImportError as e:
    logger.error(f"❌ Conversion libraries not available: {e}")
    CONVERSION_AVAILABLE = False

# Initialize FastAPI app
app = FastAPI(title="Simple MCP Server", version="1.0.0")

# Initialize converters
word_converter = WordConverter(Path("results"))
pdf_converter = PDFConverter(Path("results"))
html_converter = HTMLConverter(Path("results"))

def read_file_content(file_path: str) -> str:
    """Read content from a file path, handling various path formats."""
    try:
        # Handle Windows paths with backslashes
        normalized_path = file_path.replace('\\', '/')
        
        # Handle absolute Windows paths (D:/path/to/file)
        if ':/' in normalized_path:
            # Convert to proper Windows path
            import os
            normalized_path = os.path.normpath(file_path)
        
        with open(normalized_path, 'r', encoding='utf-8') as f:
            content = f.read()
            logger.info(f"✅ Successfully read {len(content)} characters from {file_path}")
            return content
    except Exception as e:
        logger.error(f"❌ Error reading file {file_path}: {e}")
        raise Exception(f"Failed to read file {file_path}: {str(e)}")

def get_content_from_arguments(arguments: dict) -> str:
    """Extract content from arguments, either directly or from file path."""
    content = arguments.get("content", "")
    file_path = arguments.get("file_path", "")
    
    if file_path:
        # If file_path is provided, read the file content
        content = read_file_content(file_path)
    elif not content:
        # If neither content nor file_path is provided, raise error
        raise Exception("Either 'content' or 'file_path' must be provided")
    
    return content

# Store available tools
AVAILABLE_TOOLS = [
    {
        "name": "get_summary",
        "description": "Get a summary of a webpage",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to summarize"},
                "num_sentences": {"type": "integer", "description": "Number of sentences"}
            },
            "required": ["url"]
        }
    },
    {
        "name": "convert_markdown_to_word",
        "description": "Convert markdown content to Word document. Can accept either markdown content directly or a file path to read markdown from. If file_path is provided, it will automatically read the file content.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "Markdown content (optional if file_path is provided)"},
                "file_path": {"type": "string", "description": "Path to markdown file to read (optional if content is provided)"}
            }
        }
    },
    {
        "name": "convert_markdown_to_pdf",
        "description": "Convert markdown content to PDF. Can accept either markdown content directly or a file path to read markdown from. If file_path is provided, it will automatically read the file content.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "Markdown content (optional if file_path is provided)"},
                "file_path": {"type": "string", "description": "Path to markdown file to read (optional if content is provided)"}
            }
        }
    },
    {
        "name": "convert_markdown_to_html",
        "description": "Convert markdown content to HTML. Can accept either markdown content directly or a file path to read markdown from. If file_path is provided, it will automatically read the file content.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "Markdown content (optional if file_path is provided)"},
                "file_path": {"type": "string", "description": "Path to markdown file to read (optional if content is provided)"}
            }
        }
    }
]

@app.post("/mcp")
async def handle_mcp_request(request: Request):
    """Handle MCP protocol requests."""
    try:
        body = await request.json()
        logger.info(f"Received MCP request: {body}")
        
        method = body.get("method")
        request_id = body.get("id")
        
        if method == "initialize":
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "markdown-exporter-mcp",
                        "version": "1.0.0"
                    }
                }
            })
        
        elif method == "tools/list":
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": AVAILABLE_TOOLS
                }
            })
        
        elif method == "tools/call":
            params = body.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            # Handle tool calls
            if tool_name == "get_summary":
                url = arguments.get("url", "unknown")
                num_sentences = arguments.get("num_sentences", 3)
                result = {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Summary of {url} with {num_sentences} sentences"
                        }
                    ]
                }
            
            elif tool_name == "convert_markdown_to_word":
                try:
                    content = get_content_from_arguments(arguments)
                    # Use the integrated Word converter
                    import uuid
                    temp_file = Path(f"temp_word_{uuid.uuid4().hex[:8]}.docx")
                    
                    if word_converter.convert(content, temp_file):
                        # Read the generated file
                        with open(temp_file, "rb") as f:
                            word_bytes = f.read()
                        
                        # Save to results directory
                        results_dir = Path("results")
                        results_dir.mkdir(exist_ok=True)
                        results_file = results_dir / "README.docx"
                        
                        with open(results_file, "wb") as f:
                            f.write(word_bytes)
                        
                        # Clean up temp file
                        if temp_file.exists():
                            temp_file.unlink()
                        
                        import base64
                        word_b64 = base64.b64encode(word_bytes).decode('utf-8')
                        logger.info(f"✅ Word conversion successful: {results_file} ({len(word_bytes)} bytes)")
                        result = {
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Successfully converted markdown to Word and saved to {results_file} ({len(word_bytes)} bytes)"
                                },
                                {
                                    "type": "data",
                                    "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                    "data": word_b64
                                }
                            ]
                        }
                    else:
                        result = {
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Error: Word conversion failed"
                                }
                            ]
                        }
                except Exception as e:
                    logger.error(f"Error converting to Word: {e}")
                    result = {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Error converting markdown to Word: {str(e)}"
                            }
                        ]
                    }
            
            elif tool_name == "convert_markdown_to_pdf":
                try:
                    content = get_content_from_arguments(arguments)
                    # Use the integrated PDF converter
                    import uuid
                    temp_file = Path(f"temp_pdf_{uuid.uuid4().hex[:8]}.pdf")
                    
                    if pdf_converter.convert(content, temp_file):
                        # Read the generated file
                        with open(temp_file, "rb") as f:
                            pdf_bytes = f.read()
                        
                        # Save to results directory
                        results_dir = Path("results")
                        results_dir.mkdir(exist_ok=True)
                        results_file = results_dir / "README.pdf"
                        
                        with open(results_file, "wb") as f:
                            f.write(pdf_bytes)
                        
                        # Clean up temp file
                        if temp_file.exists():
                            temp_file.unlink()
                        
                        import base64
                        pdf_b64 = base64.b64encode(pdf_bytes).decode('utf-8')
                        logger.info(f"✅ PDF conversion successful: {results_file} ({len(pdf_bytes)} bytes)")
                        result = {
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Successfully converted markdown to PDF and saved to {results_file} ({len(pdf_bytes)} bytes)"
                                },
                                {
                                    "type": "data",
                                    "mimeType": "application/pdf",
                                    "data": pdf_b64
                                }
                            ]
                        }
                    else:
                        result = {
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Error: PDF conversion failed"
                                }
                            ]
                        }
                except Exception as e:
                    logger.error(f"Error converting to PDF: {e}")
                    result = {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Error converting markdown to PDF: {str(e)}"
                            }
                        ]
                    }
            
            elif tool_name == "convert_markdown_to_html":
                try:
                    content = get_content_from_arguments(arguments)
                    # Use the integrated HTML converter
                    import uuid
                    temp_file = Path(f"temp_html_{uuid.uuid4().hex[:8]}.html")
                    
                    if html_converter.convert(content, temp_file):
                        # Read the generated file
                        with open(temp_file, "r", encoding='utf-8') as f:
                            html_content = f.read()
                        
                        # Save to results directory
                        results_dir = Path("results")
                        results_dir.mkdir(exist_ok=True)
                        results_file = results_dir / "README.html"
                        
                        with open(results_file, "w", encoding='utf-8') as f:
                            f.write(html_content)
                        
                        # Clean up temp file
                        if temp_file.exists():
                            temp_file.unlink()
                        
                        logger.info(f"✅ HTML conversion successful: {results_file} ({len(html_content)} characters)")
                        result = {
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Successfully converted markdown to HTML and saved to {results_file} ({len(html_content)} characters)"
                                },
                                {
                                    "type": "text", 
                                    "text": html_content[:500] + "..." if len(html_content) > 500 else html_content
                                }
                            ]
                        }
                    else:
                        result = {
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Error: HTML conversion failed"
                                }
                            ]
                        }
                except Exception as e:
                    logger.error(f"Error converting to HTML: {e}")
                    result = {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Error converting markdown to HTML: {str(e)}"
                            }
                        ]
                    }
            
            else:
                return JSONResponse({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method '{tool_name}' not found"
                    }
                })
            
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            })
        
        else:
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method '{method}' not found"
                }
            })
    
    except Exception as e:
        logger.error(f"Error handling MCP request: {e}")
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": body.get("id") if 'body' in locals() else None,
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        })

@app.get("/mcp")
async def mcp_get():
    """MCP endpoint for GET requests."""
    return {"message": "MCP server is running", "tools": [tool["name"] for tool in AVAILABLE_TOOLS]}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Simple MCP Server"}

def main():
    """Main function to run the MCP server."""
    port = 8001
    logger.info(f"Starting Simple MCP server on port {port}")
    logger.info(f"API docs available at: http://127.0.0.1:{port}/docs")
    logger.info(f"MCP endpoint available at: http://127.0.0.1:{port}/mcp")
    
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
