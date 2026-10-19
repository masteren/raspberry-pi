# 温度・湿度センサー（DHT11）

DHT11 で温度と湿度を計測するプログラムです。

## ファイル

- `sample.py`: 授業で配布されたサンプル（5 秒ごとに温度・湿度を表示）
- `kadai5.py`: 課題5。1 分ごとに計測して `kadai5.csv` に追記保存する
- `kadai5.csv`: `kadai5.py` で記録した計測データ（時刻, 温度[℃], 湿度[%]）
- `dht11/`: DHT11 読み取り用ライブラリ（配布資料の `dht11_sample.zip` より）

## 接続

- DHT11 の VCC → +5V
- DHT11 の DATA → GPIO26（DATA と +5V の間に 10kΩ のプルアップ抵抗）
- DHT11 の GND → GND
- NC ピンは未接続

## 実行方法

```bash
python3 sample.py   # 動作確認
python3 kadai5.py   # 課題5（[Ctrl]+[C] で終了）
```
