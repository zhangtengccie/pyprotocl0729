import os
import sqlite3
from snmpv2_get import snmpv2_get
import datetime
import time


def get_info_writedb(ip, rocommunity, dbname, seconds):
    # 如果数据库存在
    if os.path.exists(dbname):
        os.remove(dbname)  # 删除数据库
    # 如果不存在，创建并链接数据库
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    # 创建数据库的表
    cursor.execute("create table cpudb(id INTEGER PRIMARY KEY AUTOINCREMENT, time timestamp, mem_percent int)")

    while seconds > 0:
        # cpmCPUMemoryUsed
        mem_used = int(snmpv2_get("1.1.1.200", "tcpipro", "1.3.6.1.4.1.9.9.109.1.1.1.1.12.2", port=161)[1])
        # cpmCPUMemoryFree
        mem_free = int(snmpv2_get("1.1.1.200", "tcpipro", "1.3.6.1.4.1.9.9.109.1.1.1.1.13.2", port=161)[1])
        # 内存利用率
        mem_percent = round((mem_used / (mem_used + mem_free)), 4) * 100  # 小数点保留4位
        # 获取现在时间
        time_info = datetime.datetime.now()
        # 将CPU 和 时间写入数据库的表中
        cursor.execute(f'insert into cpudb(time,mem_percent) values("{time_info}","{mem_percent}")')
        # 等待5秒
        time.sleep(5)
        # 传过来的时间减去5秒
        seconds -= 5
        conn.commit()


if __name__ == '__main__':
    get_info_writedb('1.1.1.200', 'tcpipro', 'deviceinfo.sqlite', 1000)
