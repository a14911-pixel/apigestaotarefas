from con_sql import bd


class TaskModel(bd.Model):
    __tablename__ = "tarefas"

    id = bd.Column(bd.Integer, primary_key=True)
    titulo = bd.Column(bd.String(100), nullable=False)
    descricao = bd.Column(bd.Text)
    estado = bd.Column(bd.String(30), default="Pendente", nullable=False)
    utilizador_id = bd.Column(
        bd.Integer, bd.ForeignKey("utilizadores.id"), nullable=False
    )

    # Cada tarefa pertence a um utilizador.
    utilizador = bd.relationship("UserModel", back_populates="tarefas")

    def __init__(self, titulo, descricao, estado, utilizador_id):
        self.titulo = titulo
        self.descricao = descricao
        self.estado = estado
        self.utilizador_id = utilizador_id

    def json(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "estado": self.estado,
            "utilizador_id": self.utilizador_id,
        }

    @classmethod
    def find_task(cls, task_id):
        return cls.query.filter_by(id=task_id).first()

    def save_task(self):
        bd.session.add(self)
        bd.session.commit()

    def update_task(self, titulo, descricao, estado):
        self.titulo = titulo
        self.descricao = descricao
        self.estado = estado
        bd.session.commit()

    def delete_task(self):
        bd.session.delete(self)
        bd.session.commit()