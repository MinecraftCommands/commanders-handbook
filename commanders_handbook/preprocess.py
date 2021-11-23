"""
mdbook preprocessor that checks for packs and runs beet/lectern.
"""

import json
import os
import sys

from commanders_handbook.context import Context

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "supports":
            sys.exit(0)

    CWD = os.getcwd()
    print(f"Preprocessing at: {CWD}", file=sys.stderr)

    context, book = json.load(sys.stdin)
    ctx = Context(context["root"], context["config"], book)
    print(ctx.preprocess())

    # with open(f"{context['root']}/.vscode/preprocess.context.json", "w") as fp:
    #     json.dump(context, fp, indent=2)
    # with open(f"{context['root']}/.vscode/preprocess.book.json", "w") as fp:
    #     json.dump(book, fp, indent=2)
