"""
Unit tests for synthetic data generation.
"""

import pytest
import pandas as pd
import numpy as np


def test_generate_products():
    """Test products dataset generation."""
    from src.generate_data import generate_products

    df = generate_products(n_products=50, save=False)

    assert len(df) == 50
    assert 'product_id' in df.columns
    assert 'brand' in df.columns
    assert 'price' in df.columns
    assert df['price'].between(199, 2499).all()
    assert df['rating'].between(1, 5).all()


def test_generate_competitors():
    """Test competitors dataset generation."""
    from src.generate_data import generate_competitors

    df = generate_competitors(save=False)

    assert len(df) == 10
    assert df['brand'].nunique() == 10
    assert df['mrp'].gt(0).all()
    assert df['rating'].between(0, 5).all()


def test_generate_marketing_channels():
    """Test marketing channels dataset generation."""
    from src.generate_data import generate_marketing_channels

    df = generate_marketing_channels(save=False)

    assert len(df) == 6
    assert df['channel'].nunique() == 6
    assert df['cpa_estimate'].gt(0).all()
    assert df['conversion_rate'].between(0, 100).all()


def test_generate_city_metrics():
    """Test city metrics dataset generation."""
    from src.generate_data import generate_city_metrics

    df = generate_city_metrics(save=False)

    assert len(df) == 10
    assert df['city'].nunique() == 10
    assert df['population_millions'].between(0, 50).all()


def test_generate_customer_insights():
    """Test customer insights dataset generation."""
    from src.generate_data import generate_customer_insights

    customers = pd.DataFrame({
        'customer_id': ['C00001', 'C00002'],
        'age': [25, 40],
        'gender': ['F', 'M'],
        'city': ['Mumbai', 'Jaipur'],
        'city_rank': [5, 2],
        'income_bracket': ['12L+', '<3L'],
        'monthly_skincare_spend': [2000, 500],
        'sunscreen_frequency': [3, 1],
        'preferred_channel': ['Instagram', 'YouTube'],
        'skin_type': ['Oily', 'Dry'],
        'price_sensitivity': ['Medium', 'High']
    })

    df = generate_customer_insights(customers, save=False)

    assert len(df) == 2
    assert 'skincare_spending' in df.columns
    assert df['skincare_spending'].iloc[0] > df['skincare_spending'].iloc[1]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])