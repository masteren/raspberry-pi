# Raspberry Pi

Raspberry Pi で GPIO やセンサーを動かす授業の課題・練習用プログラムです。

## 課題一覧

| 課題 | 内容 | フォルダ | 使う部品 |
|:---:|---|---|---|
| 課題1 | GPIO で LED を 1 秒ごとに点滅 | [gpio_led_blink](gpio_led_blink/) | LED、抵抗 |
| 課題5 | 温度・湿度を 1 分ごとに計測して CSV に記録 | [ondo](ondo/#課題5温度湿度自動計測システム) | DHT11 |
| 課題6 | Web版 温度・湿度監視システム（CSV をブラウザでグラフ表示） | [ondo/web](ondo/#課題6web版-温度湿度監視システム) | DHT11 |

## 練習・サンプル

| フォルダ / ファイル | 内容 | 使う部品 |
|---|---|---|
| [gpio_button_led_toggle](gpio_button_led_toggle/) | タクトスイッチで LED をオン／オフ切り替え | LED、タクトスイッチ |
| [gpio_distance](gpio_distance/) | 距離センサーで距離 [cm] を表示（SPI） | GP2Y0A02、MCP3208 |
| [kyori](kyori/) | 距離センサーの練習用コピー | GP2Y0A02、MCP3208 |
| [ondo/sample.py](ondo/sample.py) | DHT11 の動作確認（5 秒ごとに表示） | DHT11 |
| [plus1to5.py](plus1to5.py) | Python の for 文の練習 | なし |

---

## 課題ごとの紹介

### 課題1：LED の点滅

GPIO26 に接続した LED を 1 秒ごとに点灯・消灯します。→ [gpio_led_blink](gpio_led_blink/)

### 課題5：温度・湿度自動計測システム

DHT11 で温度と湿度を 1 分ごとに計測し、`時刻, 温度, 湿度` の形式で `kadai5.csv` に追記します。→ [ondo](ondo/)

```
2026-11-06 10:06:26, 26.5, 49.2
2026-11-06 10:06:31, 26.5, 49.3
```

### 課題6：Web版 温度・湿度監視システム

課題5の CSV を Python の CGI で読み込み、matplotlib でグラフ画像を作ってブラウザに表示します。
Web サーバは Raspberry Pi 上の `python3 -m http.server --cgi 8080` です。→ [ondo/web](ondo/web/)

![課題6 Web版 温度・湿度監視システムの画面](ondo/docs/screenshot.png)

---

## 動作環境

- Raspberry Pi（Raspberry Pi OS）
- Python 3
- RPi.GPIO（Raspberry Pi OS に標準で入っています）

フォルダごとに追加で必要なもの：

```bash
sudo apt install python3-spidev       # gpio_distance, kyori（SPI も有効にする）
sudo apt install python3-matplotlib   # 課題6（グラフ作成）
```

## 使い方

```bash
git clone https://github.com/masteren/raspberry-pi.git
cd raspberry-pi/ondo        # 動かしたいフォルダへ移動
python3 kadai5.py           # 実行（Ctrl+C で終了）
```

接続方法や実行方法の詳細は、各フォルダの README を見てください。

## フォルダ構成

```
raspberry-pi/
├── gpio_led_blink/           【課題1】LED 点滅
├── gpio_button_led_toggle/   練習：スイッチで LED 切り替え
├── gpio_distance/            練習：距離センサー
├── kyori/                    練習：距離センサー（コピー）
├── ondo/                     温度・湿度センサー DHT11
│   ├── sample.py             練習：動作確認用サンプル
│   ├── kadai5.py             【課題5】計測して CSV に記録
│   ├── kadai5.csv            【課題5】計測データ
│   ├── dht11/                DHT11 ライブラリ
│   ├── web/                  【課題6】Web版 監視システム
│   │   ├── index.html
│   │   ├── style.css
│   │   ├── update.js
│   │   └── cgi-bin/graph.py
│   └── docs/screenshot.png   【課題6】画面のスクリーンショット
└── plus1to5.py               練習：for 文
```
