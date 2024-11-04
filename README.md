
---

# CTBU-AI

## 简介

CTBU-AI 项目使用 Flask、PyTorch、SentencePiece 等库进行自然语言处理和对话生成任务。项目依赖通过 `conda` 环境管理，以确保开发和生产环境的一致性。本项目提供了一个简洁的 Flask 应用，加载预训练的 ChatGLM-6B 模型用于对话生成。

## 项目结构

项目文件和目录结构如下：

```
CTBU-AI/
├── app/
│   ├── __init__.py            # Flask 应用的初始化
│   ├── routes.py              # 定义路由和视图函数
├── model/
│   ├── __init__.py            # 模型模块初始化
│   ├── model.py               # 模型入口
│   ├── model_chatglm_6b.py    # chatglm_6b    模型加载与回复生成
│   ├── model_cpm_generate.py  # cpm_generate  模型加载与回复生成
│   ├── model_gpt_2_chinese.py # gpt_2_chinese 模型加载与回复生成
├── templates/
│   ├── index.html             # Flask 应用的前端页面模板
├── logs/                      # 日志文件存储目录
│   └── app.log                # 日志文件
├── environment.yml            # Conda 环境配置文件
├── main.py                     # 启动 Flask 应用的入口文件
└── README.md                  # 项目说明文档
```

## 环境设置

本项目依赖多个 Python 包和库，为确保一致的开发环境，建议使用 `conda` 管理所有依赖项。请按照以下步骤设置开发环境。请根据需要选择适合你的环境文件。

### 1. 安装 Miniconda 或 Anaconda

如果还没有安装 `conda`，可以从 [Miniconda](https://docs.conda.io/en/latest/miniconda.html) 或 [Anaconda](https://www.anaconda.com/products/individual) 网站下载安装。

### 2. 创建 `conda` 环境

在项目根目录下使用以下命令来创建并配置环境：

```bash
conda remove --name CTBU-AI --all  # 删除现有环境
conda env create -f environment.yml  # 重新创建环境
```

### 3. 激活环境

创建环境之后，使用以下命令激活环境：

```bash
conda activate CTBU-AI
```

`myenv` 是在 `environment.yml` 文件中定义的环境名称，激活后即可在该环境中运行项目。

### 4. 更新环境

如果你在开发过程中安装了新的依赖项，或者项目依赖发生了变化，可以通过以下命令更新并导出环境：

```bash
conda env export > environment.yml
```

这将更新 `environment.yml` 文件，确保其包含最新的依赖项。

### 5. PIP 安装

如果你无法使用 `conda` 安装依赖项，则可以使用 `pip` 安装依赖项

```bash
pip install -r requirements.txt
```

## 运行项目

在激活 `conda` 环境后，使用以下命令运行项目：
受限于环境问题，我这里使用的是CPU,运行很慢。。。。

```bash
python main.py
```
---