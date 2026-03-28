# ============================================================
# SUPERMEMORY — このセクションを各チャンネルのCLAUDE.mdに追記
# SPACE_NAME は各チャンネルに合わせて書き換える
# ============================================================

## Memory Configuration

SPACE_NAME: "ai-farm"  # ← チャンネルごとにここだけ変える

## Space マッピング表（全チャンネル共通参照用）

| Discordチャンネル    | Space名         |
|---------------------|----------------|
| #emilus             | emilus         |
| #baca-japan         | baca-japan     |
| #hj-ax              | hj-ax          |
| #misao-hospital     | misao          |
| #zero-emi           | zero-emi       |
| #inter-holdings     | inter-holdings |
| #elena              | elena          |
| #ai-farm            | ai-farm        |
| #line-memory        | line-memory    |
| #amazon-oem         | amazon-oem     |
| #claude-code        | ccc-dev        |

---

## Memory Rules — 必ず従うこと

### 1. タスク開始時（READ — 毎回必須）

タスクを受け取ったら、コーディングや設計を始める前に必ず実行：

```
mcp__supermemory__search(
  query = タスクの概要キーワード,
  spaces = [SPACE_NAME]
)
```

取得した結果を「過去のコンテキスト」としてプロンプトに含める。
関連する記憶がなければそのままタスクを進める。

### 2. Codex設計完了時（WRITE — 必須）

Codexが設計・アーキテクチャ判断を出したら即座にwrite：

```
mcp__supermemory__add(
  content = """
[DESIGN] {タイトル}
date: {YYYY-MM-DD}
決定事項:
- {箇条書き}
理由: {なぜそうしたか}
却下した選択肢: {何を捨てたか・なぜ}
次回の注意点: {引き継ぎ事項}
  """,
  spaces = [SPACE_NAME],
  tags = ["design", SPACE_NAME]
)
```

### 3. Claude Code実装完了時（WRITE — 重要な変更のみ）

アーキテクチャに影響する実装が完了したとき：

```
mcp__supermemory__add(
  content = """
[IMPL] {タイトル}
date: {YYYY-MM-DD}
実装内容: {何を作ったか}
ファイル: {主要な変更ファイル}
依存関係: {新たに追加したもの}
注意点: {次の実装者が知るべきこと}
  """,
  spaces = [SPACE_NAME],
  tags = ["impl", SPACE_NAME]
)
```

### 4. OpenClaw実行完了時（WRITE — 必須）

クローラー・cronタスクが完了したとき：

```
mcp__supermemory__add(
  content = """
[EXECUTION] {タスク名}
date: {YYYY-MM-DD}
結果: 成功 / 失敗
有効だった設定: {具体的なパラメータ・設定値}
学んだこと: {次回に活きる知見}
失敗原因（失敗時）: {何がダメだったか}
  """,
  spaces = [SPACE_NAME],
  tags = ["execution", SPACE_NAME]
)
```

### 5. 矛盾検知時（READ + 通知）

自分の出力が過去の記録と矛盾すると気づいたとき：

```
mcp__supermemory__search(
  query = 矛盾している内容のキーワード,
  spaces = [SPACE_NAME]
)
```

結果をユーザーに明示：
「⚠️ 過去の記録と異なります: {正しい情報} / 記録日: {date}」

---

## Memory Format Rules

- writeする内容は必ず上記フォーマットを使う（タグで検索しやすくするため）
- 数字・金額・日付は必ず含める（事実として参照されるため）
- 「なぜそうしたか」の理由は省略しない（Codexが次回参照するため）
- 1回のwriteは1つのトピックに絞る（検索精度を上げるため）
