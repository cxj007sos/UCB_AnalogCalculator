import requests
from bs4 import BeautifulSoup
import os
import csv
import time



# 获取当前脚本所在的目录
current_directory = os.path.dirname(os.path.abspath(__file__))

# 构造 CSV 文件的完整路径
output_file_dlt = os.path.join(current_directory, 'dlt_lottery_data.csv')
output_file_ssq = os.path.join(current_directory, 'ssq_lottery_data.csv')


# 目标URL【start最早只能访问到07001，end可以访问到最新一期，url_dlt为大乐透，url_ssq为双色球】
url_dlt = 'http://datachart.500.com/dlt/history/newinc/history.php?start=07001&end=24111'
url_ssq = 'http://datachart.500.com/ssq/history/newinc/history.php?start=07001&end=24111'



"""这里是大乐透"""
# 发送HTTP请求
response = requests.get(url_dlt)
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
with open(output_file_dlt, 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    # 写入标题行
    writer.writerow(['期号', '前区-号码01', '前区-号码02', '前区-号码03', '前区-号码04', '前区-号码05', '后区-号码01', '后区-号码02', '奖池奖金(元)', '一等奖 注数', '一等奖 奖金', '二等奖 注数', '二等奖 奖金',  '总投注额(元)', '开奖日期'])
    # 写入数据行
    writer.writerows(lottery_data)

print(f'数据抓取完成，并保存到 {output_file_dlt} ')
print()


"""这里是双色球"""
# 发送HTTP请求
response = requests.get(url_ssq)
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
with open(output_file_ssq, 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    # 写入标题行
    writer.writerow(['期号', '红球01', '红球02', '红球03', '红球04', '红球05', '红球06', '蓝球01', '此列为空', '奖池奖金(元)', '一等奖 注数', '一等奖 奖金', '二等奖 注数', '二等奖 奖金',  '总投注额(元)', '开奖日期'])
    # 写入数据行
    writer.writerows(lottery_data)

print(f'数据抓取完成，并保存到 {output_file_ssq}')
print()

# 倒数2秒
for i in range(2, 0, -1):
    print(f"\r等待 {i} 秒后自动退出...", end='', flush=True)
    time.sleep(1)