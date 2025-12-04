import string
import random


def replace_alphabets(string_list):
    new_string_list = []
    for row in string_list:
        new_row = ""
        for char in row:
            if char.isalpha():
                new_row += random.choice(string.ascii_uppercase)
            else:
                new_row += char
        new_string_list.append(new_row) 
    return new_string_list


def create_store_map(first_floor, height):
    store_map = []
    for _ in range(height):
        floor = replace_alphabets(first_floor)
        store_map.append(floor)
    return store_map
