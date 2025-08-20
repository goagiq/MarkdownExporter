"""Structured logging configuration for Markdown Exporter."""

from typing import Any, Dict

import structlog


def setup_logging(
    level: str = "INFO",
    format_type: str = "json",
    output: str = "stdout"
) -> None:
    """Setup structured logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_type: Log format (json, text)
        output: Log output destination (stdout, stderr, file)
    """
    # Configure standard library logging
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    
    if format_type == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(
            structlog.dev.ConsoleRenderer(colors=True)
        )
    
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure output - structlog automatically outputs to stdout
    # For file output, we'll handle it in the logger factory


def get_logger(name: str = "markdownexporter") -> structlog.BoundLogger:
    """Get a structured logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Configured structured logger
    """
    return structlog.get_logger(name)


def log_function_call(func_name: str, **kwargs: Any) -> Dict[str, Any]:
    """Create a log entry for function calls.
    
    Args:
        func_name: Name of the function being called
        **kwargs: Function parameters
        
    Returns:
        Log entry dictionary
    """
    return {
        "function": func_name,
        "parameters": kwargs,
        "event": "function_call"
    }


def log_conversion_event(
    input_file: str,
    output_format: str,
    success: bool,
    error_message: str | None = None
) -> Dict[str, Any]:
    """Create a log entry for conversion events.
    
    Args:
        input_file: Input file path
        output_format: Output format (word, pdf, html)
        success: Whether conversion was successful
        error_message: Error message if conversion failed
        
    Returns:
        Log entry dictionary
    """
    log_entry = {
        "input_file": input_file,
        "output_format": output_format,
        "success": success,
        "event": "conversion"
    }
    
    if not success and error_message:
        log_entry["error"] = error_message
        
    return log_entry
