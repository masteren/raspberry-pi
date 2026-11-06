// update.js  ページ全体を再読み込みせずに、グラフと数値だけを更新する
//
// 1. graph.py をバックグラウンドで呼び出す（CSVを読み直し、graph.pngを作り直す）
// 2. 新しいグラフ画像を先に読み込んでおく
// 3. 読み込みが終わってから、表示中の内容をまとめて入れ替える
// → 画面が一瞬白くなる（ちらつく）ことがない

const REFRESH = Number(document.body.dataset.refresh) * 1000;   // 更新間隔（ミリ秒）

async function updateGraph() {
  try {
    const res = await fetch(location.href, { cache: 'no-store' });
    const html = await res.text();
    const doc = new DOMParser().parseFromString(html, 'text/html');
    const newMain = doc.getElementById('main');
    if (!newMain) return;

    const img = newMain.querySelector('img');
    const preload = new Image();
    preload.onload = () => {
      // 画像の読み込みが終わってから入れ替える
      document.getElementById('main').innerHTML = newMain.innerHTML;
    };
    preload.src = img ? img.getAttribute('src') : '';
    if (!img) document.getElementById('main').innerHTML = newMain.innerHTML;
  } catch (e) {
    console.log('更新失敗:', e);
  }
}

// 一定時間ごとに自動更新
if (REFRESH > 0) setInterval(updateGraph, REFRESH);

// 「グラフ更新」ボタン：ページを再読み込みせずにすぐ更新する
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('update')) {
    e.preventDefault();
    updateGraph();
  }
});
