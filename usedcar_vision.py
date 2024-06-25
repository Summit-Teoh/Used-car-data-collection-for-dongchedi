from matplotlib.font_manager import FontProperties
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体
font = FontProperties(fname='C:/Windows/Fonts/SimHei.ttf')  # 请将路径替换为您本地的中文字体路径

def main():
    # 从 Excel 文件中读取数据
    filepath = "6.24/dongchedi.xls"
    df = pd.read_excel(filepath, sheet_name="usdecar")

    # 选择前10的热门品牌
    top_brands = df['品牌'].value_counts().nlargest(20).index
    df_top_brands = df[df['品牌'].isin(top_brands)]

    # 选择前15的热门地区
    top_cities = df['地区'].value_counts().nlargest(20).index
    df_top_cities = df[df['地区'].isin(top_cities)]

    # 可视化 1: 官方指导价与售价的分布
    plt.figure(figsize=(12, 8))
    scatter_plot = sns.scatterplot(data=df_top_brands, x='官方指导价', y='售价', hue='品牌', palette='tab10', s=100)
    plt.title('官方指导价与售价的分布', fontproperties=font, fontsize=16)
    plt.xlabel('官方指导价 (万元)', fontproperties=font, fontsize=14)
    plt.ylabel('售价 (万元)', fontproperties=font, fontsize=14)
    # 设置图例的中文标题
    scatter_legend = plt.legend(title='品牌', bbox_to_anchor=(1.05, 1), loc='upper left', prop=font, fontsize=12)
    for text in scatter_legend.get_texts():
        text.set_fontproperties(font)
    scatter_legend.get_title().set_fontproperties(font)
    plt.tight_layout()
    plt.savefig("6.24\image\price_distribution_top_brands.png")
    plt.show()

    # 可视化 2: 热门品牌的车辆数量
    plt.figure(figsize=(12, 8))
    brand_counts = df_top_brands['品牌'].value_counts()
    sns.barplot(x=brand_counts.index, y=brand_counts.values, palette='tab10')
    plt.title('热门品牌的车辆数量', fontproperties=font, fontsize=16)
    plt.xlabel('品牌', fontproperties=font, fontsize=14)
    plt.ylabel('数量', fontproperties=font, fontsize=14)
    plt.xticks(rotation=45, fontproperties=font, fontsize=12)
    plt.tight_layout()
    plt.savefig("6.24\image\\top_brand_counts.png")
    plt.show()

    # 可视化 3: 热门地区的车辆数量
    plt.figure(figsize=(12, 8))
    city_counts = df_top_cities['地区'].value_counts()
    sns.barplot(x=city_counts.index, y=city_counts.values, palette='tab20')
    plt.title('热门地区的车辆数量', fontproperties=font, fontsize=16)
    plt.xlabel('地区', fontproperties=font, fontsize=14)
    plt.ylabel('数量', fontproperties=font, fontsize=14)
    plt.xticks(rotation=45, fontproperties=font, fontsize=12)
    plt.tight_layout()
    plt.savefig("6.24\image\\top_city_counts.png")
    plt.show()

    # 可视化 4: 不同颜色的车辆数量饼状图
    plt.figure(figsize=(12, 8))
    color_counts = df['颜色'].value_counts()
    plt.pie(color_counts.values, labels=color_counts.index, autopct='%1.1f%%', colors=sns.color_palette('tab10'), textprops={'fontproperties': font})
    plt.title('不同颜色的车辆数量占比', fontproperties=font, fontsize=16)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig("6.24\image\color_pie_chart.png")
    plt.show()

if __name__ == "__main__":
    main()
