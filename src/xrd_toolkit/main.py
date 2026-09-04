from xrd_toolkit.config import settings
from xrd_toolkit.core import processor


def main() -> None:
    """主流程：所有功能最终从这里被调用。"""
    # TODO: 用 services.data_loader 读取 XRD 数据文件，交给 processor 处理后输出结果


if __name__ == "__main__":
    main()
