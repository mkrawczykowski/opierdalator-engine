from oe import VERSION
from oe.theme import ThemeDNA
from oe.variation import VariationEngine


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
    print("Generated variations")
    print("-------------------------")

    for i in range(5):

        variation = engine.generate(dna)

        print()
        print(f"Variation {i + 1}")

        for key, value in variation.items():
            print(f"{key:10} {value:.3f}")

    print()


if __name__ == "__main__":
    main()