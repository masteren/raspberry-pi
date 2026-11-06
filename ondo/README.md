# 温度・湿度センサー（DHT11）

DHT11 で温度と湿度を計測するプログラムと、その記録をブラウザでグラフ表示する Web 版監視システムです。

## ファイル

- `sample.py`: 授業で配布されたサンプル（5 秒ごとに温度・湿度を表示）
- `kadai5.py`: 課題5。1 分ごとに計測して `kadai5.csv` に追記保存する
- `kadai5.csv`: `kadai5.py` で記録した計測データ（時刻, 温度[℃], 湿度[%]）
- `web/`: 課題6。Web版 温度・湿度監視システム（下記参照）
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

## 課題6：Web版 温度・湿度監視システム

課題5の `kadai5.csv` を読み込み、matplotlib でグラフを作ってブラウザに表示します。
Web サーバは Raspberry Pi 上で `python3 -m http.server --cgi` を使います。

| ファイル | 内容 |
|---|---|
| `web/index.html` | トップページ（`/cgi-bin/graph.py` へ移動） |
| `web/cgi-bin/graph.py` | CGI 本体。CSV を読み、`graph.png` を作成して HTML を出力 |
| `web/update.js` | ページを再読み込みせずにグラフと数値を自動更新（ちらつき防止） |
| `web/style.css` | 画面のデザイン |

### 機能

- 温度（左軸・赤）と湿度（右軸・青）の 2 軸グラフ
- 現在の温度・湿度と最終計測時刻をカード表示
- 表示範囲の切り替え：直近1時間 ／ 6時間 ／ 24時間 ／ 全データ（`graph.py?range=6h` など）
- 表示範囲内の最高・最低・平均を表で表示
- 5 秒ごとに自動更新、「グラフ更新」ボタンですぐに更新
- Python 3.13 以降で `import cgi` が使えないため、URL パラメータは環境変数 `QUERY_STRING` を `urllib.parse` で解析

### 準備

```bash
sudo apt install python3-matplotlib
```

### 実行方法

```bash
# 端末1：計測して kadai5.csv に記録
python3 kadai5.py

# 端末2：Web サーバを起動（web フォルダで実行する）
cd web
python3 -m http.server --cgi 8080
```

ブラウザで `http://<ラズパイのIPアドレス>:8080/` を開きます（ラズパイ本体なら `http://localhost:8080/`）。
`graph.py` には実行権限が必要です（`chmod +x web/cgi-bin/graph.py`）。
