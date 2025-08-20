#!/usr/bin/env python3
"""
Simple FastAPI server with file path support for markdown conversion.
"""

import sys
from pathlib import Path
from typing import Dict, Any

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fastapi import FastAPI, HTTPException
import uvicorn
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import converters
try:
    from src.core.converters import WordConverter, PDFConverter, CONVERSION_AVAILABLE
    logger.info("✅ Conversion libraries imported successfully")
except ImportError as e:
    logger.error(f"❌ Conversion libraries not available: {e}")
    CONVERSION_AVAILABLE = False

# Initialize FastAPI app
app = FastAPI(title="Simple Markdown Exporter API", version="1.0.0")

# Initialize converters
word_converter = WordConverter(Path("results"))
pdf_converter = PDFConverter(Path("results"))

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

# FastAPI endpoints
@app.get("/convert/", operation_id="convert_markdown_to_word")
async def convert_markdown_to_word_endpoint(content: str = None, file_path: str = None) -> Dict[str, Any]:
    """Convert markdown content to Word document. Can accept either content directly or a file path."""
    try:
        if not CONVERSION_AVAILABLE:
            raise HTTPException(status_code=500, detail="Conversion libraries not available")
        
        # Get content from either parameter
        if file_path:
            content = read_file_content(file_path)
        elif not content:
            raise HTTPException(status_code=400, detail="Either 'content' or 'file_path' must be provided")
        
        # Convert to Word
        import uuid
        temp_file = Path(f"temp_word_{uuid.uuid4().hex[:8]}.docx")
        
        if word_converter.convert(content, temp_file):
            # Read the generated file
            with open(temp_file, "rb") as f:
                word_bytes = f.read()
            
            # Clean up temp file
            temp_file.unlink()
            
            import base64
            word_b64 = base64.b64encode(word_bytes).decode('utf-8')
            
            return {
                "success": True,
                "message": f"Markdown converted to Word successfully ({len(word_bytes)} bytes)",
                "data": word_b64,
                "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "source": "file" if file_path else "content"
            }
        else:
            raise HTTPException(status_code=500, detail="Word conversion failed")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error converting to Word: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/convert-pdf/", operation_id="convert_markdown_to_pdf")
async def convert_markdown_to_pdf_endpoint(content: str = None, file_path: str = None) -> Dict[str, Any]:
    """Convert markdown content to PDF. Can accept either content directly or a file path."""
    try:
        if not CONVERSION_AVAILABLE:
            raise HTTPException(status_code=500, detail="Conversion libraries not available")
        
        # Get content from either parameter
        if file_path:
            content = read_file_content(file_path)
        elif not content:
            raise HTTPException(status_code=400, detail="Either 'content' or 'file_path' must be provided")
        
        # Convert to PDF
        import uuid
        temp_file = Path(f"temp_pdf_{uuid.uuid4().hex[:8]}.pdf")
        
        if pdf_converter.convert(content, temp_file):
            # Read the generated file
            with open(temp_file, "rb") as f:
                pdf_bytes = f.read()
            
            # Clean up temp file
            temp_file.unlink()
            
            import base64
            pdf_b64 = base64.b64encode(pdf_bytes).decode('utf-8')
            
            return {
                "success": True,
                "message": f"Markdown converted to PDF successfully ({len(pdf_bytes)} bytes)",
                "data": pdf_b64,
                "mime_type": "application/pdf",
                "source": "file" if file_path else "content"
            }
        else:
            raise HTTPException(status_code=500, detail="PDF conversion failed")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error converting to PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health/")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "healthy", 
        "service": "Simple Markdown Exporter API",
        "conversion_available": str(CONVERSION_AVAILABLE)
    }

@app.get("/tools/")
async def list_available_tools() -> Dict[str, Any]:
    """List available tools."""
    return {
        "tools": [
            "convert_markdown_to_word",
            "convert_markdown_to_pdf"
        ],
        "endpoints": [
            "GET /convert/ - Convert to Word (supports content or file_path)",
            "GET /convert-pdf/ - Convert to PDF (supports content or file_path)",
            "GET /health/ - Health check",
            "GET /tools/ - List available tools"
        ]
    }

def main():
    """Main function to run the API server."""
    port = 8001
    logger.info(f"Starting Simple API server on port {port}")
    logger.info(f"API docs available at: http://127.0.0.1:{port}/docs")
    logger.info(f"Health check: http://127.0.0.1:{port}/health/")
    logger.info(f"Tools list: http://127.0.0.1:{port}/tools/")
    
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
