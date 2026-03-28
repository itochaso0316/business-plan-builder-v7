# Supermemory セットアップ手順

## 所要時間: 約1時間

---

## Step 1: API Key を環境変数に追加（5分）

Mac mini の `~/.zshrc` または `~/.bashrc` に追記：

```bash
export SUPERMEMORY_API_KEY="your_api_key_here"
```

反映：
```bash
source ~/.zshrc
```

---

## Step 2: Space を11個作成（5分）

```bash
cd supermemory-setup/scripts
pip install httpx
SUPERMEMORY_API_KEY=$SUPERMEMORY_API_KEY python3 create_spaces.py
```

出力されるSpace IDをメモしておく（後でCLAUDE.mdに書く）

---

## Step 3: MCP設定を追加（10分）

CCCのMCP設定ファイルに `mcp-config/mcp.json` の内容をマージ：

```bash
# 既存のmcp.jsonがある場合はマージ
# ない場合はそのままコピー
cp mcp-config/mcp.json /path/to/your/ccc/.mcp.json
```

---

## Step 4: 各チャンネルのCLAUDE.mdに追記（20分）

`claude-md-snippets/memory-section.md` の内容を各CLAUDE.mdの末尾に追加。

**チャンネルごとに変える箇所は1行だけ：**
```
SPACE_NAME: "emilus"  ← ここをチャンネルに合わせて変える
```

変更一覧：
| CLAUDE.md | SPACE_NAME |
|-----------|------------|
| emilus/CLAUDE.md | "emilus" |
| baca-japan/CLAUDE.md | "baca-japan" |
| hj-ax/CLAUDE.md | "hj-ax" |
| misao/CLAUDE.md | "misao" |
| zero-emi/CLAUDE.md | "zero-emi" |
| inter-holdings/CLAUDE.md | "inter-holdings" |
| elena/CLAUDE.md | "elena" |
| ai-farm/CLAUDE.md | "ai-farm" |
| line-memory/CLAUDE.md | "line-memory" |
| amazon-oem/CLAUDE.md | "amazon-oem" |
| claude-code/CLAUDE.md | "ccc-dev" |

---

## Step 5: Discordボットにコマンド追加（15分）

`discord-commands/memory_commands.py` を既存のボットコードに追加。

`CHANNEL_SPACE_MAP` の `CHANNEL_ID_*` を実際のDiscord channel IDに書き換える：

```python
# Discord Developer Portal または右クリック「IDをコピー」で取得
CHANNEL_SPACE_MAP = {
    "123456789012345678": "emilus",   # 実際のIDに変更
    ...
}
```

既存のon_messageハンドラに1行追加：
```python
async def on_message(message):
    response = await handle_memory_command(str(message.channel.id), message.content)
    if response:
        await message.channel.send(response)
        return
    # 既存の処理を続ける...
```

---

## Step 6: Codex/OpenClaw呼び出しにhookを追加（10分）

`scripts/memory_hooks.py` を参照して、既存の呼び出しコードに3行追加。

---

## 動作確認

```
# Discordで試す
/remember テスト: セットアップ完了
/recall テスト
/memory-status
```

---

## トラブルシューティング

**API key エラー**
→ `echo $SUPERMEMORY_API_KEY` で確認

**Space が見つからない**
→ `create_spaces.py` を再実行

**MCP が認識されない**
→ CCCを再起動
