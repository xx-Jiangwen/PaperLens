#!/usr/bin/env python3
"""
arXiv 论文爬取 Demo
支持两种方式：
1. 使用 arxiv 官方库（推荐）
2. 使用 requests + BeautifulSoup 直接爬取
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
from typing import Optional


class ArxivCrawler:
    """arXiv 论文爬虫"""

    BASE_URL = "https://arxiv.org/abs/"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_paper(self, paper_id: str) -> dict:
        """
        获取单篇论文信息

        Args:
            paper_id: arXiv 论文 ID，如 "2301.12345" 或完整 URL

        Returns:
            包含论文信息的字典
        """
        # 提取论文 ID
        paper_id = self._extract_id(paper_id)
        url = f"{self.BASE_URL}{paper_id}"

        print(f"正在获取论文: {url}")

        response = self.session.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # 解析论文信息
        paper = {
            'id': paper_id,
            'url': url,
            'pdf_url': f"https://arxiv.org/pdf/{paper_id}",
            'title': self._get_title(soup),
            'authors': self._get_authors(soup),
            'abstract': self._get_abstract(soup),
            'categories': self._get_categories(soup),
            'submitted': self._get_date(soup, 'Submitted'),
            'updated': self._get_date(soup, 'Updated'),
            'comments': self._get_meta(soup, 'Comments'),
            'journal': self._get_meta(soup, 'Journal reference'),
            'doi': self._get_meta(soup, 'DOI'),
        }

        return paper

    def search(self, query: str, max_results: int = 10) -> list:
        """
        搜索论文

        Args:
            query: 搜索关键词
            max_results: 最大结果数

        Returns:
            论文列表
        """
        search_url = "https://arxiv.org/search/"
        params = {
            'query': query,
            'searchtype': 'all',
            'max_results': max_results
        }

        print(f"正在搜索: {query}")

        response = self.session.get(search_url, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        results = []

        # 解析搜索结果
        for item in soup.select('li.arxiv-result'):
            try:
                title_elem = item.select_one('p.title')
                link_elem = item.select_one('p.list-title a')
                abstract_elem = item.select_one('p.abstract')

                if link_elem and title_elem:
                    href = link_elem.get('href', '')
                    paper_id = self._extract_id(href)

                    results.append({
                        'id': paper_id,
                        'title': title_elem.text.strip(),
                        'abstract': abstract_elem.text.strip() if abstract_elem else '',
                        'url': f"https://arxiv.org/abs/{paper_id}",
                        'pdf_url': f"https://arxiv.org/pdf/{paper_id}",
                    })
            except Exception as e:
                print(f"解析错误: {e}")
                continue

        return results

    def _extract_id(self, text: str) -> str:
        """从文本中提取 arXiv ID"""
        # 匹配格式如: 2301.12345 或 2101.12345v1
        match = re.search(r'(\d{4}\.\d{4,5}(?:v\d+)?)', text)
        if match:
            return match.group(1)
        # 匹配旧格式如: cs/0701001
        match = re.search(r'([a-z-]+/\d{7})', text)
        if match:
            return match.group(1)
        return text

    def _get_title(self, soup) -> str:
        """获取标题"""
        title_elem = soup.select_one('h1.title')
        if title_elem:
            return title_elem.text.strip()
        return ''

    def _get_authors(self, soup) -> list:
        """获取作者列表"""
        authors = []
        for author in soup.select('div.authors a'):
            authors.append(author.text.strip())
        return authors

    def _get_abstract(self, soup) -> str:
        """获取摘要"""
        abstract_elem = soup.select_one('blockquote.abstract')
        if abstract_elem:
            # 移除 "Abstract:" 前缀
            text = abstract_elem.text.strip()
            text = re.sub(r'^Abstract:\s*', '', text)
            return text.strip()
        return ''

    def _get_categories(self, soup) -> list:
        """获取分类"""
        categories = []
        for cat in soup.select('span.primary-subject'):
            categories.append(cat.text.strip())
        for cat in soup.select('div.subsubjects span'):
            categories.append(cat.text.strip())
        return categories

    def _get_date(self, soup, label: str) -> Optional[str]:
        """获取日期"""
        for div in soup.select('div.dateline'):
            if label in div.text:
                match = re.search(r'(\d{1,2}\s+\w+\s+\d{4})', div.text)
                if match:
                    return match.group(1)
        return None

    def _get_meta(self, soup, label: str) -> Optional[str]:
        """获取元信息"""
        for tr in soup.select('tr'):
            td = tr.select_one('td.tablecell')
            if td and label in td.text:
                value = tr.select_one('td:last-child')
                if value:
                    return value.text.strip()
        return None


def format_paper(paper: dict) -> str:
    """格式化论文信息用于显示"""
    output = []
    output.append("=" * 60)
    output.append(f"标题: {paper.get('title', 'N/A')}")
    output.append("-" * 60)
    output.append(f"作者: {', '.join(paper.get('authors', []))}")
    output.append(f"链接: {paper.get('url', 'N/A')}")
    output.append(f"PDF: {paper.get('pdf_url', 'N/A')}")
    output.append(f"分类: {', '.join(paper.get('categories', []))}")
    output.append(f"提交日期: {paper.get('submitted', 'N/A')}")
    if paper.get('updated'):
        output.append(f"更新日期: {paper['updated']}")
    if paper.get('journal'):
        output.append(f"期刊: {paper['journal']}")
    if paper.get('comments'):
        output.append(f"备注: {paper['comments']}")
    output.append("-" * 60)
    output.append(f"摘要:\n{paper.get('abstract', 'N/A')}")
    output.append("=" * 60)
    return "\n".join(output)


def main():
    """主函数演示"""
    crawler = ArxivCrawler()

    print("\n" + "=" * 60)
    print("arXiv 论文爬虫 Demo")
    print("=" * 60)

    # 示例 1: 获取单篇论文
    print("\n【示例 1】获取单篇论文\n")
    paper_id = "2301.00001"  # 示例论文 ID
    try:
        paper = crawler.get_paper(paper_id)
        print(format_paper(paper))

        # 保存到 JSON
        with open('paper.json', 'w', encoding='utf-8') as f:
            json.dump(paper, f, ensure_ascii=False, indent=2)
        print(f"\n已保存到 paper.json")
    except Exception as e:
        print(f"获取论文失败: {e}")

    # 示例 2: 搜索论文
    print("\n【示例 2】搜索论文\n")
    try:
        results = crawler.search("transformer attention", max_results=5)
        for i, paper in enumerate(results, 1):
            print(f"\n{i}. {paper['title']}")
            print(f"   ID: {paper['id']}")
            print(f"   链接: {paper['url']}")

        # 保存搜索结果
        with open('search_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n已保存到 search_results.json")
    except Exception as e:
        print(f"搜索失败: {e}")


if __name__ == "__main__":
    main()