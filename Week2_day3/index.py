import pandas as pd

# Load the CSV file
df = pd.read_csv("ecommerce_sales.csv")

# Preview first 5 rows
print("First 5 rows:")
print(df.head(), "\n")

# Preview last 5 rows
print("Last 5 rows:")
print(df.tail(), "\n")

# Print column names and data types
print("Column Names and Data Types:")
print(df.dtypes, "\n")

# Show shape (rows, columns)
print("Shape of DataFrame:", df.shape, "\n")

# Check for null values
print("Null values in each column:")
print(df.isnull().sum(), "\n")

# Handle null values (example strategy)
# Fill missing numeric values with 0, string values with 'Unknown'
df = df.fillna({
    "Order ID": "Unknown",
    "Customer Name": "Unknown",
    "Product": "Unknown",
    "Category": "Unknown",
    "Quantity Ordered": 0,
    "Price Each": 0.0,
    "Order Date": "1900-01-01",
    "Purchase Address": "Unknown"
})

# Confirm no nulls left
print("Null values after handling:")
print(df.isnull().sum())







# 🔹 1. Remove rows with ANY null or missing data
df = df.dropna(how='any')

# 🔹 2. Convert Order Date to datetime format
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')

# Drop rows where conversion failed (invalid dates)
df = df.dropna(subset=['Order Date'])

# 🔹 3. Ensure Quantity Ordered and Price Each are numeric
df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'], errors='coerce')
df['Price Each'] = pd.to_numeric(df['Price Each'], errors='coerce')

# Drop rows where numeric conversion failed
df = df.dropna(subset=['Quantity Ordered', 'Price Each'])

# 🔹 4. Create new column "Total Price"
df['Total Price'] = df['Quantity Ordered'] * df['Price Each']

# ✅ Final check
print("Cleaned DataFrame:")
print(df.head())

print("\nData types after cleaning:")
print(df.dtypes)

print("\nShape after cleaning:", df.shape)


# 🔹 1. Total sales amount
total_sales = df['Total Price'].sum()
print("Total Sales Amount: $", round(total_sales, 2))

# 🔹 2. Average purchase amount
avg_purchase = df['Total Price'].mean()
print("Average Purchase Amount: $", round(avg_purchase, 2))

# 🔹 3. How many unique products were sold?
unique_products = df['Product'].nunique()
print("Unique Products Sold:", unique_products)

# 🔹 4. Count the number of orders per product
orders_per_product = df['Product'].value_counts()
print("\nOrders per Product:")
print(orders_per_product)









import matplotlib.pyplot as plt

# Load dataset (assuming already cleaned earlier)


# Ensure proper datatypes
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'], errors='coerce')
df['Price Each'] = pd.to_numeric(df['Price Each'], errors='coerce')
df = df.dropna(subset=['Order Date', 'Quantity Ordered', 'Price Each'])
df['Total Price'] = df['Quantity Ordered'] * df['Price Each']

# 🔹 1. Extract City from Purchase Address
# Assuming format: "123 Main St, New York, NY 10001"
df['City'] = df['Purchase Address'].apply(lambda x: x.split(',')[1].strip())

# 🔹 2. Find city with most number of purchases
city_counts = df['City'].value_counts()
print("🏙️ City with the most purchases:", city_counts.idxmax())
print("\nPurchases per city:\n", city_counts)

# 🔹 3. Group total sales by city
sales_by_city = df.groupby('City')['Total Price'].sum().sort_values(ascending=False)
print("\n💰 Total Sales by City:\n", sales_by_city)

# 🔹 4. Plot bar chart
plt.figure(figsize=(10,6))
sales_by_city.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title("Total Sales by City")
plt.xlabel("City")
plt.ylabel("Total Sales ($)")
plt.xticks(rotation=45)
plt.show()