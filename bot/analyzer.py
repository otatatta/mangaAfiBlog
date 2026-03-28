"""
analyzer.py
Claude APIを使って漫画を分析し、Markdown記事を生成する
"""
import anthropic
import json
import re
from datetime import datetime


def analyze_manga(manga: dict) -> dict:
    """
    Claude APIで漫画を分析する
    戻り値: 期待値・話題性・ジャンル・ファン層・宣伝文を含むdict
    """
    client = anthropic.Anthropic()

    prompt = f"""
以下の漫画について分析し、必ずJSON形式のみで返してください。前置きや説明文は不要です。

## 漫画情報
- タイトル: {manga['title']}
- 作者: {manga['author']}
- ジャンル: {manga['genre']}
- 出版社: {manga['publisher']}
- あらすじ: {manga['description']}

## 出力形式（JSON）
{{
  "expectation_score": 4,
  "expectation_reason": "期待値の理由（1〜2文）",
  "buzz_level": "高",
  "buzz_reason": "話題性の理由（1〜2文）",
  "genre_tags": ["タグ1", "タグ2", "タグ3"],
  "target_audience": "ターゲットファン層の説明（1〜2文）",
  "pr_text_short": "X（Twitter）向け宣伝文140字以内",
  "pr_text_long": "ブログ向け紹介文200字程度",
  "seo_keywords": ["キーワード1", "キーワード2", "キーワード3"]
}}

expectation_score は1〜5の整数、buzz_level は「低」「中」「高」のいずれかにしてください。
"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()

    # JSON部分だけ抽出
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        analysis = json.loads(match.group())
    else:
        raise ValueError(f"JSONを抽出できませんでした: {raw}")

    return analysis


def generate_markdown(manga: dict, analysis: dict, affiliate_tag: str) -> tuple[str, str]:
    """
    漫画情報と分析結果からMarkdown記事を生成する
    戻り値: (ファイル名, Markdownコンテンツ)
    """
    today = datetime.today()
    slug = (
        manga["title"]
        .replace(" ", "-")
        .replace("　", "-")
        .replace("/", "-")
        .lower()
    )
    # ASCIIのみに絞る（日本語はそのまま許容）
    filename = f"{today.strftime('%Y-%m-%d')}-{slug}.md"

    affiliate_url = (
        f"https://www.amazon.co.jp/dp/{manga['asin']}?tag={affiliate_tag}"
        if manga.get("asin")
        else "#"
    )

    genre_tags_str = " ".join([f'"{t}"' for t in analysis["genre_tags"]])
    seo_keywords_str = " ".join([f'"{k}"' for k in analysis["seo_keywords"]])

    # シリーズ名: タイトルから巻数部分を除去
    series_name = re.sub(r'\s*\d+巻?\s*$', '', manga['title']).strip()
    if not series_name:
        series_name = manga['title']

    cover_image = manga.get("image_url", "")

    content = f"""---
title: "{manga['title']}【新刊】期待値{analysis['expectation_score']}★ - あらすじ・見どころまとめ"
series: "{series_name}"
cover_image: "{cover_image}"
description: "{analysis['pr_text_long']}"
pubDate: "{today.strftime('%Y-%m-%d')}"
genre: "{manga['genre']}"
author_name: "{manga['author']}"
publisher: "{manga['publisher']}"
expectation_score: {analysis['expectation_score']}
buzz_level: "{analysis['buzz_level']}"
tags: [{genre_tags_str}]
seo_keywords: [{seo_keywords_str}]
affiliate_url: "{affiliate_url}"
---

## {manga['title']}

**作者**: {manga['author']}　**出版社**: {manga['publisher']}　**発売日**: {manga['release_date']}

---

## 📖 あらすじ

{manga['description']}

---

## ⭐ 期待値・評価

| 項目 | 評価 |
|---|---|
| 期待値 | {'★' * analysis['expectation_score']}{'☆' * (5 - analysis['expectation_score'])} ({analysis['expectation_score']}/5) |
| 話題性 | {analysis['buzz_level']} |

**期待値について**: {analysis['expectation_reason']}

**話題性について**: {analysis['buzz_reason']}

---

## 👥 こんな人におすすめ

{analysis['target_audience']}

---

## 🛒 購入はこちら

[Amazon で「{manga['title']}」を見る]({affiliate_url})

---

> 📢 **PR**: {analysis['pr_text_short']}
"""

    return filename, content
