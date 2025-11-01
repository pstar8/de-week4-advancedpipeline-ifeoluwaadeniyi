import json
import random
from pipeline.config import ConfigManager
from pipeline.api_client import ApiClient
from pipeline.data_enricher import DataEnricher
from pipeline.data_analyzer import DataAnalyzer


class Pipeline:
    def __init__(self, config_file='pipeline.cfg'):
     self.config_file = config_file
    
    
    def run(self):
        """ Load configuration """
        config = ConfigManager(self.config_file)  
        base_url = config.get_base_url()
        url_limit = config.get_url_limit()
        
        """ Initialize API client"""
        api_client = ApiClient(base_url, url_limit)
        
        products = api_client.get_all_products()
        print(f"   ✓ Fetched {len(products)} products")
        
        users = api_client.get_all_users()
        print(f"   ✓ Fetched {len(users)} users")
        
        # Add userId to products 
        user_ids = [user['id'] for user in users]
        for product in products:
            product['userId'] = random.choice(user_ids)
        print(f"   ✓ Products assigned to sellers\n")
        
        """ Enrich products with user data"""
        enricher = DataEnricher(products, users)
        enriched_data = enricher.enrich()
        print(f"   ✓ Enriched {len(enriched_data)} products\n")
        
        """ Analyze enriched data"""
        analyzer = DataAnalyzer(enriched_data)
        results = analyzer.analyze()
        print(f" Analyzed {len(results)} sellers\n")
        
        """ Save results to JSON file"""
        self.save_results(results)
        
        return results
    
    
    def save_results(self, results, output_file='seller_performance_report.json'):
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        
        print(f"Results saved to {output_file}")
