# GPIOでLEDの点滅

Raspberry Pi の GPIO26 に接続した LED を 1 秒ごとに点灯・消灯するプログラムです。

## ファイル

- `12I_kadai1_led.py`: 提出用 Python プログラム

## 接続

- GPIO26: 抵抗を通して LED のプラス側へ接続
- GND: LED のマイナス側へ接続
- 外付け LED を使う場合は、LED に直列で抵抗を入れてください

## 実行方法

```bash
python3 12I_kadai1_led.py
```

終了するときは `Ctrl+C` を押してください。終了時に GPIO の設定を初期化します。

## 中文说明

这个程序用于让连接在 Raspberry Pi GPIO26 上的 LED 每隔 1 秒闪烁一次。

### 文件

- `12I_kadai1_led.py`: 提交用的 Python 程序

### 接线方法

- GPIO26: 通过电阻连接到 LED 的正极
- GND: 连接到 LED 的负极
- 如果使用外接 LED，请把电阻和 LED 串联，避免 LED 损坏

### 运行方法

在 Raspberry Pi 上进入本文件夹后执行：

```bash
python3 12I_kadai1_led.py
```

如果要停止程序，按 `Ctrl+C`。程序结束时会自动清理 GPIO 设置。
