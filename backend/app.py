from flask import Flask, jsonify
from flask_cors import CORS

from routes.memoria_routes import memoria_bp


app = Flask(__name__)
CORS(app)

# Registrar las rutas del simulador
app.register_blueprint(memoria_bp)


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensaje": "API del Simulador de Gestion de Memoria",
        "estado": "Servidor funcionando correctamente"
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)