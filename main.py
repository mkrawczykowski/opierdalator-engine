import pathlib

from oe import VERSION
from oe.theme import ThemeDNA
from oe.variation import VariationEngine
from oe.renderer import PNGRenderer, LayoutRenderer
from oe.design.tokens import default_tokens
from oe.content import parse

INPUT_DIR = pathlib.Path("input")
OUTPUT_DIR = pathlib.Path("output")


def render_for_file(md_path: pathlib.Path, layout_renderer: LayoutRenderer) -> None:
    tokens = default_tokens()
    sections = parse(md_path, tokens)

    if not sections:
        print(f"  Warning: no #content sections found in {md_path.name}, skipping.")
        return

    out_dir = OUTPUT_DIR / md_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / "layout_board.png"
    layout_renderer.render(sections, tokens, str(out_file))

    print(f"  Generated: {out_file}")


def main():

    dna = ThemeDNA(
        softness=(0.80, 0.10),
        contrast=(0.30, 0.08),
        rhythm=(0.70, 0.12),
        geometry=(0.40, 0.15),
        elegance=(0.75, 0.10),
    )

    engine = VariationEngine(seed=42)

    print()
    print("===================================")
    print("      Opierdalator Engine")
    print("===================================")
    print()
    print(f"Version: {VERSION}")
    print()

    dna.describe()
    print()

    variation = engine.generate(dna)

    # --- Stary renderer (Theme Board) --- zachowany bez zmian
    renderer = PNGRenderer()
    renderer.render(dna, variation, "theme_board.png")
    print("Generated: theme_board.png")
    print()

    # --- Nowy pipeline: input/*.md → output/{name}/layout_board.png
    md_files = sorted(INPUT_DIR.glob("*.md"))

    if not md_files:
        print(f"No .md files found in {INPUT_DIR}/")
        print()
        return

    layout_renderer = LayoutRenderer()

    print(f"Processing {len(md_files)} file(s) from {INPUT_DIR}/:")
    for md_path in md_files:
        print(f"  Reading: {md_path.name}")
        render_for_file(md_path, layout_renderer)

    print()


if __name__ == "__main__":
    main()
