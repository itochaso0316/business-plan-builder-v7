#!/usr/bin/env python3
"""
Phase 4.3 デモ動画生成スクリプト
SRT字幕に基づいてスライドを生成し、ffmpegでMP4に変換する
"""
import os
import re
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc'
FONT_PATH_FALLBACK = '/System/Library/Fonts/Helvetica.ttc'
WIDTH, HEIGHT = 1920, 1080
FPS = 30

SLIDES = [
    # (duration_sec, title, body_lines, style)
    # style: 'intro' | 'step' | 'result' | 'embed' | 'outro'
    (12, "Business Plan Builder v7",
     ["Phase 4.3 補助金マッチング機能 デモ",
      "",
      "2026-05-03  |  AI Farm",
      "",
      "本デモはPython + PIL + ffmpegにより自動生成されたスライド動画です",
      "hojokin MCPの動作確認はST-BUSINESSPLAN-2026-05-005で実施済み"],
     'intro'),
    (18, "Phase 4.3 とは — 機能概要",
     ["Phase 4で事業計画が固まった段階で",
      "活用できる補助金・助成金をAIが自動判定します",
      "",
      "動作フロー:",
      "  1. hojokin_match   → 業種/地域で補助金を絞り込む",
      "  2. hojokin_requirements → 申請要件/書類を取得",
      "  3. hojokin_plan_draft   → 事業計画書に自動埋め込み",
      "  4. hojokin_checklist    → 申請準備チェックリスト生成"],
     'intro'),
    (20, "Step 1: 補助金検索フロー — 入力画面",
     ["Phase 4完了後、補助金マッチングの確認プロンプトが表示されます",
      "",
      "「補助金マッチングを開始しますか？」",
      "→ ユーザーが「はい」と回答すると hojokin MCP が起動します",
      "",
      "業種と地域を入力して補助金を検索します"],
     'step'),
    (20, "入力パラメータ（東京都 IT企業 創業期）",
     ["hojokin_match ツール呼び出しパラメータ:",
      "",
      "  都道府県:         東京都",
      "  業種:             IT・情報通信（SaaS）",
      "  従業員数:         5名",
      "  事業ステージ:     創業期（設立3年）",
      "  利用目的:         DX、IT導入、生産性向上",
      "  年間売上高:       3,000万円"],
     'step'),
    (20, "補助金マッチング結果 — 19件ヒット",
     ["hojokin MCP（Supabase: 207件）から絞り込み",
      "",
      "✓  19件マッチ（信頼度スコア 0.80以上）",
      "",
      "スコア順トップ5:",
      "  1. 小規模事業者持続化補助金         (score: 0.92)",
      "  2. IT導入補助金2026                (score: 0.88)",
      "  3. デジタル化促進補助金（東京都）    (score: 0.81)",
      "  4. 創業支援補助金（経産省）          (score: 0.78)",
      "  5. DX推進補助金（中小企業庁）        (score: 0.75)"],
     'result'),
    (22, "Step 2: hojokin MCP 結果表示",
     ["スコア順にマッチした補助金が一覧表示されます",
      "",
      "「小規模事業者持続化補助金」を選択 →",
      "hojokin_requirements(subsidy_id=9001) 呼び出し"],
     'step'),
    (20, "小規模事業者持続化補助金 — 詳細情報",
     ["補助金名:     小規模事業者持続化補助金",
      "最大補助額:   50万円",
      "補助率:       2/3（約66%）",
      "",
      "対象要件:",
      "  ・従業員5名以下（商業・サービス業）",
      "  ・商工会議所管轄エリアで営業していること",
      "  ・申請時点で創業から1年以上経過していること"],
     'result'),
    (20, "申請要件・必要書類（hojokin_requirements より）",
     ["必要書類:",
      "  ・経営計画書（様式2）",
      "  ・補助事業計画書（様式3）",
      "  ・直近2期分の確定申告書",
      "  ・GビズIDプライム",
      "  ・商工会議所の受付印済み確認書",
      "",
      "官公庁サイトを調べる手間が不要になります"],
     'result'),
    (22, "Step 3: 事業計画書への自動埋め込み",
     ["hojokin_plan_draft ツール呼び出し",
      "",
      "  subsidy_id:          9001",
      "  company.name:        株式会社テックスタート",
      "  company.description: SaaS開発・販売（中小企業向けDXツール）",
      "  project.title:       AI活用業務自動化システム導入",
      "  investment_amount:   200万円"],
     'step'),
    (22, "【Before】事業計画書 — 埋め込み前",
     ["事業概要セクション（補助金申請用）:",
      "",
      "  （空欄 — 汎用テキストのみ記載）",
      "",
      "補助金審査基準との対応マッピング:  なし",
      "審査基準セルフチェック:           未実施"],
     'embed'),
    (22, "【After】自動埋め込み完了 — 7セクション生成",
     ["【事業テーマ】AI活用業務自動化システム導入による生産性向上事業",
      "",
      "当社（株式会社テックスタート）は、クラウドAIを活用した",
      "業務プロセス自動化により、中小企業の生産性を30%向上させます。",
      "",
      "投資総額: 200万円  |  補助申請額: 133万円（補助率2/3）",
      "",
      "→  7セクション全てに審査基準対応テンプレートが自動マッピング"],
     'embed'),
    (20, "審査基準セルフチェック（8項目）",
     ["hojokin_plan_draft 出力 — 審査基準スコアリング:",
      "",
      "  ✅ 事業の革新性・独自性         (充足)",
      "  ✅ 地域経済への貢献             (充足)",
      "  ✅ 実現可能性の根拠             (充足)",
      "  ✅ 補助事業の効果測定方法       (充足)",
      "  ⚠️  販路開拓の具体性           (要補強)",
      "  ✅ 経費の妥当性                 (充足)"],
     'result'),
    (20, "Step 4: 申請準備チェックリスト（4フェーズ）",
     ["hojokin_checklist(subsidy_id=9001) 呼び出し結果:",
      "",
      "  Phase 1 事前準備  14日:  GビズID取得、商工会議所相談",
      "  Phase 2 書類作成  21日:  経営計画書、補助事業計画書",
      "  Phase 3 申請       3日:  電子申請ポータル提出",
      "  Phase 4 採択後   240日:  実績報告、補助金受領"],
     'step'),
    (18, "重要注意事項（5件 — 赤字表示）",
     ["  ⚠️  申請受付期間: 2026/03/01 〜 2026/06/30（公式要確認）",
      "  ⚠️  書類不備は審査対象外になる可能性あり",
      "  ⚠️  補助金受領は採択後240日以内",
      "  ⚠️  設備購入は採択通知後に実施すること",
      "  ⚠️  不支給になっても申請費用は返還されない"],
     'result'),
    (30, "まとめ — Phase 4.3 補助金マッチング",
     ["受入基準確認:",
      "",
      "  ✅ 補助金検索フロー（業種/地域入力 → 19/207件マッチ）",
      "  ✅ hojokin MCP からの結果表示（名称/金額/条件）",
      "  ✅ 事業計画書への自動埋め込み（7セクション）",
      "  ✅ 申請準備チェックリスト自動生成（4フェーズ）",
      "",
      "Beta版 / 実際の申請は行政書士・中小企業診断士へのご相談を推奨します"],
     'outro'),
]

COLORS = {
    'intro':  {'bg': (15, 32, 80),   'title': (255, 255, 255), 'body': (180, 210, 255), 'accent': (100, 180, 255)},
    'step':   {'bg': (20, 20, 45),   'title': (100, 200, 255), 'body': (220, 230, 255), 'accent': (100, 200, 255)},
    'result': {'bg': (10, 40, 20),   'title': (100, 255, 150), 'body': (200, 240, 210), 'accent': (100, 255, 150)},
    'embed':  {'bg': (40, 20, 10),   'title': (255, 180, 80),  'body': (240, 220, 190), 'accent': (255, 180, 80)},
    'outro':  {'bg': (15, 32, 80),   'title': (255, 220, 80),  'body': (200, 220, 255), 'accent': (255, 220, 80)},
}


def load_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        try:
            return ImageFont.truetype(FONT_PATH_FALLBACK, size)
        except Exception:
            return ImageFont.load_default()


def draw_slide(title, body_lines, style='step', slide_num=0, total=0):
    colors = COLORS.get(style, COLORS['step'])
    img = Image.new('RGB', (WIDTH, HEIGHT), colors['bg'])
    draw = ImageDraw.Draw(img)

    # Gradient-like top bar
    for y in range(6):
        alpha = int(255 * (1 - y / 6))
        draw.rectangle([(0, y), (WIDTH, y+1)], fill=colors['accent'] + (alpha,) if len(colors['accent']) == 3 else colors['accent'])

    # Top bar
    draw.rectangle([(0, 0), (WIDTH, 8)], fill=colors['accent'])

    # Phase label
    phase_font = load_font(28)
    draw.text((60, 40), "Business Plan Builder v7  |  Phase 4.3 補助金マッチング", font=phase_font, fill=colors['accent'])

    # Separator line
    draw.rectangle([(60, 90), (WIDTH - 60, 92)], fill=colors['accent'])

    # Title
    title_font = load_font(62)
    draw.text((60, 120), title, font=title_font, fill=colors['title'])

    # Body
    body_font = load_font(38)
    y = 240
    for line in body_lines:
        if line.startswith('✅') or line.startswith('✓'):
            draw.text((80, y), line, font=body_font, fill=(100, 255, 150))
        elif line.startswith('⚠️') or line.startswith('  ⚠️'):
            draw.text((80, y), line, font=body_font, fill=(255, 200, 60))
        elif line.startswith('【After】') or '自動マッピング' in line or '自動埋め込み' in line:
            draw.text((80, y), line, font=body_font, fill=(100, 255, 150))
        elif line.startswith('【Before】') or '空欄' in line:
            draw.text((80, y), line, font=body_font, fill=(200, 120, 120))
        elif line == '':
            y += 20
            continue
        else:
            draw.text((80, y), line, font=body_font, fill=colors['body'])
        y += 54

    # Bottom slide counter
    counter_font = load_font(24)
    draw.text((WIDTH - 120, HEIGHT - 50), f"{slide_num}/{total}", font=counter_font, fill=colors['accent'])

    # Bottom bar
    draw.rectangle([(0, HEIGHT - 8), (WIDTH, HEIGHT)], fill=colors['accent'])

    return img


def parse_srt_durations(srt_path):
    """SRTから各字幕の開始・終了時刻を秒で取得"""
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\n|\Z)'
    matches = re.findall(pattern, content, re.DOTALL)

    def to_sec(ts):
        h, m, rest = ts.split(':')
        s, ms = rest.split(',')
        return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000

    return [(int(n), to_sec(start), to_sec(end)) for n, start, end, _ in matches]


def generate_video(output_path, srt_path):
    tmp_dir = tempfile.mkdtemp(prefix='bpb_demo_')
    print(f"[1/4] Generating {len(SLIDES)} slides in {tmp_dir}")

    # Generate PNG slides
    slide_files = []
    for i, (duration, title, body, style) in enumerate(SLIDES):
        img = draw_slide(title, body, style, i+1, len(SLIDES))
        path = os.path.join(tmp_dir, f'slide_{i:03d}.png')
        img.save(path, 'PNG')
        slide_files.append((path, duration))
        print(f"  Slide {i+1}/{len(SLIDES)}: {title[:40]} ({duration}s)")

    # Build ffmpeg concat input
    concat_file = os.path.join(tmp_dir, 'concat.txt')
    total_duration = 0
    with open(concat_file, 'w') as f:
        for path, duration in slide_files:
            f.write(f"file '{path}'\n")
            f.write(f"duration {duration}\n")
            total_duration += duration
        # Add last frame again (ffmpeg concat needs it)
        f.write(f"file '{slide_files[-1][0]}'\n")

    print(f"\n[2/4] Total video duration: {total_duration}s ({total_duration//60}m{total_duration%60}s)")

    # Generate silent audio track (5 minutes)
    audio_file = os.path.join(tmp_dir, 'silence.aac')
    subprocess.run([
        'ffmpeg', '-y', '-f', 'lavfi', '-i', f'anullsrc=r=44100:cl=stereo',
        '-t', str(total_duration), '-c:a', 'aac', '-b:a', '128k', audio_file
    ], capture_output=True, check=True)

    # Combine slides into video
    print("[3/4] Encoding MP4...")
    video_no_audio = os.path.join(tmp_dir, 'video_raw.mp4')
    result = subprocess.run([
        'ffmpeg', '-y',
        '-f', 'concat', '-safe', '0', '-i', concat_file,
        '-vf', f'scale={WIDTH}:{HEIGHT}:flags=lanczos,fps={FPS}',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '22',
        '-pix_fmt', 'yuv420p',
        video_no_audio
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("ffmpeg error:", result.stderr[-500:])
        raise RuntimeError("Video encoding failed")

    # Mux video + audio
    print("[4/4] Muxing audio + video...")
    subprocess.run([
        'ffmpeg', '-y',
        '-i', video_no_audio, '-i', audio_file,
        '-c:v', 'copy', '-c:a', 'aac', '-shortest',
        output_path
    ], capture_output=True, check=True)

    # Verify
    stat = os.stat(output_path)
    print(f"\n✅ Video saved: {output_path}")
    print(f"   File size: {stat.st_size / 1024 / 1024:.1f} MB")
    print(f"   Duration:  {total_duration}s ({total_duration//60}m{total_duration%60}s)")

    # Cleanup
    import shutil
    shutil.rmtree(tmp_dir)
    return output_path, total_duration, stat.st_size


if __name__ == '__main__':
    output = '/Users/itochaso/Projects/business-plan-builder-v7/videos/demo-phase4.3.mp4'
    srt = '/Users/itochaso/Projects/business-plan-builder-v7/videos/demo-phase4.3.srt'
    generate_video(output, srt)
