import os
import requests
from fontlist import replace_unrecognized_chars
import xlrd
from xlutils.copy import copy
import xlwt
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from tqdm import tqdm  

def main():
    start_time = time.time()
    datalist = GetData()
    savepath = "6.24/dongchedi.xls"
    SaveData(datalist, savepath)
    end_time = time.time()
    print(f"总运行时间: {end_time - start_time:.2f} 秒")

def GetData():
    url = "https://www.dongchedi.com/motor/pc/sh/sh_sku_list?aid=1839&app_name=auto_web_pc"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    datalist = []
    payload = {
        "sh_city_name": "全国",
        "page": "1"
    }
    sku_id_list = []

    data_fetch_start_time = time.time()
    for i in range(10):  # 获取页面信息
        payload["page"] = str(i + 1)
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            json_data = response.json()
            car_info_list = json_data['data']['search_sh_sku_info_list']
            for car_info in car_info_list:
                data = [
                    car_info['brand_name'],
                    car_info['title'],
                    replace_unrecognized_chars(car_info['official_price']).rstrip(),
                    replace_unrecognized_chars(car_info['sh_price']).rstrip(),
                    car_info['brand_source_city_name'],
                    str(car_info['sku_id']),
                ]
                sub_title = replace_unrecognized_chars(car_info['sub_title']).rstrip()
                parts = sub_title.split('|')
                data.append(parts[0].replace("里程数：", "").strip())
                data.append(parts[1].strip())

                image_url = car_info['image']
                data.append(image_url)
                datalist.append(data)

                sku_id = car_info['sku_id']
                sku_id_list.append(sku_id)
        else:
            print(f"数据获取失败: {response.status_code}")
    data_fetch_end_time = time.time()
    print(f"数据获取时间: {data_fetch_end_time - data_fetch_start_time:.2f} 秒")

    color_fetch_start_time = time.time()
    color_map = GetCarColors(sku_id_list, headers)
    color_fetch_end_time = time.time()
    print(f"颜色获取时间: {color_fetch_end_time - color_fetch_start_time:.2f} 秒")

    for data in datalist:
        sku_id = int(data[5])
        data.pop(5)  # 移除id列
        data.append(color_map.get(sku_id, "N/A"))

    return datalist

def GetCarColors(sku_id_list, headers):
    color_map = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_sku_id = {executor.submit(GetCarColor, sku_id, headers): sku_id for sku_id in sku_id_list}
        
        # 使用 tqdm 进度条
        for future in tqdm(as_completed(future_to_sku_id), total=len(future_to_sku_id), desc="获取颜色"):
            sku_id = future_to_sku_id[future]
            try:
                color = future.result()
                color_map[sku_id] = color
            except Exception as e:
                print(f"获取 SKU {sku_id} 的颜色时出错: {e}")
                color_map[sku_id] = "N/A"
    return color_map

def GetCarColor(sku_id, headers):
    url = f"https://www.dongchedi.com/usedcar/{sku_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        
        color_tags = soup.find_all('p', class_='car-archives_value__3YXEW')
        if color_tags and len(color_tags) > 0:
            return color_tags[7].text.strip()
        else:
            return "N/A"
    else:
        return "N/A"

def Auto_Type(datalist, sheet):
    col_width = []
    for i in range(len(datalist[0])):
        for j in range(len(datalist)):
            number1 = number2 = 0
            for char in datalist[j][i]:
                try:
                    if 0x4e00 <= ord(char) <= 0x9fff or ord(char) == 0x0020:
                        number1 += 2
                    else:
                        number2 += 1
                except Exception as e:
                    if hasattr(e, "code"):
                        print(e.code)
                    if hasattr(e, "reason"):
                        print(e.reason)
            number = number1 + number2
            if j == 0:
                col_width.append(number)
            else:
                if col_width[i] < number:
                    col_width[i] = number
        width = 256 * (col_width[i] + 1)
        if width >= 65535:
            width = 65535
        sheet.col(i).width = width

def SaveData(datalist, savepath):
    if not os.path.isfile(savepath):
        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet("usdecar")
        Auto_Type(datalist, sheet)
        print("表格创建成功\n")
    else:
        rb = xlrd.open_workbook(savepath, formatting_info=True)
        book = copy(rb)
        sheet = book.get_sheet(0)
        print("表格打开成功\n")
    
    col_names = ["品牌", "车型", "官方指导价", "售价", "地区","上牌日期", "里程数" ,"图片链接", "颜色"]
    for i, col_name in enumerate(col_names):
        sheet.write(0, i, col_name)
    
    for i, data in enumerate(tqdm(datalist, desc="保存数据")):  # 使用 tqdm 进度条
        # print(f"正在写入第{i+1}条数据")
        for j, value in enumerate(data):
            sheet.write(i + 1, j, value)
    
    book.save(savepath)
    print("数据保存成功")

if __name__ == "__main__":
    main()
    print("爬取完毕")
