"""
ConvertiColor - Interface graphique principale.
Application de conversion de couleurs avec Tkinter.
"""

from typing import Any, Dict, Tuple, Optional
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from src.color_converter import ColorConverter, ColorHarmony, ContrastChecker

# Ajouter le dossier src au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class RoundedFrame(tk.Canvas):
    """Canvas simulant un cadre avec coins arrondis."""
    bg_color: str
    radius: int

    CONFIGURE_EVENT = "<Configure>"

    def __init__(self, parent: tk.Widget, bg_color: str = "#FFFFFF",
                 radius: int = 15, **kwargs: Any) -> None:
        super().__init__(parent, highlightthickness=0, **kwargs)
        self.bg_color = bg_color
        self.radius = radius
        self.bind(self.CONFIGURE_EVENT, self._draw_rounded)

    def _draw_rounded(self, event: Optional[tk.Event] = None) -> None:
        """Dessine le rectangle arrondi."""
        self.delete("rounded")
        w = self.winfo_width()
        h = self.winfo_height()
        r = self.radius

        # Créer un rectangle arrondi
        self.create_arc(0, 0, 2*r, 2*r, start=90, extent=90,  # type: ignore
                        fill=self.bg_color, outline=self.bg_color, tags="rounded")
        self.create_arc(w-2*r, 0, w, 2*r, start=0, extent=90,    # type: ignore
                        fill=self.bg_color, outline=self.bg_color, tags="rounded")
        self.create_arc(0, h-2*r, 2*r, h, start=180, extent=90,  # type: ignore
                        fill=self.bg_color, outline=self.bg_color, tags="rounded")
        self.create_arc(w-2*r, h-2*r, w, h, start=270, extent=90,  # type: ignore
                        fill=self.bg_color, outline=self.bg_color, tags="rounded")

        self.create_rectangle(r, 0, w-r, h, fill=self.bg_color, outline=self.bg_color,
                              tags="rounded")
        self.create_rectangle(0, r, w, h-r, fill=self.bg_color, outline=self.bg_color,
                              tags="rounded")

    def set_color(self, color: str) -> None:
        """Change la couleur de fond."""
        self.bg_color = color
        self._draw_rounded()



class ConvertiColorApp:
    """Application principale ConvertiColor."""

    BG_COLOR: str = '#F5F5F5'
    FONT_MAIN: str = 'Segoe UI'
    FONT_MONO: str = 'Consolas'
    STYLE_TITLE: str = 'Title.TLabel'
    STYLE_SUBTITLE: str = 'Subtitle.TLabel'
    STYLE_SECTION: str = 'Section.TLabel'
    STYLE_VALUE: str = 'Value.TLabel'

    FORMATS: Dict[str, Tuple[str, str]] = {
        'hex': ('Hexadécimal', '#RRGGBB'),
        'rgb': ('RGB', 'R, G, B (0-255)'),
        'cmyk': ('CMJN', 'C, M, J, N (0-100%)'),
        'hsl': ('HSL', 'H (0-360), S, L (0-100%)'),
        'hsv': ('HSV', 'H (0-360), S, V (0-100%)')
    }

    def __init__(self) -> None:
        self.root: tk.Tk = tk.Tk()
        self.root.title("ConvertiColor - Convertisseur de couleurs")
        self.root.geometry("520x750")
        self.root.minsize(480, 700)
        self.root.configure(bg=self.BG_COLOR)

        # Variables
        self.input_format: tk.StringVar = tk.StringVar(value='hex')
        self.input_value: tk.StringVar = tk.StringVar()
        self.current_rgb: Tuple[int, int, int] = (128, 128, 128)  # Gris par défaut
        self.contrast_rgb: Tuple[int, int, int] = (255, 255, 255)  # Blanc par défaut

        # Créer l'interface
        self._create_widgets()
        self._update_display()

        # Style
        self._setup_style()

    def _setup_style(self) -> None:
        """Configure le style ttk."""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure(self.STYLE_TITLE, font=(self.FONT_MAIN, 16, 'bold'),
                        background=self.BG_COLOR)
        style.configure(self.STYLE_SUBTITLE, font=(self.FONT_MAIN, 10),
                        background=self.BG_COLOR, foreground='#666')
        style.configure(self.STYLE_SECTION, font=(self.FONT_MAIN, 11, 'bold'),
                        background=self.BG_COLOR)
        style.configure(self.STYLE_VALUE, font=(self.FONT_MONO, 11),
                        background=self.BG_COLOR)

        style.configure('TRadiobutton', font=(self.FONT_MAIN, 10), background=self.BG_COLOR)
        style.configure('TButton', font=(self.FONT_MAIN, 10))
        style.configure('Copy.TButton', font=(self.FONT_MAIN, 8))
        style.configure('TFrame', background=self.BG_COLOR)
        style.configure('TLabelframe', background=self.BG_COLOR)
        style.configure('TLabelframe.Label', background=self.BG_COLOR)
        style.configure('TLabel', background=self.BG_COLOR)

    def _create_widgets(self) -> None:
        """Crée tous les widgets de l'interface."""
        # Container principal avec scrollbar
        container = ttk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True)

        # Canvas pour le scroll
        self.canvas = tk.Canvas(container, bg=self.BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical",
                                  command=self.canvas.yview)  # type: ignore

        # Frame scrollable
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            RoundedFrame.CONFIGURE_EVENT,
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Bind mousewheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Pack canvas et scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Main frame dans le scrollable frame
        main_frame = ttk.Frame(self.scrollable_frame, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Bind pour ajuster la largeur du canvas
        container.bind(RoundedFrame.CONFIGURE_EVENT, self._on_frame_configure)

        # Titre
        title_label = ttk.Label(main_frame, text="🎨 ConvertiColor", style=self.STYLE_TITLE)
        title_label.pack(pady=(0, 5))

        subtitle = ttk.Label(main_frame, text="Convertisseur de couleurs multi-formats",
                             style=self.STYLE_SUBTITLE)
        subtitle.pack(pady=(0, 15))

        # --- Section aperçu couleur ---
        preview_frame = ttk.Frame(main_frame)
        preview_frame.pack(fill=tk.X, pady=(0, 15))

        self.color_preview = RoundedFrame(
            preview_frame,
            bg_color="#808080",
            radius=15,
            width=200,
            height=100
        )
        self.color_preview.pack(pady=5)

        # --- Section entrée ---
        input_frame = ttk.LabelFrame(main_frame, text=" Entrée ", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 15))

        # Sélection du format
        format_frame = ttk.Frame(input_frame)
        format_frame.pack(fill=tk.X, pady=(0, 10))

        for fmt, (name, _) in self.FORMATS.items():
            rb = ttk.Radiobutton(
                format_frame,
                text=name,
                value=fmt,
                variable=self.input_format,
                command=self._update_placeholder
            )
            rb.pack(side=tk.LEFT, padx=5)

        # Champ de saisie
        entry_frame = ttk.Frame(input_frame)
        entry_frame.pack(fill=tk.X)

        self.input_entry = ttk.Entry(entry_frame, textvariable=self.input_value,
                                     font=('Consolas', 12))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_entry.bind('<Return>', lambda e: self._convert())

        convert_btn = ttk.Button(entry_frame, text="Convertir", command=self._convert)
        convert_btn.pack(side=tk.RIGHT)

        # Placeholder
        self.placeholder_label = ttk.Label(input_frame, text="Format: #RRGGBB",
                                           style=self.STYLE_SUBTITLE)
        self.placeholder_label.pack(anchor=tk.W, pady=(5, 0))

        # --- Section résultats ---
        results_frame = ttk.LabelFrame(main_frame, text=" Résultats ", padding="10")
        results_frame.pack(fill=tk.X, pady=(0, 15))

        self.result_labels: Dict[str, ttk.Label] = {}
        self.result_entries: Dict[str, tk.StringVar] = {}

        for fmt, (name, _) in self.FORMATS.items():
            row = ttk.Frame(results_frame)
            row.pack(fill=tk.X, pady=3)

            label = ttk.Label(row, text=f"{name}:", width=12, style='Section.TLabel')
            label.pack(side=tk.LEFT)

            value_var = tk.StringVar()
            entry = ttk.Entry(row, textvariable=value_var, font=('Consolas', 11),
                              state='readonly', width=25)
            entry.pack(side=tk.LEFT, padx=5)

            copy_btn = ttk.Button(row, text="📋", width=3,
                                  command=lambda v=value_var: self._copy_to_clipboard(v.get()))
            copy_btn.pack(side=tk.LEFT)

            self.result_entries[fmt] = value_var

        # --- Section harmonies ---
        harmony_frame = ttk.LabelFrame(main_frame, text=" Harmonies de couleurs ", padding="10")
        harmony_frame.pack(fill=tk.X, pady=(0, 15))

        self.harmony_canvas = tk.Canvas(harmony_frame, height=60, bg=self.BG_COLOR,
                                        highlightthickness=0)
        self.harmony_canvas.pack(fill=tk.X)

        harmony_labels = ttk.Frame(harmony_frame)
        harmony_labels.pack(fill=tk.X)

        for text in ["Originale", "Complémentaire", "Analogue 1", "Analogue 2", "Triadique 1"]:
            lbl = ttk.Label(harmony_labels, text=text, font=('Segoe UI', 8), anchor='center')
            lbl.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # --- Section contraste ---
        contrast_frame = ttk.LabelFrame(main_frame, text=" Vérificateur de contraste WCAG ",
                                        padding="10")
        contrast_frame.pack(fill=tk.X, pady=(0, 10))

        contrast_input_frame = ttk.Frame(contrast_frame)
        contrast_input_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(contrast_input_frame, text="Couleur de fond (hex):").pack(side=tk.LEFT)
        self.contrast_entry = ttk.Entry(contrast_input_frame, width=15, font=('Consolas', 10))
        self.contrast_entry.insert(0, "#FFFFFF")
        self.contrast_entry.pack(side=tk.LEFT, padx=10)

        check_btn = ttk.Button(contrast_input_frame, text="Vérifier", command=self._check_contrast)
        check_btn.pack(side=tk.LEFT)

        # Aperçu contraste
        self.contrast_preview = tk.Canvas(contrast_frame, height=50, highlightthickness=1,
                                          highlightbackground="#ccc")
        self.contrast_preview.pack(fill=tk.X, pady=5)

        # Résultats contraste
        self.contrast_result = ttk.Label(contrast_frame, text="Ratio: -- | WCAG: --",
                                         style='Value.TLabel')
        self.contrast_result.pack()

        self.wcag_details = ttk.Label(contrast_frame, text="", style=self.STYLE_SUBTITLE)
        self.wcag_details.pack()

    def _update_placeholder(self) -> None:
        """Met à jour le placeholder selon le format sélectionné."""
        fmt = self.input_format.get()
        _, hint = self.FORMATS[fmt]
        self.placeholder_label.config(text=f"Format: {hint}")

    def _convert(self) -> None:
        """Convertit la couleur entrée."""
        try:
            input_str = self.input_value.get().strip()
            if not input_str:
                messagebox.showwarning("Entrée vide", "Veuillez entrer une valeur de couleur.")
                return

            fmt = self.input_format.get()
            self.current_rgb = ColorConverter.parse_input(input_str, fmt)
            self._update_display()

        except ValueError as e:
            messagebox.showerror("Erreur de format", str(e))

    def _update_display(self) -> None:
        """Met à jour l'affichage avec la couleur actuelle."""
        r, g, b = self.current_rgb

        # Convertir vers tous les formats
        results = ColorConverter.convert_all(r, g, b)

        # Mettre à jour les champs de résultat
        self.result_entries['hex'].set(results['hex'])
        self.result_entries['rgb'].set(f"{r}, {g}, {b}")
        c, m, y, k = results['cmyk']
        self.result_entries['cmyk'].set(f"{c}%, {m}%, {y}%, {k}%")
        h, s, l = results['hsl']
        self.result_entries['hsl'].set(f"{h}°, {s}%, {l}%")
        h, s, v = results['hsv']
        self.result_entries['hsv'].set(f"{h}°, {s}%, {v}%")

        # Mettre à jour l'aperçu
        hex_color = results['hex']
        self.color_preview.set_color(hex_color)

        # Mettre à jour les harmonies
        self._update_harmonies()

        # Mettre à jour le contraste
        self._check_contrast()

    def _update_harmonies(self) -> None:
        """Met à jour l'affichage des harmonies."""
        r, g, b = self.current_rgb

        # Couleurs à afficher
        colors: list[Tuple[int, int, int]] = [
            (r, g, b),  # Originale
            ColorHarmony.complementary(r, g, b),  # Complémentaire
            ColorHarmony.analogous(r, g, b)[0],  # Analogue 1
            ColorHarmony.analogous(r, g, b)[1],  # Analogue 2
            ColorHarmony.triadic(r, g, b)[0],  # Triadique 1
        ]

        self.harmony_canvas.delete("all")
        canvas_width = self.harmony_canvas.winfo_width()
        if canvas_width < 10:
            canvas_width = 400  # Valeur par défaut

        box_width = canvas_width // len(colors)
        box_height = 50

        for i, (cr, cg, cb) in enumerate(colors):
            x1 = i * box_width + 5
            x2 = (i + 1) * box_width - 5
            hex_c = f"#{cr:02X}{cg:02X}{cb:02X}"

            # Dessiner un rectangle arrondi (simulé)
            self.harmony_canvas.create_rectangle(
                x1, 5, x2, box_height,
                fill=hex_c,
                outline="#999",
                width=1
            )

    def _check_contrast(self) -> None:
        """Vérifie le contraste WCAG."""
        try:
            contrast_hex = self.contrast_entry.get().strip()
            if not contrast_hex:
                contrast_hex = "#FFFFFF"

            self.contrast_rgb = ColorConverter.hex_to_rgb(contrast_hex)

            # Calculer le ratio
            ratio = ContrastChecker.contrast_ratio(self.current_rgb, self.contrast_rgb)
            wcag = ContrastChecker.wcag_rating(ratio)

            # Mettre à jour l'aperçu
            self.contrast_preview.delete("all")
            bg_hex = ColorConverter.rgb_to_hex(*self.contrast_rgb)
            fg_hex = ColorConverter.rgb_to_hex(*self.current_rgb)

            self.contrast_preview.configure(bg=bg_hex)
            self.contrast_preview.create_text(
                self.contrast_preview.winfo_width() // 2 or 200,
                25,
                text="Exemple de texte avec cette couleur",
                fill=fg_hex,
                font=(self.FONT_MAIN, 12, 'bold')
            )

            # Afficher le résultat
            rating = "❌ Échoue"
            if wcag['AAA_normal']:
                rating = "✅ AAA (Excellent)"
            elif wcag['AA_normal']:
                rating = "✅ AA (Bon)"
            elif wcag['AA_large']:
                rating = "⚠️ AA grands textes"

            self.contrast_result.config(text=f"Ratio: {ratio}:1 | {rating}")

            details: list[str] = []
            details.append(f"AA normal (≥4.5): {'✅' if wcag['AA_normal'] else '❌'}")
            details.append(f"AA large (≥3.0): {'✅' if wcag['AA_large'] else '❌'}")
            details.append(f"AAA normal (≥7.0): {'✅' if wcag['AAA_normal'] else '❌'}")
            details.append(f"AAA large (≥4.5): {'✅' if wcag['AAA_large'] else '❌'}")
            self.wcag_details.config(text=" | ".join(details))

        except ValueError:
            self.contrast_result.config(text="Format hexadécimal invalide")
            self.wcag_details.config(text="")

    def _copy_to_clipboard(self, value: str) -> None:
        """Copie une valeur dans le presse-papier."""
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        self.root.update()

        # Feedback visuel temporaire
        messagebox.showinfo("Copié", f"'{value}' copié dans le presse-papier!")

    def _on_mousewheel(self, event: tk.Event) -> None:
        """Gère le scroll avec la molette de la souris."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_frame_configure(self, event: tk.Event) -> None:
        """Ajuste la largeur du contenu scrollable."""
        self.canvas.itemconfig(
            self.canvas.find_withtag("all")[0],
            width=event.width
        )

    def run(self) -> None:
        """Lance l'application."""
        self.root.mainloop()



def main() -> None:
    """Point d'entrée principal."""
    app = ConvertiColorApp()
    app.run()


if __name__ == "__main__":
    main()
