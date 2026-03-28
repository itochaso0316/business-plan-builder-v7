#!/usr/bin/env python3
"""
Supermemory Space一括作成スクリプト
使い方: SUPERMEMORY_API_KEY=your_key python3 create_spaces.py
"""

import os
import httpx
import json

API_KEY = os.environ.get("SUPERMEMORY_API_KEY")
BASE_URL = "https://api.supermemory.ai/v3"

SPACES = [
    {"name": "emilus",          "description": "EMILUSブランド - Rakuten/Amazon EC, スカルプケア化粧水"},
    {"name": "baca-japan",      "description": "Baca Japan - マレーシア/インドネシア政府情報メディア"},
    {"name": "hj-ax",           "description": "HJ社AXDept - Claude Enterprise社内AI導入"},
    {"name": "misao",           "description": "操レディスホスピタル - Web/マーケティング"},
    {"name": "zero-emi",        "description": "ゼロエミ - 廃棄物マッチングNPOシステム"},
    {"name": "inter-holdings",  "description": "Inter Holdings - 農水省企画競争対応"},
    {"name": "elena",           "description": "Elena Co. - Amazon OEM/PB事業"},
    {"name": "ai-farm",         "description": "AI Farm株式会社 - 全社プロジェクト共通"},
    {"name": "line-memory",     "description": "LINE-MEMORY - LINE→Slack通知bot"},
    {"name": "amazon-oem",      "description": "Amazon OEM - Keepa/SellerSprite自動調査"},
    {"name": "ccc-dev",         "description": "Claude Code Channels開発 - アーキテクチャ/変更履歴"},
]

def create_space(name: str, description: str) -> dict:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": name,
        "description": description
    }
    resp = httpx.post(f"{BASE_URL}/spaces", headers=headers, json=payload)
    return {"name": name, "status": resp.status_code, "body": resp.json()}

def main():
    if not API_KEY:
        print("ERROR: SUPERMEMORY_API_KEY が設定されていません")
        print("実行方法: SUPERMEMORY_API_KEY=your_key python3 create_spaces.py")
        return

    print(f"Supermemory Space を {len(SPACES)} 個作成します...\n")
    results = []

    for space in SPACES:
        result = create_space(space["name"], space["description"])
        results.append(result)
        status = "✓" if result["status"] in (200, 201) else "✗"
        print(f"  {status} {space['name']} (HTTP {result['status']})")

    print(f"\n完了: {sum(1 for r in results if r['status'] in (200,201))}/{len(SPACES)} 成功")

    # space_id一覧を出力（CLAUDE.mdのマッピングに使う）
    print("\n--- Space ID 一覧（CLAUDE.mdに記載用）---")
    for r in results:
        if r["status"] in (200, 201):
            sid = r["body"].get("id", "N/A")
            print(f'  "{r["name"]}": "{sid}"')

if __name__ == "__main__":
    main()
