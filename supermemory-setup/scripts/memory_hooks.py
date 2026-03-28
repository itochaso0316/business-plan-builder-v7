"""
CCC内のCodex/OpenClaw呼び出しラッパーに差し込むMemory Hook
既存の呼び出しコードのbefore/afterに追加する
"""

import os
import httpx
from datetime import date

SUPERMEMORY_API_KEY = os.environ.get("SUPERMEMORY_API_KEY")
BASE_URL = "https://api.supermemory.ai/v3"

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

def _h():
    return {"Authorization": f"Bearer {SUPERMEMORY_API_KEY}", "Content-Type": "application/json"}

# ──────────────────────────────────────────
# BEFORE: Codex/Claude Code 呼び出し前に実行
# 過去の設計判断をcontextとして取得
# ──────────────────────────────────────────
def memory_read_context(channel_id: str, task_summary: str) -> str:
    """
    既存のCodex/Claude Code呼び出しの直前に実行。
    返り値をシステムプロンプトの末尾に追加する。
    """
    space = get_space(channel_id)
    params = {"q": task_summary, "spaces": space, "limit": 5}
    resp = httpx.get(f"{BASE_URL}/memories/search", headers=_h(), params=params)

    if resp.status_code != 200 or not resp.json().get("results"):
        return ""  # 記憶なし → 何も追加しない

    results = resp.json()["results"]
    lines = ["\n\n## 過去の設計判断・実行記録（Supermemory）\n"]
    lines.append("以下は過去にこのプロジェクトで記録された情報です。矛盾しないよう参照してください：\n")
    for r in results:
        lines.append(f"---\n{r.get('content', '')}\n")
    return "\n".join(lines)


# ──────────────────────────────────────────
# AFTER: Codex設計完了後に実行
# ──────────────────────────────────────────
def memory_write_design(channel_id: str, title: str, decision: str,
                         reason: str, rejected: str = "", notes: str = "") -> bool:
    """
    Codexの設計出力が返ってきた直後に実行。
    """
    space = get_space(channel_id)
    content = f"""[DESIGN] {title}
date: {date.today()}
決定事項:
{decision}
理由: {reason}
却下した選択肢: {rejected or 'なし'}
次回の注意点: {notes or 'なし'}"""

    payload = {"content": content, "spaces": [space], "tags": ["design", space]}
    resp = httpx.post(f"{BASE_URL}/memories", headers=_h(), json=payload)
    return resp.status_code in (200, 201)


# ──────────────────────────────────────────
# AFTER: OpenClaw実行完了後に実行
# ──────────────────────────────────────────
def memory_write_execution(channel_id: str, task_name: str, success: bool,
                            learned: str, config: str = "", failure_reason: str = "") -> bool:
    """
    OpenClawのタスクが完了した直後に実行。
    """
    space = get_space(channel_id)
    content = f"""[EXECUTION] {task_name}
date: {date.today()}
結果: {"成功" if success else "失敗"}
有効だった設定: {config or 'なし'}
学んだこと: {learned}
失敗原因: {failure_reason or 'なし'}"""

    payload = {"content": content, "spaces": [space], "tags": ["execution", space]}
    resp = httpx.post(f"{BASE_URL}/memories", headers=_h(), json=payload)
    return resp.status_code in (200, 201)


# ──────────────────────────────────────────
# 使い方サンプル（既存コードへの差し込みイメージ）
# ──────────────────────────────────────────
"""
# ── 既存のCodex呼び出しコード（変更前） ──
def call_codex(channel_id, task):
    prompt = build_prompt(task)
    result = codex_api.call(prompt)
    return result

# ── 変更後（3行追加するだけ） ──
def call_codex(channel_id, task):
    past_context = memory_read_context(channel_id, task)   # 追加①
    prompt = build_prompt(task) + past_context              # 追加②
    result = codex_api.call(prompt)
    memory_write_design(channel_id, task, result, ...)      # 追加③
    return result

# ── 既存のOpenClaw呼び出しコード（変更前） ──
def call_openclaw(channel_id, crawler_task):
    result = openclaw.run(crawler_task)
    return result

# ── 変更後（2行追加するだけ） ──
def call_openclaw(channel_id, crawler_task):
    past_context = memory_read_context(channel_id, crawler_task)  # 追加①
    result = openclaw.run(crawler_task, context=past_context)      # 追加②
    memory_write_execution(channel_id, crawler_task,               # 追加③
                           success=result.ok, learned=result.notes)
    return result
"""
