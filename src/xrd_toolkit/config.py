from pathlib import Path

# 项目根目录：基于本文件位置定位，无论从哪里启动程序都能准确找到根目录
BASE_DIR = Path(__file__).resolve().parents[2]  # config.py → xrd_toolkit → src → 根目录


class Settings:
    APP_NAME = "XRD Toolkit"
    # .env 配置文件路径，后续可用它存放数据目录、输出路径等配置
    ENV_PATH = BASE_DIR / ".env"


settings = Settings()