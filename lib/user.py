class User():

    def __init__(self, id, name, username, email, password):
        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.password = password
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"User({self.name}, {self.username}, {self.email}, {self.password})"
    
    def is_valid(self):
        if self.name == "" or self.name == None:
            return False
        elif self.username == "" or self.username == None:
            return False
        elif self.email == "" or self.email == None:
            return False
        elif self.password == "" or self.password == None:
            return False
        else:
            return True