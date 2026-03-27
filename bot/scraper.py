"""
scraper.py
今週発売の新刊漫画情報を収集する
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time


def get_this_week_range():
    """今週（月〜日）の日付範囲を返す"""
    today = datetime.today()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday


def scrape_amazon_manga(keyword="漫画 新刊", max_results=20):
    """
    Amazon.co.jp から今週の新刊漫画を取得する
    ※ 実運用では公式PA-APIの使用を推奨（アソシエイト契約が必要）
    """
    results = []
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    # NOTE: 本番ではAmazon PA-APIを使用すること
    # https://affiliate.amazon.co.jp/assoc_credentials/home
    # ここではデモ用のダミーデータを返す
    print("[scraper] Amazon PA-API未設定のためデモデータを使用")
    return _get_demo_data()


def _get_demo_data():
    """開発・テスト用のダミーデータ"""
    monday, sunday = get_this_week_range()
    week_str = monday.strftime("%Y/%m/%d")

    return [
        {
            "title": "サンプル漫画A 第3巻",
            "author": "作者A",
            "genre": "少年漫画・バトル",
            "release_date": week_str,
            "asin": "B00EXAMPLE1",
            "publisher": "集英社",
            "description": "熱血主人公が仲間と共に強敵に挑む王道バトル漫画の最新刊。",
            "cover_url": "",
        },
        {
            "title": "サンプル漫画B 第1巻",
            "author": "作者B",
            "genre": "少女漫画・ラブコメ",
            "release_date": week_str,
            "asin": "B00EXAMPLE2",
            "publisher": "講談社",
            "description": "話題の新連載が待望の単行本化。甘酸っぱい青春ラブコメ。",
            "cover_url": "",
        },
        {
            "title": "サンプル漫画C 第7巻",
            "author": "作者C",
            "genre": "青年漫画・ミステリー",
            "release_date": week_str,
            "asin": "B00EXAMPLE3",
            "publisher": "小学館",
            "description": "累計100万部突破の人気ミステリー漫画、クライマックスへ。",
            "cover_url": "",
        },
    ]


def fetch_new_releases():
    """メインの収集関数"""
    print("[scraper] 今週の新刊漫画を収集中...")
    releases = scrape_amazon_manga()
    print(f"[scraper] {len(releases)}件取得完了")
    return releases
