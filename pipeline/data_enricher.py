import pandas as pd


class DataEnricher:
    def __init__(self, products, users):

        self.products_df = pd.DataFrame(products)
        self.users_df = pd.DataFrame(users)
    

    def enrich(self):
        merged_df = pd.merge(
            self.products_df,
            self.extract_user_fields(self.users_df),
            how='left',
            left_on='userId',
            right_on='userId',
            suffixes=('', '_user')
        )

        enriched_df = self.calculate_revenue(merged_df)

        return enriched_df

    def extract_user_fields(self, users_df):        
        extracted = users_df[['id', 'username', 'email', 'name']].copy()
        
        extracted['firstname'] = users_df['name'].apply(lambda x: x.get('firstname'))
        
        extracted['lastname'] = users_df['name'].apply(lambda x: x.get('lastname'))
        
        extracted = extracted.drop('name', axis=1)
        
        extracted = extracted.rename(columns={'id': 'userId'})
        
        return extracted
        
    
    def calculate_revenue(self, df):
        df['quantity'] = df['rating'].apply(lambda x: x.get('count', 0))
        df['revenue'] = df['price'] * df['quantity']
        
        return df