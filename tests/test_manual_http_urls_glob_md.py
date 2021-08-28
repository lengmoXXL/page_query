from pathlib import Path

from page_query.rule.manual_http_urls_glob_md import ManualHttpUrlsGlobMarkdown

def test_manual_http_urls_glob_md(tmp_path: Path):
    example_file = tmp_path / 'a_b_c.md'
    example_file.write_text('\n'.join([
        "```yaml",
        "tags: [a]",
        "http_urls:",
        "- https://pie.dev/get",
        "```",
        "summary",
    ]))

    rule = ManualHttpUrlsGlobMarkdown([str(tmp_path) + "/*.md"])
    pages = list(rule.pages())
    assert len(pages) == 1

    page = pages[0]
    assert page['title'] == 'a b c'
    assert page['tags'] == ['a']
    assert page['http_urls'] == ['https://pie.dev/get']
    assert page['summary'] == 'summary'