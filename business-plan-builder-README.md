# Business Plan Builder

> 経営者と対話しながら事業計画を共同構築するClaude Codeエージェント

## できること

- **8フェーズの対話型プロセス**で事業計画を一から作る
- 業種・目的に応じた**専門家チーム（100+候補）を動的に招集**
- **補佐CEO・通訳・議事録係**が常駐してディスカッションをサポート
- **既存顧客データ**をMCP連携で直接分析（Shopify / GA4など）
- 未開拓市場では**想定ペルソナを一緒に構築**
- **AI活用前提の事業計画**を設計 + Claude Code向け仕様書を出力
- PPTは**AI臭くならないデザイン**で生成（テンプレート踏襲対応）
- 経営者が**腑に落ちるまで何度でも**ディスカッションを繰り返す

## クイックスタート

```bash
# 1. Skillをインストール
/plugin add business-plan-builder.skill

# 2. 依存Skillをインストール
/plugin marketplace add anthropics/skills
/plugin install pptx@skills docx@skills xlsx@skills

# 3. Claude Codeを起動して話しかける
claude
> 事業計画を一緒に作りたい
```

## フロー概要

```
Phase 0   → 既存資料の読み込み
Phase 0.5 → デスクトップリサーチ（仮説構築・叩き台）
Phase 1   → 深層ヒアリング（10カテゴリ）
Phase 1.5 → 専門家チーム編成
Phase 2   → 専門家会議（分析・提案・納得ループ）
Phase 3   → 市場・競合・法規制リサーチ（本格版）
Phase 4   → 事業計画書 共同ブラッシュアップ
Phase 5   → 最終アウトプット生成
```

詳細は **[SPEC.md](SPEC.md)** を参照。

## 推奨MCP

| MCP | 用途 |
|-----|------|
| Web Search | リサーチ（Phase 0.5・3） |
| Shopify | 既存EC事業の顧客データ |
| Canva | スライド生成 |
| Slack | 議事録共有 |

## ファイル構成

```
SKILL.md                    ← メイン制御
SPEC.md                     ← この仕様書
references/                 ← 質問集・ガイド・法規制
personas/                   ← 専門家定義・ファシリテーター
frameworks/                 ← ビジネスフレームワーク
output-templates/           ← アウトプット仕様・PPT設計ガイド
```

## ライセンス

AI Farm株式会社 / 改変・再配布は自由
