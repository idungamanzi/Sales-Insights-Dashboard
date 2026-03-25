import pandas as pd
file_path = "data/global_ecommerce_sales.csv"
df = pd.read_csv(file_path)

print("Initial shape:", df.shape)
print(df.head())

# 2. STANDARDIZE COLUMN NAMES
df.columns = df.columns.str.lower().str.strip()
print("\nColumns after cleaning:", df.columns)

# 3. DATA CLEANING
# Convert date column
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

# Drop missing critical values
df = df.dropna(subset=['order_date', 'order_id', 'total_amount'])

# Remove duplicates
df = df.drop_duplicates()

# Ensure numeric columns
df['total_amount'] = pd.to_numeric(df['total_amount'], errors='coerce')
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')

# Fill missing values
df['quantity'] = df['quantity'].fillna(1)

# Time features
df['year'] = df['order_date'].dt.year
df['month'] = df['order_date'].dt.month
df['month_name'] = df['order_date'].dt.strftime('%b')

# Rename for consistency
df = df.rename(columns={
    'country': 'region',
    'category': 'product_category'
})

# Segment orders by value tier instead:
df['order_tier'] = pd.cut(
    df['total_amount'],
    bins=[0, 250, 750, 1500, float('inf')],
    labels=['Small', 'Medium', 'Large', 'XL']
)

# Average Order Value
df['avg_order_value'] = df['total_amount'] / df['quantity']

# flag column
max_date = df['order_date'].max()
df['is_partial_month'] = (
    (df['order_date'].dt.year == max_date.year) &
    (df['order_date'].dt.month == max_date.month)
).astype(int)

# print statement to document it:
partial = df[df['is_partial_month'] == 1]
print(f"Partial month: {max_date.strftime('%B %Y')}, "
      f"{len(partial)} orders, "
      f"${partial['total_amount'].sum():,.0f} revenue")

output_path = "data/cleaned_ecommerce_data.csv"
df.to_csv(output_path, index=False)