# ナレッジベース運用マニュアル

## 1. ディレクトリ構造

```
knowledge-base/
  _registry.md              # マスターインデックス（全企業・事業・PJ一覧）
  _active-context.md        # 現在のセッション対象（企業/事業/PJ）
  _template/                # 新規エンティティ作成用テンプレート
    company/
    business/
    project/
  companies/
    {company-slug}/
      _index.md
      company-profile.md
      owner-profile.md
      businesses/
        {business-slug}/
          _index.md
          business-profile.md
          financial-lens.md
          projects/
            {project-slug}/
              _index.md
              project-profile.md
              phase-state.md
              sessions/
              financials/
              decisions/
```

各ディレクトリの `{slug}` は英数字・ハイフンで構成する（例: `acme-corp`, `ec-business`, `expansion-2025`）。

---

## 2. 特殊ファイルの役割

### `_registry.md`（マスターインデックス）

ナレッジベース全体の一覧。全企業・事業・PJのスラッグ、ステータス、最終更新日を管理する。新規エンティティ作成時は必ずここに追記する。

### `_active-context.md`（セッション対象）

現在のセッションでどの企業・事業・PJを対象としているかを記録する。セッション開始時に最初に確認し、対象が変わった場合は更新する。

```markdown
# Active Context
- company: acme-corp
- business: ec-business
- project: expansion-2025
- updated: 2026-03-28
```

---

## 3. 新規エンティティの作成タイミングと手順

### 新規企業の作成

- ユーザーがこれまで登録されていない企業について事業計画を作りたいと言った場合
- `_template/company/` の内容を `companies/{new-slug}/` にコピー
- `_registry.md` に追記

### 新規事業の作成

- 既存企業の下に新しい事業ドメインが発生した場合
- `_template/business/` の内容を該当企業の `businesses/{new-slug}/` にコピー
- 企業の `_index.md` に追記

### 新規プロジェクトの作成

- 既存事業の下に新しい事業計画PJ（補助金申請、新規事業立ち上げ等）が発生した場合
- `_template/project/` の内容を該当事業の `projects/{new-slug}/` にコピー
- 事業の `_index.md` に追記

---

## 4. テンプレートの運用

`_template/` 配下のファイルは雛形として維持する。直接編集せず、コピーして使用する。テンプレート自体の改善が必要な場合は、既存エンティティには影響を与えずにテンプレートのみ更新する。

---

## 5. セッション終了チェックリスト

セッション終了時に以下を必ず実行する。

1. **議事録の保存** -- `sessions/YYYY-MM-DD.md` にセッション内容を記録
2. **`_index.md` の更新** -- セッションの要約（1-2行）を追記
3. **`phase-state.md` の更新** -- フェーズの進捗状況を反映
4. **プロファイルの更新** -- `project-profile.md`, `business-profile.md`, `owner-profile.md` に新たな知見を反映
5. **意思決定の記録** -- `decisions/` に重要な決定事項を記録
6. **`financial-lens.md` の更新** -- 財務関連の議論があった場合のみ
7. **KPI の更新** -- KPI指標に変更があった場合

---

## 6. コンテキストバジェット

### 制約

1セッションで読み込めるナレッジは **約4,000語** を上限とする。

### 運用ルール

- セッション開始時は `_index.md` のサマリーを読み込む。セッションファイル本体は読み込まない
- 必要な場合のみ、特定のセッションファイルやプロファイルを追加で読み込む
- 全ファイルを一括読み込みしない

---

## 7. サマリゼーションルール（Tier制）

### Tier 1: フルセッション記録

- `sessions/YYYY-MM-DD.md` にセッションの全内容を記録
- 直近のセッションはこの形式で保持

### Tier 2: セッションインデックス + 累積インサイト

- `_index.md` にセッション一覧と各セッションの1-2行サマリーを記載
- 累積的な気づきを段落形式でまとめる

### Tier 3: プロファイルへの統合

- 十分なセッションが蓄積されたら、インサイトを `project-profile.md`, `business-profile.md`, `owner-profile.md` に統合
- プロファイルファイルが「生きたドキュメント」として機能するようにする

### 20セッション超過時の圧縮ルール

セッション数が20を超えた場合:

1. 古いセッションのインサイトをプロファイルファイルに統合する
2. `_index.md` の累積インサイト段落には直近5-10セッション分のみ残す
3. 古いセッションファイル（`sessions/` 内）は削除せず保持するが、日常的には参照しない
4. プロファイルファイルが「唯一の真実の源」として機能するようにする

---

## 8. Git コミット規約

```
Session YYYY-MM-DD: [1行サマリー]
```

例:

```
Session 2026-03-28: Phase 3 完了、財務モデル初版作成
Session 2026-03-27: オーナーヒアリング実施、事業概要確定
Session 2026-03-25: 新規PJ「expansion-2025」作成、Phase 1 開始
```

コミットは1セッション＝1コミットを基本とする。セッション中に複数回コミットが必要な場合は、末尾に連番を付ける（例: `Session 2026-03-28-2: ...`）。
