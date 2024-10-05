import requests
from bs4 import BeautifulSoup
import os
import csv

# 获取当前脚本所在的目录
current_directory = os.path.dirname(os.path.abspath(__file__))

# 构造 CSV 文件的完整路径
output_file = os.path.join(current_directory, 'dlt_lottery_data.csv')

# 目标URL【start最早只能访问到07001，end可以访问到最新一期】
url = 'http://datachart.500.com/dlt/history/newinc/history.php?start=07001&end=24111'

# 发送HTTP请求
response = requests.get(url)
response.encoding = 'utf-8'  # 确保编码正确

# 解析HTML内容
soup = BeautifulSoup(response.text, 'html.parser')

# 定位包含开奖数据的表格体
tbody = soup.find('tbody', id="tdata")

# 存储开奖数据的列表
lottery_data = []

# 遍历每一行数据
for tr in tbody.find_all('tr'):
    tds = tr.find_all('td')
    if tds:
        # 提取数据并添加到列表
        lottery_data.append([td.text for td in tds])

# 写入CSV文件
with open(output_file, 'w', newline='', encoding='ANSI') as csvfile:
    writer = csv.writer(csvfile)
    # 写入标题行
    writer.writerow(['期号', '号码1', '号码2', '号码3', '号码4', '号码5', '号码6', '号码7', '奖池奖金(元)', '一等奖 注数', '一等奖 奖金', '二等奖 注数', '二等奖 奖金',  '总投注额(元)', '开奖日期'])
    # 写入数据行
    writer.writerows(lottery_data)

print('数据抓取完成，并保存到dlt_lottery_data.csv文件中。')