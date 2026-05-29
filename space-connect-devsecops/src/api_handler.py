"""
Space Connect - API Handler
Integração segura com APIs externas utilizando variáveis de ambiente
"""

import os
import logging
import requests
from requests.exceptions import RequestException, Timeout
from src.config import config

logger = logging.getLogger(__name__)


class APIHandler:
    """Handler para requisições às APIs externas do Space Connect"""
    
    # Timeouts para requisições
    REQUEST_TIMEOUT = 30
    RETRY_ATTEMPTS = 3
    
    @staticmethod
    def get_satellite_data(coordinates: dict) -> dict:
        """
        Obtém dados de satélites usando API segura
        
        Args:
            coordinates: Dict com latitude e longitude
            
        Returns:
            Dict com dados satelitais
            
        Raises:
            ValueError: Se API key não configurada
            RequestException: Se falhar a requisição
        """
        api_key = config.SATELLITE_API_KEY
        
        if not api_key:
            logger.error("SATELLITE_API_KEY não configurada. Configure via GitHub Secrets.")
            raise ValueError("SATELLITE_API_KEY não configurada")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "latitude": coordinates.get("lat"),
            "longitude": coordinates.get("lon"),
            "data_type": "telemetry"
        }
        
        try:
            response = requests.post(
                f"{config.SATELLITE_BASE_URL}/data",
                json=payload,
                headers=headers,
                timeout=APIHandler.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            logger.info(f"Dados satelitais obtidos para coordenadas {coordinates}")
            return response.json()
            
        except Timeout:
            logger.error("Timeout ao conectar com API de satélites")
            raise
        except RequestException as e:
            logger.error(f"Erro ao conectar com API de satélites: {str(e)}")
            raise
    
    @staticmethod
    def get_weather_data(coordinates: dict) -> dict:
        """
        Obtém dados de clima usando API segura
        
        Args:
            coordinates: Dict com latitude e longitude
            
        Returns:
            Dict com dados meteorológicos
        """
        api_secret = config.WEATHER_API_SECRET
        
        if not api_secret:
            logger.error("WEATHER_API_SECRET não configurada. Configure via GitHub Secrets.")
            raise ValueError("WEATHER_API_SECRET não configurada")
        
        headers = {
            "X-API-Key": api_secret,
            "Accept": "application/json"
        }
        
        params = {
            "lat": coordinates.get("lat"),
            "lon": coordinates.get("lon"),
            "units": "metric"
        }
        
        try:
            response = requests.get(
                f"{config.WEATHER_API_URL}/current",
                params=params,
                headers=headers,
                timeout=APIHandler.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            logger.info(f"Dados de clima obtidos para coordenadas {coordinates}")
            return response.json()
            
        except RequestException as e:
            logger.error(f"Erro ao conectar com API de clima: {str(e)}")
            raise
    
    @staticmethod
    def get_logistics_status(shipment_id: str) -> dict:
        """
        Obtém status de logística usando token seguro
        
        Args:
            shipment_id: ID do envio
            
        Returns:
            Dict com status da logística
        """
        api_token = config.LOGISTICA_API_TOKEN
        
        if not api_token:
            logger.error("LOGISTICA_API_TOKEN não configurada. Configure via GitHub Secrets.")
            raise ValueError("LOGISTICA_API_TOKEN não configurada")
        
        headers = {
            "Authorization": f"Token {api_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(
                f"{config.LOGISTICA_API_URL}/shipments/{shipment_id}",
                headers=headers,
                timeout=APIHandler.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            logger.info(f"Status de logística obtido para envio {shipment_id}")
            return response.json()
            
        except RequestException as e:
            logger.error(f"Erro ao conectar com API de logística: {str(e)}")
            raise
    
    @staticmethod
    def health_check() -> bool:
        """
        Verifica se todos os serviços estão acessíveis
        
        Returns:
            True se todos os serviços estão OK
        """
        services_status = {}
        
        # Verificar Satellite API
        try:
            response = requests.get(
                f"{config.SATELLITE_BASE_URL}/health",
                timeout=5
            )
            services_status["satellite"] = response.status_code == 200
        except RequestException:
            services_status["satellite"] = False
            logger.warning("Satellite API não acessível")
        
        # Verificar Weather API
        try:
            response = requests.get(
                f"{config.WEATHER_API_URL}/health",
                timeout=5
            )
            services_status["weather"] = response.status_code == 200
        except RequestException:
            services_status["weather"] = False
            logger.warning("Weather API não acessível")
        
        # Verificar Logistics API
        try:
            response = requests.get(
                f"{config.LOGISTICA_API_URL}/health",
                timeout=5
            )
            services_status["logistics"] = response.status_code == 200
        except RequestException:
            services_status["logistics"] = False
            logger.warning("Logistics API não acessível")
        
        logger.info(f"Health check result: {services_status}")
        return all(services_status.values())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Teste de inicialização
    try:
        logger.info("Space Connect API Handler inicializado")
        logger.info(f"Ambiente: {config.ENVIRONMENT}")
        logger.info(f"Debug mode: {config.DEBUG}")
    except Exception as e:
        logger.error(f"Erro ao inicializar: {str(e)}")
