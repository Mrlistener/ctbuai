import yaml
import os

# @auth: Lizx
# @date: 2024-10-25

class AppConfig:
    _config = None

    @classmethod
    def load_config(cls, config_file="config.yml"):
        """加载配置文件"""
        with open(config_file, "r", encoding="utf-8") as file:
            cls._config = yaml.safe_load(file)

    @classmethod
    def get_app_config(cls):
        """获取应用程序配置"""
        if cls._config is None:
            raise ValueError("Configuration not loaded. Call 'load_config' first.")
        return cls._config.get('app', {})

    @classmethod
    def get_logging_config(cls):
        """获取日志配置"""
        if cls._config is None:
            raise ValueError("Configuration not loaded. Call 'load_config' first.")
        return cls._config.get('logging', {})

    # 便捷方法
    @classmethod
    def get_host(cls):
        return cls.get_app_config().get('host', '127.0.0.1')

    @classmethod
    def get_port(cls):
        return cls.get_app_config().get('port', 5000)

    @classmethod
    def is_debug(cls):
        return cls.get_app_config().get('debug', False)

    @classmethod
    def get_model_type(cls):
        return cls.get_app_config().get('model_type', 'gpt2')

    @classmethod
    def get_log_dir(cls):
        return cls.get_logging_config().get('log_dir', 'logs')

    @classmethod
    def get_log_file(cls):
        return os.path.join(cls.get_log_dir(), cls.get_logging_config().get('log_file', 'app.log'))

    @classmethod
    def get_log_level(cls):
        return cls.get_logging_config().get('log_level', 'INFO')

    @classmethod
    def get_log_format(cls):
        return cls.get_logging_config().get('log_format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
