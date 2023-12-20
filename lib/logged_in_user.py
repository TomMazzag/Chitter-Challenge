class User_logged_in():

    def __init__(self, id, name, username, email, password):
        self.id = id
        self.name = name
        self.username = username
        self.email = email
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__