#!/usr/bin/env python3
# graph.py  Web版 温度・湿度監視システム（CGI）
#
# 課題5の kadai5.csv を読み込み、matplotlib でグラフ(PNG)を作成し、
# <img> タグで表示する HTML を出力する。
# Python 3.13 以降は cgi モジュールが使えないため、
# URL のパラメータは環境変数 QUERY_STRING を urllib.parse で解析する。
import os
import sys
import csv
import time
import datetime
import urllib.parse

os.environ.setdefault('MPLCONFIGDIR', '/tmp/matplotlib')   # matplotlib の作業用フォルダ
import matplotlib
matplotlib.use('Agg')                     # 画面のない CGI で描画するための設定
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ---- 設定 ----
CGI_DIR = os.path.dirname(os.path.abspath(__file__))       # web/cgi-bin
WEB_DIR = os.path.dirname(CGI_DIR)                          # web
CSV_FILE = os.path.join(WEB_DIR, '..', 'kadai5.csv')        # 課題5のCSV（webの1つ上）
PNG_FILE = os.path.join(WEB_DIR, 'graph.png')               # 作成するグラフ画像
REFRESH = 5                                                 # 自動更新の間隔（秒）

# 表示範囲（最新データからさかのぼる時間）
RANGES = [
    ('1h',  '直近1時間',  datetime.timedelta(hours=1)),
    ('6h',  '直近6時間',  datetime.timedelta(hours=6)),
    ('24h', '直近24時間', datetime.timedelta(hours=24)),
    ('all', '全データ',   None),
]


def read_csv():
    """CSV を読み込み、(時刻, 温度, 湿度) のリストを返す"""
    data = []
    with open(CSV_FILE, encoding='utf-8', newline='') as f:
        for row in csv.reader(f):
            if len(row) < 3:
                continue
            try:
                t = datetime.datetime.strptime(row[0].strip(), '%Y-%m-%d %H:%M:%S')
                data.append((t, float(row[1]), float(row[2])))
            except ValueError:                 # 形式の違う行は読み飛ばす
                continue
    return data


def make_graph(data):
    """温度（左軸）と湿度（右軸）の2軸グラフを PNG で保存する"""
    times = [d[0] for d in data]
    temps = [d[1] for d in data]
    humis = [d[2] for d in data]
    marker = 'o' if len(data) <= 60 else None   # データが少ないときは点も表示

    fig, ax1 = plt.subplots(figsize=(10, 5), dpi=100)
    ax1.plot(times, temps, color='#d62728', marker=marker, markersize=3,
             label='Temperature')
    ax1.set_ylabel('Temperature (°C)', color='#d62728')
    ax1.tick_params(axis='y', labelcolor='#d62728')
    ax1.set_ylim(min(temps) - 2, max(temps) + 2)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()                          # 右側に湿度用の軸を作る
    ax2.plot(times, humis, color='#1f77b4', marker=marker, markersize=3,
             label='Humidity')
    ax2.set_ylabel('Humidity (%)', color='#1f77b4')
    ax2.tick_params(axis='y', labelcolor='#1f77b4')
    ax2.set_ylim(min(humis) - 5, max(humis) + 5)

    # 横軸の時刻表示（1日以上なら日付も表示）
    span = times[-1] - times[0]
    fmt = '%m/%d %H:%M' if span >= datetime.timedelta(days=1) else ('%H:%M' if span >= datetime.timedelta(minutes=10) else '%H:%M:%S')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter(fmt))
    fig.autofmt_xdate()

    lines = ax1.get_lines() + ax2.get_lines()
    ax1.legend(lines, [l.get_label() for l in lines], loc='upper left')
    ax1.set_title('{} - {}'.format(times[0].strftime('%Y-%m-%d %H:%M'),
                                   times[-1].strftime('%Y-%m-%d %H:%M')))
    fig.tight_layout()
    fig.savefig(PNG_FILE)
    plt.close(fig)


def stats_row(name, unit, values):
    return ('<tr><th>{}</th><td>{:.1f}{}</td><td>{:.1f}{}</td><td>{:.1f}{}</td></tr>'
            .format(name, max(values), unit, min(values), unit,
                    sum(values) / len(values), unit))


def build_page(body):
    return '''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>Web版 温度・湿度監視システム</title>
<link rel="stylesheet" href="/style.css">
</head>
<body data-refresh="{refresh}">
<h1>Web版 温度・湿度監視システム</h1>
<div id="main">
{body}
<p class="note">{refresh}秒ごとに自動更新 ／ ページ作成：{now}</p>
</div>
<script src="/update.js"></script>
</body>
</html>'''.format(refresh=REFRESH, body=body,
                  now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def main():
    # URL のパラメータ（例: graph.py?range=6h）を取得
    query = urllib.parse.parse_qs(os.environ.get('QUERY_STRING', ''))
    key = query.get('range', ['1h'])[0]
    if key not in [r[0] for r in RANGES]:
        key = '1h'

    try:
        data = read_csv()
    except FileNotFoundError:
        return build_page('<p class="error">CSVファイルが見つかりません：{}</p>'
                          .format(os.path.normpath(CSV_FILE)))
    if not data:
        return build_page('<p class="error">CSVにデータがありません。</p>')

    latest = data[-1]
    delta = dict((r[0], r[2]) for r in RANGES)[key]
    if delta is not None:                      # 最新データから指定時間分だけ取り出す
        data = [d for d in data if d[0] >= latest[0] - delta]

    make_graph(data)

    # 表示範囲の切り替えボタン
    buttons = ''.join(
        '<a class="btn{}" href="?range={}">{}</a>'.format(
            ' active' if r[0] == key else '', r[0], r[1])
        for r in RANGES)
    # グラフ更新ボタン（押すとCSVを読み直してグラフを作り直す）
    buttons += '<a class="btn update" href="?range={}">グラフ更新</a>'.format(key)

    body = '''
<div class="cards">
  <div class="card temp"><div class="label">現在の温度</div><div class="value">{t:.1f}<span>℃</span></div></div>
  <div class="card humi"><div class="label">現在の湿度</div><div class="value">{h:.1f}<span>%</span></div></div>
  <div class="card time"><div class="label">最終計測</div><div class="value small">{at}</div></div>
</div>
<div class="buttons">{buttons}</div>
<img src="/graph.png?t={stamp}" alt="温度・湿度グラフ">
<table>
  <tr><th></th><th>最高</th><th>最低</th><th>平均</th></tr>
  {row_t}
  {row_h}
</table>
<p class="note">表示データ数：{n}件</p>
'''.format(t=latest[1], h=latest[2], at=latest[0].strftime('%Y-%m-%d %H:%M:%S'),
           buttons=buttons, stamp=int(time.time()),
           row_t=stats_row('温度', '℃', [d[1] for d in data]),
           row_h=stats_row('湿度', '%', [d[2] for d in data]),
           n=len(data))
    return build_page(body)


if __name__ == '__main__':
    page = main()
    sys.stdout.reconfigure(encoding='utf-8')
    print('Content-Type: text/html; charset=utf-8')
    print()                                    # ヘッダーの終わりは空行
    print(page)
