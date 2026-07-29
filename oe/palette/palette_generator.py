import colorsys


class PaletteGenerator:
    """
    Generuje prostą paletę kolorów na podstawie ThemeVariation.

    Aktualna implementacja jest celowo prosta.
    Jej zadaniem jest udowodnienie architektury,
    a nie wygenerowanie idealnej identyfikacji wizualnej.
    """

    def generate(self, variation):

        softness = variation["softness"]
        contrast = variation["contrast"]
        elegance = variation["elegance"]

        #
        # Kolor bazowy
        #

        hue = 0.58 + (elegance - 0.5) * 0.08
        saturation = 0.18 + softness * 0.35
        value = 0.60 + contrast * 0.20

        primary = self._hsv(hue, saturation, value)

        secondary = self._hsv(
            hue,
            saturation * 0.45,
            min(1.0, value + 0.15),
        )

        surface = self._hsv(
            hue,
            saturation * 0.12,
            0.92,
        )

        background = self._hsv(
            hue,
            saturation * 0.04,
            0.96,
        )

        text = self._hsv(
            hue,
            saturation * 0.18,
            0.20,
        )

        return {
            "primary": primary,
            "secondary": secondary,
            "surface": surface,
            "background": background,
            "text": text,
        }

    # -------------------------------------------------

    def _hsv(
        self,
        h,
        s,
        v,
    ):

        r, g, b = colorsys.hsv_to_rgb(h, s, v)

        return "#{:02X}{:02X}{:02X}".format(
            int(r * 255),
            int(g * 255),
            int(b * 255),
        )