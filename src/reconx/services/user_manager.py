class UserManagerService:
    def __init__(self):
        self.users = []

    def add_user(self, user: dict):
        self.users.append(user)
