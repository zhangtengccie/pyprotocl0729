import os
import sqlite3
from snmpv2_get import snmpv2_get
import datetime
import time
import sqlite3
from snmpv2_get import snmpv2_get
import datetime
import time
import random
import datetime

from matplotlib import pyplot as plt
import matplotlib
# conn = sqlite3.connect('mem_Total_db.sqlite')
# cursor = conn.cursor()
# cursor.execute("create table routerdb(id INTEGER PRIMARY KEY AUTOINCREMENT, time timestamp, mem_percent int)")

# 读取CPU利用率写入数据库
def write_mem_values_db(seconds):
    conn = sqlite3.connect('mem_Total_db.sqlite')
    cursor = conn.cursor()
    id = 0
    while seconds > 0:
        id+=1
        now = time.time()
        mem_free = snmpv2_get("1.1.1.200", "tcpipro", "1.3.6.1.4.1.9.9.48.1.1.1.6.1", port=161)[1]
        # mem-used
        mem_used = snmpv2_get("1.1.1.200", "tcpipro", "1.3.6.1.4.1.9.9.48.1.1.1.5.1", port=161)[1]
        #mem_total
        mem_total = int(mem_free) + int(mem_used)
        mem_util = int(mem_used) / int(mem_total)
        mem_pre = int(mem_util*100)
        cursor.execute(f'insert into routerdb(id,time,mem_percent) values("{id}","{now}","{mem_pre}")')
        # print(mem_util)
        cursor.fetchall()
        conn.commit()
        time.sleep(5)
        seconds -= 5
# 从数据库中读取时间和CPU利用率
mem_values_dict = {}
def read_mem_values_db():

    conn = sqlite3.connect('mem_Total_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('select * from routerdb')
    all_result = cursor.fetchall()
    for x in all_result:
        mem_values_dict[x[1]]=x[2]
    return mem_values_dict

print(matplotlib.matplotlib_fname())
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
plt.rcParams['font.family'] = 'sans-serif'
colorlist = ['r', 'b', 'g', 'y']

import matplotlib.pyplot as plt
import matplotlib.dates as md
import dateutil
def mat_line(cpu_usage_list):
    # 调节图形大小，宽，高
    fig = plt.figure(figsize=(6, 6))
    # 一共一行, 每行一图, 第一图
    ax = fig.add_subplot(111)

    # 处理X轴时间格式
    import matplotlib.dates as mdate
    # ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S')) # 设置时间标签显示格式
    ax.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))  # 设置时间标签显示格式

    # 处理Y轴百分比格式
    import matplotlib.ticker as mtick
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%d%%'))

    # 把cpu_usage_list的数据,拆分为x轴的时间,与y轴的利用率
    x = []
    y = []

    for time, cpu in cpu_usage_list:
        x.append(time)
        y.append(cpu)

    # 添加主题和注释
    plt.title('路由器MEM利用率')
    plt.xlabel('采集时间')
    plt.ylabel('MEM利用率')

    fig.autofmt_xdate()  # 当x轴太拥挤的时候可以让他自适应

    # 实线红色
    ax.plot(x, y, linestyle='solid', color='r', label='R1')
    # 虚线黑色
    # ax.plot(x, y, linestyle='dashed', color='b', label='R1')
    ax.set_ylim(bottom=0, top=100)
    # 如果你有两套数据,完全可以在一幅图中绘制双线
    # ax.plot(x2, y2, linestyle='dashed', color='b', label='R2')

    # 设置说明的位置
    ax.legend(loc='upper left')

    # 保存到图片
    plt.savefig('result1.png')
    # 绘制图形
    plt.show()
import datetime
if __name__ == '__main__':
    # write_mem_values_db(60)
    cpu_dict = read_mem_values_db()
    # print(cpu_dict)

    # 画折线图
    line_data = []
    for i in cpu_dict.items():
        x = datetime.datetime.utcfromtimestamp(int(i[0]))
        xy = x, i[1]
        line_data.append(xy)
    print(line_data)
    mat_line(line_data)

