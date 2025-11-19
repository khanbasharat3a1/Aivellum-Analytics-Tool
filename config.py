"""
Configuration settings for Aivellum Analytics Platform
"""
import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'aivellum-v2.3-optimized')
    JSON_SORT_KEYS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # File settings
    DATA_FILE = 'Aivellum_Sales.xlsx'
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    # Logging
    LOG_DIR = 'logs'
    LOG_FILE = 'aivellum.log'
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # Cache settings
    CACHE_TIMEOUT = 3600  # 1 hour
    
    # API settings
    DEFAULT_PAGE_SIZE = 100
    MAX_PAGE_SIZE = 1000
    
    # CORS origins
    CORS_ORIGINS = [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'http://localhost:5000',
        'http://127.0.0.1:5000'
    ]

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'INFO'
    
    # Override with environment variables in production
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-this-in-production'

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}