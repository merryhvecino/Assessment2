#!/usr/bin/env python3
"""
Configuration settings for Kaiwhakarite Rawa
Centralized configuration management with environment variable support
"""

from typing import List
from pathlib import Path
from decouple import config


class DatabaseConfig:
    """Database configuration section"""
    # Database URL - supports SQLite and MySQL
    # SQLite: 'sqlite:///../database/kaiwhakarite.db'
    # MySQL: 'mysql+pymysql://username:password@localhost:3306/kaiwhakarite'
    URL: str = config(
        'DATABASE_URL', 
        default='sqlite:///../database/kaiwhakarite.db'
    )
    
    # Connection Pool Settings (for MySQL)
    POOL_SIZE: int = config('DB_POOL_SIZE', default=10, cast=int)
    MAX_OVERFLOW: int = config('DB_MAX_OVERFLOW', default=20, cast=int)
    POOL_TIMEOUT: int = config('DB_POOL_TIMEOUT', default=30, cast=int)
    POOL_RECYCLE: int = config('DB_POOL_RECYCLE', default=3600, cast=int)
    
    # MySQL specific settings
    MYSQL_HOST: str = config('MYSQL_HOST', default='localhost')
    MYSQL_PORT: int = config('MYSQL_PORT', default=3306, cast=int)
    MYSQL_USER: str = config('MYSQL_USER', default='kaiwhakarite_user')
    MYSQL_PASSWORD: str = config('MYSQL_PASSWORD', default='')
    MYSQL_DATABASE: str = config('MYSQL_DATABASE', default='kaiwhakarite_db')
    MYSQL_CHARSET: str = config('MYSQL_CHARSET', default='utf8mb4')
    
    @classmethod
    def get_mysql_url(cls) -> str:
        """Generate MySQL connection URL from components"""
        return (f"mysql+pymysql://{cls.MYSQL_USER}:{cls.MYSQL_PASSWORD}"
                f"@{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DATABASE}"
                f"?charset={cls.MYSQL_CHARSET}")


class SecurityConfig:
    """Security configuration section"""
    SECRET_KEY: str = config(
        'SECRET_KEY', 
        default='your_secret_key_here_make_it_very_long_and_secure_'
                'change_in_production'
    )
    ALGORITHM: str = config('ALGORITHM', default='HS256')
    ACCESS_TOKEN_EXPIRE_HOURS: int = config(
        'ACCESS_TOKEN_EXPIRE_HOURS', 
        default=24, 
        cast=int
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = config(
        'REFRESH_TOKEN_EXPIRE_DAYS',
        default=30,
        cast=int
    )


class FileConfig:
    """File upload configuration section"""
    UPLOAD_DIR: str = config('UPLOAD_DIR', default='./uploads')
    MAX_UPLOAD_SIZE: int = config(
        'MAX_UPLOAD_SIZE', 
        default=10485760, 
        cast=int
    )  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [
        '.jpg', '.jpeg', '.png', '.gif', '.pdf', 
        '.doc', '.docx', '.xls', '.xlsx'
    ]


class CORSConfig:
    """CORS configuration section"""
    ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://192.168.1.4:3000",
        "http://172.16.40.33:3000",
        "http://172.16.40.33:3001",
    ]
    
    @classmethod
    def get_origins(cls) -> List[str]:
        """Get CORS origins with environment-specific settings"""
        debug_mode = config('DEBUG', default=True, cast=bool)
        if debug_mode:
            return cls.ORIGINS + ["*"]
        return cls.ORIGINS


class EmailConfig:
    """Email configuration section"""
    HOST: str = config('EMAIL_HOST', default='smtp.gmail.com')
    PORT: int = config('EMAIL_PORT', default=587, cast=int)
    USERNAME: str = config('EMAIL_USERNAME', default='')
    PASSWORD: str = config('EMAIL_PASSWORD', default='')
    FROM_ADDRESS: str = config(
        'EMAIL_FROM', 
        default='Kaiwhakarite Rawa <noreply@kaiwhakarite.co.nz>'
    )
    USE_TLS: bool = config('EMAIL_USE_TLS', default=True, cast=bool)


class AppConfig:
    """Application configuration section"""
    NAME: str = "Kaiwhakarite Rawa"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Inventory and Resource Management System"
    DEBUG: bool = config('DEBUG', default=True, cast=bool)
    LOG_LEVEL: str = config('LOG_LEVEL', default='INFO')
    
    # Admin settings
    ADMIN_EMAIL: str = config(
        'ADMIN_EMAIL', 
        default='admin@kaiwhakarite.co.nz'
    )
    
    # API settings
    API_PREFIX: str = "/api/v1"
    DOCS_URL: str = "/docs" if config('DEBUG', default=True, cast=bool) \
        else None


class Settings:
    """Main settings class that combines all configuration sections"""
    
    def __init__(self):
        # Initialize configuration sections
        self.database = DatabaseConfig()
        self.security = SecurityConfig()
        self.files = FileConfig()
        self.cors = CORSConfig()
        self.email = EmailConfig()
        self.app = AppConfig()
        
        # Legacy compatibility properties
        self.DATABASE_URL = self.database.URL
        self.SECRET_KEY = self.security.SECRET_KEY
        self.ALGORITHM = self.security.ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_HOURS = \
            self.security.ACCESS_TOKEN_EXPIRE_HOURS
        self.UPLOAD_DIR = self.files.UPLOAD_DIR
        self.MAX_UPLOAD_SIZE = self.files.MAX_UPLOAD_SIZE
        self.CORS_ORIGINS = self.cors.get_origins()
        self.EMAIL_HOST = self.email.HOST
        self.EMAIL_PORT = self.email.PORT
        self.EMAIL_USERNAME = self.email.USERNAME
        self.EMAIL_PASSWORD = self.email.PASSWORD
        self.EMAIL_FROM = self.email.FROM_ADDRESS
        self.ADMIN_EMAIL = self.app.ADMIN_EMAIL
        self.DEBUG = self.app.DEBUG
        self.APP_NAME = self.app.NAME
        self.APP_VERSION = self.app.VERSION
        self.APP_DESCRIPTION = self.app.DESCRIPTION
        
        # Ensure required directories exist
        self._create_directories()
    
    def _create_directories(self) -> None:
        """Create necessary directories"""
        directories = [
            self.files.UPLOAD_DIR,
            'database',
            'logs'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def get_database_url(self) -> str:
        """Get database URL with proper path resolution"""
        if self.database.URL.startswith('sqlite:'):
            # Ensure database directory exists
            db_path = self.database.URL.replace('sqlite:///', '')\
                .replace('sqlite://', '')
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        return self.database.URL


# Global settings instance
settings = Settings()


# Export commonly used settings for backwards compatibility
DATABASE_URL = settings.DATABASE_URL
SECRET_KEY = settings.SECRET_KEY
DEBUG = settings.DEBUG 