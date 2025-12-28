import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('register_numbers.csv')

# Basic dataset information
print("=" * 80)
print("DATASET OVERVIEW")
print("=" * 80)
print(f"\nTotal Records: {len(df):,}")
print(f"Total Columns: {len(df.columns)}")
print(f"\nColumn Names and Types:")
print(df.dtypes)

print("\n" + "=" * 80)
print("DATA SUMMARY")
print("=" * 80)
print(df.describe())

print("\n" + "=" * 80)
print("MISSING VALUES")
print("=" * 80)
print(df.isnull().sum())

print("\n" + "=" * 80)
print("PRICE STATISTICS")
print("=" * 80)
print(f"Min Price: {df['price'].min():,}")
print(f"Max Price: {df['price'].max():,}")
print(f"Mean Price: {df['price'].mean():,.2f}")
print(f"Median Price: {df['price'].median():,.2f}")

print("\n" + "=" * 80)
print("REGIONAL DISTRIBUTION")
print("=" * 80)
print(df['region_name'].value_counts().head(10))

print("\n" + "=" * 80)
print("CITY DISTRIBUTION")
print("=" * 80)
print(df['city_name'].value_counts().head(10))

print("\n" + "=" * 80)
print("VIEWS STATISTICS")
print("=" * 80)
print(f"Min Views: {df['views'].min()}")
print(f"Max Views: {df['views'].max()}")
print(f"Mean Views: {df['views'].mean():.2f}")
print(f"Median Views: {df['views'].median():.2f}")

print("\n" + "=" * 80)
print("PRICE RANGES")
print("=" * 80)
price_ranges = pd.cut(df['price'], bins=[0, 1000, 5000, 10000, 20000, float('inf')],
                      labels=['<1K', '1K-5K', '5K-10K', '10K-20K', '>20K'])
print(price_ranges.value_counts().sort_index())

print("\n" + "=" * 80)
print("DATE RANGE")
print("=" * 80)
df['created_at'] = pd.to_datetime(df['created_at'])
print(f"Earliest Listing: {df['created_at'].min()}")
print(f"Latest Listing: {df['created_at'].max()}")

print("\n" + "=" * 80)
print("SAMPLE RECORDS")
print("=" * 80)
print(df.head(10))
