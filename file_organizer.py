"""Automated File Organizer & Cleanup Utility.

Sorts the files in a folder into sub-folders by type (Images, Documents, ...).
Uses only the standard library (os, shutil, argparse).

Usage:
    python file_organizer.py                  # asks for a folder, shows preview
    python file_organizer.py "C:/Users/me/Downloads"
    python file_organizer.py "C:/Users/me/Downloads" --apply
    python file_organizer.py "C:/Users/me/Downloads" --apply --clean-empty

Without --apply it only PREVIEWS what would move (safe dry run).
Nothing is ever deleted, except empty folders if you pass --clean-empty.
"""

import argparse
import os
import shutil

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".tiff"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md"},
    "Spreadsheets": {".xls", ".xlsx", ".csv", ".ods"},
    "Presentations": {".ppt", ".pptx", ".odp"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".json", ".ipynb"},
    "Installers": {".exe", ".msi", ".dmg", ".apk"},
}
OTHER = "Others"


def category_for(filename):
    """Return the category folder name for a file based on its extension."""
    ext = os.path.splitext(filename)[1].lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return OTHER


def unique_path(path):
    """If path exists, return 'name (1).ext', 'name (2).ext', ... instead."""
    base, ext = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = f"{base} ({counter}){ext}"
        counter += 1
    return path


def organize(folder, apply=False):
    """Move files in `folder` into category sub-folders. Returns a summary dict."""
    summary = {}
    for name in sorted(os.listdir(folder)):
        source = os.path.join(folder, name)
        if not os.path.isfile(source) or name.startswith("."):
            continue  # skip folders and hidden files
        category = category_for(name)
        target_dir = os.path.join(folder, category)
        target = unique_path(os.path.join(target_dir, name))
        summary[category] = summary.get(category, 0) + 1
        print(f"  {name}  ->  {category}/{os.path.basename(target)}")
        if apply:
            os.makedirs(target_dir, exist_ok=True)
            shutil.move(source, target)
    return summary


def remove_empty_folders(folder):
    """Remove empty sub-folders (bottom-up). Returns how many were removed."""
    removed = 0
    for root, dirs, files in os.walk(folder, topdown=False):
        if root != folder and not os.listdir(root):
            os.rmdir(root)
            print(f"  removed empty folder: {os.path.relpath(root, folder)}")
            removed += 1
    return removed


def main():
    parser = argparse.ArgumentParser(description="Sort files into folders by type.")
    parser.add_argument("folder", nargs="?", help="folder to organize")
    parser.add_argument("--apply", action="store_true", help="actually move files")
    parser.add_argument("--clean-empty", action="store_true",
                        help="remove empty sub-folders afterwards")
    args = parser.parse_args()

    folder = args.folder or input("Folder to organize: ").strip().strip('"')
    folder = os.path.abspath(os.path.expanduser(folder))
    if not os.path.isdir(folder):
        print(f"Error: '{folder}' is not a folder.")
        return

    mode = "ORGANIZING" if args.apply else "PREVIEW (nothing will be moved)"
    print(f"\n{mode}: {folder}\n")
    summary = organize(folder, apply=args.apply)

    if not summary:
        print("No files to organize.")
    else:
        print("\nSummary:")
        for category, count in sorted(summary.items()):
            print(f"  {category}: {count} file(s)")
    if args.apply and args.clean_empty:
        print(f"\nEmpty folders removed: {remove_empty_folders(folder)}")
    if not args.apply and summary:
        print("\nThis was a preview. Add --apply to move the files.")


if __name__ == "__main__":
    main()
