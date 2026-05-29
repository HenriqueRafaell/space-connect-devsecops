"""
Space Connect - Arquivo de Configuração
Utiliza variáveis de ambiente para segurança
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env (apenas para desenvolvimento local)
load_dotenv()


class Config:
    """Configuração base da aplicação"""
    
    # Satellite APIs
    SATELLITE_API_KEY = os.environ.get("SATELLITE_API_KEY")
    SATELLITE_BASE_URL = os.environ.get("SATELLITE_BASE_URL", "https://api.satellite.example.com")
    
    # AWS Configuration
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
    
    # Weather and Agriculture APIs
    WEATHER_API_SECRET = os.environ.get("WEATHER_API_SECRET")
    WEATHER_API_URL = os.environ.get("WEATHER_API_URL", "https://api.weather.example.com")
    AGRICULTURE_DATA_TOKEN = os.environ.get("AGRICULTURE_DATA_TOKEN")
    
    # Database Configuration
    DATABASE_HOST = os.environ.get("DATABASE_HOST", "localhost")
    DATABASE_PORT = os.environ.get("DATABASE_PORT", "5432")
    DATABASE_USER = os.environ.get("DATABASE_USER", "admin")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "space_connect")
    DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    
    # Logistics API
    LOGISTICA_API_TOKEN = os.environ.get("LOGISTICA_API_TOKEN")
    LOGISTICA_API_URL = os.environ.get("LOGISTICA_API_URL", "https://api.logistica.example.com")
    
    # Application Settings
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
    
    # Validation
    @staticmethod
    def validate_required_secrets():
        """Valida se as secrets críticas estão configuradas"""
        required = [
            "SATELLITE_API_KEY",
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "WEATHER_API_SECRET",
            "DATABASE_PASSWORD",
            "LOGISTICA_API_TOKEN"
        ]
        
        missing = [key for key in required if not os.environ.get(key)]
        
        if missing:
            raise ValueError(f"Secrets obrigatórias não configuradas: {', '.join(missing)}")
        
        return True


class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    DEBUG = True
    ENVIRONMENT = "development"


class ProductionConfig(Config):
    """Configuração para produção"""
    DEBUG = False
    ENVIRONMENT = "production"
    
    # Em produção, todas as secrets são obrigatórias
    @classmethod
    def init_app(cls):
        cls.validate_required_secrets()


class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    DATABASE_NAME = "space_connect_test"


# Seleção de configuração
def get_config():
    """Retorna a configuração apropriada baseada no ambiente"""
    env = os.environ.get("ENVIRONMENT", "development")
    
    if env == "production":
        return ProductionConfig
    elif env == "testing":
        return TestingConfig
    else:
        return DevelopmentConfig


# Instância de configuração ativa
config = get_config()
