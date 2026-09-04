# XRD Toolkit

XRD 数据处理工具集：读取 XRD 数据文件，进行背景扣除、寻峰等处理并输出结果。

## 项目结构

```
.
├── data/          # XRD 原始数据（不进 git）
├── scripts/       # 独立脚本
├── src/xrd_toolkit/
│   ├── main.py            # 程序入口
│   ├── config.py          # 全局配置（.env 路径等）
│   ├── core/processor.py  # XRD 处理逻辑（待实现）
│   ├── services/data_loader.py  # XRD 数据文件解析（待实现）
│   └── utils/             # 工具函数
└── tests/         # 测试
```

## 安装

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 使用

```bash
xrd-toolkit
```
