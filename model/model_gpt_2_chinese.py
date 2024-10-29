import logging
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm
import time
import torch

# @auth: Lizx
# @date: 2024-10-25

# 获取日志记录器
logger = logging.getLogger(__name__)

model_gpt_2_chinese = None
tokenizer_gpt_2_chinese = None


# 加载 GPT-2 中文模型和分词器
# 模型路径：resource/gpt-2-chinese
# 模型大小：1.5GB
# 模型介绍：GPT-2 中文模型，基于 GPT-2 模型，使用中文语料训练，支持中文输入，支持多轮对话。
# 模型来源：https://huggingface.co/THUDM/gpt-2-chinese
def load_gpt2_chinese_model():
    global model_gpt_2_chinese, tokenizer_gpt_2_chinese  # 确保全局变量可用
    if model_gpt_2_chinese is None or tokenizer_gpt_2_chinese is None:
        # 获取当前工程的根目录
        project_root = os.path.dirname(os.path.abspath(__file__))
        # 获取模型路径
        model_path = os.path.join(project_root, "resource", "gpt-2-chinese")
        absolute_model_path = os.path.abspath(model_path)
        logger.info(f"gpt-2-chinese Model path: {absolute_model_path}")
        # 加载 GPT-2 Chinese 模型和分词器，记录时间和进度条
        try:
            start_time = time.time()
            logger.info("Loading GPT-2 Chinese model_gpt_2_chinese and tokenizer_gpt_2_chinese...")
            # 使用进度条显示加载进度
            with tqdm(total=100, desc="Loading Tokenizer and Model",
                      bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
                # 加载分词器
                tokenizer_gpt_2_chinese = AutoTokenizer.from_pretrained(model_path)
                pbar.update(50)  # 分词器加载完成

                # 根据设备（GPU 或 CPU）加载模型
                if torch.cuda.is_available():
                    model_gpt_2_chinese = AutoModelForCausalLM.from_pretrained(model_path).half().cuda()  # 使用 GPU
                else:
                    model_gpt_2_chinese = AutoModelForCausalLM.from_pretrained(model_path).float()  # 使用 CPU
                pbar.update(50)  # 模型加载完成

            end_time = time.time()
            logger.info(
                f"GPT-2 Chinese model_gpt_2_chinese and tokenizer_gpt_2_chinese loaded successfully in {end_time - start_time:.2f} seconds.")
        except Exception as e:
            logger.error(f"Error loading GPT-2 Chinese model: {str(e)}")
            raise e  # 确保错误抛出，应用停止
        return "success"


def generate_response_gpt_2_chinese(user_input):
    try:
        logger.info(f"Received user input: {user_input}")

        # 将输入转化为模型所需的格式
        # 添加 padding 和 truncation 以处理不同长度的输入
        inputs = tokenizer_gpt_2_chinese(user_input, return_tensors="pt", padding=True, truncation=True).to(
            model_gpt_2_chinese.device)
        logger.debug(f"Tokenized input: {inputs}")

        # 使用模型生成对话响应
        outputs = model_gpt_2_chinese.generate(
            inputs["input_ids"],  # 将输入 ID 传递给模型
            max_length=100,  # 最大输出长度
            do_sample=True,  # 允许生成的文本带有一定随机性
            top_p=0.7,  # nucleus sampling，控制生成的多样性
            temperature=0.9,  # 温度系数，值越高生成的文本越随机
            num_return_sequences=1  # 只返回一个生成结果
        )
        logger.debug(f"Model output: {outputs}")

        # 解码生成的结果，将 token 转化为字符串
        response = tokenizer_gpt_2_chinese.decode(outputs[0], skip_special_tokens=True)
        logger.info(f"Generated response: {response}")

        return response
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return "抱歉，我无法处理您的请求。"
