#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
轻触开关控制 LED（Toggle 切换式）
タクトスイッチによる LED 制御（オルタネイト型）
LED Toggle Control with Tactile Switch

硬件 / ハードウェア / Hardware:
  - LED  → GPIO18（针12 / ピン12 / Pin 12），内置限流电阻 / 電流制限抵抗内蔵 / Built-in current resistor
  - 开关 → GPIO26（针37 / ピン37 / Pin 37），上拉电阻接法 / プルアップ接続 / Pull-up wiring

按一次开关 LED 点亮，再按一次 LED 熄灭。
スイッチを1回押すと LED が点灯、もう1回押すと消灯。
Press once to turn the LED on, press again to turn it off.
"""

import RPi.GPIO as GPIO
import time

# ── 引脚定义 / ピン定義 / Pin Definition ─────────────────
LED_PIN    = 18   # LED 控制引脚 / LED 制御ピン / LED control pin（BCM）
BUTTON_PIN = 26   # 开关输入引脚 / スイッチ入力ピン / Button input pin（BCM）

# ── 消抖时间 / チャタリング防止時間 / Debounce Time ────────
DEBOUNCE_MS = 200  # 单位毫秒 / ミリ秒単位 / in milliseconds

# ── LED 状态变量 / LED 状態変数 / LED State Variable ──────
led_state = False  # False = 熄灭/消灯/OFF，True = 点亮/点灯/ON


def button_callback(channel):
    """
    下降沿中断回调 / 立下りエッジ割り込みコールバック / Falling-edge interrupt callback
    消抖由 add_event_detect 的 bouncetime 参数负责。
    チャタリング防止は add_event_detect の bouncetime パラメータが担当。
    Debouncing is handled by the bouncetime parameter in add_event_detect.
    """
    global led_state

    # 切换 LED 状态 / LED 状態をトグル / Toggle LED state
    led_state = not led_state
    GPIO.output(LED_PIN, GPIO.HIGH if led_state else GPIO.LOW)

    if led_state:
        print("[按键/ボタン/Button] LED 点亮 / 点灯 / ON")
    else:
        print("[按键/ボタン/Button] LED 熄灭 / 消灯 / OFF")


def main():
    # ── GPIO 初始化 / GPIO 初期化 / GPIO Initialization ──
    GPIO.setmode(GPIO.BCM)      # 使用 BCM 编号 / BCM 番号を使用 / Use BCM numbering
    GPIO.setwarnings(False)     # 关闭占用警告 / 使用警告を無効化 / Suppress warnings

    # 配置 LED 引脚为输出，初始低电平（熄灭）
    # LED ピンを出力に設定、初期値は LOW（消灯）
    # Set LED pin as output, initial state LOW (OFF)
    GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)

    # 配置开关引脚为输入，启用内部上拉
    # スイッチピンを入力に設定、内部プルアップを有効化
    # Set button pin as input with internal pull-up enabled
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # 注册下降沿中断（含消抖）/ 立下りエッジ割り込みを登録（チャタリング防止付き）
    # Register falling-edge interrupt with debounce
    GPIO.add_event_detect(
        BUTTON_PIN,
        GPIO.FALLING,
        callback=button_callback,
        bouncetime=DEBOUNCE_MS
    )

    print("程序已启动 / プログラム起動完了 / Program started")
    print("按 Ctrl+C 退出 / Ctrl+C で終了 / Press Ctrl+C to exit")

    try:
        # 主循环：保持运行，逻辑由中断回调驱动
        # メインループ：実行を維持、ロジックは割り込みコールバックが担当
        # Main loop: keep running, logic is driven by interrupt callback
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        # 捕获 Ctrl+C，优雅退出 / Ctrl+C を検出、正常終了 / Caught Ctrl+C, exiting gracefully
        print("\n正在退出… / 終了中… / Exiting…")

    finally:
        # 释放 GPIO 资源 / GPIO リソースを解放 / Release GPIO resources
        GPIO.cleanup()
        print("GPIO 已清理 / GPIO クリーンアップ完了 / GPIO cleaned up")


if __name__ == "__main__":
    main()
