"""
Streamlit dashboard for Premium Sunscreen Launch Strategy analysis.
Provides interactive visualizations and insights for market planning.
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# Project paths
ROOT_DIR = Path(__file__).parent.parent
RAW_DATA_DIR = ROOT_DIR / "data" / "raw"

st.set_page_config(
    page_title="Premium Sunscreen Launch Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    """Load all generated datasets."""
    datasets = {}
    try:
        datasets['products'] = pd.read_csv(RAW_DATA_DIR / "Indian_Cosmetics_Products.csv")
        datasets['customers'] = pd.read_csv(RAW_DATA_DIR / "Customers.csv")
        datasets['orders'] = pd.read_csv(RAW_DATA_DIR / "Orders.csv")
        datasets['competitors'] = pd.read_csv(RAW_DATA_DIR / "Competitor_Products.csv")
        datasets['cities'] = pd.read_csv(RAW_DATA_DIR / "City_Metrics.csv")
        datasets['channels'] = pd.read_csv(RAW_DATA_DIR / "Marketing_Channels.csv")
        datasets['insights'] = pd.read_csv(RAW_DATA_DIR / "Customer_Insights.csv")
    except FileNotFoundError:
        st.warning("Data files not found. Please run `python src/generate_data.py` first.")
        st.stop()
    return datasets


def main():
    st.title("☀️ Premium Sunscreen Launch Strategy Dashboard")
    st.markdown("---")

    data = load_data()

    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Products", f"{len(data['products']):,}")
    with col2:
        st.metric("Total Customers", f"{len(data['customers']):,}")
    with col3:
        st.metric("Total Orders", f"{len(data['orders']):,}")
    with col4:
        avg_price = data['products']['price'].mean()
        st.metric("Avg Product Price", f"₹{avg_price:,.0f}")

    st.markdown("---")

    # Tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs([
        "Products & Sales 📊",
        "Customer Insights 👥",
        "Competitive Analysis 🏆",
        "Marketing Channels 📣"
    ])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Products by Category")
            fig = px.pie(
                data['products'],
                names='category',
                hole=0.3,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Products by Brand")
            fig = px.bar(
                data['products'].groupby('brand').size().reset_index(name='count'),
                x='brand',
                y='count',
                color='count',
                color_continuous_scale='Sunset'
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Price Distribution")
        fig = px.histogram(
            data['products'],
            x='price',
            nbins=30,
            color='category' if 'category' in data['products'] else None,
            title="Product Price Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Customers by City")
            fig = px.bar(
                data['customers'].groupby('city').size().reset_index(name='count'),
                x='city',
                y='count',
                color='count',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Income Bracket Distribution")
            fig = px.pie(
                data['customers'],
                names='income_bracket',
                hole=0.3
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Monthly Skincare Spending by Tier")
        tier_map = {1: 'Tier 1', 2: 'Tier 2', 3: 'Tier 3', 4: 'Tier 4'}
        df_insights = data['insights'].copy()
        tier_counts = df_insights['city_rank'].map({5: 'Tier 1', 4: 'Tier 2', 3: 'Tier 3', 2: 'Tier 4'})
        df_insights['city_tier'] = tier_counts
        fig = px.box(
            df_insights,
            x='city_tier',
            y='skincare_spending',
            title='Skincare Spending by City Tier'
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Competitor Comparison")
            fig = px.scatter(
                data['competitors'],
                x='mrp',
                y='rating',
                size='reviews',
                color='positioning',
                hover_name='brand',
                title='Price vs Rating by Brand'
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Brand Positioning Matrix")
            fig = px.scatter(
                data['competitors'],
                x='mrp',
                y='reviews',
                color='positioning',
                hover_name='product_name',
                title='Price vs Reviews'
            )
            st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            data['competitors'][['brand', 'product_name', 'spf', 'mrp', 'rating', 'positioning']],
            hide_index=True
        )

    with tab4:
        st.subheader("Marketing Channel Performance")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=data['channels']['channel'],
            y=data['channels']['cpa_estimate'],
            name='CPA (₹)',
            marker_color='indianred'
        ))
        fig.add_trace(go.Bar(
            x=data['channels']['channel'],
            y=data['channels']['conversion_rate'],
            name='Conversion Rate (%)',
            marker_color='goldenrod'
        ))
        fig.update_layout(
            barmode='group',
            title="CPA & Conversion by Channel"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            data['channels'].rename(columns={'cpa_estimate': 'CPA Estimate (₹)', 'conversion_rate': 'Conversion Rate (%)'}),
            hide_index=True
        )

    # Footer
    st.markdown("---")
    st.markdown("Generated with [Streamlit](https://streamlit.io) | "
                f"Data: {len(data['products'])} products, {len(data['customers'])} customers")


if __name__ == "__main__":
    main()