from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, id, username, es_admin=False):
        self.id = str(id)
        self.username = username
        self.es_admin = es_admin
