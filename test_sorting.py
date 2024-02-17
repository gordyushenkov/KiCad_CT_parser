import re

# Sample list of alphanumeric values
values = ['A10', 'A1', 'A2', 'B2', 'C5', 'D1', 'E20']

# Define a custom sorting key function
# def custom_sort_key(value):
#     # Use regular expression to split the value into non-digits and digits parts
#     parts = re.split(r'(\d+)', value)
#     # Convert the digits part to an integer for sorting
#     return int(parts[1])


def custom_sort_key(value):
    # Use regular expression to split the value into non-digits and digits parts
    parts = re.split(r'(\d+)', value)
    # Convert the digits part to an integer for sorting
    return (parts[0], int(parts[1]))

# Sort the list using the custom sorting key function
sorted_values = sorted(values, key=custom_sort_key)

# Print the sorted list
print(sorted_values)