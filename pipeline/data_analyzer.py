import pandas as pd


class DataAnalyzer:
    def __init__(self, enriched_df):
        self.enriched_df = enriched_df
    
    
    def analyze(self):
        grouped = self.enriched_df.groupby('username').agg({
            'revenue': 'sum', 'price': ['count', 'mean']
        })
        
        grouped.columns = ['_'.join(col).strip() for col in grouped.columns.values] 
        
        grouped = grouped.rename(columns={
            'revenue_sum': 'total_revenue',
            'price_count': 'product_count',
            'price_mean': 'average_price'
        })
        
        result = grouped.to_dict('index') 
        
        return result