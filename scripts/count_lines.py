"""Count meaningful project lines and refresh docs/line_count.md."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INCLUDED = ["src", "tests", "examples", "scripts"]
SKIP_PARTS = {"__pycache__", ".venv", "venv", ".amarr", ".git", ".pytest_cache", "build", "dist"}
EXTENSIONS = {".py", ".js", ".css", ".html", ".md", ".yaml", ".toml", ".txt", ".svg", ""}


def meaningful_lines(path: Path) -> int:
    """Count non-blank, non-trivial-comment lines."""
    count = 0
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if path.suffix == ".py" and stripped.startswith("#"):
            continue
        count += 1
    return count


def iter_files() -> list[Path]:
    """Iterate counted files."""
    files: list[Path] = []
    for folder in INCLUDED:
        base = ROOT / folder
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if any(part in SKIP_PARTS for part in path.parts):
                continue
            if path.suffix in EXTENSIONS or path.name == "Makefile":
                files.append(path)
    return files


def main() -> int:
    """Print counts and write Markdown summary."""
    by_folder: dict[str, int] = {folder: 0 for folder in INCLUDED}
    for path in iter_files():
        rel = path.relative_to(ROOT)
        folder = rel.parts[0]
        by_folder[folder] += meaningful_lines(path)
    total = sum(by_folder.values())
    for folder, count in by_folder.items():
        print(f"{folder}: {count}")
    print(f"total: {total}")
    if total < 7000:
        print("warning: below 7000 meaningful lines")
    if total > 9000:
        print("warning: above 9000 meaningful lines")
    lines = ["# Line Count", "", "| Folder | Meaningful lines |", "| --- | ---: |"]
    for folder, count in by_folder.items():
        lines.append(f"| {folder} | {count} |")
    lines.extend(["", f"**Total repository code lines:** {total}", ""])
    if total < 7000:
        lines.append("Warning: below the target range.")
    elif total > 9000:
        lines.append("Warning: above the target range.")
    else:
        lines.append("The repository is within the requested 7,000 to 9,000 line range.")
    (ROOT / "docs" / "line_count.md").write_text("\n".join(lines), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
