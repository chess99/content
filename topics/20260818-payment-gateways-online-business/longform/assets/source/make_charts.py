from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.lines import Line2D


OUT_DIR = Path(__file__).resolve().parents[1]
FONT_PATH = Path(r"C:\Windows\Fonts\msyh.ttc")
DPI = 144

if FONT_PATH.exists():
    font_name = font_manager.FontProperties(fname=str(FONT_PATH)).get_name()
    plt.rcParams["font.family"] = font_name

plt.rcParams.update(
    {
        "axes.unicode_minus": False,
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FFFFFF",
        "savefig.facecolor": "#FFFFFF",
        "text.color": "#17212B",
        "axes.labelcolor": "#667085",
        "xtick.color": "#667085",
        "ytick.color": "#17212B",
        "axes.edgecolor": "#D0D5DD",
    }
)


def add_header(fig, title, subtitle):
    fig.text(0.075, 0.955, title, fontsize=28, fontweight="bold", ha="left", va="top")
    fig.text(0.075, 0.905, subtitle, fontsize=16, color="#475467", ha="left", va="top")


def add_footer(fig, text):
    fig.text(0.075, 0.02, text, fontsize=13.2, color="#667085", ha="left", va="bottom", linespacing=1.45)


def save(fig, filename):
    fig.savefig(OUT_DIR / filename, dpi=DPI)
    plt.close(fig)


def chart_three_lenses():
    categories = ["AI 产品", "创作和专业软件", "开发工具和基础设施", "商业 SaaS 和生产力", "教育和知识产品", "游戏和虚拟商品"]
    signal = np.array([57.5, 5.0, 2.0, 9.3, 4.2, 7.6])
    equal = np.array([17.1, 27.4, 10.8, 6.0, 11.3, 3.4])
    merchants = np.array([14.0, 14.3, 24.9, 11.2, 9.1, 6.1])

    series = [
        (signal, -0.23, "#D95D48", "支付活动信号｜看规模"),
        (equal, 0.00, "#315E7D", "五个入口等权｜看平台结构"),
        (merchants, 0.23, "#3E9182", "已分类来源域名｜看数量"),
    ]

    fig, ax = plt.subplots(figsize=(7.5, 10), dpi=DPI)
    fig.subplots_adjust(left=0.35, right=0.96, top=0.72, bottom=0.20)
    add_header(fig, "换一把尺，答案就变了", "同一批支付入口来源，三种口径回答三件不同的事")

    legend_y = [0.855, 0.822, 0.789]
    for (_, _, color, label), yy in zip(series, legend_y):
        fig.add_artist(Line2D([0.08, 0.125], [yy, yy], transform=fig.transFigure, color=color, linewidth=6, solid_capstyle="round"))
        fig.text(0.145, yy, label, fontsize=17, ha="left", va="center", color="#344054")

    y = np.arange(len(categories))
    for values, offset, color, _ in series:
        yy = y + offset
        ax.hlines(yy, 0, values, color=color, linewidth=4.5, alpha=0.9)
        ax.scatter(values, yy, s=130, color=color, edgecolor="white", linewidth=1.8, zorder=3)
        for value, pos in zip(values, yy):
            ax.text(value + 1.1, pos, f"{value:.1f}%", va="center", ha="left", fontsize=17, color="#17212B")

    ax.set_yticks(y, categories, fontsize=18)
    ax.invert_yaxis()
    ax.set_xlim(0, 68)
    ax.set_xticks(np.arange(0, 61, 10), [f"{v}%" for v in range(0, 61, 10)], fontsize=14.5)
    ax.grid(axis="x", color="#EAECF0", linewidth=1.0)
    ax.set_axisbelow(True)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=14)
    ax.tick_params(axis="x", length=0, pad=9)

    add_footer(fig, "仅展示六个主要类别，各组不会合计到 100%。\n来源域名口径排除 125 个未分类域名。\n样本为 2026 年 7 月五个专用支付入口的已采集头部来源。")
    save(fig, "chart-01-three-lenses.png")


def chart_gateway_ecosystems():
    gateways = ["Stripe Checkout", "Stripe Payment Links", "FastSpring", "PayPro Global", "Razorpay Payment Pages"]
    categories = ["AI 产品", "创作和专业软件", "开发工具和基础设施", "教育和知识产品", "商业 SaaS 和生产力", "游戏和虚拟商品", "未识别", "其他已识别"]
    category_display = {
        "创作和专业软件": "专业软件",
        "开发工具和基础设施": "开发工具",
        "商业 SaaS 和生产力": "商业 SaaS",
    }
    values = np.array(
        [
            [62.956, 3.903, 1.319, 2.277, 9.541, 8.222, 1.446, 10.336],
            [22.317, 13.897, 7.535, 5.749, 6.311, 3.793, 25.566, 14.832],
            [0.0, 73.057, 8.901, 0.225, 1.782, 2.716, 3.181, 10.138],
            [0.0, 42.372, 35.989, 0.0, 2.377, 2.103, 10.344, 6.814],
            [0.0, 3.760, 0.328, 48.383, 9.956, 0.0, 33.044, 4.529],
        ]
    )
    rank_colors = ["#175CD3", "#4E7FD3", "#86A8DD", "#C3D2EB"]

    fig, ax = plt.subplots(figsize=(7.5, 13.5), dpi=DPI)
    fig.subplots_adjust(left=0.08, right=0.96, top=0.82, bottom=0.15)
    add_header(fig, "换个支付入口，生意就换了一批", "每个入口只展示占比最高的四类，所有横条使用同一把 0—80% 标尺")

    cursor = 0.0
    bar_height = 0.46
    bar_step = 0.82
    group_gap = 1.25

    for gateway, row in zip(gateways, values):
        ax.text(-34.5, cursor, gateway, fontsize=19.5, fontweight="bold", ha="left", va="center", color="#17212B")
        order = np.argsort(row)[::-1][:4]
        for rank, idx in enumerate(order):
            yy = cursor + 0.72 + rank * bar_step
            value = row[idx]
            category = categories[idx]
            ax.text(-34.5, yy, category_display.get(category, category), fontsize=16.5, ha="left", va="center", color="#475467")
            ax.barh(yy, value, height=bar_height, color=rank_colors[rank])
            ax.text(value + 1.0, yy, f"{value:.1f}%", fontsize=16.5, ha="left", va="center", color="#17212B")
        cursor += 0.72 + 4 * bar_step + group_gap
        ax.hlines(cursor - group_gap / 2, -34.5, 80, color="#EAECF0", linewidth=1.0)

    ax.set_xlim(-36, 85)
    ax.set_ylim(-0.6, cursor - 0.2)
    ax.invert_yaxis()
    ax.set_yticks([])
    ax.set_xticks(np.arange(0, 81, 20), [f"{v}%" for v in range(0, 81, 20)], fontsize=14.5)
    ax.grid(axis="x", color="#EAECF0", linewidth=1.0)
    ax.set_axisbelow(True)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.tick_params(axis="x", length=0, pad=9)

    add_footer(fig, "颜色深浅只表示入口内部排名，不代表行业类别。\n未展示类别仍计入原始结构。份额按清理后可归因的支付活动信号计算。\n这些数据不能解释平台选择的因果。")
    save(fig, "chart-02-gateway-ecosystems.png")


def chart_relative_momentum():
    categories = ["创作和专业软件", "开发工具和基础设施", "游戏和虚拟商品", "内容和线下消费", "商业 SaaS 和生产力", "健康和生活服务", "通用数字产品", "教育和知识产品", "AI 产品", "金融和交易服务"]
    change = np.array([44.7, 26.6, 23.4, 18.9, 18.6, 13.5, 10.6, 8.9, 0.9, -9.9])
    effective_n = np.array([36, 66, 18, 15, 32, 9, 23, 24, 43, 7])
    new_n = np.array([11, 17, 2, 7, 6, 0, 6, 6, 3, 3])

    fig, ax = plt.subplots(figsize=(7.5, 11.2), dpi=DPI)
    fig.subplots_adjust(left=0.37, right=0.95, top=0.80, bottom=0.18)
    add_header(fig, "AI 规模最大，份额动量却接近零", "来源份额变化只反映支付入口内的相对位置，不代表行业收入增速")

    y = np.arange(len(categories))
    colors = np.where(change >= 0, "#087A65", "#B42318")
    ax.hlines(y, np.minimum(change, 0), np.maximum(change, 0), color=colors, linewidth=4.2, alpha=0.82)
    ax.scatter(change, y, s=155, color=colors, edgecolor="white", linewidth=1.8, zorder=3)

    for value, yy, n, new in zip(change, y, effective_n, new_n):
        ax.text(value + 1.2, yy - 0.12, f"{value:+.1f}%", va="center", ha="left", fontsize=17, fontweight="bold", color="#17212B")
        ax.text(58.5, yy + 0.18, f"样本 {n}｜新来源 {new}", va="center", ha="right", fontsize=14.5, color="#667085")

    ax.axvline(0, color="#98A2B3", linewidth=1.2)
    ax.set_yticks(y, categories, fontsize=17)
    ax.invert_yaxis()
    ax.set_xlim(-14, 60)
    ax.set_xticks(np.arange(-10, 51, 10), [f"{v}%" for v in range(-10, 51, 10)], fontsize=14.5)
    ax.grid(axis="x", color="#EAECF0", linewidth=1.0)
    ax.set_axisbelow(True)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=13)
    ax.tick_params(axis="x", length=0, pad=9)

    add_footer(fig, "样本为进入中位数计算的有效记录。\n新来源因没有上月变化值而被排除。\n不同类别的小基数、入口构成和缺失方式都会放大或压低变化。")
    save(fig, "chart-03-relative-momentum.png")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    chart_three_lenses()
    chart_gateway_ecosystems()
    chart_relative_momentum()
