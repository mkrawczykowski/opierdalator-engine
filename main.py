import pathlib

from oe import VERSION
from oe.theme import ThemeDNA
from oe.variation import VariationEngine
from oe.renderer import PNGRenderer, LayoutRenderer
from oe.design.tokens import default_tokens
from oe.content import parse, parse_tokens, build_sections, parse_settings, TokenVariator

INPUT_DIR = pathlib.Path("input")
OUTPUT_DIR = pathlib.Path("output")


def render_project(
    project_dir: pathlib.Path,
    layout_renderer: LayoutRenderer,
    variator: TokenVariator,
) -> None:
    name = project_dir.name
    contents_path = project_dir / "contents.md"
    settings_path = project_dir / "settings.md"

    settings = parse_settings(settings_path)
    base_tokens = default_tokens()

    # Najpierw aplikuj ustawienia z MD (kolory, padding z #components)
    # na default_tokens — to jest baza dla variatora.
    md_tokens = parse_tokens(contents_path, base_tokens)

    # Wstępne parsowanie sekcji tylko po to, żeby sprawdzić czy #content istnieje
    probe = parse(contents_path, md_tokens)
    if not probe:
        print(f"  Warning: no #content found in {name}/contents.md, skipping.")
        return

    out_dir = OUTPUT_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"  Project: {name}  "
          f"[layouts={settings.no_of_layouts}, variability={settings.variability_pct}%]")

    for i in range(1, settings.no_of_layouts + 1):
        # Variator działa na tokenach z MD (nie na surowych defaults)
        varied_tokens = variator.vary(md_tokens, settings.variability_pct, seed=i)

        # Buduj sekcje z varied_tokens — bez ponownego aplikowania MD
        sections = build_sections(contents_path, varied_tokens)

        out_file = out_dir / f"layout_board_{i}.png"
        layout_renderer.render(sections, varied_tokens, str(out_file))
        print(f"    Generated: {out_file.name}")


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

    # --- Nowy pipeline: input/{name}/contents.md → output/{name}/layout_board_N.png
    project_dirs = sorted(
        p for p in INPUT_DIR.iterdir()
        if p.is_dir() and (p / "contents.md").exists()
    )

    if not project_dirs:
        print(f"No projects found in {INPUT_DIR}/")
        print()
        return

    layout_renderer = LayoutRenderer()
    variator = TokenVariator()

    print(f"Processing {len(project_dirs)} project(s) from {INPUT_DIR}/:")
    for project_dir in project_dirs:
        render_project(project_dir, layout_renderer, variator)

    print()


if __name__ == "__main__":
    main()
