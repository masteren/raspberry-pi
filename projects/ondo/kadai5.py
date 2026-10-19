#!/usr/bin/python3
# kadai5.py  温度・湿度の計測（DHT11）
import time
import datetime
import RPi.GPIO as GPIO
import dht11

PIN = 26                    # DHT11のDATAを接続したGPIO（BCM番号）
INTERVAL = 60               # 計測間隔（秒）
CSV_FILE = 'kadai5.csv'     # 保存先ファイル

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
sensor = dht11.DHT11(pin=PIN)

def save_csv(now, temp, humi):
    # 時刻, 温度, 湿度 を1行で作成（改行はCR+LF）
    line = '{},{:5.1f},{:5.1f}\r\n'.format(
        now.strftime('%Y-%m-%d %H:%M:%S'), temp, humi)
    # UTF-8・追記モード（newline=''で改行コードを変換しない）
    with open(CSV_FILE, 'a', encoding='utf-8', newline='') as f:
        f.write(line)
    return line

try:
    while True:
        start = time.time()
        result = sensor.read()                  # 計測（失敗時はライブラリ内で再試行）
        now = datetime.datetime.now()
        if result.is_valid():
            print(save_csv(now, result.temperature, result.humidity), end='')
        else:
            print(now.strftime('%Y-%m-%d %H:%M:%S'), '計測エラー')
        elapsed = time.time() - start           # 計測にかかった時間を差し引いて1分毎にする
        time.sleep(max(0, INTERVAL - elapsed))

except KeyboardInterrupt:                       # [Ctrl]+[C] で停止
    print('\n[Ctrl]+[C] 終了')
finally:
    GPIO.cleanup()
