import itertools
import string

def generate_combinations(length):
    chars = string.ascii_letters + string.digits
    for i in range(1, length + 1):
        for combination in itertools.product(chars, repeat=i):
            yield ''.join(combination)
            
def save_combination_to_file(filename, length):
    with open(filename, 'w') as file:
        for combination in generate_combinations(length):
            file.write(combination + '\n')
            
save_combination_to_file('combination.txt', 8)
