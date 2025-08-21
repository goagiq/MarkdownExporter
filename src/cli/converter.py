"""Command-line interface for markdown conversion."""

import argparse
import sys
from pathlib import Path
import logging

from ..core.markdown_converter import MarkdownConverter

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Convert markdown files to PDF, Word, and HTML formats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert README.md to all formats
  python -m src.cli.converter README.md
  
  # Convert to specific format
  python -m src.cli.converter README.md --format pdf
  
  # Specify output directory
  python -m src.cli.converter README.md --output-dir ./output
  
  # Use custom MCP server
  python -m src.cli.converter README.md --mcp-url http://localhost:8002/mcp
        """
    )
    
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the input markdown file"
    )
    
    parser.add_argument(
        "--format", "-f",
        choices=["word", "pdf", "html", "all"],
        default="all",
        help="Output format (default: all)"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default="results",
        help="Output directory (default: results)"
    )
    
    parser.add_argument(
        "--output-file",
        type=str,
        help="Specific output file path (only for single format conversion)"
    )
    
    parser.add_argument(
        "--mcp-url",
        type=str,
        default="http://localhost:8001/mcp",
        help="MCP server URL (default: http://localhost:8001/mcp)"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    parser.add_argument(
        "--list-tools",
        action="store_true",
        help="List available MCP tools and exit"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    
    # Create converter
    converter = MarkdownConverter(mcp_url=args.mcp_url)
    
    # Handle tool listing
    if args.list_tools:
        print("Available MCP tools:")
        tools = converter.list_available_tools()
        if tools:
            for tool in tools:
                print(f"  - {tool}")
        else:
            print("  No tools available or failed to connect to MCP server")
        return
    
    # Validate input file
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
    
    if not input_path.suffix.lower() in ['.md', '.markdown']:
        print(f"Warning: Input file doesn't have a markdown extension: {input_path}")
    
    try:
        if args.format == "all":
            # Convert to all formats
            print(f"Converting {input_path} to all formats...")
            results = converter.convert_to_all_formats(input_path, args.output_dir)
            
            print("\n✅ Conversion completed successfully!")
            print("Generated files:")
            for format_name, output_path in results.items():
                file_size = output_path.stat().st_size
                print(f"  - {format_name.title()}: {output_path} ({file_size:,} bytes)")
        
        else:
            # Convert to specific format
            print(f"Converting {input_path} to {args.format} format...")
            
            output_file = None
            if args.output_file:
                output_file = Path(args.output_file)
            
            result_path = converter.convert_file(input_path, args.format, output_file)
            
            file_size = result_path.stat().st_size
            print(f"\n✅ Conversion completed successfully!")
            print(f"Generated file: {result_path} ({file_size:,} bytes)")
    
    except Exception as e:
        print(f"\n❌ Conversion failed: {e}")
        logger.error(f"Conversion error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
