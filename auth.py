import pandas as pd

USER_FILE = "data/users.csv"

def authenticate(username, password):
    users = pd.read_csv(USER_FILE)

    user = users[
        (users["username"] == username) &
        (users["password"] == password)
    ]

    if not user.empty:
        return {
            "user_id": user.iloc[0]["user_id"],
            "name": user.iloc[0]["name"],
            "role": user.iloc[0]["role"]
        }

    return None