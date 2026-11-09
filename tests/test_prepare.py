"""Basic smoke tests for the PNG preparation utility."""

import tempfile
import unittest
from pathlib import Path
from PIL import Image
from creative_toolkit.prepare import prepare_image


class PrepareTests(unittest.TestCase):
    def test_transparent_canvas_and_dimensions(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "source.png"
            target = root / "output.png"
            Image.new("RGBA", (100, 50), (255, 0, 0, 255)).save(source)
            prepare_image(source, target, 200, 200)
            with Image.open(target) as result:
                self.assertEqual(result.size, (200, 200))
                self.assertEqual(result.mode, "RGBA")
                self.assertEqual(result.getpixel((0, 0))[3], 0)
                self.assertEqual(result.getpixel((100, 100)), (255, 0, 0, 255))

    def test_reject_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            prepare_image(Path("x.png"), Path("y.png"), 0, 100)


if __name__ == "__main__":
    unittest.main()
