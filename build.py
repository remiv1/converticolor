"""
Script de build pour créer les exécutables Windows et Linux.
Utilise PyInstaller pour générer les packages.
"""

import subprocess
import sys
import os
import shutil
import argparse
from pathlib import Path


def clean_build():
    """Nettoie les dossiers de build précédents."""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ Supprimé: {dir_name}")

    # Nettoyer les fichiers .spec
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"✓ Supprimé: {spec_file}")


def build_windows():
    """Construit l'exécutable Windows (.exe)."""
    print("\n" + "="*50)
    print("Construction de l'exécutable Windows...")
    print("="*50 + "\n")

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',                    # Un seul fichier exe
        '--windowed',                   # Pas de console
        '--name=ConvertiColor',         # Nom de l'exécutable
        '--icon=assets/icon.ico',       # Icône (si disponible)
        '--paths=src',                  # Ajouter src au PYTHONPATH
        '--hidden-import=color_converter',  # Inclure le module
        'src/main.py'                   # Script principal
    ]

    # Vérifier si l'icône existe
    if not os.path.exists('assets/icon.ico'):
        cmd = [c for c in cmd if 'icon=' not in c]
        print("⚠ Icône non trouvée, build sans icône...")

    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Build Windows terminé!")
        print("   Exécutable: dist/ConvertiColor.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur lors du build Windows: {e}")
        return False


def build_linux():
    """Construit l'exécutable Linux."""
    print("\n" + "="*50)
    print("Construction de l'exécutable Linux...")
    print("="*50 + "\n")

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',                    # Un seul fichier
        '--windowed',                   # Mode graphique
        '--name=converticolor',         # Nom de l'exécutable (minuscule pour Linux)
        'src/main.py'                   # Script principal
    ]

    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Build Linux terminé!")
        print("   Exécutable: dist/converticolor")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur lors du build Linux: {e}")
        return False


def create_appimage():
    """Crée un AppImage pour Linux (nécessite appimagetool)."""
    print("\n" + "="*50)
    print("Création de l'AppImage Linux...")
    print("="*50 + "\n")

    appdir = Path('ConvertiColor.AppDir')

    # Créer la structure AppDir
    (appdir / 'usr' / 'bin').mkdir(parents=True, exist_ok=True)
    (appdir / 'usr' / 'share' / 'applications').mkdir(parents=True, exist_ok=True)
    (appdir / 'usr' / 'share' / 'icons').mkdir(parents=True, exist_ok=True)

    # Copier l'exécutable
    if os.path.exists('dist/converticolor'):
        shutil.copy('dist/converticolor', appdir / 'usr' / 'bin' / 'converticolor')
        os.chmod(appdir / 'usr' / 'bin' / 'converticolor', 0o755)

    # Créer le fichier .desktop
    desktop_content = """[Desktop Entry]
Type=Application
Name=ConvertiColor
Comment=Convertisseur de couleurs multi-formats
Exec=converticolor
Icon=converticolor
Categories=Graphics;Utility;
Terminal=false
"""
    (appdir / 'usr' / 'share' / 'applications' / 'converticolor.desktop') \
        .write_text(desktop_content)
    (appdir / 'converticolor.desktop').write_text(desktop_content)

    # Créer AppRun
    apprun_content = """#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin:${PATH}"
exec "${HERE}/usr/bin/converticolor" "$@"
"""
    apprun_path = appdir / 'AppRun'
    apprun_path.write_text(apprun_content)
    os.chmod(apprun_path, 0o755)

    print("✅ Structure AppDir créée!")
    print("   Pour créer l'AppImage final, exécutez:")
    print("   appimagetool ConvertiColor.AppDir ConvertiColor-x86_64.AppImage")

    return True


def install_dependencies():
    """Installe les dépendances nécessaires."""
    print("\n" + "="*50)
    print("Installation des dépendances...")
    print("="*50 + "\n")

    dependencies = ['pyinstaller']

    for dep in dependencies:
        print(f"Installation de {dep}...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', dep], check=True)

    print("\n✅ Dépendances installées!")

def _parse_args() -> argparse.Namespace:
    """Parse les arguments de ligne de commande."""
    parser = argparse.ArgumentParser(description='Build ConvertiColor')
    parser.add_argument('--clean', action='store_true', help='Nettoyer les builds précédents')
    parser.add_argument('--windows', action='store_true', help='Build Windows uniquement')
    parser.add_argument('--linux', action='store_true', help='Build Linux uniquement')
    parser.add_argument('--appimage', action='store_true', help='Créer AppImage suite build Linux')
    parser.add_argument('--install-deps', action='store_true', help='Installer les dépendances')
    parser.add_argument('--all', action='store_true', help='Build toutes les plateformes')

    return parser.parse_args()

def _build_for_current_platform(include_appimage: bool) -> None:
    """Construit pour la plateforme courante."""
    if sys.platform == 'win32':
        build_windows()
    else:
        build_linux()
        if include_appimage:
            create_appimage()


def _run_selected_builds(args: argparse.Namespace) -> None:
    """Exécute les builds sélectionnés par les arguments."""
    if args.windows:
        build_windows()
    if args.linux:
        build_linux()
    if args.appimage:
        create_appimage()


def _has_build_target(args: argparse.Namespace) -> bool:
    """Vérifie si un target de build est spécifié."""
    return bool(args.windows or args.linux or args.appimage)


def main():
    """Point d'entrée principal du script de build."""
    args = _parse_args()

    # Se placer dans le dossier du projet
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    if args.install_deps:
        install_dependencies()
        return

    if args.clean:
        clean_build()
        if not _has_build_target(args) and not args.all:
            return

    if args.all or not _has_build_target(args):
        _build_for_current_platform(args.appimage)
    else:
        _run_selected_builds(args)

    print("\n" + "="*50)
    print("Build terminé!")
    print("="*50)


if __name__ == "__main__":
    main()
