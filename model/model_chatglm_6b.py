import logging
import os
from transformers import AutoTokenizer, AutoModel
import numpy as np
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
            logger.info("Loading ChatGLM-6B model and tokenizer...")

            # 使用进度条显示加载进度
            with tqdm(total=100, desc="Loading Tokenizer and Model",
                      bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
                # 加载分词器
                tokenizer_chatglm_6b = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True,
                                                                     revision="main")
                pbar.update(50)  # 更新进度条到一半

                # 加载模型，基于是否有 GPU 可用
                model_loading_args = {"trust_remote_code": True, "revision": "main"}
                if torch.cuda.is_available():
                    model_chatglm_6b = AutoModel.from_pretrained(model_path, **model_loading_args).cuda()
                else:
                    model_chatglm_6b = AutoModel.from_pretrained(model_path, **model_loading_args).float()
                pbar.update(50)  # 更新进度条到完成
            end_time = time.time()
            logger.info(f"Model and tokenizer loaded successfully in {end_time - start_time:.2f} seconds.")
        except AttributeError as e:
            logger.error("Tokenizer attribute error. Check 'sp_tokenizer' attribute compatibility.")
            raise AttributeError("Check compatibility of 'sp_tokenizer' attribute in tokenizer.")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise e  # 确保错误抛出，应用停止
        return "success"

# 对话生成函数
def generate_response_chatglm_6b(user_input):
    load_chatglm_6b_model()
    try:
        logger.info(f"Received user input: {user_input}")

        # 将输入转化为模型所需的格式，确保添加 attention_mask
        inputs = tokenizer_chatglm_6b(user_input, return_tensors="pt", padding=True)

        # 确保 attention_mask 存在并优化为单一 tensor 格式
        if "attention_mask" not in inputs:
            inputs["attention_mask"] = torch.ones(inputs["input_ids"].shape, dtype=torch.bool)

        # 转换 attention_mask 为布尔类型
        inputs["attention_mask"] = inputs["attention_mask"].to(torch.bool)

        logger.debug(f"Tokenized input: {inputs}")

        # 使用模型生成对话响应
        outputs = model_chatglm_6b.generate(**inputs, max_length=512, do_sample=True, top_p=0.7, temperature=0.5)
        logger.debug(f"Model output: {outputs}")

        # 解码生成的结果
        response = tokenizer_chatglm_6b.decode(outputs[0], skip_special_tokens=True)
        logger.info(f"Generated response: {response}")

        return response
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return "抱歉，我无法处理你的请求。"