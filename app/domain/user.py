class User:
    def __init__(self, id: int, name: str | None, email: str | None, avatar_url: str | None):
        self.id = id
        self.name = name
        self.email = email
        self.avatar_url = avatar_url
