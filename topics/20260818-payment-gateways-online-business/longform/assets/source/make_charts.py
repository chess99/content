from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager


OUT_DIR = Path(__file__).resolve().parents[1]
FONT_PATH = Path(r"C:\Windows\Fonts\msyh.ttc")

if FONT_PATH.exists():
    font_name = font_manager.FontProperties(fname=str(FONT_PATH)).get_name()
    plt.rcParams["font.family"] = font_name

plt.rcParams.update(
    {
        "axes.unicode_minus": False,
        "figure.facecolor": "#F7F4EE",
        "axes.facecolor": "#F7F4EE",
        "savefig.facecolor": "#F7F4EE",
        "text.color": "#1D2A32",
        "axes.labelcolor": "#52616A",
        "xtick.color": "#66737A",
        "ytick.color": "#1D2A32",
        "axes.edgecolor": "#D5D0C7",
    }
)


def add_header(fig, title, subtitle):
    fig.text(0.075, 0.94, title, fontsize=25, fontweight="bold", ha="left", va="top")
    fig.text(0.075, 0.892, subtitle, fontsize=12.5, color="#5F6D73", ha="left", va="top")


def add_footer(fig, text):
    fig.text(0.075, 0.035, text, fontsize=9.5, color="#7A827F", ha="left", va="bottom")


def chart_three_lenses():
    categories = ["AI 产品", "创作和专业软件", "开发工具和基础设施", "商业 SaaS 和生产力", "教育和知识产品", "游戏和虚拟商品"]
    signal = np.array([57.5, 5.0, 2.0, 9.3, 4.2, 7.6])
    equal = np.array([17.1, 27.4, 10.8, 6.0, 11.3, 3.4])
    merchants = np.array([14.0, 14.3, 24.9, 11.2, 9.1, 6.1])

    fig, ax = plt.subplots(figsize=(12, 7.2), dpi=160)
    fig.subplots_adjust(left=0.245, right=0.95, top=0.79, bottom=0.15)
    add_header(fig, "同一批来源，换一把尺子，答案就变了", "规模口径突出 AI，来源域名数量口径则突出开发工具与专业软件")

    y = np.arange(len(categories))
    h = 0.22
    colors = ["#D95D48", "#315E7D", "#3E9182"]
    labels = ["按支付活动信号", "五个入口等权", "按已分类来源域名数"]

    for values, offset, color, label in zip([signal, equal, merchants], [-h, 0, h], colors, labels):
        bars = ax.barh(y + offset, values, height=h * 0.78, color=color, label=label)
        for bar, value in zip(bars, values):
            ax.text(value + 0.65, bar.get_y() + bar.get_height() / 2, f"{value:.1f}%", va="center", ha="left", fontsize=9.5, color="#26343A")

    ax.set_yticks(y, categories, fontsize=11.5)
    ax.invert_yaxis()
    ax.set_xlim(0, 62)
    ax.set_xticks(np.arange(0, 61, 10), [f"{v}%" for v in range(0, 61, 10)])
    ax.grid(axis="x", color="#D9D4CB", linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=12)
    ax.tick_params(axis="x", length=0, pad=8)
    ax.legend(loc="lower right", bbox_to_anchor=(1.0, 1.025), ncol=3, frameon=False, fontsize=10.5, handlelength=1.4, columnspacing=1.8)
    add_footer(fig, "仅展示六个主要类别。样本来自 2026 年 7 月五个专用支付入口。来源域名数口径排除了 125 个未分类域名。")
    fig.savefig(OUT_DIR / "chart-01-three-lenses.png", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


def chart_gateway_ecosystems():
    gateways = ["Stripe Checkout", "Stripe Payment Links", "FastSpring", "PayPro Global", "Razorpay Payment Pages"]
    categories = ["AI 产品", "创作和专业软件", "开发工具和基础设施", "教育和知识产品", "商业 SaaS 和生产力", "游戏和虚拟商品", "未识别", "其他已识别"]
    values = np.array(
        [
            [62.956, 3.903, 1.319, 2.277, 9.541, 8.222, 1.446, 10.336],
            [22.317, 13.897, 7.535, 5.749, 6.311, 3.793, 25.566, 14.832],
            [0.0, 73.057, 8.901, 0.225, 1.782, 2.716, 3.181, 10.138],
            [0.0, 42.372, 35.989, 0.0, 2.377, 2.103, 10.344, 6.814],
            [0.0, 3.760, 0.328, 48.383, 9.956, 0.0, 33.044, 4.529],
        ]
    )
    colors = ["#D95D48", "#3E9182", "#315E7D", "#7A68A6", "#C18B34", "#B85D78", "#A7AAA5", "#D8D2C8"]

    fig, ax = plt.subplots(figsize=(12, 7.4), dpi=160)
    fig.subplots_adjust(left=0.21, right=0.95, top=0.78, bottom=0.24)
    add_header(fig, "换一个支付入口，生意就换了一批", "五个专用支付页的来源结构已经出现明显分化")

    y = np.arange(len(gateways))
    left = np.zeros(len(gateways))
    for idx, (category, color) in enumerate(zip(categories, colors)):
        bars = ax.barh(y, values[:, idx], left=left, color=color, height=0.54, label=category)
        for row, (bar, value) in enumerate(zip(bars, values[:, idx])):
            if value >= 7.0:
                text_color = "white" if idx <= 5 else "#27343A"
                ax.text(left[row] + value / 2, bar.get_y() + bar.get_height() / 2, f"{value:.1f}%", ha="center", va="center", fontsize=9.4, color=text_color, fontweight="bold")
        left += values[:, idx]

    ax.set_yticks(y, gateways, fontsize=11.5)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xticks(np.arange(0, 101, 20), [f"{v}%" for v in range(0, 101, 20)])
    ax.grid(axis="x", color="#D9D4CB", linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=10)
    ax.tick_params(axis="x", length=0, pad=8)
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, -0.16), ncol=4, frameon=False, fontsize=9.5, handlelength=1.5, columnspacing=1.5)
    add_footer(fig, "每条横条均按该入口清理后可归因的支付活动信号计算。其他已识别包含健康、内容、金融和通用数字产品等类别。")
    fig.savefig(OUT_DIR / "chart-02-gateway-ecosystems.png", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


def chart_relative_momentum():
    categories = ["创作和专业软件", "开发工具和基础设施", "游戏和虚拟商品", "内容和线下消费", "商业 SaaS 和生产力", "健康和生活服务", "通用数字产品", "教育和知识产品", "AI 产品", "金融和交易服务"]
    change = np.array([44.7, 26.6, 23.4, 18.9, 18.6, 13.5, 10.6, 8.9, 0.9, -9.9])
    effective_n = np.array([36, 66, 18, 15, 32, 9, 23, 24, 43, 7])
    new_n = np.array([11, 17, 2, 7, 6, 0, 6, 6, 3, 3])

    fig, ax = plt.subplots(figsize=(12, 7.8), dpi=160)
    fig.subplots_adjust(left=0.25, right=0.94, top=0.79, bottom=0.15)
    add_header(fig, "AI 规模最大，专业软件的相对动量更高", "来源份额环比变化中位数只反映支付入口内的相对位置，不代表行业收入增速")

    y = np.arange(len(categories))
    colors = np.where(change >= 0, "#3E9182", "#B6574C")
    ax.hlines(y, np.minimum(change, 0), np.maximum(change, 0), color=colors, linewidth=3, alpha=0.78)
    sizes = 65 + effective_n * 2.5
    ax.scatter(change, y, s=sizes, color=colors, edgecolor="#F7F4EE", linewidth=1.6, zorder=3)

    for x, yy, n, new in zip(change, y, effective_n, new_n):
        label_y = yy - 0.24 if x < 0 else yy
        ax.text(x + 1.1, label_y, f"{x:+.1f}%   n={n}   新 {new}", va="center", ha="left", fontsize=9.7, color="#27343A")

    ax.axvline(0, color="#6D7778", linewidth=1.0)
    ax.set_yticks(y, categories, fontsize=11.2)
    ax.invert_yaxis()
    ax.set_xlim(-16, 56)
    ax.set_xticks(np.arange(-10, 51, 10), [f"{v}%" for v in range(-10, 51, 10)])
    ax.grid(axis="x", color="#D9D4CB", linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=12)
    ax.tick_params(axis="x", length=0, pad=8)
    add_footer(fig, "圆点大小与 n 均表示进入中位数计算的有效记录数。新表示没有上月变化值的新来源数量。小基数会放大变化。")
    fig.savefig(OUT_DIR / "chart-03-relative-momentum.png", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    chart_three_lenses()
    chart_gateway_ecosystems()
    chart_relative_momentum()
