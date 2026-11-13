from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from con_sql import bd
from models.tarefa import TaskModel
from models.user import UserModel
from resources.tarefa import Tarefas, Tarefa
from resources.user import UserRegister, UserLogin

# Variável que representa a aplicação.
app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

# Configurações iguais ao exemplo das aulas.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tarefas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "a_minha_palavra_secreta_para_a_api_de_tarefas"

# Rotas da API.
api.add_resource(UserRegister, "/registo")
api.add_resource(UserLogin, "/login")
api.add_resource(Tarefas, "/tarefas")
api.add_resource(Tarefa, "/tarefas/<int:id_tarefa>")

# Ligar a base de dados à aplicação.
bd.init_app(app)

# Criar as tabelas e o admin, caso ainda não existam.
with app.app_context():
    bd.create_all()

    admin_encontrado = UserModel.find_user("admin@empresa.local")
    if admin_encontrado is None:
        novo_admin = UserModel(
            "admin", "admin@empresa.local", "Admin123!", "admin"
        )
        novo_admin.save_user()

if __name__ == "__main__":
    app.run(debug=True)