"""Simple open-source image requirements checker (requires Pillow).

Examples:
  python check_image.py design.png --width 9744 --height 7000 --max-mb 50 --transparent
  python check_image.py mockup.png --width 1500 --height 1500
"""

import argparse
from pathlib import Path

from PIL import Image


def check_image(path: Path, width=None, height=None, max_mb=None, transparent=False):
    """Return a list of detected issues; an empty list means PASS."""
    issues = []
    if not path.is_file():
        return [f"File not found: {path}"]
    if max_mb is not None and path.stat().st_size > max_mb * 1024 * 1024:
        issues.append(f"File exceeds {max_mb:g} MiB")
    try:
        with Image.open(path) as img:
            if width is not None and img.width != width:
                issues.append(f"Width is {img.width}px, expected {width}px")
            if height is not None and img.height != height:
                issues.append(f"Height is {img.height}px, expected {height}px")
            if transparent:
                alpha_min, _ = img.convert("RGBA").getchannel("A").getextrema()
                if alpha_min == 255:
                    issues.append("No transparent pixels found")
    except (OSError, ValueError) as exc:
        issues.append(f"Could not open image: {exc}")
    return issues


def main():
    parser = argparse.ArgumentParser(description="Check image dimensions, file size, and transparency")
    parser.add_argument("image", type=Path, help="Path to an image file")
    parser.add_argument("--width", type=int, help="Required width in pixels")
    parser.add_argument("--height", type=int, help="Required height in pixels")
    parser.add_argument("--max-mb", type=float, help="Maximum file size in MiB")
    parser.add_argument("--transparent", action="store_true", help="Require some transparent pixels")
    args = parser.parse_args()
    if ((args.width is not None and args.width <= 0)
            or (args.height is not None and args.height <= 0)
            or (args.max_mb is not None and args.max_mb <= 0)):
        parser.error("Width, height, and max-mb must be positive")

    issues = check_image(args.image, args.width, args.height, args.max_mb, args.transparent)
    if issues:
        for issue in issues:
            print("FAIL:", issue)
        raise SystemExit(1)
    print("PASS: Image meets the selected requirements")


if __name__ == "__main__":
    main()
