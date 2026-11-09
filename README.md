# Open Creative Automation Toolkit

An early-stage open-source Python toolkit for repeatable design preparation and creative workflows. Inspired by practical print-on-demand and e-commerce needs, but not affiliated with any specific store or platform.

## Current capabilities

- Resize PNG/JPEG images to fit a target canvas while preserving aspect ratio.
- Export transparent PNG files when transparency is present (or for padded regions).
- Batch-process images in a folder using a simple command-line interface.

**Status:** First public prototype. Video editing, mockup automation, marketing workflows, and AI Skills are ideas on the roadmap, **not implemented features**. This project has no claimed user base or download history.

## Install

Requires Python 3.10+.

```bash
python -m pip install -r requirements.txt
```

## Examples

```bash
python -m creative_toolkit.prepare input.png output.png --width 2952 --height 3661
python -m creative_toolkit.prepare input_folder output_folder --width 1500 --height 1500
```

The image is scaled to fit within the requested dimensions without cropping, and centered on a transparent RGBA canvas. By default, images are **not enlarged** beyond their source resolution; add `--allow-upscale` to allow enlargement (which does **not** create missing source detail). JPEG originals do not magically become background-free; background removal is not yet included.

## Roadmap

1. Image validation (alpha channel, dimensions, file size).
2. Configurable print presets and batch manifests.
3. Mockup templates and extensible creative workflows.
4. Optional integrations with AI coding agents and video workflows.

## Contributing

Issues and pull requests are welcome. Please describe the problem, include reproducible examples, and keep contributions small and testable.

## License

MIT. See LICENSE.
