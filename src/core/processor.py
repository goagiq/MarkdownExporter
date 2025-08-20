"""Markdown processing core with unicode and emoji removal."""

import re
from pathlib import Path
from typing import List, Optional

import emoji
import markdown
from unidecode import unidecode


class MarkdownProcessor:
    """Core markdown processor with text cleaning capabilities."""
    
    def __init__(self, remove_unicode: bool = True, remove_emoji: bool = True):
        """Initialize the markdown processor.
        
        Args:
            remove_unicode: Whether to remove unicode characters
            remove_emoji: Whether to remove emoji characters
        """
        self.remove_unicode = remove_unicode
        self.remove_emoji = remove_emoji
        self.md = markdown.Markdown(extensions=['tables', 'fenced_code', 'codehilite'])
    
    def clean_text(self, text: str) -> str:
        """Clean text by removing unicode and emoji characters.
        
        Args:
            text: Input text to clean
            
        Returns:
            Cleaned text
        """
        if self.remove_emoji:
            text = emoji.replace_emoji(text, replace='')
        
        if self.remove_unicode:
            text = unidecode(text)
        
        # Remove any remaining non-ASCII characters
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        
        return text.strip()
    
    def process_file(self, file_path: Path) -> str:
        """Process a markdown file and return cleaned content.
        
        Args:
            file_path: Path to the markdown file
            
        Returns:
            Processed markdown content
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return self.process_content(content)
    
    def process_content(self, content: str) -> str:
        """Process markdown content and return cleaned version.
        
        Args:
            content: Raw markdown content
            
        Returns:
            Processed markdown content
        """
        # Clean the content
        cleaned_content = self.clean_text(content)
        
        # Process markdown extensions
        cleaned_content = self._process_mermaid_diagrams(cleaned_content)
        cleaned_content = self._process_tables(cleaned_content)
        cleaned_content = self._process_images(cleaned_content)
        
        return cleaned_content
    
    def _process_mermaid_diagrams(self, content: str) -> str:
        """Process Mermaid diagrams in the content.
        
        Args:
            content: Markdown content
            
        Returns:
            Content with processed Mermaid diagrams
        """
        # Find Mermaid code blocks
        mermaid_pattern = r'```mermaid\s*\n(.*?)\n```'
        
        def replace_mermaid(match):
            diagram_code = match.group(1)
            # Clean the diagram code
            cleaned_diagram = self.clean_text(diagram_code)
            return f'```mermaid\n{cleaned_diagram}\n```'
        
        return re.sub(mermaid_pattern, replace_mermaid, content, flags=re.DOTALL)
    
    def _process_tables(self, content: str) -> str:
        """Process tables to ensure proper formatting.
        
        Args:
            content: Markdown content
            
        Returns:
            Content with processed tables
        """
        # Ensure table alignment is left-aligned
        table_pattern = r'(\|[^|]*\|[^|]*\|[^|]*\|)'
        
        def process_table_row(match):
            row = match.group(1)
            # Remove any alignment markers and ensure left alignment
            row = re.sub(r':-+:', '---', row)
            row = re.sub(r':-+', '---', row)
            return row
        
        return re.sub(table_pattern, process_table_row, content)
    
    def _process_images(self, content: str) -> str:
        """Process image references in the content.
        
        Args:
            content: Markdown content
            
        Returns:
            Content with processed images
        """
        # Clean image alt text
        image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        
        def clean_image(match):
            alt_text = match.group(1)
            url = match.group(2)
            
            # Clean alt text
            cleaned_alt = self.clean_text(alt_text)
            
            return f'![{cleaned_alt}]({url})'
        
        return re.sub(image_pattern, clean_image, content)
    
    def extract_metadata(self, content: str) -> dict:
        """Extract metadata from markdown content.
        
        Args:
            content: Markdown content
            
        Returns:
            Dictionary of metadata
        """
        metadata = {}
        
        # Extract front matter if present
        front_matter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
        front_matter_match = re.search(front_matter_pattern, content, re.DOTALL)
        
        if front_matter_match:
            front_matter = front_matter_match.group(1)
            for line in front_matter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
        
        # Extract title from first heading
        title_pattern = r'^#\s+(.+)$'
        title_match = re.search(title_pattern, content, re.MULTILINE)
        if title_match:
            metadata['title'] = self.clean_text(title_match.group(1))
        
        return metadata
    
    def validate_content(self, content: str) -> List[str]:
        """Validate markdown content and return warnings.
        
        Args:
            content: Markdown content to validate
            
        Returns:
            List of warning messages
        """
        warnings = []
        
        # Check for unclosed code blocks
        code_block_count = content.count('```')
        if code_block_count % 2 != 0:
            warnings.append("Unclosed code block detected")
        
        # Check for unclosed links
        open_brackets = content.count('[') - content.count(']')
        if open_brackets != 0:
            warnings.append("Unclosed markdown links detected")
        
        # Check for table formatting issues
        lines = content.split('\n')
        in_table = False
        for i, line in enumerate(lines):
            if '|' in line and line.strip().startswith('|'):
                if not in_table:
                    in_table = True
            elif in_table and line.strip() == '':
                in_table = False
            elif in_table and '|' not in line:
                warnings.append(f"Table formatting issue at line {i+1}")
        
        return warnings
