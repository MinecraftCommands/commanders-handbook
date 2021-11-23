import copy
import io
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable
from zipfile import ZipFile

from beet import Context as BeetContext
from beet import ProjectConfig, config_error_handler, run_beet
from lectern import Document

GENERATED_DIR = "__generated__"
PACKS_DIR = "packs"
TEMPLATE_PATTERN = re.compile(r"\{\{\s*\#packs\s*\}\}")


def beet_default(ctx: BeetContext):
    document = ctx.inject(Document)
    document.cache = None
    document.add_markdown(ctx.meta["source"])


@dataclass
class Result:
    book: dict
    packs: Dict[Path, bytes] = field(default_factory=lambda: dict())


@dataclass
class Context:
    root: str
    config: dict
    book: dict

    @property
    def root_path(self) -> Path:
        return Path(self.root)

    # DELETEME unused
    @property
    def build_path(self) -> Path:
        return (
            self.root_path / self.config["build"]["build-dir"] / "commanders_handbook"
        )

    @property
    def generated_path(self) -> Path:
        return self.root_path / self.config["book"]["src"] / GENERATED_DIR

    @property
    def packs_path(self) -> Path:
        return self.root_path / self.config["book"]["src"] / GENERATED_DIR / PACKS_DIR

    def print(self, message: str):
        print(message, file=sys.stderr)

    def build_packs(
        self, result: Result, section: dict, chapter: dict, content: str
    ) -> Iterable[Path]:
        chapter_path = Path(chapter["path"])
        chapter_output_path = self.packs_path / chapter_path

        base_config = {
            "name": chapter_path.with_suffix("").name,
            "pipeline": [__name__],
            "meta": {
                "source": content,
            },
        }

        with config_error_handler():
            config = (
                ProjectConfig()
                .resolve(self.root_path)
                .with_defaults(ProjectConfig(**base_config).resolve(self.root_path))
            )

        with run_beet(config) as ctx:
            for pack in ctx.packs:
                if pack:
                    fp = io.BytesIO()

                    with ZipFile(fp, mode="w") as output:
                        pack.dump(output)
                        output.writestr("source.md", content)

                    pack_name = str(pack.name)
                    pack_output_path = (
                        chapter_output_path.parent / pack_name
                    ).with_suffix(".zip")

                    data = fp.getvalue()

                    self.print(f"  Built pack: {pack_name} ({len(data)} bytes)")

                    result.packs[pack_output_path] = data

                    pack_rel = pack_output_path.relative_to(self.generated_path.parent)
                    depth = len(chapter_path.parents) - 1
                    pack_up = Path("../" * depth)
                    yield pack_up / pack_rel

    def process_content(
        self, result: Result, section: dict, chapter: dict, content: str
    ):
        if TEMPLATE_PATTERN.search(content):
            filepaths = list(self.build_packs(result, section, chapter, content))
            lines = [f"- [{filepath.name}]({filepath})" for filepath in filepaths]
            replacement = "\n".join(lines)
            chapter["content"] = TEMPLATE_PATTERN.sub(replacement, content)

    def process_chapter(self, result: Result, section: dict, chapter: dict):
        # process the chapter's own content
        if isinstance(content := chapter.get("content"), str):
            self.process_content(result, section, chapter, content)

        # recursively process any sub-sections
        if isinstance(subsections := chapter.get("sub_items"), list):
            for subsection in subsections:
                if isinstance(subsection, dict):
                    self.process_section(result, subsection)

    def process_section(self, result: Result, section: dict):
        # make sure it's a chapter
        if isinstance(chapter := section.get("Chapter"), dict):
            self.process_chapter(result, section, chapter)

    def process(self) -> Result:
        result = Result(book=copy.deepcopy(self.book))

        # process root sections
        if isinstance(sections := result.book.get("sections"), list):
            for section in sections:
                if isinstance(section, dict):
                    self.process_section(result, section)

        return result

    def preprocess(self) -> str:
        result = self.process()

        for filepath, data in result.packs.items():
            self.print(f"  Writing pack: {filepath} ({len(data)} bytes)")
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, "wb") as fp:
                fp.write(data)

        return json.dumps(result.book)

    # DELETEME unused
    def render(self):
        result = self.process()
        for filepath, data in result.packs.items():
            self.print(f"  Writing pack: {filepath} ({len(data)} bytes)")
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, "wb") as fp:
                fp.write(data)
