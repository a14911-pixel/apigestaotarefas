from con_sql import bd


class UserModel(bd.Model):
    __tablename__ = "utilizadores"

    id = bd.Column(bd.Integer, primary_key=True)
    username = bd.Column(bd.String(40), unique=True, nullable=False)
    email = bd.Column(bd.String(120), unique=True, nullable=False)
    password = bd.Column(bd.String(255), nullable=False)
    tipo = bd.Column(bd.String(20), default="utilizador", nullable=False)

    # Um utilizador pode ter várias tarefas
    tarefas = bd.relationship("TaskModel", back_populates="utilizador")

    # Construtor da classe
    def __init__(self, username, email, password, tipo="utilizador"):
        self.username = username
        self.email = email
        self.password = password
        self.tipo = tipo

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "tipo": self.tipo,
        }

    @classmethod
    def find_user(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    def save_user(self):
        bd.session.add(self)
        bd.session.commit()
