

# Reading the file.txt 

with open("file.txt", "r") as file:

    read_file = file.readlines()
    print("read_file", read_file) 
    print("=" * 50)


cleaned_lines = [line for line in read_file if line.strip() != ""]

print("cleaned_lines", cleaned_lines)  

with open("ans.txt", "w") as write_file:
    write_file.writelines(cleaned_lines)


print("✅ Empty lines removed successfully!")
