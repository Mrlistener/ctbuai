import concurrent
import logging
import threading
from app.exceptions import ModelLoadingError
from model.model_chatglm_6b import load_chatglm_6b_model, generate_response_chatglm_6b
from model.model_cpm_generate import load_cpm_generate_model, generate_response_generate_model
from model.model_gpt_2_chinese import load_gpt2_chinese_model, generate_response_gpt_2_chinese

# @auth: Lizx
# @date: 2024-10-25

# 获取日志记录器
logger = logging.getLogger(__name__)

model_type = None


def set_model_type(mt):
    global model_type
    model_type = mt


def get_model_type():
    return model_type


def load_model():
    if model_type == "chatglm-6b":
        load_chatglm_6b_model()
    elif model_type == "gpt2":
        load_gpt2_chinese_model()
    elif model_type == "cpm_generate":
        load_cpm_generate_model()
    elif model_type == "All":
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                # 谨慎同时一次性加载三个 很有可能电脑会卡死！！！！！！
                executor.submit(load_chatglm_6b_model()),  # 加载 ChatGLM-6B 模型
                executor.submit(load_gpt2_chinese_model()),  # 加载 GPT-2 模型
                executor.submit(load_cpm_generate_model())  # 加载 CPM Generate 模型
            ]

            # 等待所有模型加载完成
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    logger.info(f"Model loaded: {result}")
                except Exception as e:
                    logger.error(f"Error loading model: {str(e)}")

            # 所有模型加载完毕后，继续执行生成逻辑
            logger.info("All models loaded successfully.")
    else:
        raise ModelLoadingError("error model type")


def generate_response(user_input, user_input_model_type):
    if not user_input_model_type or user_input_model_type == "":
        user_input_model_type = model_type
    if user_input_model_type == "chatglm-6b":
        response = generate_response_chatglm_6b(user_input)
    elif user_input_model_type == "gpt2":
        response = generate_response_gpt_2_chinese(user_input)
    elif user_input_model_type == "cpm_generate":
        response = generate_response_generate_model(user_input)
    else:
        response = "错误的模型类型"
    return response
