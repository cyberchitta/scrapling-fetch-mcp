from functools import reduce
from json import dumps
from re import compile
from re import error as re_error
from typing import Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from scrapling_fetch_mcp._markdownify import _CustomMarkdownify
from scrapling_fetch_mcp._scrapling import browse_url


def _require_web_url(url: str) -> str:
    scheme = urlparse(url).scheme.lower()
    if scheme not in ("http", "https"):
        raise ValueError(
            f"unsupported URL scheme '{scheme}': only http/https are allowed"
        )
    return url


def _html_to_markdown(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for script in soup(["script", "style"]):
        script.extract()
    body_elm = soup.find("body")
    return _CustomMarkdownify().convert_soup(body_elm if body_elm else soup)


def _search_content(
    content: str, pattern: str, context_chars: int = 200
) -> tuple[str, int]:
    try:
        matches = list(compile(pattern).finditer(content))
        if not matches:
            return "", 0
        chunks = [
            (
                max(0, match.start() - context_chars),
                min(len(content), match.end() + context_chars),
            )
            for match in matches
        ]
        merged_chunks = reduce(
            lambda acc, chunk: (
                [*acc[:-1], (acc[-1][0], max(acc[-1][1], chunk[1]))]
                if acc and chunk[0] <= acc[-1][1]
                else [*acc, chunk]
            ),
            chunks,
            [],
        )
        result_sections = [
            f"॥๛॥\n[Position: {start}-{end}]\n{content[start:end]}"
            for start, end in merged_chunks
        ]
        return "\n".join(result_sections), len(matches)
    except re_error as e:
        return f"ERROR: Invalid regex pattern: {str(e)}", 0


def _create_metadata(
    total_length: int,
    retrieved_length: int,
    is_truncated: bool,
    start_index: Optional[int] = None,
    match_count: Optional[int] = None,
) -> str:
    metadata = {
        "total_length": total_length,
        "retrieved_length": retrieved_length,
        "is_truncated": is_truncated,
        "percent_retrieved": round((retrieved_length / total_length) * 100, 2)
        if total_length > 0
        else 100,
    }
    if start_index is not None:
        metadata["start_index"] = start_index
    if match_count is not None:
        metadata["match_count"] = match_count
    return dumps(metadata)


async def fetch_page_impl(
    url: str, mode: str, format: str, max_length: int, start_index: int
) -> str:
    page = await browse_url(_require_web_url(url), mode)
    is_markdown = format == "markdown"
    full_content = (
        _html_to_markdown(page.html_content) if is_markdown else page.html_content
    )

    total_length = len(full_content)
    truncated_content = full_content[start_index : start_index + max_length]
    is_truncated = total_length > (start_index + max_length)

    metadata_json = _create_metadata(
        total_length, len(truncated_content), is_truncated, start_index
    )
    return f"METADATA: {metadata_json}\n\n{truncated_content}"


async def fetch_pattern_impl(
    url: str,
    search_pattern: str,
    mode: str,
    format: str,
    max_length: int,
    context_chars: int,
) -> str:
    page = await browse_url(_require_web_url(url), mode)
    is_markdown = format == "markdown"
    full_content = (
        _html_to_markdown(page.html_content) if is_markdown else page.html_content
    )

    original_length = len(full_content)
    matched_content, match_count = _search_content(
        full_content, search_pattern, context_chars
    )

    if not matched_content:
        metadata_json = _create_metadata(original_length, 0, False, None, 0)
        return f"METADATA: {metadata_json}\n\n"

    truncated_content = matched_content[:max_length]
    is_truncated = len(matched_content) > max_length

    metadata_json = _create_metadata(
        original_length, len(truncated_content), is_truncated, None, match_count
    )
    return f"METADATA: {metadata_json}\n\n{truncated_content}"
