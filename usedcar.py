import os
from bs4 import BeautifulSoup
import requests
from fontlist import replace_unrecognized_chars
import xlrd
from xlutils.copy import copy
import xlwt
import time

#程序入口
def main():
    start_time = time.time()
    #1. 爬取网页
    datalist = GetData()
    savepath = "6.17/dongchedi.xls"#Excel路径
    end_time = time.time()
    print(f"总运行时间: {end_time - start_time:.2f} 秒")
   

    #3. 保存数据
    SavaData(datalist,savepath)
def GetData():
    # 定义请求URL和请求头
    url = "https://www.dongchedi.com/motor/pc/sh/sh_sku_list?aid=1839&app_name=auto_web_pc"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    datalist = []

    # 定义POST请求的payload
    payload = {
        "sh_city_name": "全国",
        "page" : "1"
    }
    for i in range(2):  # 获取30个页面信息
        payload["page"] = str(i + 1)  # 更新字典中的page键的值
        # print(payload)
        # print(f"第{i+1}页已开始")

        # 发送POST请求
        response = requests.post(url, headers=headers, data=payload)

        # 确保请求成功
        if response.status_code == 200:
            # 解析返回的JSON数据
            jsonusercar = response.json()
            # print(jsonusercar)


            car_info_list = jsonusercar['data']['search_sh_sku_info_list']
            # print(car_info_list)
            
            
            for car_info in car_info_list:
                data = []
                brand_name = car_info['brand_name']
                data.append(brand_name)
                car_name = car_info['title']
                data.append(car_name)
                
                #解密未定义字符
                official_price = replace_unrecognized_chars(car_info['official_price']).rstrip()   
                data.append(official_price)
                sh_price = replace_unrecognized_chars(car_info['sh_price']).rstrip()
                data.append(sh_price)
                sub_title = replace_unrecognized_chars(car_info['sub_title']).rstrip()
                #分割sub_title为上牌日期和公里数
                parts = sub_title.split('|') # 使用'|'字符进行分割
                year_part = parts[0].strip()  # 去除前后的空格
                registration_date = year_part.replace("里程数：", "").strip()  # 去除"里程数："前缀
                data.append(registration_date)
                kilometres = parts[1].strip()
                data.append(kilometres)
                city_name = car_info['brand_source_city_name']
                data.append(city_name)
                sku_id = car_info['sku_id']
                

                sku_id = car_info['sku_id']
                color = GetCarColor(sku_id)
                data.append(color)

                image_url = car_info['image']
                data.append(image_url)
                # print(data)
                datalist.append(data)#追加每页信息
                              
        else:
            print(f"Failed to retrieve data: {response.status_code}")
    return datalist         

def GetCarColor(sku_id):
    url = f"https://www.dongchedi.com/usedcar/{sku_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        # print(soup)
        color_tag = soup.find_all('p', class_='car-archives_value__3YXEW')
        if color_tag:
            return color_tag[7].text.strip()
        else:
            return "N/A"
    else:
        return "N/A"

#自适应列宽设置
def Auto_Type(datalist,sheet):
    col_width = []

    for i in range(len(datalist[0])):# 每列
        for j in range(len(datalist)):# 每行
            number1 = number2 = 0#统计字符宽度
            for char in datalist[j][i]:
                try:
                    if 0x4e00 <= ord(char) <= 0x9fff or ord(char) == 0x0020:#unicode字符集（utf-8解码）
                        number1 += 2
                    else:
                        number2 += 1
                except Exception as e:
                    if hasattr(e, "code"):  # 出错代码
                        print(e.code)
                    if hasattr(e, "reason"):  # 出错原因
                        print(e.reason)
            number = number1 + number2
            if j == 0:
                col_width.append(number)# 数组增加一个元素
            else:
                if col_width[i] < number:# 获得每列中的内容的最大宽度
                    col_width[i] = number
        width = 256*(col_width[i]+1)
        if width >= 65535:
            width = 65535
        sheet.col(i).width = width#设置列宽


#保存数据到Excel
def SavaData(datalist,savepath):
    if not(os.path.isfile(savepath)):
        book = xlwt.Workbook(encoding="utf-8")#创建文件
        sheet = book.add_sheet("usdecar")#创建表单
        Auto_Type(datalist, sheet)# type: ignore #自适应列宽
        print("表格创建成功\n")
    else:
        rb = xlrd.open_workbook(savepath,formatting_info=True)#打开文件
        book = copy(rb)
        sheet = book.get_sheet(0)#打开表单
        print("表格打开成功\n")
    col = ["品牌","车型","官方指导价","售价","里程数","地区","上牌日期","颜色","图片链接"]         
    for i in range(len(datalist[0])):
        sheet.write(0,i,col[i])#写入第一行
    for i in range(len(datalist)):#存入数据
        print("正在写入第%s条"%(i+1))
        data = datalist[i]
        for j in range(len(datalist[0])):
            sheet.write(i+1,j,data[j])

    book.save(savepath)#保存数据

if __name__ == "__main__":
    #调用函数
    main()
    print("爬取完毕")
