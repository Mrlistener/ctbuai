import logging
import os
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm
import time
import torch

# @auth: Lizx
# @date: 2024-10-25

# 获取日志记录器
logger = logging.getLogger(__name__)

# 全局变量
model_chatglm_6b = None
tokenizer_chatglm_6b = None


# 加载 chatglm_6b
# 模型路径：resource/chatglm_6b
# 模型大小：12.4GB
# 模型介绍：清华大学开源中文语料训练，支持中文输入，支持多轮对话。
# 模型来源：https://huggingface.co/THUDM/chatglm-6b
def load_chatglm_6b_model():
    global model_chatglm_6b, tokenizer_chatglm_6b
    if model_chatglm_6b is None or tokenizer_chatglm_6b is None:
        # 获取当前工程的根目录
        project_root = os.path.dirname(os.path.abspath(__file__))
        # 获取模型路径
        model_path = os.path.join(project_root, "resource", "chatglm-6b")
        absolute_model_path = os.path.abspath(model_path)
        logger.info(f"chatglm-6b Model path: {absolute_model_path}")
        # 加载 ChatGLM-6B 模型和分词器，记录时间和进度条
        try:
            start_time = time.time()
            logger.info("Loading ChatGLM-6B model_chatglm_6b and tokenizer_chatglm_6b...")
            # 使用进度条显示加载进度
            with tqdm(total=100, desc="Loading Tokenizer and Model",
                      bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
                if torch.cuda.is_available():
                    tokenizer_chatglm_6b = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True,
                                                                         revision="main")
                    pbar.update(50)  # 更新进度条一半，因为分词器加载完成
                    # 使用GPU
                    model_chatglm_6b = AutoModel.from_pretrained(model_path, trust_remote_code=True,
                                                                 revision="main").cuda()
                    pbar.update(50)  # 模型加载完成
                else:
                    tokenizer_chatglm_6b = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True,
                                                                         revision="main")
                    pbar.update(50)  # 更新进度条一半，因为分词器加载完成
                    # 使用CPU
                    model_chatglm_6b = AutoModel.from_pretrained(model_path, trust_remote_code=True,
                                                                 revision="main").float()
                    pbar.update(50)  # 模型加载完成
            end_time = time.time()
            logger.info(
                f"Model_chatglm_6b and tokenizer_chatglm_6b loaded successfully in {end_time - start_time:.2f} seconds.")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise e  # 确保错误抛出，应用停止
        return "success"


# 对话生成函数
def generate_response_chatglm_6b(user_input):
    load_chatglm_6b_model()
    try:
        logger.info(f"Received user input: {user_input}")

        # 将输入转化为模型所需的格式
        inputs = tokenizer_chatglm_6b(user_input, return_tensors="pt")
        logger.debug(f"Tokenized input: {inputs}")

        # 使用模型生成对话响应
        outputs = model_chatglm_6b.generate(**inputs, max_length=2024, do_sample=True, top_p=0.7, temperature=0.5)
        logger.debug(f"Model output: {outputs}")

        # 解码生成的结果
        response = tokenizer_chatglm_6b.decode(outputs[0], skip_special_tokens=True)
        logger.info(f"Generated response: {response}")

        return response
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return "抱歉，我无法处理你的请求。"
