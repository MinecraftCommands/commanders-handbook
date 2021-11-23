# DELETEME unused

"""
mdbook renderer that writes pack zip files.
"""

import json
import os
import sys

from commanders_handbook.context import Context

if __name__ == "__main__":
    CWD = os.getcwd()
    print(f"Rendering at: {CWD}", file=sys.stderr)

    data = json.load(sys.stdin)
    ctx = Context(data["root"], data["config"], data["book"])
    ctx.render()

    # with open(f"{data['root']}/.vscode/render.data.json", "w") as fp:
    #     json.dump(data, fp, indent=2)
