from xrd_toolkit.config import settings
from xrd_toolkit.core import processor


def main() -> None:
    """程序入口：后续在此串联「数据加载 → XRD 处理 → 结果输出」流程。"""
    # TODO: 用 services.data_loader 读取 XRD 数据文件，交给 processor 处理后输出结果


if __name__ == "__main__":
    main()