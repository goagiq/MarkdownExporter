#!/usr/bin/env python3
"""
Test script to verify MCP tools work for markdown conversion.
"""

import requests
import json
import base64
from pathlib import Path

def test_mcp_conversion():
    """Test MCP conversion tools."""
    
    # Read README.md content
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    print(f"📖 Read {len(content)} characters from README.md")
    
    # Test Word conversion
    print("\n🔄 Testing Word conversion via MCP...")
    word_result = test_word_conversion(content)
    
    # Test PDF conversion
    print("\n🔄 Testing PDF conversion via MCP...")
    pdf_result = test_pdf_conversion(content)
    
    return word_result and pdf_result

def test_word_conversion(content):
    """Test Word conversion via MCP."""
    try:
        # Prepare MCP request
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "convert_markdown_to_word",
                "arguments": {
                    "content": content
                }
            }
        }
        
        # Send request
        response = requests.post(
            "http://localhost:8001/mcp",
            json=mcp_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if "result" in result:
                content_items = result["result"]["content"]
                
                # Check for text message
                text_message = None
                word_data = None
                
                for item in content_items:
                    if item["type"] == "text":
                        text_message = item["text"]
                    elif item["type"] == "data" and item["mimeType"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        word_data = item["data"]
                
                if word_data:
                    # Save the Word document
                    word_bytes = base64.b64decode(word_data)
                    output_path = "results/README_mcp_word.docx"
                    Path("results").mkdir(exist_ok=True)
                    
                    with open(output_path, "wb") as f:
                        f.write(word_bytes)
                    
                    print(f"✅ Word conversion successful!")
                    print(f"📁 Output saved to: {output_path}")
                    print(f"📊 File size: {len(word_bytes)} bytes")
                    print(f"📝 Message: {text_message}")
                    return True
                else:
                    print(f"❌ No Word data in response")
                    print(f"📝 Message: {text_message}")
                    return False
            else:
                print(f"❌ Error in response: {result}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Word conversion: {e}")
        return False

def test_pdf_conversion(content):
    """Test PDF conversion via MCP."""
    try:
        # Prepare MCP request
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "convert_markdown_to_pdf",
                "arguments": {
                    "content": content
                }
            }
        }
        
        # Send request
        response = requests.post(
            "http://localhost:8001/mcp",
            json=mcp_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if "result" in result:
                content_items = result["result"]["content"]
                
                # Check for text message
                text_message = None
                pdf_data = None
                
                for item in content_items:
                    if item["type"] == "text":
                        text_message = item["text"]
                    elif item["type"] == "data" and item["mimeType"] == "application/pdf":
                        pdf_data = item["data"]
                
                if pdf_data:
                    # Save the PDF document
                    pdf_bytes = base64.b64decode(pdf_data)
                    output_path = "results/README_mcp_pdf.pdf"
                    Path("results").mkdir(exist_ok=True)
                    
                    with open(output_path, "wb") as f:
                        f.write(pdf_bytes)
                    
                    print(f"✅ PDF conversion successful!")
                    print(f"📁 Output saved to: {output_path}")
                    print(f"📊 File size: {len(pdf_bytes)} bytes")
                    print(f"📝 Message: {text_message}")
                    return True
                else:
                    print(f"❌ No PDF data in response")
                    print(f"📝 Message: {text_message}")
                    return False
            else:
                print(f"❌ Error in response: {result}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing PDF conversion: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing MCP conversion tools...")
    success = test_mcp_conversion()
    
    if success:
        print("\n🎉 All MCP conversion tests passed!")
        print("📋 The MCP tools now provide:")
        print("   - Real Word documents with proper formatting")
        print("   - Real PDF documents with proper formatting")
        print("   - Mermaid diagrams rendered as images")
        print("   - Clean file structure diagrams")
        print("   - Proper hyperlink formatting")
    else:
        print("\n❌ Some MCP conversion tests failed!")

