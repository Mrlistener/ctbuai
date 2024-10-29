# @auth: Lizx
# @date: 2024-10-24 14:00

import logging

from AppConfig import AppConfig
from app import create_app
from model.model import load_model, set_model_type
from logging_config import configure_logging  # 导入日志配置模块

# 加载配置文件
AppConfig.load_config("config.yml")

# 创建 Flask 应用
app = create_app()

if __name__ == "__main__":
    # 配置日志
    configure_logging(log_file=AppConfig.get_log_file(), log_level=AppConfig.get_log_level(),
                      log_format=AppConfig.get_log_format())

    # 获取日志记录器
    logger = logging.getLogger(__name__)

    # 加载模型
    set_model_type(AppConfig.get_model_type())
    load_model()

    # 运行 Flask 应用
    logger.info(
        f"Starting application on {AppConfig.get_host()}:{AppConfig.get_port()} with debug={AppConfig.is_debug()}")
    app.run(host=AppConfig.get_host(), port=AppConfig.get_port(), debug=AppConfig.is_debug(), use_reloader=False,threaded=True)
