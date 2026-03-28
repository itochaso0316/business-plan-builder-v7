"""
Discord Supermemory コマンド実装
既存のDiscordボット（Claude Code Channels）に追加するコマンド群

CHANNEL_SPACE_MAP に実際のchannel_idを設定してから使う
"""

import os
import httpx
from datetime import date

SUPERMEMORY_API_KEY = os.environ.get("SUPERMEMORY_API_KEY")
BASE_URL = "https://api.supermemory.ai/v3"

# channel_id → space名 マッピング
# 実際のDiscord channel_idに書き換える
CHANNEL_SPACE_MAP = {
    "CHANNEL_ID_EMILUS":         "emilus",
    "CHANNEL_ID_BACA_JAPAN":     "baca-japan",
    "CHANNEL_ID_HJ_AX":          "hj-ax",
    "CHANNEL_ID_MISAO":          "misao",
    "CHANNEL_ID_ZERO_EMI":       "zero-emi",
    "CHANNEL_ID_INTER_HOLDINGS": "inter-holdings",
    "CHANNEL_ID_ELENA":          "elena",
    "CHANNEL_ID_AI_FARM":        "ai-farm",
    "CHANNEL_ID_LINE_MEMORY":    "line-memory",
    "CHANNEL_ID_AMAZON_OEM":     "amazon-oem",
    "CHANNEL_ID_CCC_DEV":        "ccc-dev",
}

def get_space(channel_id: str) -> str:
    return CHANNEL_SPACE_MAP.get(str(channel_id), "ai-farm")

def _headers() -> dict:
    return {
        "Authorization": f"Bearer {SUPERMEMORY_API_KEY}",
        "Content-Type": "application/json"
    }

# ──────────────────────────────────────────
# /remember [内容]
# 現在のchannelのSpaceに記憶を保存
# ──────────────────────────────────────────
async def cmd_remember(channel_id: str, content: str) -> str:
    space = get_space(channel_id)
    payload = {
        "content": f"[FACT] {content}\ndate: {date.today()}",
        "spaces": [space],
        "tags": ["fact", space]
    }
    resp = httpx.post(f"{BASE_URL}/memories", headers=_headers(), json=payload)
    if resp.status_code in (200, 201):
        return f"✓ `{space}` に記憶しました"
    return f"✗ 失敗 (HTTP {resp.status_code}): {resp.text}"

# ──────────────────────────────────────────
# /recall [キーワード]
# 現在のSpaceで検索して返す
# ──────────────────────────────────────────
async def cmd_recall(channel_id: str, query: str) -> str:
    space = get_space(channel_id)
    params = {"q": query, "spaces": space, "limit": 5}
    resp = httpx.get(f"{BASE_URL}/memories/search", headers=_headers(), params=params)
    if resp.status_code != 200:
        return f"✗ 検索失敗 (HTTP {resp.status_code})"

    results = resp.json().get("results", [])
    if not results:
        return f"🔍 `{space}` に「{query}」に関する記憶はありません"

    lines = [f"🔍 `{space}` の検索結果 ({len(results)}件):\n"]
    for i, r in enumerate(results, 1):
        content = r.get("content", "")[:200]
        lines.append(f"**{i}.** {content}\n")
    return "\n".join(lines)

# ──────────────────────────────────────────
# /decision [タイトル] [内容]
# 設計判断を記録（Codexが次回参照する）
# ──────────────────────────────────────────
async def cmd_decision(channel_id: str, title: str, content: str) -> str:
    space = get_space(channel_id)
    formatted = f"""[DESIGN] {title}
date: {date.today()}
決定事項: {content}
記録者: Kosuke (手動)"""
    payload = {
        "content": formatted,
        "spaces": [space],
        "tags": ["design", space, "manual"]
    }
    resp = httpx.post(f"{BASE_URL}/memories", headers=_headers(), json=payload)
    if resp.status_code in (200, 201):
        return f"✓ 設計判断を `{space}` に記録しました\n```\n{title}\n```"
    return f"✗ 失敗 (HTTP {resp.status_code})"

# ──────────────────────────────────────────
# /factcheck [内容]
# 過去の記録と照合して矛盾を指摘
# ──────────────────────────────────────────
async def cmd_factcheck(channel_id: str, claim: str) -> str:
    space = get_space(channel_id)
    params = {"q": claim, "spaces": space, "limit": 3}
    resp = httpx.get(f"{BASE_URL}/memories/search", headers=_headers(), params=params)
    if resp.status_code != 200:
        return f"✗ 検索失敗"

    results = resp.json().get("results", [])
    if not results:
        return f"📋 `{space}` に関連する記録なし。新しい情報として `/remember` で登録できます"

    lines = [f"📋 「{claim}」に関する過去の記録:\n"]
    for r in results:
        content = r.get("content", "")[:300]
        lines.append(f"```\n{content}\n```\n")
    lines.append("矛盾がある場合は `/memory-fix` で修正してください")
    return "\n".join(lines)

# ──────────────────────────────────────────
# /memory-status
# 全Spaceの状態を一覧表示
# ──────────────────────────────────────────
async def cmd_memory_status() -> str:
    lines = ["📊 **Supermemory Space 状態**\n"]
    for channel_label, space in [
        ("#emilus",          "emilus"),
        ("#baca-japan",      "baca-japan"),
        ("#hj-ax",           "hj-ax"),
        ("#misao-hospital",  "misao"),
        ("#zero-emi",        "zero-emi"),
        ("#inter-holdings",  "inter-holdings"),
        ("#elena",           "elena"),
        ("#ai-farm",         "ai-farm"),
        ("#line-memory",     "line-memory"),
        ("#amazon-oem",      "amazon-oem"),
        ("#claude-code",     "ccc-dev"),
    ]:
        resp = httpx.get(
            f"{BASE_URL}/memories/search",
            headers=_headers(),
            params={"q": "*", "spaces": space, "limit": 1}
        )
        count = resp.json().get("total", "?") if resp.status_code == 200 else "error"
        lines.append(f"  `{space}` ({channel_label}): {count}件")
    return "\n".join(lines)

# ──────────────────────────────────────────
# /memory-fix [キーワード] [修正内容]
# 該当記憶を削除して新しい内容でwrite
# ──────────────────────────────────────────
async def cmd_memory_fix(channel_id: str, keyword: str, new_content: str) -> str:
    space = get_space(channel_id)

    # 旧記憶を検索
    params = {"q": keyword, "spaces": space, "limit": 1}
    resp = httpx.get(f"{BASE_URL}/memories/search", headers=_headers(), params=params)
    results = resp.json().get("results", []) if resp.status_code == 200 else []

    deleted = False
    if results:
        old_id = results[0].get("id")
        if old_id:
            del_resp = httpx.delete(f"{BASE_URL}/memories/{old_id}", headers=_headers())
            deleted = del_resp.status_code in (200, 204)

    # 新しい内容でwrite
    payload = {
        "content": f"[FACT] {new_content}\ndate: {date.today()}\n(修正済み: {keyword})",
        "spaces": [space],
        "tags": ["fact", "correction", space]
    }
    add_resp = httpx.post(f"{BASE_URL}/memories", headers=_headers(), json=payload)
    if add_resp.status_code in (200, 201):
        action = "旧記憶を削除して更新" if deleted else "新規追加（旧記憶が見つからず）"
        return f"✓ `{space}` の記憶を修正しました ({action})\n```\n{new_content}\n```"
    return f"✗ 更新失敗"


# ──────────────────────────────────────────
# Discord コマンドルーター
# 既存botのon_message等から呼び出す
# ──────────────────────────────────────────
async def handle_memory_command(channel_id: str, message: str) -> str | None:
    msg = message.strip()

    if msg.startswith("/remember "):
        return await cmd_remember(channel_id, msg[10:].strip())

    elif msg.startswith("/recall "):
        return await cmd_recall(channel_id, msg[8:].strip())

    elif msg.startswith("/decision "):
        parts = msg[10:].strip().split(" ", 1)
        title = parts[0] if parts else "無題"
        content = parts[1] if len(parts) > 1 else ""
        return await cmd_decision(channel_id, title, content)

    elif msg.startswith("/factcheck "):
        return await cmd_factcheck(channel_id, msg[11:].strip())

    elif msg.strip() == "/memory-status":
        return await cmd_memory_status()

    elif msg.startswith("/memory-fix "):
        parts = msg[12:].strip().split(" ", 1)
        keyword = parts[0] if parts else ""
        new_content = parts[1] if len(parts) > 1 else ""
        return await cmd_memory_fix(channel_id, keyword, new_content)

    return None  # メモリコマンドでなければNoneを返す
