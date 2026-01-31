"""
Module de conversion de couleurs entre différents formats.
Supporte : HEX, RGB, CMYK, HSL, HSV
"""

import re
from typing import Tuple, Dict, Any, List

RE_FLOAT_NUMBER = r'[\d.]+'


class ColorConverter:
    """Classe principale pour la conversion de couleurs."""

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convertit une couleur hexadécimale en RGB."""
        hex_color = hex_color.lstrip('#')

        # Support format court (#RGB)
        if len(hex_color) == 3:
            hex_color = ''.join([c * 2 for c in hex_color])

        if len(hex_color) != 6:
            raise ValueError(f"Format hexadécimal invalide: {hex_color}")

        try:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return (r, g, b)
        except ValueError as e:
            raise ValueError(f"Format hexadécimal invalide: {hex_color}") from e

    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """Convertit RGB en hexadécimal."""
        if not all(0 <= x <= 255 for x in (r, g, b)):
            raise ValueError("Les valeurs RGB doivent être entre 0 et 255")
        return f"#{r:02X}{g:02X}{b:02X}"

    @staticmethod
    def rgb_to_cmyk(r: int, g: int, b: int) -> Tuple[float, float, float, float]:
        """Convertit RGB en CMJN (CMYK)."""
        if r == 0 and g == 0 and b == 0:
            return (0.0, 0.0, 0.0, 100.0)

        # Normaliser RGB en 0-1
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0

        # Calculer K (noir)
        k = 1 - max(r_norm, g_norm, b_norm)

        if k == 1:
            return (0.0, 0.0, 0.0, 100.0)

        # Calculer C, M, J
        c = (1 - r_norm - k) / (1 - k)
        m = (1 - g_norm - k) / (1 - k)
        y = (1 - b_norm - k) / (1 - k)

        # Convertir en pourcentage
        return (
            round(c * 100, 1),
            round(m * 100, 1),
            round(y * 100, 1),
            round(k * 100, 1)
        )

    @staticmethod
    def cmyk_to_rgb(c: float, m: float, y: float, k: float) -> Tuple[int, int, int]:
        """Convertit CMJN (CMYK) en RGB."""
        # Convertir de pourcentage en 0-1
        c = c / 100.0
        m = m / 100.0
        y = y / 100.0
        k = k / 100.0

        r = round(255 * (1 - c) * (1 - k))
        g = round(255 * (1 - m) * (1 - k))
        b = round(255 * (1 - y) * (1 - k))

        return (
            max(0, min(255, r)),
            max(0, min(255, g)),
            max(0, min(255, b))
        )

    @staticmethod
    def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
        """Convertit RGB en HSL."""
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0

        max_c = max(r_norm, g_norm, b_norm)
        min_c = min(r_norm, g_norm, b_norm)
        delta = max_c - min_c

        # Luminosité
        l = (max_c + min_c) / 2

        if delta == 0:
            h = 0
            s = 0
        else:
            # Saturation
            s = delta / (1 - abs(2 * l - 1))

            # Teinte
            if max_c == r_norm:
                h = 60 * (((g_norm - b_norm) / delta) % 6)
            elif max_c == g_norm:
                h = 60 * (((b_norm - r_norm) / delta) + 2)
            else:
                h = 60 * (((r_norm - g_norm) / delta) + 4)

        return (
            round(h, 1),
            round(s * 100, 1),
            round(l * 100, 1)
        )

    @staticmethod
    def hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
        """Convertit HSL en RGB."""
        s = s / 100.0
        l = l / 100.0

        c = (1 - abs(2 * l - 1)) * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = l - c / 2

        if 0 <= h < 60:
            r_prime, g_prime, b_prime = c, x, 0
        elif 60 <= h < 120:
            r_prime, g_prime, b_prime = x, c, 0
        elif 120 <= h < 180:
            r_prime, g_prime, b_prime = 0, c, x
        elif 180 <= h < 240:
            r_prime, g_prime, b_prime = 0, x, c
        elif 240 <= h < 300:
            r_prime, g_prime, b_prime = x, 0, c
        else:
            r_prime, g_prime, b_prime = c, 0, x

        r = round((r_prime + m) * 255)
        g = round((g_prime + m) * 255)
        b = round((b_prime + m) * 255)

        return (
            max(0, min(255, r)),
            max(0, min(255, g)),
            max(0, min(255, b))
        )

    @staticmethod
    def rgb_to_hsv(r: int, g: int, b: int) -> Tuple[float, float, float]:
        """Convertit RGB en HSV."""
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0

        max_c = max(r_norm, g_norm, b_norm)
        min_c = min(r_norm, g_norm, b_norm)
        delta = max_c - min_c

        # Valeur
        v = max_c

        # Saturation
        s = 0 if max_c == 0 else delta / max_c

        # Teinte
        if delta == 0:
            h = 0
        elif max_c == r_norm:
            h = 60 * (((g_norm - b_norm) / delta) % 6)
        elif max_c == g_norm:
            h = 60 * (((b_norm - r_norm) / delta) + 2)
        else:
            h = 60 * (((r_norm - g_norm) / delta) + 4)

        return (
            round(h, 1),
            round(s * 100, 1),
            round(v * 100, 1)
        )

    @staticmethod
    def hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
        """Convertit HSV en RGB."""
        s = s / 100.0
        v = v / 100.0

        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c

        if 0 <= h < 60:
            r_prime, g_prime, b_prime = c, x, 0
        elif 60 <= h < 120:
            r_prime, g_prime, b_prime = x, c, 0
        elif 120 <= h < 180:
            r_prime, g_prime, b_prime = 0, c, x
        elif 180 <= h < 240:
            r_prime, g_prime, b_prime = 0, x, c
        elif 240 <= h < 300:
            r_prime, g_prime, b_prime = x, 0, c
        else:
            r_prime, g_prime, b_prime = c, 0, x

        r = round((r_prime + m) * 255)
        g = round((g_prime + m) * 255)
        b = round((b_prime + m) * 255)

        return (
            max(0, min(255, r)),
            max(0, min(255, g)),
            max(0, min(255, b))
        )

    @classmethod
    def convert_all(cls, r: int, g: int, b: int) -> Dict[str, Any]:
        """Convertit RGB vers tous les formats."""
        return {
            'hex': cls.rgb_to_hex(r, g, b),
            'rgb': (r, g, b),
            'cmyk': cls.rgb_to_cmyk(r, g, b),
            'hsl': cls.rgb_to_hsl(r, g, b),
            'hsv': cls.rgb_to_hsv(r, g, b)
        }

    @classmethod
    def parse_input(cls, input_str: str, format_type: str) -> Tuple[int, int, int]:
        """Parse une entrée utilisateur et retourne RGB."""
        input_str = input_str.strip()
        if format_type == 'hex':
            return cls.hex_to_rgb(input_str)
        elif format_type == 'rgb':
            return cls._parse_rgb(input_str)
        elif format_type == 'cmyk':
            return cls._parse_cmyk(input_str)
        elif format_type == 'hsl':
            return cls._parse_hsl(input_str)
        elif format_type == 'hsv':
            return cls._parse_hsv(input_str)
        else:
            raise ValueError(f"Format inconnu: {format_type}")

    @staticmethod
    def _parse_rgb(input_str: str) -> Tuple[int, int, int]:
        values = re.findall(r'\d+', input_str)
        if len(values) != 3:
            raise ValueError("Format RGB invalide. Utilisez: R, G, B")
        r, g, b = map(int, values)
        if not all(0 <= x <= 255 for x in (r, g, b)):
            raise ValueError("Les valeurs RGB doivent être entre 0 et 255")
        return (r, g, b)

    @staticmethod
    def _parse_cmyk(input_str: str) -> Tuple[int, int, int]:
        values = re.findall(RE_FLOAT_NUMBER, input_str)
        if len(values) != 4:
            raise ValueError("Format CMJN invalide. Utilisez: C, M, J, N")
        c, m, y, k = map(float, values)
        return ColorConverter.cmyk_to_rgb(c, m, y, k)

    @staticmethod
    def _parse_hsl(input_str: str) -> Tuple[int, int, int]:
        values = re.findall(RE_FLOAT_NUMBER, input_str)
        if len(values) != 3:
            raise ValueError("Format HSL invalide. Utilisez: H, S, L")
        h, s, l = map(float, values)
        return ColorConverter.hsl_to_rgb(h, s, l)

    @staticmethod
    def _parse_hsv(input_str: str) -> Tuple[int, int, int]:
        values = re.findall(RE_FLOAT_NUMBER, input_str)
        if len(values) != 3:
            raise ValueError("Format HSV invalide. Utilisez: H, S, V")
        h, s, v = map(float, values)
        return ColorConverter.hsv_to_rgb(h, s, v)


class ColorHarmony:
    """Calcul des harmonies de couleurs."""

    @staticmethod
    def complementary(r: int, g: int, b: int) -> Tuple[int, int, int]:
        """Retourne la couleur complémentaire."""
        h, s, l = ColorConverter.rgb_to_hsl(r, g, b)
        h_comp = (h + 180) % 360
        return ColorConverter.hsl_to_rgb(h_comp, s, l)

    @staticmethod
    def triadic(r: int, g: int, b: int) -> List[Tuple[int, int, int]]:
        """Retourne les couleurs triadiques."""
        h, s, l = ColorConverter.rgb_to_hsl(r, g, b)
        return [
            ColorConverter.hsl_to_rgb((h + 120) % 360, s, l),
            ColorConverter.hsl_to_rgb((h + 240) % 360, s, l)
        ]

    @staticmethod
    def analogous(r: int, g: int, b: int) -> List[Tuple[int, int, int]]:
        """Retourne les couleurs analogues."""
        h, s, l = ColorConverter.rgb_to_hsl(r, g, b)
        return [
            ColorConverter.hsl_to_rgb((h - 30) % 360, s, l),
            ColorConverter.hsl_to_rgb((h + 30) % 360, s, l)
        ]

    @staticmethod
    def split_complementary(r: int, g: int, b: int) -> List[Tuple[int, int, int]]:
        """Retourne les couleurs complémentaires divisées."""
        h, s, l = ColorConverter.rgb_to_hsl(r, g, b)
        return [
            ColorConverter.hsl_to_rgb((h + 150) % 360, s, l),
            ColorConverter.hsl_to_rgb((h + 210) % 360, s, l)
        ]


class ContrastChecker:
    """Vérification du contraste entre couleurs (WCAG)."""

    @staticmethod
    def get_luminance(r: int, g: int, b: int) -> float:
        """Calcule la luminance relative selon WCAG."""
        def adjust(c: float) -> float:
            c = c / 255.0
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

        return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)

    @classmethod
    def contrast_ratio(cls, rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
        """Calcule le ratio de contraste entre deux couleurs."""
        lum1 = cls.get_luminance(*rgb1)
        lum2 = cls.get_luminance(*rgb2)

        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)

        return round((lighter + 0.05) / (darker + 0.05), 2)

    @classmethod
    def wcag_rating(cls, ratio: float) -> Dict[str, bool]:
        """Retourne les niveaux WCAG atteints."""
        contrast_levels: Dict[str, bool] = {
            'AA_normal': ratio >= 4.5,
            'AA_large': ratio >= 3.0,
            'AAA_normal': ratio >= 7.0,
            'AAA_large': ratio >= 4.5
        }
        return contrast_levels
