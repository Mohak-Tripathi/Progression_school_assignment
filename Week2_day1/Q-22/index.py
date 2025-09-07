


def compare_files(first_file, second_file):

    with open(first_file, "r") as file: 
        my_file1 = file.readlines()
    
    with open(second_file, "r") as file: 
        my_file2 = file.readlines()
    
    print(my_file1, my_file2, "consoling")
    max_length = max(len(my_file1), len(my_file2)) 
    print("max_length", max_length)

    for i in range(max_length):
        line1 = my_file1[i].strip() if i < len(my_file1) else "No content"
        line2 = my_file2[i].strip() if i < len(my_file2) else "No content"


        if line1 != line2:
            print(f"Line {i+1} differ")
            print(f"line 1 here is {line1}")
            print(f"line 2 here is {line2}")
            print("-" * 40)




compare_files("file1.txt", "file2.txt")