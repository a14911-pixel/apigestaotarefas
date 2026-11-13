from flask_restful import Resource, reqparse
from hmac import compare_digest
from flask_jwt_extended import create_access_token
from models.user import UserModel


class UserRegister(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("username", type=str, required=True, help="Username obrigatório")
    argumentos.add_argument("email", type=str, required=True, help="Email obrigatório")
    argumentos.add_argument("password", type=str, required=True, help="Password obrigatória")

    def post(self):
        dados = UserRegister.argumentos.parse_args()
        email = dados["email"].lower()
        user_encontrado = UserModel.find_user(email)

        if user_encontrado:
            return {"message": "Email already exists"}, 400
        user_encontrado = UserModel.query.filter_by(
            username=dados["username"]
        ).first()
        if user_encontrado:
            return {"message": "Username already exists"}, 400

        novo_user = UserModel(
            dados["username"], email, dados["password"], "utilizador"
        )
        novo_user.save_user()
        return novo_user.json(), 201


class UserLogin(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("email", type=str, required=True, help="Email obrigatório")
    argumentos.add_argument("password", type=str, required=True, help="Password obrigatória")

    def post(self):
        dados = UserLogin.argumentos.parse_args()
        user = UserModel.find_user(dados["email"].lower())

        if user and compare_digest(user.password, dados["password"]):
            # Guardar o ID numérico no token, para o podermos ler com int().
            token = create_access_token(identity=str(user.id))
            return {"access_token": token}, 200

        return {"message": "Email or password invalid"}, 401
