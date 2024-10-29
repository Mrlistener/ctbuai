# @auth: Lizx
# @date: 2024-10-25

import logging
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm
import time
import torch

model_cpm_generate = None
tokenizer_cpm_generate = None

# 日志记录器
logger = logging.getLogger(__name__)

def load_cpm_generate_model():
    global model_cpm_generate, tokenizer_cpm_generate
    if model_cpm_generate is None or tokenizer_cpm_generate is None:
        # 获取当前工程的根目录
        project_root = os.path.dirname(os.path.abspath(__file__))
        # 获取模型路径
        model_path = os.path.join(project_root, "resource", "cpm-generate")
        absolute_model_path = os.path.abspath(model_path)
        logger.info(f"cpm-generate Model path: {absolute_model_path}")
        try:
            start_time = time.time()
            logger.info("Loading CPM-Generate model and tokenizer...")

            with tqdm(total=100, desc="Loading Tokenizer and Model",
                      bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
                # 加载分词器
                tokenizer_cpm_generate = AutoTokenizer.from_pretrained(model_path)
                pbar.update(50)  # 更新进度条，表示分词器加载完成

                # 根据设备选择 CPU 或 GPU 加载模型
                if torch.cuda.is_available():
                    model_cpm_generate = AutoModelForCausalLM.from_pretrained(model_path).half().cuda()
                else:
                    model_cpm_generate = AutoModelForCausalLM.from_pretrained(model_path).float()
                pbar.update(50)  # 更新进度条，表示模型加载完成

            end_time = time.time()
            logger.info(f"CPM-Generate model and tokenizer loaded successfully in {end_time - start_time:.2f} seconds.")
        except Exception as e:
            logger.error(f"Error loading CPM-Generate model: {str(e)}")
            raise e
        return "success"


def generate_response_generate_model(user_input):
    try:
        load_cpm_generate_model()
        logger.info(f"Received user input: {user_input}")
        # 将输入文本转换为模型输入格式
        inputs = tokenizer_cpm_generate(user_input, return_tensors="pt", padding=True, truncation=True).to(model_cpm_generate.device)
        logger.debug(f"Tokenized input: {inputs}")

        # 使用模型生成回复
        outputs = model_cpm_generate.generate(
            inputs["input_ids"],
            max_length=100,  # 生成回复的最大长度
            do_sample=True,  # 随机采样以增加生成多样性
            top_p=0.7,  # Nucleus sampling 参数
            temperature=0.9,  # 控制生成的随机性
            num_return_sequences=1  # 生成一个回复
        )
        logger.debug(f"Model output: {outputs}")

        # 解码生成的文本
        response = tokenizer_cpm_generate.decode(outputs[0], skip_special_tokens=True)
        logger.info(f"Generated response: {response}")

        return response
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return "抱歉，我无法处理您的请求。"