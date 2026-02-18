from typing import Dict, List, Optional
import logging
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class MailchimpAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.mailchimp.com/v3.0"
        
    def create_campaign(self, campaign_data: Dict) -> Dict:
        """Creates a new email campaign in Mailchimp."""
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            response = requests.post(
                f"{self.base_url}/campaigns",
                json=campaign_data,
                headers=headers
            )
            
            if not response.ok:
                raise MailchimpAPIError(f"API request failed: {response.text}")
                
            logger.info("Campaign created successfully.")
            return response.json()
            
        except Exception as e:
            logger.error(f"Mailchimp API error: {str(e)}")
            raise

    def send_campaign(self, campaign_id: str) -> Dict:
        """Sends an existing email campaign."""
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            response = requests.post(
                f"{self.base_url}/campaigns/{campaign_id}/actions/send",
                headers=headers
            )
            
            if not response.ok:
                raise MailchimpAPIError(f"Send request failed: {response.text}")
                
            logger.info("Campaign sent successfully.")
            return response.json()
            
        except Exception as e:
            logger.error(f"Mailchimp API error: {str(e)}")
            raise

class MailchimpAPIError(Exception):
    pass