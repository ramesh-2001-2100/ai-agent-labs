try:
    first_number = int(input("Enter the first number: "))
    second_number = int(input("Enter the second number: "))
    result = first_number / second_number
    print(f"The result of dividing {first_number} by {second_number} is: {result}")
except Exception:
    print("Error: There is a problem with the program. Please check your input and try again.")
