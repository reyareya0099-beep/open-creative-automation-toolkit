"""Fit image assets to a transparent PNG canvas without cropping."""

import argparse
from pathlib import Path
from PIL import Image, ImageOps

SUPPORTED = {".png", ".jpg", ".jpeg", ".webp"}


def prepare_image(source: Path, destination: Path, width: int, height: int, allow_upscale: bool = False) -> None:
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGBA")
        scale = min(width / image.width, height / image.height)
        if not allow_upscale:
            scale = min(scale, 1.0)
        new_size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
        if new_size != image.size:
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        canvas.alpha_composite(image, ((width - image.width) // 2, (height - image.height) // 2))
        destination.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(destination, format="PNG", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare transparent PNG canvases for print or product listings.")
    parser.add_argument("source", type=Path, help="Input image or directory")
    parser.add_argument("destination", type=Path, help="Output PNG or directory")
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--height", type=int, required=True)
    parser.add_argument("--allow-upscale", action="store_true")
    args = parser.parse_args()

    if args.source.is_file():
        prepare_image(args.source, args.destination, args.width, args.height, args.allow_upscale)
        print(f"Created {args.destination}")
    elif args.source.is_dir():
        inputs = sorted(path for path in args.source.iterdir() if path.is_file() and path.suffix.lower() in SUPPORTED)
        for path in inputs:
            output = args.destination / (path.stem + ".png")
            prepare_image(path, output, args.width, args.height, args.allow_upscale)
            print(f"Created {output}")
        print(f"Processed {len(inputs)} image(s)")
    else:
        parser.error("Input must be an existing image file or directory")


if __name__ == "__main__":
    main()
