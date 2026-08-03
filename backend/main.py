"""Punto de entrada principal de la aplicación B.A.M.

Este módulo NO debe contener lógica de negocio. Su única responsabilidad
es: crear la app de Flask, cargar la configuración inicial (core/) y
registrar las rutas expuestas por la capa de presentación (api/).
"""

from flask import Flask, g
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.api.v1.routes import register_routes
from app.core.config import settings
from app.core.database import SessionLocal


def create_app() -> Flask:
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = settings.JWT_ACCESS_TOKEN_EXPIRES

    JWTManager(app)
    CORS(app, resources={r"/api/*": {"origins": settings.CORS_ORIGINS}}, supports_credentials=True)

    register_routes(app)

    @app.before_request
    def before_request():
        g.db = SessionLocal()

    @app.teardown_appcontext
    def teardown_appcontext(exception=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
