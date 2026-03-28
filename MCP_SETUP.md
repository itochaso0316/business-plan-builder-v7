# Hojokin MCP サーバー セットアップガイド

## 概要
Business Plan Builder v7 から補助金・助成金マッチングMCPサーバーに接続します。
Phase 4で事業計画が固まった段階で、自動で補助金を判定→申請書テンプレート生成ができます。

## セットアップ手順

### 1. hojokin-mcp をインストール
```bash
pip install hojokin-mcp
```

### 2. Claude Codeの設定確認
`.claude/settings.json` は設定済みです。追加作業は不要です。

### 3. 使い方
Claude Codeセッション中に以下のような質問をすると、MCPツールが自動で呼ばれます:

```
「東京都の製造業、従業員10名で使える補助金を教えて」
→ hojokin_match が呼ばれ、該当補助金をリスト表示

「小規模事業者持続化補助金の申請要件を教えて」
→ hojokin_requirements が呼ばれ、要件・必要書類を表示

「この事業計画に基づいて補助金申請書のドラフトを作って」
→ hojokin_plan_draft が呼ばれ、テンプレートを返却
```

## 利用可能なMCPツール

| ツール | 説明 |
|--------|------|
| `hojokin_match` | 企業情報から該当補助金をマッチング |
| `hojokin_requirements` | 補助金の申請要件・必要書類を取得 |
| `hojokin_checklist` | 申請準備チェックリストを生成 |
| `hojokin_plan_draft` | 事業計画書テンプレートを生成 |

## Phase 4.3 での自動フロー

BPBのPhase 4（事業計画書の共同執筆）完了後、以下が自動提案されます:
1. 補助金マッチング → 該当補助金リスト
2. 申請要件確認 → 必要書類・審査基準
3. 計画書ドラフト → テンプレート生成
4. チェックリスト → 申請準備手順

## トラブルシューティング

### `hojokin-mcp` コマンドが見つからない
```bash
pip install hojokin-mcp
# または
pip install --user hojokin-mcp
```

### MCPサーバーに接続できない
Supabaseの接続情報は `.claude/settings.json` に設定済みです。
ローカルJSONフォールバックがあるので、Supabase接続なしでも基本機能は動きます。
