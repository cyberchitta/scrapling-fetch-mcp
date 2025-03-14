from typing import Optional
from pydantic import BaseModel, Field
from scrapling.defaults import AsyncFetcher, StealthyFetcher
from readabilipy import simple_tree_from_html_string
from scrapling_mcp._markdownify import _CustomMarkdownify


class UrlFetchRequest(BaseModel):
    url: str = Field(..., description="URL to fetch")
    mode: str = Field(
        "basic", description="Fetching mode (basic, stealth, or max-stealth)"
    )
    format: str = Field("markdown", description="Output format (html or markdown)")


async def fetch_url(request: UrlFetchRequest) -> str:
    if request.mode == "basic":
        page = await AsyncFetcher.get(request.url, stealthy_headers=True)
    elif request.mode == "stealth":
        page = await StealthyFetcher.async_fetch(
            request.url, headless=True, network_idle=True
        )
    elif request.mode == "max-stealth":
        page = await StealthyFetcher.async_fetch(
            request.url,
            headless=True,
            block_webrtc=True,
            network_idle=True,
            disable_resources=False,
            block_images=False,
        )
    else:
        raise ValueError(f"Unknown mode: {request.mode}")
    return _extract_content(page, request)


def _extract_content(page, request) -> str:
    is_markdown = request.format == "markdown"
    return _html_to_markdown(page.html_content) if is_markdown else page.html_content


def _html_to_markdown(html: str, **kwargs) -> str:
    tree = simple_tree_from_html_string(html)
    return _CustomMarkdownify().convert_soup(tree)
