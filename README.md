# 📚 manga-affiliate-bot

毎週の新刊漫画を自動収集・分析・記事化するアフィリエイトBotです。

## 構成

```
manga-affiliate-bot/
├── astro-blog/          # Astro製ブログ（Cloudflare Pagesにデプロイ）
│   └── src/
│       ├── content/manga/  # 自動生成されるMarkdown記事
│       ├── pages/          # Astroページ
│       ├── layouts/        # レイアウト
│       └── components/     # UIコンポーネント
├── bot/                 # Python自動化Bot
│   ├── scraper.py       # 新刊情報収集
│   ├── analyzer.py      # Claude APIで分析・記事生成
│   ├── publisher.py     # GitHubにpush
│   └── main.py          # エントリーポイント
└── .github/workflows/
    └── weekly-bot.yml   # 毎週月曜自動実行
```

## フロー

1. GitHub Actions が毎週月曜 09:00 JST に起動
2. `bot/scraper.py` が Amazon・その他から今週の新刊漫画を収集
3. `bot/analyzer.py` が Claude API で各作品を分析（期待値・話題性・ジャンル・ファン層・宣伝文）
4. Markdownファイルを `astro-blog/src/content/manga/` に生成
5. `bot/publisher.py` が GitHub にコミット＆プッシュ
6. Cloudflare Pages が自動ビルド＆デプロイ

## セットアップ

### 必要なシークレット（GitHub Secrets に登録）

| キー | 内容 |
|---|---|
| `ANTHROPIC_API_KEY` | Claude APIキー |
| `AMAZON_ASSOCIATE_TAG` | Amazonアソシエイトタグ |
| `GH_TOKEN` | GitHubパーソナルアクセストークン（repo権限） |

### ローカル開発

```bash
# Astroブログ
cd astro-blog
npm install
npm run dev

# Bot（Python 3.11+）
cd bot
pip install -r requirements.txt
python main.py --dry-run  # 実際にはpushしない
```

## ライセンス

MIT
