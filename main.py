from oe import VERSION
from oe.theme import ThemeDNA


def main():

    dna = ThemeDNA(
        softness=0.84,
        contrast=0.27,
        rhythm=0.71,
        geometry=0.42,
        elegance=0.79
    )

    print()
    print("===================================")
    print("      Opierdalator Engine")
    print("===================================")
    print()
    print(f"Version: {VERSION}")
    print()

    dna.describe()

    print()


if __name__ == "__main__":
    main()