"""
publisher.py
生成したMarkdownファイルをAstroブログのcontentディレクトリに書き出す
（GitへのpushはGitHub Actionsが行う）
"""
import os
from pathlib import Path


CONTENT_DIR = Path(__file__).parent.parent / "astro-blog" / "src" / "content" / "manga"


def publish(filename: str, content: str, dry_run: bool = False) -> Path:
    """
    Markdownファイルを書き出す
    dry_run=True のときはファイルを実際に書かずパスだけ返す
    """
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    filepath = CONTENT_DIR / filename

    if dry_run:
        print(f"[publisher] DRY RUN: {filepath}")
        print("--- コンテンツプレビュー ---")
        print(content[:500] + "..." if len(content) > 500 else content)
        return filepath

    filepath.write_text(content, encoding="utf-8")
    print(f"[publisher] 保存完了: {filepath}")
    return filepath
