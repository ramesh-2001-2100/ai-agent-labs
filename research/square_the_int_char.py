def sum_of_square_digits(n):
    # The input 'n' is a positive integer.
    # Convert the integer 'n' to a string to iterate over the digits.
    # For each digit, convert it back to integer and calculate its square.
    # Add the square to a running total.
    # Return the total.

    n = int(input())
    string_of_n = str(n)
    result = 0
    for char in string_of_n:
        integer_char = int(char)
        result += integer_char ** 2
    
    print(result)

sum_of_square_digits(720)

