# Business Plan Builder — Claude Code 実行仕様書

**バージョン**: v5.0  
**対象**: Claude Code（他人の環境でも動作可能な設計）  
**最終更新**: 2026-03

---

## 1. このシステムの概要

経営者・起業家との対話を通じて事業計画を共同構築するAIエージェントシステム。

### 何をするか

1. 経営者との深いヒアリング対話（Phase 0〜1）
2. 事前リサーチで会話の叩き台を作成（Phase 0.5）
3. 業種・目的に応じた専門家チームを動的に編成（Phase 1.5）
4. 専門家全員でクリティカルフィードバック・ブラッシュアップ（Phase 2）
5. 市場・競合・法規制の本格リサーチ（Phase 3）
6. 事業計画書・ピッチデッキ・財務モデルの出力（Phase 5）

### 誰が使うか

- 新規事業を立ち上げようとしている経営者・起業家
- AI Farm株式会社が支援するクライアント
- このSkillを自分の環境で走らせたい他のClaude Codeユーザー

---

## 2. システム構成

```
business-plan-builder/
├── SKILL.md                          ← メイン制御（Phaseロジック・進行ルール）
├── references/
│   ├── phase1-questions.md           ← 10カテゴリ詳細質問集
│   ├── customer-data-guide.md        ← 顧客データ収集・分析ガイド
│   ├── feasibility-ai-guide.md       ← 実行可能性・AI活用設計ガイド
│   └── compliance-research.md        ← 国別・業種別法規制チェックリスト
├── personas/
│   ├── expert-personas.md            ← コア6専門家の詳細定義
│   ├── expert-library.md             ← 追加専門家ライブラリ（100+候補）
│   └── facilitator-roles.md          ← 補佐CEO・通訳・議事録係の定義
├── frameworks/
│   └── business-frameworks.md        ← Lean Canvas等10フレームワーク
└── output-templates/
    ├── output-specs.md               ← アウトプット仕様（PPT/Word/Excel）
    └── ppt-design-guide.md           ← PPT非AI臭設計ガイド
```

---

## 3. 必要なMCP・ツール

### 必須MCP（ないと動かない機能あり）

なし（コアフローはMCPなしで動作する）

### 推奨MCP（あると機能が大幅に強化される）

| MCP | 用途 | 接続設定 |
|-----|------|---------|
| **Web Search** | Phase 0.5のデスクトップリサーチ・Phase 3の本格リサーチ | Claude Codeデフォルト or Brave Search MCP |
| **Shopify** | 既存EC事業の販売データ・顧客データ取得 | `https://mcp.shopify.com` |
| **Google Analytics** | サイトアクセス・コンバージョンデータ | GA4 MCP |
| **Canva** | ピッチデッキ・スライドの自動生成 | `https://mcp.canva.com/mcp` |
| **Slack** | ディスカッション結果の共有・通知 | `https://mcp.slack.com/mcp` |
| **Gmail/Google Drive** | 議事録の保存・共有 | Google MCP |

### 必要なClaude Code Skill

| Skill | 用途 | インストール方法 |
|-------|------|----------------|
| **pptx** | ピッチデッキ・プレゼン生成 | `/plugin marketplace add anthropics/skills` → pptx |
| **docx** | 事業計画書（Word）生成 | 同上 → docx |
| **xlsx** | 財務モデル（Excel）生成 | 同上 → xlsx |
| **pdf** | PDF変換・結合 | 同上 → pdf |
| **file-reading** | アップロードされた資料の読み込み | 同上 → file-reading |
| **this skill** | 本Skillそのもの | 下記インストール手順を参照 |

### オプションMCP（特定ユースケースで有効）

| MCP | 用途 |
|-----|------|
| Stripe | サブスク系事業のユニットエコノミクス分析 |
| HubSpot / Salesforce | BtoB事業のCRMデータ分析 |
| Notion | 議事録・事業計画書をNotionに保存 |
| Airtable | 財務モデルデータの管理 |

---

## 4. インストール手順

### 4-1. Claude Codeのインストール（未導入の場合）

```bash
npm install -g @anthropic-ai/claude-code
```

要件：Node.js 18以上、Anthropic APIキー

### 4-2. 本Skillのインストール

**方法A：.skillファイルから（推奨）**
```bash
# Claude Codeを起動
claude

# Skillをインストール
/plugin add /path/to/business-plan-builder.skill
```

**方法B：フォルダを直接配置**
```bash
# Skillフォルダをコピー
cp -r business-plan-builder/ ~/.claude/skills/

# Claude Codeを再起動して確認
claude
/skills list
```

**方法C：GitHubリポジトリから（共有する場合）**
```bash
git clone https://github.com/[your-repo]/business-plan-builder ~/.claude/skills/business-plan-builder
```

### 4-3. 依存Skillのインストール

```bash
# Claude Codeの公式Skillマーケットプレイスから
/plugin marketplace add anthropics/skills
/plugin install docx@skills
/plugin install pptx@skills
/plugin install xlsx@skills
/plugin install pdf@skills
/plugin install file-reading@skills
```

### 4-4. MCP接続設定（推奨）

`~/.claude/mcp.json` または `claude_desktop_config.json` に追記：

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "YOUR_BRAVE_API_KEY"
      }
    },
    "shopify": {
      "type": "url",
      "url": "https://mcp.shopify.com",
      "note": "Shopify管理者権限が必要"
    },
    "canva": {
      "type": "url",
      "url": "https://mcp.canva.com/mcp",
      "note": "Canvaアカウントが必要"
    },
    "slack": {
      "type": "url",
      "url": "https://mcp.slack.com/mcp",
      "note": "Slackワークスペースのbot権限が必要"
    }
  }
}
```

---

## 5. 起動方法と基本的な使い方

### 起動

```bash
# プロジェクトディレクトリで起動
claude

# または対話モードで直接起動
claude --dangerously-skip-permissions
```

### 基本的なトリガー

以下のいずれかを言うとSkillが自動起動する：

```
「事業計画を作りたい」
「ビジネスプランを一緒に考えてほしい」
「新規事業のアイデアがある」
「投資家向けのピッチデッキを作りたい」
「起業を考えている」
```

### 資料がある場合

```bash
# Claude Codeに資料を渡す方法
claude --add-file /path/to/business-plan.pdf
claude --add-file /path/to/financial-model.xlsx

# または起動後にファイルパスを伝える
claude
> /path/to/business-plan.pdf を読み込んで事業計画を一緒に作ってほしい
```

---

## 6. Phaseごとの処理フローと実装詳細

### Phase 0：資料読み込み

```
input:  PDF / Word / Excel / PPT / 画像（任意）
tool:   file-reading skill → markitdown / pdf skill
output: 事業サマリー（業種・フェーズ・数値・未検討事項）
```

### Phase 0.5：デスクトップリサーチ

```
input:  Phase 0から推定した業種・地域・キーワード
tool:   web_search（Brave Search MCP or Claude Code標準）
output: 市場仮説・競合候補・規制有無・トレンド（叩き台として提示）
注意:   結果はすべて「仮説」として扱う。Phase 1で覆ることが前提
```

### Phase 1：ヒアリング

```
input:  経営者との対話
tool:   なし（純粋な対話）
        ただし既存顧客データがある場合：
        → Shopify MCP / GA4 MCP でデータ取得
        → CSVがある場合：xlsx skill で分析
output: 10カテゴリ情報 + 顧客データ分析 + リソース・AI活用意向
```

### Phase 1.5：専門家選定

```
input:  Phase 1で収集した情報
process: expert-library.md の選定マトリクスを参照
output: 推奨専門家リスト → 経営者が承認 → 参加メンバー確定
```

### Phase 2：専門家会議

```
input:  Phase 1の情報 + 確定した専門家リスト
process: expert-personas.md + expert-library.md + facilitator-roles.md を参照
output: 各専門家のフィードバック（🔴/🟡/🟢形式）
        補佐CEO介入（コンフリクト時）
        通訳（用語平易化）
        議事録（MarkdownファイルまたはSlack投稿）
```

### Phase 3：本格リサーチ

```
input:  Phase 2で固まった事業方向性
tool:   web_search（複数クエリ・出典付き）
output: 市場規模（TAM/SAM/SOM・出典付き）
        競合比較マトリクス
        法規制チェックリスト（compliance-research.md参照）
        業界トレンドレポート
```

### Phase 4：共同執筆

```
input:  Phase 1-3の全情報
process: business-frameworks.md のフレームワーク適用
output: 事業計画書ドラフト（Markdown）
        経営者とのイテレーション（A/B/C案提示→選択→修正）
```

### Phase 5：アウトプット生成

```
input:  Phase 4の完成ドラフト
tool:   pptx skill / docx skill / xlsx skill

【PPT生成フロー】
1. テンプレートがある場合：
   → thumbnail.py でスライド視覚化
   → pptx skill editing.md のワークフローに従う
   → ppt-design-guide.md の「テンプレート踏襲優先度」を厳守

2. テンプレートがない場合：
   → ppt-design-guide.md のレイアウト種別を参照
   → pptxgenjs.md に従いゼロから生成
   → カード方式・箇条書き多用を禁止
   → 1スライド1メッセージ原則を徹底

【Word生成フロー】
   → docx skill に従い生成
   → output-specs.md の「事業計画書」構成に準拠

【Excel生成フロー】
   → xlsx skill に従い生成
   → output-specs.md の「財務モデル」シート構成に準拠

【AI活用仕様書（AI活用前提の場合）】
   → feasibility-ai-guide.md のPart 4「Claude Code向け仕様書」テンプレートに従い生成
   → Markdownファイルとして出力
```

---

## 7. CLAUDE.md推奨設定（プロジェクト単位で使う場合）

プロジェクトルートに以下の `CLAUDE.md` を配置する：

```markdown
# Business Plan Builder プロジェクト

## このプロジェクトについて
事業計画共同構築AIエージェント。
経営者との対話を通じて事業計画を作成する。

## 重要な原則
- 経営者の言葉を最優先する（Phase 0.5の仮説に引っ張られない）
- 一度に聞く質問は最大2つまで
- 腑に落ちるまで何度でも繰り返す（納得ループ）
- PPTはAI臭くしない（ppt-design-guide.md参照）

## よく使うコマンド
- /skills list → インストール済みSkill確認
- /mcp list → 接続済みMCP確認

## ファイル構成
- Skillファイル: ~/.claude/skills/business-plan-builder/
- 議事録出力先: ./output/minutes/
- 最終成果物: ./output/deliverables/
```

---

## 8. 出力ファイル管理

```bash
# 推奨ディレクトリ構成
project-root/
├── CLAUDE.md                    ← 上記設定
├── input/
│   ├── existing-materials/      ← Phase 0でアップロードする既存資料
│   └── customer-data/           ← 顧客データCSV等
├── output/
│   ├── minutes/                 ← 議事録（Markdown）
│   │   └── YYYY-MM-DD-phase2.md
│   ├── research/                ← Phase 0.5・3のリサーチ結果
│   │   ├── desktop-research.md
│   │   └── full-research.md
│   └── deliverables/            ← Phase 5の最終成果物
│       ├── pitch-deck.pptx
│       ├── business-plan.docx
│       ├── financial-model.xlsx
│       └── ai-spec.md           ← AI活用仕様書
└── templates/
    └── company-template.pptx    ← テンプレートPPTX（ある場合）
```

---

## 9. トラブルシューティング

| 症状 | 原因 | 対処 |
|------|------|------|
| Skillが起動しない | Skillが正しく配置されていない | `/skills list` で確認・再インストール |
| Web検索が動かない | Brave Search MCPが未設定 | MCP設定ファイルを確認 |
| PPT生成でエラー | pptx skillが未インストール | `/plugin install pptx@skills` |
| Shopifyデータが取得できない | MCP接続権限不足 | Shopify管理者権限を確認 |
| 議事録が保存されない | outputディレクトリが存在しない | `mkdir -p output/minutes` を実行 |

---

## 10. 他のユーザーへの共有方法

### .skillファイルで共有（推奨）

```bash
# パッケージング（skill-creatorスキルで実行）
cd /path/to/skills/examples/skill-creator
python -m scripts.package_skill /path/to/business-plan-builder /output/dir

# 生成された .skill ファイルを相手に渡す
# 相手側のインストール手順：
# /plugin add business-plan-builder.skill
```

### GitHubで共有

```bash
git init business-plan-builder
cd business-plan-builder
git add .
git commit -m "Initial: Business Plan Builder v5"
git remote add origin https://github.com/[username]/business-plan-builder
git push -u origin main

# 相手はこれでインストール可能：
# /plugin marketplace add [username]/business-plan-builder
```

### 注意事項（共有時）

- APIキー・MCPトークンは .gitignore に入れる
- 顧客データCSV等はリポジトリに含めない
- CLAUDE.mdのプロジェクト固有設定は各自で調整

---

## 11. 成長型ナレッジベース（Knowledge Base）

### 概要

セッションを重ねるごとに会社・事業・プロジェクトの知識が蓄積され、より精度の高い事業計画を作れるようになる仕組み。

### 3階層構造

```
knowledge-base/
├── _registry.md                    # 全社・事業・PJ一覧
├── _active-context.md              # 今のセッションの対象
│
└── companies/{company-slug}/       ← 会社レベル
    ├── profile.md                  # ミッション・バリュー・沿革
    ├── owner-profile.md            # オーナー名・背景・意思決定スタイル
    ├── financial-lens.md           # オーナーの財務の「読み方」
    ├── team-roster.md              # チーム構成
    ├── industry-context.md         # 業界知識の蓄積
    ├── decision-log.md             # 意思決定ログ（追記型）
    ├── data-sources.md             # 接続済みMCP・データソース一覧
    ├── financials/                 # 財務データ（インサイト形式）
    │   ├── _index.md
    │   ├── closing-status.md       # 月次締め状況
    │   └── annual-trends.md
    │
    └── businesses/{biz-slug}/      ← 事業レベル
        ├── profile.md
        ├── kpi-definitions.md
        ├── kpi-actuals.md          # 計画 vs 実績
        ├── competitor-map.md
        ├── customer-insights.md
        │
        └── projects/{pj-slug}/     ← プロジェクトレベル
            ├── plan.md             # 最新版の事業計画
            ├── plan-versions/
            ├── expert-team.md
            ├── phase-state.md
            ├── sessions/
            │   ├── _index.md       # 累積インサイト付きインデックス
            │   └── YYYY-MM-DD.md
            ├── research/
            └── deliverables/
```

### セッションライフサイクル

1. **開始時**: `_active-context.md` を読み、対象の会社/事業/PJ を特定。該当する knowledge-base ファイルをロード（コンテキスト予算 ~4000語）
2. **実行中**: 通常のPhaseフローに加え、累積知識が専門家エージェントに渡される
3. **終了時**: 議事録保存、プロファイル更新、意思決定ログ追記、KPI更新、Financial Lens リファイン

### 成長サイクル

| セッション | 蓄積状態 | 効果 |
|-----------|---------|------|
| 1回目 | 白紙 | ゼロからヒアリング。通常フロー |
| 5回目 | 会社・オーナー・財務の見方を把握 | 専門家がリアルデータで議論 |
| 20回目 | 半年分の実績＋40件の意思決定ログ | 過去の判断の結果も踏まえた助言 |

---

## 12. 会計SaaS連携

### 対応MCP

| MCP | 用途 | 取得データ |
|-----|------|-----------|
| freee | 仕訳・試算表・PL/BS | 月次試算表、勘定科目別残高 |
| Money Forward | 仕訳・レポート | 同上 |
| Shopify | EC売上 | 注文・売上・商品別データ |
| Stripe | サブスク課金 | MRR・チャーン・LTV |
| Google Analytics | トラフィック | セッション・CV率 |

### 締め確認フロー

会計データを使用する際は**必ず**以下を確認：

1. 「○月分まで月次の締め作業は完了していますか？」
2. 確定月 → **fact**（事業計画の根拠として使用可能）
3. 未締め月 → **provisional**（予測のインプットとして参考利用、fact扱いしない）
4. `closing-status.md` に記録

### Financial Lens（財務の読み方学習）

初回の財務データアップロード時に、オーナーに6つの質問を行い、その人固有の「数字の読み方」を `financial-lens.md` に記録。以降すべての財務分析はその視点を起点にする。

### 予測生成

- 確定月のトレンド（直近6-12ヶ月）+ 季節性 + 暫定月データ
- **楽観 / 基準 / 悲観** のレンジで提示
- 事業計画書では「確定fact」と「予測」を明確に分離

---

## 13. 累積知識のエージェント連携

Phase 2・4.5・6 で起動される専門家エージェントに、以下の累積知識変数が追加で渡される：

| 変数 | 内容 |
|------|------|
| `{{COMPANY_PROFILE}}` | 会社プロファイル要約 |
| `{{FINANCIAL_LENS}}` | オーナーの財務の見方 |
| `{{BUSINESS_KPIS}}` | 直近3ヶ月のKPI実績 |
| `{{RELEVANT_DECISIONS}}` | 関連する過去の意思決定 |
| `{{CHANGES_SINCE_LAST}}` | 前回セッションからの変化 |
| `{{FINANCIAL_ACTUALS}}` | 会計データ（確定/暫定区分付き） |

これにより、セッションを重ねるほど専門家の分析がリアルデータに基づいた具体的なものになる。

### 新規エージェントプロンプト

| ファイル | 用途 |
|---------|------|
| `agent-prompts/financial-review-expert.md` | 財務データレビュー（Phase 6E / 単独レビュー） |
| `agent-prompts/kpi-check-in.md` | 定期KPIチェックイン（Phase 6E、軽量版） |
