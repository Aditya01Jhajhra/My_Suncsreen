"""
Export the key charts for the launch strategy report as PNGs into reports/charts/.
Run after src/generate_data.py has populated data/raw/.
"""

import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
RAW_DIR = ROOT_DIR / "data" / "raw"
CHARTS_DIR = ROOT_DIR / "reports" / "charts"

sns.set_theme(style="whitegrid")


def main():
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    products = pd.read_csv(RAW_DIR / "Indian_Cosmetics_Products.csv")
    competitors = pd.read_csv(RAW_DIR / "Competitor_Products.csv")
    cities = pd.read_csv(RAW_DIR / "City_Metrics.csv")
    channels = pd.read_csv(RAW_DIR / "Marketing_Channels.csv")

    con = duckdb.connect()
    con.register("cities", cities)
    con.register("channels", channels)

    # --- Chart 1: competitor price vs rating -------------------------------
    fig, ax = plt.subplots(figsize=(8, 5))
    sizes = competitors["reviews"] / competitors["reviews"].max() * 400 + 30
    ax.scatter(competitors["mrp"], competitors["rating"], s=sizes,
               c=competitors["mrp"], cmap="viridis", alpha=0.8, edgecolor="white")
    for _, row in competitors.iterrows():
        ax.annotate(row["brand"], (row["mrp"], row["rating"]), fontsize=8,
                    xytext=(4, 4), textcoords="offset points")
    ax.set_xlabel("MRP (₹)")
    ax.set_ylabel("Rating")
    ax.set_title("Competitor price vs. rating (bubble size = reviews)")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "01_competitor_positioning.png", dpi=150)
    plt.close(fig)

    # --- Chart 2: city opportunity score ------------------------------------
    city_opportunity = con.sql("""
        SELECT city,
               avg_monthly_skincare_spend,
               e_commerce_penetration,
               competition_count,
               ROUND(avg_monthly_skincare_spend * e_commerce_penetration
                     / NULLIF(competition_count, 0), 1) AS opportunity_score
        FROM cities
        ORDER BY opportunity_score DESC
    """).df()

    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(data=city_opportunity, x="opportunity_score", y="city",
                hue="city", legend=False, palette="rocket", ax=ax)
    ax.set_title("City launch-opportunity score (spend × e-comm penetration / competition)")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "02_city_opportunity.png", dpi=150)
    plt.close(fig)

    # --- Chart 3: channel true CPA -----------------------------------------
    channel_cpa = con.sql("""
        SELECT channel,
               ROUND(
                   CASE WHEN channel = 'Influencers'
                        THEN cpa_estimate / (monthly_volume * conversion_rate / 100.0)
                        ELSE cpa_estimate / (conversion_rate / 100.0)
                   END, 2
               ) AS true_cpa
        FROM channels
        ORDER BY true_cpa ASC
    """).df()

    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.barplot(data=channel_cpa, x="true_cpa", y="channel",
                hue="channel", legend=False, palette="mako", ax=ax)
    ax.set_xlabel("True cost per acquisition (₹)")
    ax.set_title("Marketing channel cost-efficiency (lower = better)")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "03_channel_true_cpa.png", dpi=150)
    plt.close(fig)

    # --- Chart 4: price distribution by category ----------------------------
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.histplot(data=products, x="price", hue="category", bins=25, ax=ax, multiple="stack")
    ax.set_title("Product price distribution by category")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "04_price_distribution.png", dpi=150)
    plt.close(fig)

    print(f"✓ 4 charts exported to {CHARTS_DIR}")
    print("\nCity opportunity ranking:")
    print(city_opportunity.to_string(index=False))
    print("\nChannel true CPA ranking:")
    print(channel_cpa.to_string(index=False))


if __name__ == "__main__":
    main()