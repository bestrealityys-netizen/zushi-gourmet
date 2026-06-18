#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""template.html の __DATA__ に data/restaurants.json を差し込み index.html を生成する。
index.html は直接編集せず、必ずこのスクリプトで再生成すること。"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data", "restaurants.json")
TEMPLATE = os.path.join(ROOT, "template.html")
OUTPUT = os.path.join(ROOT, "index.html")


def main():
    with open(DATA, "r", encoding="utf-8") as f:
        data = json.load(f)  # 妥当性確認を兼ねて読み込み

    n = len(data.get("restaurants", []))
    if n == 0:
        sys.exit("restaurants が空です。")

    with open(TEMPLATE, "r", encoding="utf-8") as f:
        tpl = f.read()
    if "__DATA__" not in tpl:
        sys.exit("template.html に __DATA__ プレースホルダがありません。")

    # JSON を JS リテラルとして安全に埋め込む
    payload = json.dumps(data, ensure_ascii=False)
    payload = payload.replace("</", "<\\/")  # </script> 対策
    html = tpl.replace("__DATA__", payload)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

    # 生成物の簡易検証
    assert html.lstrip().startswith("<!DOCTYPE"), "先頭が DOCTYPE ではありません"
    assert html.rstrip().endswith("</html>"), "末尾が </html> ではありません"
    size = os.path.getsize(OUTPUT)
    print(f"OK index.html を生成: {n}件 / {size:,} bytes")


if __name__ == "__main__":
    main()
