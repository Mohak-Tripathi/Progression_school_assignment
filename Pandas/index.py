import pandas as pd
# data = [10, 22, 33, 44, 54]
# index = ['a', 'b', 'c', 'd', 'e']


# series = pd.Series(data, index=index)
# print(series)
# print(series.sum(), series.mean(), series.max(), series.min(), series.std())





# Create a simple 2D list
data = [
    [1, 2, 3],
    [4, 5, 6]
]

# Create DataFrame from the list
df = pd.DataFrame(data)

# Display the DataFrame
print(df)




print("#" * 50)

# Create a simple 2D list
data = [
    [1, 2, 3],
    [4, 5, 6]
]

columns = ["c0", "c1" , "c2"]
index= ["r0", "r1"]

# Create DataFrame from the list
df = pd.DataFrame(data, columns=columns, index=index)

# Display the DataFrame
print(df)

print("def.shape", df.shape)
print("def.columns", df.columns)
print("def.index", df.index)
print("def.info", df.info())
print("def.describe", df.describe())
print("def.head", df.head())
print("def.tail", df.tail())
print(df.loc["R1"] )

