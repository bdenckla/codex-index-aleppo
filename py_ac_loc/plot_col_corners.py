"""
Scatter plot of column corners in relative image space for all pages.

Shows TL, TR, BL, BR corners of both columns across all 24 pages,
plotted in image-space coordinates (y-axis inverted).

Usage:
    python py_ac_loc/plot_col_corners.py
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt

COORD_DIR = Path(__file__).resolve().parent / "column-coordinates"
OUT_DIR = Path(__file__).resolve().parent.parent / ".novc"


def main():
    pages = sorted(COORD_DIR.glob("*.json"))
    if not pages:
        print("No coordinate files found.")
        return

    # Separate recto (r) and verso (v) pages.
    corners = {
        "r": {"col1": [], "col2": []},
        "v": {"col1": [], "col2": []},
    }

    for p in pages:
        data = json.loads(p.read_text(encoding="utf-8"))
        page_id = data["page"]
        side = "r" if page_id.endswith("r") else "v"
        for col_key in ("col1", "col2"):
            rel = data["columns"][col_key]["rel"]
            x, y, w, h = rel["x"], rel["y"], rel["w"], rel["h"]
            corners[side][col_key].extend([
                (x, y, "TL"), (x + w, y, "TR"),
                (x, y + h, "BL"), (x + w, y + h, "BR"),
            ])

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_title("Column Corners in Relative Image Space (all pages)", fontsize=13)
    ax.set_xlabel("x (relative)")
    ax.set_ylabel("y (relative)")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(1.02, -0.02)  # invert y so top of image is at top
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)

    markers = {"TL": "^", "TR": ">", "BL": "v", "BR": "<"}
    # Recto = warm colours, Verso = cool colours
    colors = {
        ("r", "col1"): "red",
        ("r", "col2"): "orange",
        ("v", "col1"): "blue",
        ("v", "col2"): "cornflowerblue",
    }

    for side in ("r", "v"):
        side_label = "recto" if side == "r" else "verso"
        for col_key in ("col1", "col2"):
            col_label = "C1" if col_key == "col1" else "C2"
            color = colors[(side, col_key)]
            pts = corners[side][col_key]
            for corner_type in ("TL", "TR", "BL", "BR"):
                subset = [(x, y) for x, y, ct in pts if ct == corner_type]
                if subset:
                    xs = [p[0] for p in subset]
                    ys = [p[1] for p in subset]
                    ax.scatter(xs, ys, c=color, marker=markers[corner_type],
                               s=40, zorder=3,
                               label=f"{side_label} {col_label} {corner_type}")

    ax.legend(fontsize=7, loc="lower center", ncol=4)

    fig.tight_layout()
    OUT_DIR.mkdir(exist_ok=True)
    out_path = OUT_DIR / "col_coord_scatter.png"
    persistent_path = COORD_DIR.parent / "col_coord_scatter.png"
    fig.savefig(str(out_path), dpi=150)
    fig.savefig(str(persistent_path), dpi=150)
    print(f"Saved to {out_path}")
    print(f"Saved to {persistent_path}")


if __name__ == "__main__":
    main()
