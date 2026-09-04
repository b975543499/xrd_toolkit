from pathlib import Path

# 项目根目录：基于本文件位置定位，无论从哪里启动程序都能准确找到根目录
# __file__ = "本文件自己的路径"；parents[2] = config.py → xrd_toolkit → src → 项目根目录
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings:
    APP_NAME = "XRD Toolkit"
    # .env 配置文件路径，后续可用它存放数据目录、输出路径等配置
    ENV_PATH = BASE_DIR / ".env"
    # 说明：配置文件里只放"当前代码真正用得到"的项。
    # 将来做"像素 → 2θ 角度标定"时，再把波长、探测器距离等仪器参数加回来。


settings = Settings()
