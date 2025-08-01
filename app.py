#!/usr/bin/env python3

import requests
import redis
import json
import logging
import sys
from datetime import datetime
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('getter_service.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def send(message):
    try:
        logger.info("Sending message to Redis")
        r = redis.Redis(host=config.host, 
                        port=config.port)
        r.publish(config.channel, message)
        logger.info("Message sent successfully")
    except redis.RedisError as e:
        logger.error(f"Failed to send message to Redis: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while sending message: {e}")
        raise

def make_request(url, description):
    """Make a resilient HTTP request with proper error handling"""
    try:
        logger.info(f"Making request to: {description}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        logger.info(f"Request successful: {description}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for {description}: {e}")
        logger.error(f"URL: {url}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response for {description}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during request for {description}: {e}")
        raise

def main():
    try:
        logger.info("Initializing getter service")
        
        # Get tenders list
        tenders_data = make_request(config.url_tenders, "tenders list")
        
        if not tenders_data or 'Listado' not in tenders_data:
            logger.error("Invalid response format: 'Listado' not found in tenders data")
            sys.exit(1)
        
        tenders_list = tenders_data['Listado']
        if not tenders_list:
            logger.warning("No tenders found in the response")
            return
        
        logger.info(f"Found {len(tenders_list)} tenders, processing first 5")
        
        for i in range(min(5, len(tenders_list))):
            try:
                tender_code = tenders_list[i]['CodigoExterno']
                url = config.url_by_code(tender_code)
                
                # Get individual tender details
                tender_response = make_request(url, f"tender details for code {tender_code}")
                
                if not tender_response or 'Listado' not in tender_response or not tender_response['Listado']:
                    logger.error(f"Invalid tender response for code {tender_code}")
                    continue
                
                tender = tender_response['Listado'][0]
                
                message = {
                    'id': i,
                    'status': "pre-processed",
                    'createdAt': datetime.now().strftime('%Y-%m-%d'),
                    'payload': {
                        'code': tender['CodigoExterno'],
                        'title': tender['Nombre'],
                        'description': tender['Descripcion']
                    }
                }
                
                send(json.dumps(message))
                logger.info(f"Successfully processed tender {i+1}/5")
                
            except Exception as e:
                logger.error(f"Failed to process tender {i+1}: {e}")
                # Continue with next tender instead of stopping the entire process
                continue
        
        logger.info("Getter service completed successfully")
        
    except Exception as e:
        logger.error(f"Critical error in main function: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 