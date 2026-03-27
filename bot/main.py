"""
main.py
漫画アフィリエイトBot エントリーポイント
"""
import os
import sys
import argparse
from scraper import fetch_new_releases
from analyzer import analyze_manga, generate_markdown
from publisher import publish


def main(dry_run: bool = False):
    affiliate_tag = os.environ.get("AMAZON_ASSOCIATE_TAG", "your-associate-tag-22")

    print("=" * 50)
    print("📚 漫画アフィリエイトBot 起動")
    print("=" * 50)

    # 1. 新刊収集
    releases = fetch_new_releases()
    if not releases:
        print("[main] 新刊が見つかりませんでした。終了します。")
        return

    # 2. 各漫画を分析 → Markdown生成 → 保存
    success = 0
    for manga in releases:
        try:
            print(f"\n[main] 処理中: {manga['title']}")

            analysis = analyze_manga(manga)
            filename, content = generate_markdown(manga, analysis, affiliate_tag)
            publish(filename, content, dry_run=dry_run)

            success += 1

        except Exception as e:
            print(f"[main] エラー ({manga['title']}): {e}")
            continue

    print(f"\n{'=' * 50}")
    print(f"✅ 完了: {success}/{len(releases)} 件の記事を生成")
    print("=" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="漫画アフィリエイトBot")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="ファイルを実際に書き出さずプレビューのみ",
    )
    args = parser.parse_args()
    main(dry_run=args.dry_run)
