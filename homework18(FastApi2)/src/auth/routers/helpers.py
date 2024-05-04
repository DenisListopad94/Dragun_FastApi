import random
from typing import List



def generate_users(num_users: int) -> List:
    users = []
    for i in range(1, num_users + 1):
        user = {
            "id": i,
            "first_name": f"some_name_{i}",
            "last_name": f"some_name_{i}",
            "age": random.randint(18, 60),
            "email": f"some_email_{i}@example.com",
            "photo": f"/img/users/{random.randint(1, 3)}.webp"
        }
        users.append(user)
    return users
