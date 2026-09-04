"""XRD 图像处理：对读进来的 2D 强度数组做各种计算。

本文件的代码不负责读文件、不负责画图，只做"纯计算"——
这正是 core（核心）层的定位：输入 numpy 数组，输出计算结果。
"""

import numpy as np


def line_profile(image: np.ndarray, center=None, angle_deg: float = 0.0):
    """沿过圆心、与水平方向成 angle_deg 的直线采样强度。

    参数：
        image     —— 2D numpy 数组，image[行][列] = 该像素的强度
        center    —— 圆心 (行, 列)。不传时默认图像几何中心；
                     真实数据必须传衍射环的圆心（直射光斑位置）
        angle_deg —— 直线与水平方向的夹角（度），0 = 水平线

    返回：
        t        —— 每个采样点到圆心的距离（像素）。圆心左侧为负、右侧为正
        intensity—— 每个采样点的强度（经过插值）

    为什么要插值？采样点不一定正好落在像素格点上（比如斜线），
    用周围 4 个像素按距离加权平均，得到的曲线更平滑、更接近真实。
    """

    h, w = image.shape
    if center is None:
        cy, cx = h / 2.0, w / 2.0   # 几何中心
    else:
        cy, cx = center             # 注意：center 是 (行, 列) = (y, x)

    # 【知识点】弧度：180° = π。numpy 的三角函数只认弧度，
    # np.radians 负责"角度 → 弧度"的换算。
    theta = np.radians(angle_deg)
    cos_t, sin_t = np.cos(theta), np.sin(theta)

    # 直线方程：x = cx + t·cosθ, y = cy + t·sinθ（t 是沿直线的距离）
    # 先算出 t 的合法范围——保证采样点不出图像边界。
    # 圆心不居中时两侧能走的距离不同，硬截断会让边缘像素被重复采样。
    t_min, t_max = -float(np.hypot(h, w)), float(np.hypot(h, w))
    for c, lo_edge, hi_edge in (
            (cos_t, -cx, w - 1 - cx),   # x 方向约束：0 ≤ x ≤ w-1
            (sin_t, -cy, h - 1 - cy)):  # y 方向约束：0 ≤ y ≤ h-1
        if abs(c) < 1e-12:
            continue  # 该方向没有移动（如水平线时 sinθ = 0）
        if c > 0:
            t_max = min(t_max, hi_edge / c)
            t_min = max(t_min, lo_edge / c)
        else:
            t_max = min(t_max, lo_edge / c)
            t_min = max(t_min, hi_edge / c)

    # 采样点序列：t_min 到 t_max，间隔 1 像素
    t = np.arange(np.ceil(t_min), np.floor(t_max) + 1, dtype=np.float64)

    # 【知识点】向量化：t 是"一串数"（几千个元素的数组），
    # xs = cx + t * cos_t 是"对这一串里的每个数同时计算"。
    # numpy 的数组运算不需要 for 循环——又快又简洁，
    # 写 XRD 数值代码时，能整列一起算的永远别写 for。
    xs = cx + t * cos_t
    ys = cy + t * sin_t

    # ── 双线性插值：每个采样点用周围 4 个像素加权平均 ──
    # x0, y0 = 采样点左上方的像素；fx, fy = 采样点在该像素内的小数位置 (0~1)
    x0 = np.floor(xs).astype(int)
    y0 = np.floor(ys).astype(int)
    fx = xs - x0
    fy = ys - y0

    # 四个邻居的坐标，clip 防止越界
    # 【知识点】np.clip：把数值"夹"在范围内——小于 0 变 0、
    # 大于 w-1 变 w-1。防止下标越界报错（Python 越界会直接崩）。
    x0c = np.clip(x0, 0, w - 1)
    y0c = np.clip(y0, 0, h - 1)
    x1c = np.clip(x0 + 1, 0, w - 1)
    y1c = np.clip(y0 + 1, 0, h - 1)

    # 四个邻居的强度
    i00 = image[y0c, x0c]  # 左上
    i10 = image[y0c, x1c]  # 右上
    i01 = image[y1c, x0c]  # 左下
    i11 = image[y1c, x1c]  # 右下

    # 按距离加权平均：离哪个像素近，它的权重就大
    intensity = (i00 * (1 - fx) * (1 - fy)
                 + i10 * fx * (1 - fy)
                 + i01 * (1 - fx) * fy
                 + i11 * fx * fy)
    return t, intensity
