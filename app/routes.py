# @auth: Lizx
# @date: 2024-10-24 14:00

from flask import Blueprint, request, jsonify, render_template
from model import generate_response

import logging

main = Blueprint('main', __name__)

# 获取日志记录器
logger = logging.getLogger(__name__)


@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@main.route("/api/generate", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    model_type = request.json.get("model_type")  # 获取模型类型
    if not user_input:
        return jsonify({"error": "Message is required"}), 400
    if not model_type:
        return jsonify({"error": "model_type is required"}), 400

    try:
        bot_response = generate_response(user_input, model_type)  # 调用响应
        bot_response = bot_response.replace("ChatGLM-6B", "小U")
        bot_response = bot_response.replace(" ", "")
        length = len(user_input)
        bot_response = bot_response[length:]
        logger.info(f"Generated bot response: {bot_response}")  # 记录模型响应日志
        return jsonify({"response": bot_response})
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")  # 记录错误日志
        return jsonify({"error": str(e)}), 500
