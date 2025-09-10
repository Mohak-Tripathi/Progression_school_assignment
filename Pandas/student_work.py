import pandas as pd

# Load the CSV
student_data = pd.read_csv('./student_data.csv')

# Preview the top 5 rows
print(student_data.head())
print("$"*60)
print(student_data.head(3))
print("$"*60)
print(student_data.tail(3))
print("$"*60)

# print("Sampleing chapter")
# print(student_data.sample())        # Returns 1 random row
# print(student_data.sample(n=5))     # Returns 5 random rows
# print(student_data.sample(frac=0.1))  # Returns 10% of total rows



print(student_data.columns)
print(student_data.columns.to_list())


# View index (row labels)
print(student_data.index)

# Convert index to list
print(student_data.index.to_list())

print(student_data.shape, "shape")
print(student_data.size, "size")
print(student_data.info(), "info")
print(student_data.describe(), "describe")



print("#" * 100)
print(student_data.loc[0, 'Age'])


print(student_data.loc[[0, 7, 10], ['Age', 'Height', 'Weight']])

print(# Rows 0 to 5 and columns 'Age', 'Height'
student_data.loc[0:5, ['Age', 'Height']])



print(student_data.loc[0:5, ["Age"]])

print(student_data.loc[[0, 7, 10], ['Age', 'Height', 'Weight']])



print(# From beginning to row 20
student_data.loc[:20])


print(student_data.iloc[0:10], "tension")

print(student_data.iloc[0:10, 1:5])


print("filteration now")

tall_students = student_data.loc[student_data['Height'] > 1.75]
print(tall_students)


smart_and_studious = student_data[
    (student_data['CGPA'] > 9.0) & (student_data['Study_Hours'] > 4)
]
print(smart_and_studious, "SS")


student_data.loc[1, 'Age'] = 63
print(student_data.head())



student_data.loc[:, 'Participation_Clubs'] = 'Yes'
print(student_data.head())

# Change CGPA for 5th student to 10.0
student_data.loc[4, 'CGPA'] = 10.0

# Set all 'Department' values to 'ECE'
student_data.loc[:, 'Department'] = 'ECE'



student_data.to_csv("student_dataset_modified.csv", index=False)
