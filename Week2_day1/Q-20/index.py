

def word_count(file_name):
    with open(file_name, "r") as file:
        content = file.read() 

        total_lines = content.splitlines()
        print("*" * 50)
        print(total_lines, "total_lines")
        print("*" * 50)

        print("#" * 50)
        total_words = content.split()
        print("total_word", total_words)
        print("#" * 50)
        
        total_character = len(content)

        return (len(total_lines), len(total_words), total_character)

file_name = "file.txt"
res_lines, res_words, res_char = word_count(file_name)

print(res_lines, res_words, res_char)