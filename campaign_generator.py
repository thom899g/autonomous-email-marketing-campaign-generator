from mailchimp_api import MailchimpAPI
from data_analyzer import DataAnalyzer
from datetime import datetime
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class CampaignGenerator:
    def __init__(self, api_key: str, list_id: str):
        self.mailchimp = MailchimpAPI(api_key)
        self.list_id = list_id
        self.data_analyzer = DataAnalyzer()
        
    def generate_campaign(self, audience_segment: Dict) -> Dict:
        """Generates a personalized email campaign based on audience data."""
        try:
            # Analyze customer behavior to determine preferences
            preferences = self.data_analyzer.analyze(audience_segment)
            
            # Create content tailored to preferences
            subject_line = f"Special Offer for {preferences['interest']}"
            body = (
                f"Greetings, {audience_segment['first_name']}\n\n"
                f"We noticed you're interested in {preferences['interest']}. Check out our latest offer!"
            )
            
            # Determine optimal send time
            send_time = self._calculate_optimal_send_time(audience_segment)
            
            campaign_data = {
                'subject': subject_line,
                'body': body,
                'send_time': send_time.isoformat(),
                'audience': audience_segment
            }
            
            logger.info("Campaign generated successfully.")
            return campaign_data
            
        except Exception as e:
            logger.error(f"Campaign generation failed: {str(e)}")
            raise CampaignGenerationError(f"Failed to generate campaign: {str(e)}")

    def _calculate_optimal_send_time(self, audience_segment: Dict) -> datetime:
        """Determines the best time to send the email for maximum engagement."""
        # Simplified example logic; real implementation would use behavioral data
        user_timezone = audience_segment.get('timezone', 'UTC')
        optimal_hour = self.data_analyzer.determine_optimal_hour(user_timezone)
        
        return datetime.combine(datetime.today(), datetime.min.time()).replace(
            hour=optimal_hour, minute=0, second=0, tzinfo=user_timezone)

class CampaignGenerationError(Exception):
    pass