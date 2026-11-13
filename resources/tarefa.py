from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.tarefa import TaskModel
from models.user import UserModel


class Tarefas(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("titulo", type=str, required=True, help="Título obrigatório")
    argumentos.add_argument("descricao", type=str)
    argumentos.add_argument("estado", type=str)

    # Listar tarefas.
    @jwt_required()
    def get(self):
        x = int(get_jwt_identity())
        user = UserModel.query.filter_by(id=x).first()

        if user.tipo == "admin":
            tarefas = TaskModel.query.all()
        else:
            tarefas = TaskModel.query.filter_by(utilizador_id=x).all()

        return {"tarefas": [tarefa.json() for tarefa in tarefas]}, 200

    # Inserir uma tarefa.
    @jwt_required()
    def post(self):
        dados = Tarefas.argumentos.parse_args()
        x = int(get_jwt_identity())

        if dados["estado"] is None:
            dados["estado"] = "Pendente"
        if dados["descricao"] is None:
            dados["descricao"] = ""
        if dados["estado"] not in ["Pendente", "Em curso", "Concluída"]:
            return {"message": "Invalid state"}, 400

        nova_tarefa = TaskModel(
            dados["titulo"], dados["descricao"], dados["estado"], x
        )
        nova_tarefa.save_task()
        return nova_tarefa.json(), 201


class Tarefa(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("titulo", type=str)
    argumentos.add_argument("descricao", type=str)
    argumentos.add_argument("estado", type=str)

    # Consultar, atualizar ou eliminar uma tarefa específica.
    @jwt_required()
    def get(self, id_tarefa):
        x = int(get_jwt_identity())
        user = UserModel.query.filter_by(id=x).first()
        tarefa_encontrada = TaskModel.find_task(id_tarefa)

        if tarefa_encontrada:
            if user.tipo == "admin" or tarefa_encontrada.utilizador_id == x:
                return tarefa_encontrada.json(), 200
            return {"message": "You do not have permission"}, 403
        return {"message": "Task not found"}, 404

    @jwt_required()
    def put(self, id_tarefa):
        dados = Tarefa.argumentos.parse_args()
        x = int(get_jwt_identity())
        user = UserModel.query.filter_by(id=x).first()
        tarefa_encontrada = TaskModel.find_task(id_tarefa)

        if tarefa_encontrada:
            if user.tipo != "admin" and tarefa_encontrada.utilizador_id != x:
                return {"message": "You do not have permission"}, 403

            titulo = dados["titulo"] or tarefa_encontrada.titulo
            if dados["descricao"] is None:
                descricao = tarefa_encontrada.descricao
            else:
                descricao = dados["descricao"]
            estado = dados["estado"] or tarefa_encontrada.estado

            if estado not in ["Pendente", "Em curso", "Concluída"]:
                return {"message": "Invalid state"}, 400

            tarefa_encontrada.update_task(titulo, descricao, estado)
            return tarefa_encontrada.json(), 200

        return {"message": "Task not found"}, 404

    @jwt_required()
    def delete(self, id_tarefa):
        x = int(get_jwt_identity())
        user = UserModel.query.filter_by(id=x).first()
        tarefa_encontrada = TaskModel.find_task(id_tarefa)

        if tarefa_encontrada:
            if user.tipo != "admin" and tarefa_encontrada.utilizador_id != x:
                return {"message": "You do not have permission"}, 403

            tarefa_encontrada.delete_task()
            return {"message": "Task deleted"}, 200

        return {"message": "Task not found"}, 404
