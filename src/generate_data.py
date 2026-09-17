"""
Generate synthetic datasets for the Premium Sunscreen Launch Strategy project.
Creates realistic Indian market data for cosmetics sales, competitor products,
city metrics, marketing channels, and customer-level data.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

np.random.seed(42)

# Project root directory
ROOT_DIR = Path(__file__).parent.parent
RAW_DATA_DIR = ROOT_DIR / "data" / "raw"


def ensure_dirs():
    """Ensure output directories exist."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


def generate_products(n_products=850, save=True):
    """Generate Indian cosmetics products dataset."""
    categories = ['Sunscreen', 'Moisturizer', 'Cleanser', 'Serum', 'Makeup', 'Fragrance']
    brands = ['Aurelia', 'Minimalist', 'Neutrogena', 'Supergoop', 'Vaseline', 'Forestane', 'Himalaya', 'Biotique', 'Lakmé', 'Mamaearth']
    spfs = [15, 30, 50, 'NA']
    finishes = ['Matte', 'Glowy', 'Natural', 'Shine-Free']

    products = []
    for i in range(n_products):
        brand = np.random.choice(brands, p=[0.12, 0.15, 0.12, 0.08, 0.10, 0.08, 0.10, 0.08, 0.07, 0.10])
        price = np.random.choice([199, 299, 399, 499, 599, 699, 799, 899, 999, 1499, 1999, 2499],
                                 p=[0.08]*9 + [0.12, 0.10, 0.06])
        category = 'Sunscreen' if np.random.random() < 0.18 else np.random.choice(categories[1:])
        spf = np.random.choice(spfs, p=[0.45, 0.30, 0.22, 0.03])
        size = 50 if spf != 'NA' else np.random.choice([30, 50, 75, 100])
        finish = 'Natural' if category == 'Sunscreen' else np.random.choice(finishes)
        rating = np.clip(np.random.beta(5, 2) * 5, 1, 5)
        review_count = np.random.poisson(150) + 10

        products.append({
            'product_id': f'P{i+1:04d}',
            'brand': brand,
            'product_name': f'{brand} SunGuard {spf} {finish}' if category == 'Sunscreen' else f'{brand} Product {i}',
            'category': category,
            'price': price,
            'size_ml': size,
            'spf': spf,
            'finish': finish,
            'rating': round(rating, 2),
            'review_count': review_count,
            'launch_date': (datetime(2022, 1, 1) + timedelta(days=np.random.randint(0, 730))).strftime('%Y-%m-%d'),
            'is_luxury': 1 if price >= 1500 else 0
        })

    products_df = pd.DataFrame(products)
    if save:
        output_path = RAW_DATA_DIR / "Indian_Cosmetics_Products.csv"
        products_df.to_csv(output_path, index=False)
        print(f"  ✓ Products: {len(products_df)} rows → {output_path}")
    return products_df


def generate_customers(n_customers=3500, save=True):
    """Generate customer demographics dataset."""
    cities = ['Mumbai', 'Delhi', 'Bengaluru', 'Hyderabad', 'Pune', 'Chennai', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Lucknow']
    city_ranks = [5, 5, 5, 4, 4, 3, 3, 2, 2, 2]  # 5=Tier 1, 4=Tier 2, 3=Tier 3, 2=Tier 4

    customers = []
    for i in range(n_customers):
        city = np.random.choice(cities, p=[0.15, 0.15, 0.12, 0.10, 0.10, 0.08, 0.08, 0.07, 0.07, 0.08])
        income_bracket = np.random.choice(['<3L', '3L-6L', '6L-12L', '12L+'],
                                           p=[0.15, 0.35, 0.30, 0.20])

        customers.append({
            'customer_id': f'C{i+1:05d}',
            'age': np.random.randint(18, 55),
            'gender': np.random.choice(['F', 'M', 'Other'], p=[0.88, 0.10, 0.02]),
            'city': city,
            'city_rank': city_ranks[cities.index(city)],
            'income_bracket': income_bracket,
            'monthly_skincare_spend': round(np.random.gamma(2, 800) + 200, 2),
            'sunscreen_frequency': np.random.choice([0, 1, 2, 3, 4, 5], p=[0.15, 0.20, 0.20, 0.18, 0.15, 0.12]),
            'preferred_channel': np.random.choice(['Instagram', 'YouTube', 'Google', 'Nykaa', 'Physical Retail', 'Influencers'],
                                                   p=[0.10, 0.15, 0.12, 0.20, 0.23, 0.20]),
            'skin_type': np.random.choice(['Dry', 'Oily', 'Combination', 'Normal'], p=[0.20, 0.25, 0.30, 0.25]),
            'price_sensitivity': np.random.choice(['Low', 'Medium', 'High'], p=[0.20, 0.40, 0.40])
        })

    customers_df = pd.DataFrame(customers)
    if save:
        output_path = RAW_DATA_DIR / "Customers.csv"
        customers_df.to_csv(output_path, index=False)
        print(f"  ✓ Customers: {len(customers_df)} rows → {output_path}")
    return customers_df


def generate_orders(products_df, customers_df, n_orders=12000, save=True):
    """Generate orders dataset."""
    orders = []
    for order_id in range(1, n_orders + 1):
        customer = customers_df.iloc[np.random.randint(len(customers_df))]
        order_date = datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 365))
        n_items = np.random.randint(1, 4)

        for _ in range(n_items):
            product = products_df.iloc[np.random.randint(len(products_df))]
            quantity = np.random.randint(1, 3)

            discount_pct = np.random.choice([0, 5, 10, 15, 20, 25], p=[0.40, 0.25, 0.15, 0.10, 0.07, 0.03])
            final_price = product['price'] * (1 - discount_pct / 100)

            orders.append({
                'order_id': f'O{order_id:05d}',
                'product_id': product['product_id'],
                'customer_id': customer['customer_id'],
                'order_date': order_date.strftime('%Y-%m-%d'),
                'quantity': quantity,
                'list_price': product['price'],
                'discount_pct': discount_pct,
                'final_price': round(final_price, 2),
                'city': customer['city']
            })

    orders_df = pd.DataFrame(orders)
    if save:
        output_path = RAW_DATA_DIR / "Orders.csv"
        orders_df.to_csv(output_path, index=False)
        print(f"  ✓ Orders: {len(orders_df)} rows → {output_path}")
    return orders_df


def generate_competitors(save=True):
    """Generate competitor products dataset."""
    competitors = [
        ('Minimalist', 'SPF 50', 50, 50, 499, 18000, 4.4, 'Gel', 'Silicone-free, Niacinamide, Zinc Oxide'),
        ('Neutrogena', 'Ultra Sheer Dry-Touch', 50, 50, 649, 25000, 4.3, 'Lotion', 'Avobenzone, Homosalate, Octisalate'),
        ('Supergoop!', 'Unseen Sunscreen', 40, 50, 3199, 2500, 4.6, 'Gel', 'Ethylhexyl Methoxycinnamate, Zinc Oxide'),
        ('La Roche Posay', 'Anthelios Age Correct', 50, 50, 899, 12000, 4.5, 'Cream', 'Mexoryl XL, Octocrylene, Titanium Dioxide'),
        ('ISDIN', 'UVelix Dry Touch', 50, 50, 799, 8500, 4.4, 'Lotion', 'Mexoryl SX, Avobenzone'),
        ('Biore', 'UV Aqua Rich Watery', 50, 50, 549, 28000, 4.2, 'Gel', 'Ethylhexyl Methoxycinnamate, Octocrylene'),
        ('Himalaya', 'UV Protection Face Cream', 50, 50, 399, 15000, 4.1, 'Cream', 'Zinc Oxide, Turmeric Extract'),
        ('Vaseline', 'Intensive Care SPF 50', 50, 50, 249, 35000, 3.9, 'Lotion', 'Oxybenzone, Avobenzone'),
        ('CeraVe', 'Hydrating Mineral Sunscreen', 30, 34, 750, 5000, 4.3, 'Cream', 'Zinc Oxide, Hyaluronic Acid'),
        ("Sun'bly", "Daily Care Sunscreen", 50, 50, 450, 4200, 4.2, "Gel", "Zinc Oxide, Centella Asiatica")
    ]

    competitor_df = pd.DataFrame([
        {
            'brand': brand,
            'product_name': name,
            'spf': int(spf),
            'size_ml': size,
            'mrp': price,
            'reviews': reviews,
            'rating': rating,
            'texture': texture,
            'key_ingredients': ingredients,
            'positioning': 'Mass' if price < 700 else 'Premium' if price < 1500 else 'Luxury',
            'is_luxury': 1 if price >= 1500 else 0
        }
        for brand, name, spf, size, price, reviews, rating, texture, ingredients in competitors
    ])
    if save:
        output_path = RAW_DATA_DIR / "Competitor_Products.csv"
        competitor_df.to_csv(output_path, index=False)
        print(f"  ✓ Competitors: {len(competitor_df)} rows → {output_path}")
    return competitor_df


def generate_city_metrics(save=True):
    """Generate city-level metrics dataset."""
    cities = ['Mumbai', 'Delhi', 'Bengaluru', 'Hyderabad', 'Pune', 'Chennai', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Lucknow']
    city_ranks = [5, 5, 5, 4, 4, 3, 3, 2, 2, 2]

    city_metrics = []
    for city in cities:
        rank = city_ranks[cities.index(city)]
        tier_map = {5: 'Tier 1', 4: 'Tier 2', 3: 'Tier 3', 2: 'Tier 4'}
        purchase_power = {'Tier 1': 8.5, 'Tier 2': 6.8, 'Tier 3': 5.2, 'Tier 4': 4.1}[tier_map[rank]]

        city_metrics.append({
            'city': city,
            'population_millions': round(np.random.uniform(2.5, 15.0), 1),
            'avg_monthly_skincare_spend': round(purchase_power * 650, 0),
            'e_commerce_penetration': round(0.35 + (rank - 2) * 0.12, 2),
            'premium_beauty_density': rank * 0.8 + np.random.uniform(0, 0.3),
            'competition_count': rank * 3 + np.random.randint(0, 5)
        })

    city_df = pd.DataFrame(city_metrics)
    if save:
        output_path = RAW_DATA_DIR / "City_Metrics.csv"
        city_df.to_csv(output_path, index=False)
        print(f"  ✓ Cities: {len(city_df)} rows → {output_path}")
    return city_df


def generate_marketing_channels(save=True):
    """Generate marketing channel benchmarks dataset."""
    # Fixed: Influencers tuple had vol/conv swapped (was 0.6, 5000000; should be 5000000, 0.6)
    channels = [
        ('Instagram', 2.50, 1200000, 0.8, 'Awareness'),
        ('YouTube', 3.20, 800000, 1.2, 'Education'),
        ('Influencers', 250000, 5000000, 0.6, 'Trust'),  # FIXED: swapped vol/conv
        ('Google Ads', 3.80, 5000000, 2.5, 'Intent'),
        ('Nykaa', 0.30, 600, 0.9, 'Conversion'),
        ('Physical Retail', 1.80, 400, 1.5, 'Trust'),
    ]

    marketing_df = pd.DataFrame([
        {
            'channel': ch,
            'cpa_estimate': cpa,
            'monthly_volume': vol,
            'conversion_rate': conv,
            'primary_use': use
        }
        for ch, cpa, vol, conv, use in channels
    ])
    if save:
        output_path = RAW_DATA_DIR / "Marketing_Channels.csv"
        marketing_df.to_csv(output_path, index=False)
        print(f"  ✓ Channels: {len(marketing_df)} rows → {output_path}")
    return marketing_df


def generate_customer_insights(customers_df, save=True):
    """Generate customer-level insights dataset."""
    customer_insights = []
    for _, c in customers_df.iterrows():
        # FIXED: city_rank >= 1 was always true; use tier-based logic
        tier = {5: 1, 4: 2, 3: 3, 2: 4}[c['city_rank']]  # 1=Tier 1, 4=Tier 4
        multiplier = 0.7 if tier <= 2 else 0.5  # Higher spending in Tier 1-2 cities
        base_spending = c['monthly_skincare_spend'] * multiplier
        customer_insights.append({
            'customer_id': c['customer_id'],
            'age': c['age'],
            'gender': c['gender'],
            'city': c['city'],
            'city_rank': c['city_rank'],
            'income_bracket': c['income_bracket'],
            'monthly_spending': c['monthly_skincare_spend'],
            'skincare_spending': round(base_spending, 2),
            'sunscreen_usage': c['sunscreen_frequency'],
            'purchase_frequency': c['sunscreen_frequency'] + np.random.randint(0, 3),
            'preferred_channel': c['preferred_channel'],
            'brand_preference': np.random.choice(['Aurelia', 'Minimalist', 'Neutrogena', 'Supergoop!', 'Lakmé']),
            'price_sensitivity': c['price_sensitivity'],
            'spf_preference': np.random.choice([30, 50, 'NA'], p=[0.35, 0.60, 0.05]),
            'skin_type': c['skin_type'],
            'influencer_influence': np.random.choice(['Low', 'Medium', 'High'], p=[0.50, 0.35, 0.15])
        })

    insights_df = pd.DataFrame(customer_insights)
    if save:
        output_path = RAW_DATA_DIR / "Customer_Insights.csv"
        insights_df.to_csv(output_path, index=False)
        print(f"  ✓ Customer Insights: {len(insights_df)} rows → {output_path}")
    return insights_df


def main():
    """Generate all synthetic datasets."""
    ensure_dirs()
    print("🚀 Generating synthetic datasets for Premium Sunscreen Launch Strategy...")

    products_df = generate_products()
    customers_df = generate_customers()
    generate_orders(products_df, customers_df)
    generate_competitors()
    generate_city_metrics()
    generate_marketing_channels()
    generate_customer_insights(customers_df)

    print("\n✅ All synthetic datasets generated successfully!")


if __name__ == "__main__":
    main()