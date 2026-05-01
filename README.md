# Business Plan Builder v7

> 経営者と対話しながら事業計画を共同構築するマルチエージェント経営会議システム — Claude Code / Anthropic Agent SDK 対応

## 主な機能

- **8フェーズの対話型プロセス** — Phase 0（資料読み込み）から Phase 5（最終アウトプット）まで一貫して伴走
- **専門家チームの並列起動** — CFO・CMO・CTO・CPO・弁護士・AI専門家など100+候補から動的に招集し、Claude Agent SDK で同時グリリング
- **競合CEOペルソナ生成** — 競合企業のCEOを仮想人物として起動し、敵の目線からの事業検証を実施
- **補助金・助成金マッチング** — Hojokin MCP連携で事業計画から利用可能な補助金を自動判定
- **既存データ直結分析** — Shopify / GA4 / Airtable 等のMCP連携で実データをリアルタイム活用

## インストール手順

### 前提条件

- [Claude Code](https://claude.ai/code) がインストール済みであること
- Anthropic API キーが設定済みであること

### セットアップ

```bash
# 1. リポジトリをクローン
git clone https://github.com/itochaso0316/business-plan-builder-v7.git
cd business-plan-builder-v7

# 2. Claude Code でプロジェクトを開く
claude

# 3. セッションを開始する
> 事業計画を一緒に作りたい
```

### スキルとして利用する場合

```bash
# skill ファイルをインストール
/plugin add business-plan-builder-v7.skill
```

詳細なセットアップ手順・設定オプションは **[セットアップ & 運用ガイド](guide.html)** を参照してください。

## フロー概要

```
Phase 0   → 既存資料の読み込み（矛盾・空白の特定）
Phase 0.5 → デスクトップリサーチ（仮説構築・競合4層マッピング）
Phase 0.7 → データソース棚卸し・MCP連携セットアップ
Phase 1   → 深層ヒアリング（10カテゴリ）
Phase 1.5 → 専門家チーム編成・競合CEOペルソナ生成
Phase 2   → 専門家グリリング（Agent並列起動 / 3ラウンド）
Phase 3   → 市場・競合・法規制リサーチ
Phase 4   → 事業計画書 共同執筆
Phase 4.3 → 補助金・助成金マッチング（Hojokin MCP）
Phase 4.5 → 実現可能性ストレステスト（Agent並列起動）
Phase 5   → 最終アウトプット生成
Phase 6   → イテレーション（再経営会議）
```

## ファイル構成

```
guide.html              ← セットアップ & 運用ガイド（HTML版）
CLAUDE.md               ← Claude Code 向け制御指示
business-plan-builder-SPEC.md ← 詳細仕様書
references/             ← フェーズ別質問集・調査ガイド・法規制リスト
personas/               ← 専門家定義・競合CEOテンプレート
agent-prompts/          ← Agentラウンド別プロンプトテンプレート
frameworks/             ← ビジネスフレームワーク集
output-templates/       ← アウトプット仕様・PPTデザインガイド
docs/                   ← ケーススタディ等
```

## ライセンス

MIT License — 詳細は [LICENSE](LICENSE) を参照してください。
