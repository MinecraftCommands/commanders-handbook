"""
mdbook preprocessor that checks for data packs and runs lectern.

https://rust-lang.github.io/mdBook/for_developers/preprocessors.html#hooking-into-mdbook
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Iterable
from zipfile import ZipFile

from beet import Context, ProjectConfig, config_error_handler, run_beet
from lectern import Document

TEMPLATE_PATTERN = re.compile(r"\{\{\s*\#packs\s*\}\}")


def beet_default(ctx: Context):
    document = ctx.inject(Document)
    document.cache = None
    document.add_markdown(ctx.meta["source"])


def build_pack(
    context: dict, book: dict, section: dict, chapter: dict, content: str
) -> Iterable[Path]:
    build_path = context["config"]["build"]["build-dir"]

    chapter_path = Path(chapter["path"])
    chapter_output_path = Path(build_path).absolute() / chapter_path
    chapter_output_path.parent.mkdir(parents=True, exist_ok=True)

    project_directory = os.getcwd()

    base_config = {
        "name": chapter_path.with_suffix("").name,
        "pipeline": [__name__],
        "meta": {
            "source": content,
            "build_attachments": {},
        },
    }

    with config_error_handler():
        config = (
            ProjectConfig()
            .resolve(project_directory)
            .with_defaults(ProjectConfig(**base_config).resolve(project_directory))
        )

    with run_beet(config) as ctx:
        for pack in ctx.packs:
            if pack:
                pack_name = str(pack.name)
                pack_output_path = (chapter_output_path.parent / pack_name).with_suffix(
                    ".zip"
                )

                print(f"Writing pack: {pack_output_path}", file=sys.stderr)

                with ZipFile(pack_output_path, mode="w") as output:
                    pack.dump(output)
                    output.writestr("source.md", content)

                yield pack_output_path


def process_content(
    context: dict, book: dict, section: dict, chapter: dict, content: str
):
    def repl(match) -> str:
        filepaths = list(build_pack(context, book, section, chapter, content))
        lines = [f"- [{filepath.name}]({filepath})" for filepath in filepaths]
        return "\n".join(lines)

    chapter["content"] = TEMPLATE_PATTERN.sub(repl, content)


def process_chapter(context: dict, book: dict, section: dict, chapter: dict):
    # process the chapter's own content
    if isinstance(content := chapter.get("content"), str):
        process_content(context, book, section, chapter, content)

    # recursively process any sub-sections
    if isinstance(subsections := chapter.get("sub_items"), list):
        for subsection in subsections:
            if isinstance(subsection, dict):
                process_section(context, book, subsection)


def process_section(context: dict, book: dict, section: dict):
    # make sure it's a chapter
    if isinstance(chapter := section.get("Chapter"), dict):
        process_chapter(context, book, section, chapter)


def process(context: dict, book: dict):
    # process root sections
    if isinstance(sections := book.get("sections"), list):
        for section in sections:
            if isinstance(section, dict):
                process_section(context, book, section)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "supports":
            sys.exit(0)
    context, book = json.load(sys.stdin)
    process(context, book)
    print(json.dumps(book))
