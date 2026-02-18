import logging
from datetime import datetime, timedelta
from typing import Dict, List
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class PerformanceMonitor:
    def __init__(self, api_key: str, list_id: str):
        self.mailchimp = MailchimpAPI(api_key)
        self.list_id = list_id
        
    def monitor_campaign(self, campaign_id: str) -> Dict:
        """Monitors email campaign performance and returns metrics."""
        try:
            # Get campaign statistics
            stats = self._fetch_stats(campaign_id)
            
            if not stats:
                raise NoCampaignDataError("No data available for the campaign.")
                
            # Analyze engagement
            open_rate = self._calculate_open_rate(stats['opens'], stats['sent'])
            conversion_rate = self._calculate_conversion_rate(
                stats['clicks'], stats['sent'])
                
            metrics = {
                'open_rate': open_rate,
                'conversion_rate': conversion_rate,
                'last_sent_time': datetime.fromisoformat(stats['last_send']),