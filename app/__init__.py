# @auth: Lizx
# @date: 2024-10-24 14:00

from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes import main
    app.register_blueprint(main)

    return app