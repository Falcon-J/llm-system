"""
Logging utilities for the application
"""

import logging
import sys
from typing import Optional
from pathlib import Path


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: Optional[str] = None
) -> logging.Logger:
    """
    Setup logging configuration for the application
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
        log_format: Optional custom log format
        
    Returns:
        Configured logger instance
    """
    if log_format is None:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[]
    )
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_formatter = logging.Formatter(log_format)
    console_handler.setFormatter(console_formatter)
    
    # Add file handler if specified
    handlers = [console_handler]
    if log_file:
        # Create log directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_formatter = logging.Formatter(log_format)
        file_handler.setFormatter(file_formatter)
        handlers.append(file_handler)
    
    # Configure root logger with handlers
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    for handler in handlers:
        root_logger.addHandler(handler)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class LoggerMixin:
    """Mixin class to add logging capabilities to any class"""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class"""
        return logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")


def log_execution_time(func):
    """
    Decorator to log function execution time
    
    Usage:
        @log_execution_time
        def my_function():
            pass
    """
    import time
    import functools
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.4f} seconds: {e}")
            raise
    
    return wrapper


def log_async_execution_time(func):
    """
    Decorator to log async function execution time
    
    Usage:
        @log_async_execution_time
        async def my_async_function():
            pass
    """
    import time
    import functools
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        start_time = time.time()
        
        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.4f} seconds: {e}")
            raise
    
    return wrapper
