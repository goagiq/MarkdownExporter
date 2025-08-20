"""Header and Footer Configuration Management."""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class HeaderFooterConfig:
    """Configuration manager for document headers and footers."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_path: Path to configuration file. If None, uses default location.
        """
        if config_path is None:
            config_path = "config/header_footer.yaml"
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file.
        
        Returns:
            Configuration dictionary
        """
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                logger.info(f"✅ Loaded header/footer config from {self.config_path}")
                return config
            else:
                logger.warning(f"⚠️ Config file not found: {self.config_path}")
                return self._get_default_config()
        except Exception as e:
            logger.error(f"❌ Error loading config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration.
        
        Returns:
            Default configuration dictionary
        """
        return {
            "header": {
                "text": "GoAGI",
                "font_size": 10,
                "font_name": "Arial",
                "alignment": "center",
                "color": "#333333",
                "bold": False,
                "italic": False
            },
            "footer": {
                "text": "Copyright (c) 2025 GoAGI All rights reserved.",
                "font_size": 9,
                "font_name": "Arial",
                "alignment": "center",
                "color": "#666666",
                "bold": False,
                "italic": False
            },
            "page": {
                "margin_top": 1.0,
                "margin_bottom": 1.0,
                "margin_left": 1.0,
                "margin_right": 1.0,
                "header_distance": 0.5,
                "footer_distance": 0.5
            }
        }
    
    def get_header_config(self) -> Dict[str, Any]:
        """Get header configuration.
        
        Returns:
            Header configuration dictionary
        """
        return self.config.get("header", {})
    
    def get_footer_config(self) -> Dict[str, Any]:
        """Get footer configuration.
        
        Returns:
            Footer configuration dictionary
        """
        return self.config.get("footer", {})
    
    def get_page_config(self) -> Dict[str, Any]:
        """Get page configuration.
        
        Returns:
            Page configuration dictionary
        """
        return self.config.get("page", {})
    
    def get_header_text(self) -> str:
        """Get header text.
        
        Returns:
            Header text string
        """
        return self.get_header_config().get("text", "GoAGI")
    
    def get_footer_text(self) -> str:
        """Get footer text.
        
        Returns:
            Footer text string
        """
        return self.get_footer_config().get("text", "Copyright (c) 2025 GoAGI All rights reserved.")
    
    def reload_config(self) -> None:
        """Reload configuration from file."""
        self.config = self._load_config()
        logger.info("🔄 Header/footer configuration reloaded")
