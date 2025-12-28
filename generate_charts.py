import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set professional style for business presentations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Load the dataset
print("Loading dataset...")
df = pd.read_csv('register_numbers.csv')
df['created_at'] = pd.to_datetime(df['created_at'])
df['year_month'] = df['created_at'].dt.to_period('M')

print(f"Dataset loaded: {len(df):,} records")

# Create charts directory if it doesn't exist
import os
os.makedirs('charts', exist_ok=True)

# ============================================================================
# 1. MARKET OVERVIEW: Regional Distribution
# ============================================================================
print("Generating Chart 1: Market Share by Region...")
fig, ax = plt.subplots(figsize=(12, 7))
top_regions = df['region_name'].value_counts().head(10)
colors = sns.color_palette("viridis", len(top_regions))
bars = ax.barh(range(len(top_regions)), top_regions.values, color=colors)
ax.set_yticks(range(len(top_regions)))
ax.set_yticklabels(top_regions.index)
ax.set_xlabel('Number of Listings', fontweight='bold')
ax.set_ylabel('Region', fontweight='bold')
ax.set_title('Market Share by Region - Top 10 Markets', fontweight='bold', fontsize=16, pad=20)
ax.invert_yaxis()

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars, top_regions.values)):
    percentage = (value / len(df)) * 100
    ax.text(value + 20, i, f'{value:,} ({percentage:.1f}%)',
            va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/01_market_share_by_region.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 2. PRICING ANALYSIS: Price Distribution
# ============================================================================
print("Generating Chart 2: Price Distribution by Category...")
fig, ax = plt.subplots(figsize=(12, 7))
price_ranges = pd.cut(df['price'],
                      bins=[0, 1000, 5000, 10000, 20000, float('inf')],
                      labels=['Budget\n(<1,000)', 'Standard\n(1K-5K)',
                             'Premium\n(5K-10K)', 'Luxury\n(10K-20K)',
                             'Ultra-Premium\n(>20K)'])
price_counts = price_ranges.value_counts().sort_index()
colors = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#9b59b6']
bars = ax.bar(range(len(price_counts)), price_counts.values, color=colors, edgecolor='black', linewidth=1.5)
ax.set_xticks(range(len(price_counts)))
ax.set_xticklabels(price_counts.index, fontweight='bold')
ax.set_ylabel('Number of Listings', fontweight='bold')
ax.set_xlabel('Price Category', fontweight='bold')
ax.set_title('Inventory Distribution by Price Segment', fontweight='bold', fontsize=16, pad=20)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, price_counts.values)):
    percentage = (value / len(df)) * 100
    ax.text(i, value + 30, f'{value:,}\n({percentage:.1f}%)',
            ha='center', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('charts/02_price_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 3. REVENUE POTENTIAL: Average Price by Region
# ============================================================================
print("Generating Chart 3: Average Price by Region...")
fig, ax = plt.subplots(figsize=(12, 7))
avg_price_by_region = df.groupby('region_name')['price'].agg(['mean', 'count']).sort_values('mean', ascending=False).head(10)
colors = sns.color_palette("coolwarm", len(avg_price_by_region))
bars = ax.barh(range(len(avg_price_by_region)), avg_price_by_region['mean'].values, color=colors)
ax.set_yticks(range(len(avg_price_by_region)))
ax.set_yticklabels(avg_price_by_region.index)
ax.set_xlabel('Average Price (AZN)', fontweight='bold')
ax.set_ylabel('Region', fontweight='bold')
ax.set_title('Average Listing Price by Region - Top 10 Markets', fontweight='bold', fontsize=16, pad=20)
ax.invert_yaxis()

# Add value labels
for i, (bar, value, count) in enumerate(zip(bars, avg_price_by_region['mean'].values, avg_price_by_region['count'].values)):
    ax.text(value + 100, i, f'{value:,.0f} AZN (n={count})',
            va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/03_average_price_by_region.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 4. MARKET TRENDS: Listings Over Time
# ============================================================================
print("Generating Chart 4: Market Activity Over Time...")
fig, ax = plt.subplots(figsize=(14, 7))
monthly_listings = df.groupby('year_month').size()
monthly_listings.index = monthly_listings.index.to_timestamp()

ax.plot(monthly_listings.index, monthly_listings.values,
        marker='o', linewidth=2.5, markersize=6, color='#3498db')
ax.fill_between(monthly_listings.index, monthly_listings.values, alpha=0.3, color='#3498db')
ax.set_xlabel('Month', fontweight='bold')
ax.set_ylabel('Number of Listings', fontweight='bold')
ax.set_title('Marketplace Activity Trend - Monthly Listings', fontweight='bold', fontsize=16, pad=20)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)

# Add trend annotation
avg_monthly = monthly_listings.mean()
ax.axhline(y=avg_monthly, color='red', linestyle='--', linewidth=2, label=f'Average: {avg_monthly:.0f} listings/month')
ax.legend(fontsize=11)

plt.tight_layout()
plt.savefig('charts/04_market_activity_trend.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 5. CUSTOMER ENGAGEMENT: Views Distribution
# ============================================================================
print("Generating Chart 5: Customer Engagement Levels...")
fig, ax = plt.subplots(figsize=(12, 7))
view_ranges = pd.cut(df['views'],
                     bins=[0, 10, 25, 50, 100, float('inf')],
                     labels=['Low\n(1-10)', 'Medium\n(11-25)',
                            'High\n(26-50)', 'Very High\n(51-100)',
                            'Viral\n(>100)'])
view_counts = view_ranges.value_counts().sort_index()
colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#27ae60']
bars = ax.bar(range(len(view_counts)), view_counts.values, color=colors, edgecolor='black', linewidth=1.5)
ax.set_xticks(range(len(view_counts)))
ax.set_xticklabels(view_counts.index, fontweight='bold')
ax.set_ylabel('Number of Listings', fontweight='bold')
ax.set_xlabel('Engagement Level (Views)', fontweight='bold')
ax.set_title('Customer Engagement Distribution', fontweight='bold', fontsize=16, pad=20)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, view_counts.values)):
    percentage = (value / len(df)) * 100
    ax.text(i, value + 30, f'{value:,}\n({percentage:.1f}%)',
            ha='center', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('charts/05_customer_engagement.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 6. PRICING STRATEGY: Price vs Views Relationship
# ============================================================================
print("Generating Chart 6: Price vs Customer Interest...")
fig, ax = plt.subplots(figsize=(12, 7))

# Create price segments for analysis
df['price_segment'] = pd.cut(df['price'],
                             bins=[0, 1000, 5000, 10000, 20000, float('inf')],
                             labels=['<1K', '1K-5K', '5K-10K', '10K-20K', '>20K'])

avg_views_by_price = df.groupby('price_segment')['views'].mean().sort_index()
colors = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#9b59b6']
bars = ax.bar(range(len(avg_views_by_price)), avg_views_by_price.values,
              color=colors, edgecolor='black', linewidth=1.5)
ax.set_xticks(range(len(avg_views_by_price)))
ax.set_xticklabels(avg_views_by_price.index, fontweight='bold')
ax.set_ylabel('Average Views per Listing', fontweight='bold')
ax.set_xlabel('Price Segment (AZN)', fontweight='bold')
ax.set_title('Customer Interest by Price Segment', fontweight='bold', fontsize=16, pad=20)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, avg_views_by_price.values)):
    ax.text(i, value + 0.5, f'{value:.1f} views',
            ha='center', fontweight='bold', fontsize=11)

plt.tight_layout()
plt.savefig('charts/06_price_vs_interest.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 7. GEOGRAPHIC OPPORTUNITIES: City Market Analysis
# ============================================================================
print("Generating Chart 7: Top Cities by Market Size...")
fig, ax = plt.subplots(figsize=(12, 7))
top_cities = df['city_name'].value_counts().head(10)
colors = sns.color_palette("magma", len(top_cities))
bars = ax.barh(range(len(top_cities)), top_cities.values, color=colors)
ax.set_yticks(range(len(top_cities)))
ax.set_yticklabels(top_cities.index)
ax.set_xlabel('Number of Listings', fontweight='bold')
ax.set_ylabel('City', fontweight='bold')
ax.set_title('Top 10 Cities by Marketplace Activity', fontweight='bold', fontsize=16, pad=20)
ax.invert_yaxis()

# Add value labels
for i, (bar, value) in enumerate(zip(bars, top_cities.values)):
    percentage = (value / len(df)) * 100
    ax.text(value + 20, i, f'{value:,} ({percentage:.1f}%)',
            va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/07_top_cities.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 8. PREMIUM SEGMENT ANALYSIS: High-Value Listings
# ============================================================================
print("Generating Chart 8: Premium Market Analysis...")
fig, ax = plt.subplots(figsize=(12, 7))

# Analyze premium listings (>10,000 AZN)
premium_df = df[df['price'] > 10000]
premium_by_region = premium_df['region_name'].value_counts().head(8)

colors = sns.color_palette("rocket_r", len(premium_by_region))
bars = ax.bar(range(len(premium_by_region)), premium_by_region.values,
              color=colors, edgecolor='black', linewidth=1.5)
ax.set_xticks(range(len(premium_by_region)))
ax.set_xticklabels(premium_by_region.index, rotation=45, ha='right', fontweight='bold')
ax.set_ylabel('Number of Premium Listings', fontweight='bold')
ax.set_xlabel('Region', fontweight='bold')
ax.set_title('Premium Segment Distribution (Listings >10,000 AZN)',
             fontweight='bold', fontsize=16, pad=20)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, premium_by_region.values)):
    ax.text(i, value + 1, f'{value}', ha='center', fontweight='bold', fontsize=11)

# Add total premium listings annotation
total_premium = len(premium_df)
total_premium_pct = (total_premium / len(df)) * 100
ax.text(0.98, 0.98, f'Total Premium Listings: {total_premium} ({total_premium_pct:.1f}%)',
        transform=ax.transAxes, ha='right', va='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
        fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/08_premium_segment.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 9. SEASONAL PATTERNS: Quarterly Performance
# ============================================================================
print("Generating Chart 9: Quarterly Market Performance...")
fig, ax = plt.subplots(figsize=(14, 7))

df['quarter'] = df['created_at'].dt.to_period('Q')
quarterly_stats = df.groupby('quarter').agg({
    'id': 'count',
    'price': 'mean'
}).rename(columns={'id': 'listings', 'price': 'avg_price'})

# Create dual axis chart
ax2 = ax.twinx()
quarters_str = [str(q) for q in quarterly_stats.index]

bars = ax.bar(range(len(quarterly_stats)), quarterly_stats['listings'].values,
              alpha=0.7, color='#3498db', label='Number of Listings', edgecolor='black')
line = ax2.plot(range(len(quarterly_stats)), quarterly_stats['avg_price'].values,
                color='#e74c3c', marker='o', linewidth=3, markersize=8,
                label='Average Price')

ax.set_xticks(range(len(quarterly_stats)))
ax.set_xticklabels(quarters_str, rotation=45, ha='right', fontweight='bold')
ax.set_ylabel('Number of Listings', fontweight='bold', color='#3498db')
ax2.set_ylabel('Average Price (AZN)', fontweight='bold', color='#e74c3c')
ax.set_xlabel('Quarter', fontweight='bold')
ax.set_title('Quarterly Market Performance - Volume & Pricing', fontweight='bold', fontsize=16, pad=20)
ax.tick_params(axis='y', labelcolor='#3498db')
ax2.tick_params(axis='y', labelcolor='#e74c3c')

# Add legends
ax.legend(loc='upper left', fontsize=11)
ax2.legend(loc='upper right', fontsize=11)

plt.tight_layout()
plt.savefig('charts/09_quarterly_performance.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 10. COMPETITIVE LANDSCAPE: Market Concentration
# ============================================================================
print("Generating Chart 10: Market Concentration Analysis...")
fig, ax = plt.subplots(figsize=(12, 7))

# Calculate cumulative market share
region_counts = df['region_name'].value_counts()
region_pct = (region_counts / len(df) * 100).values
cumulative_pct = np.cumsum(region_pct)

x = range(len(region_pct))
bars = ax.bar(x, region_pct, alpha=0.7, color='#3498db', label='Individual Share', edgecolor='black')
line = ax.plot(x, cumulative_pct, color='#e74c3c', marker='o', linewidth=3,
               markersize=6, label='Cumulative Share')

ax.axhline(y=80, color='green', linestyle='--', linewidth=2, alpha=0.7, label='80% Market Share')
ax.set_xlabel('Region (Ranked by Market Share)', fontweight='bold')
ax.set_ylabel('Market Share (%)', fontweight='bold')
ax.set_title('Market Concentration - Pareto Analysis', fontweight='bold', fontsize=16, pad=20)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

# Find 80% threshold
threshold_idx = np.where(cumulative_pct >= 80)[0][0] if any(cumulative_pct >= 80) else len(cumulative_pct)
ax.text(threshold_idx + 0.5, 82, f'Top {threshold_idx + 1} regions\nrepresent 80%\nof market',
        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
        fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/10_market_concentration.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n" + "="*80)
print("CHART GENERATION COMPLETED SUCCESSFULLY!")
print("="*80)
print(f"\nAll 10 business insight charts have been saved to the 'charts/' directory")
print("\nGenerated Charts:")
print("  1. Market Share by Region")
print("  2. Price Distribution by Category")
print("  3. Average Price by Region")
print("  4. Market Activity Trend")
print("  5. Customer Engagement Distribution")
print("  6. Price vs Customer Interest")
print("  7. Top Cities by Market Size")
print("  8. Premium Segment Analysis")
print("  9. Quarterly Performance")
print(" 10. Market Concentration Analysis")
print("\n" + "="*80)
