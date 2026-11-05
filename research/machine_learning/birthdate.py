from datetime import datetime

def calculate_age(birthdate_str):
    try:
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    print(f"You are {age} years old.")

if __name__ == "__main__":
    user_input = input("Enter your birthdate (YYYY-MM-DD): ")
    calculate_age(user_input)