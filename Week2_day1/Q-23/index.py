# Q23: Create Dictionary from Word File with Word Lengths

def create_word_length_dict(filename):
    word_dict = {}
    with open(filename, "r") as f:
        for line in f:
            word = line.strip()  # remove newline/spaces
            if word:  # skip empty lines
                word_dict[word] = len(word)
    return word_dict


# Example usage
file_name = "dictionary.txt"   # replace with your file path
word_lengths = create_word_length_dict(file_name)

print(word_lengths, "word-length")

# Print first 10 entries as a sample
# for word, length in list(word_lengths.items())[:10]:
#     print(f"{word}: {length}")
