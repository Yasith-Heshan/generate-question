from enum import Enum

class TableName(Enum):
    QUESTIONS = "questions"
    # Add more table names as needed

# Example usage:
# TableName.USERS.value  # returns "users"