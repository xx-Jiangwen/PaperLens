#!/usr/bin/env python3
"""
使用 arxiv 官方库爬取论文（推荐方式）
安装: pip install arxiv
"""

import arxiv
import json
from datetime import datetime


def search_papers(query: str, max_results: int = 10):
    """搜索论文"""
    print(f"\n搜索: {query}")
    print("-" * 60)

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    results = []
    for paper in search.results():
        results.append({
            'id': paper.entry_id.split('/')[-1],
            'title': paper.title,
            'authors': [a.name for a in paper.authors],
            'summary': paper.summary,
            'published': paper.published.isoformat() if paper.published else None,
            'updated': paper.updated.isoformat() if paper.updated else None,
            'url': paper.entry_id,
            'pdf_url': paper.pdf_url,
            'categories': paper.categories,
            'comment': paper.comment,
            'journal_ref': paper.journal_ref,
        })

        print(f"标题: {paper.title}")
        print(f"ID: {paper.entry_id.split('/')[-1]}")
        print(f"发布: {paper.published}")
        print("-" * 40)

    return results


def get_paper_by_id(paper_id: str):
    """根据 ID 获取论文"""
    print(f"\n获取论文: {paper_id}")
    print("-" * 60)

    search = arxiv.Search(id_list=[paper_id])
    paper = next(search.results(), None)

    if paper:
        return {
            'id': paper.entry_id.split('/')[-1],
            'title': paper.title,
            'authors': [a.name for a in paper.authors],
            'summary': paper.summary,
            'published': paper.published.isoformat() if paper.published else None,
            'updated': paper.updated.isoformat() if paper.updated else None,
            'url': paper.entry_id,
            'pdf_url': paper.pdf_url,
            'categories': list(paper.categories),
            'comment': paper.comment,
            'journal_ref': paper.journal_ref,
            'primary_category': paper.primary_category,
            'doi': paper.doi,
        }
    return None


def format_paper(paper: dict) -> str:
    """格式化论文信息"""
    output = []
    output.append("=" * 60)
    output.append(f"标题: {paper.get('title', 'N/A')}")
    output.append("-" * 60)
    output.append(f"作者: {', '.join(paper.get('authors', []))}")
    output.append(f"链接: {paper.get('url', 'N/A')}")
    output.append(f"PDF: {paper.get('pdf_url', 'N/A')}")
    output.append(f"分类: {paper.get('primary_category', 'N/A')}")
    output.append(f"发布日期: {paper.get('published', 'N/A')}")
    if paper.get('journal_ref'):
        output.append(f"期刊: {paper['journal_ref']}")
    if paper.get('doi'):
        output.append(f"DOI: {paper['doi']}")
    output.append("-" * 60)
    output.append(f"摘要:\n{paper.get('summary', 'N/A')[:500]}...")
    output.append("=" * 60)
    return "\n".join(output)


def main():
    print("=" * 60)
    print("arXiv 官方库 Demo")
    print("=" * 60)

    # 示例 1: 搜索论文
    print("\n【示例 1】搜索论文")
    results = search_papers("attention is all you need transformer", max_results=5)
    with open('search_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\n已保存到 search_results.json")

    # 示例 2: 根据 ID 获取论文
    print("\n【示例 2】根据 ID 获取论文")
    paper = get_paper_by_id("1706.03762")  # Attention Is All You Need
    if paper:
        print(format_paper(paper))
        with open('paper.json', 'w', encoding='utf-8') as f:
            json.dump(paper, f, ensure_ascii=False, indent=2)
        print("\n已保存到 paper.json")

    # 示例 3: 下载 PDF
    print("\n【示例 3】下载 PDF")
    paper = arxiv.Search(id_list=["1706.03762"])
    result = next(paper.results())
    print(f"正在下载: {result.title}")
    result.download_pdf(filename="transformer.pdf")
    print("已下载到 transformer.pdf")


if __name__ == "__main__":
    main()