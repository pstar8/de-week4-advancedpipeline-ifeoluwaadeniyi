from pipeline.pipeline import Pipeline

def main():
    """Run the complete pipeline"""
    pipeline = Pipeline('pipeline.cfg')
    results = pipeline.run()
    
    
    for username, metrics in results.items():
        print(f"\n{username}:")
        print(f"  Total Revenue: ${metrics['total_revenue']:.2f}")
        print(f"  Products Sold: {metrics['product_count']}")
        print(f"  Avg Price: ${metrics['average_price']:.2f}")


if __name__ == "__main__":
    main()