import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from textutil import slugify, truncate


class TextUtilTests(unittest.TestCase):
    def test_slugify_basic(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_slugify_collapses_space_runs_to_single_hyphen(self):
        # Issue #20 repro: runs of spaces must collapse to exactly one hyphen,
        # and leading/trailing spaces must not produce edge hyphens.
        cases = [
            ("Hello World", "hello-world"),
            ("Hello  World", "hello-world"),
            ("Hello   World", "hello-world"),
            (" hello ", "hello"),
            ("  hello  world  ", "hello-world"),
            ("Hello", "hello"),
            ("", ""),
            ("   ", ""),
            (" ", ""),
            ("A", "a"),
            ("HELLO  WORLD", "hello-world"),
            ("Hello World Foo", "hello-world-foo"),
            ("hello-world", "hello-world"),
            (" a  b   c ", "a-b-c"),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                result = slugify(text)
                self.assertEqual(repr(result), repr(expected))
                self.assertNotIn("--", result)
                self.assertFalse(result.startswith("-"))
                self.assertFalse(result.endswith("-"))
                self.assertEqual(result, result.lower())
                self.assertNotIn(" ", result)

    def test_slugify_is_idempotent(self):
        once = slugify("Hello  World")
        self.assertEqual(slugify(once), once)

    def test_truncate_short_text_untouched(self):
        self.assertEqual(truncate("abcdef", 10), "abcdef")

    def test_truncate_appends_ellipsis_when_cut(self):
        # Issue #11 repro: the docstring is the spec, so a cut must mark the cut.
        self.assertEqual(truncate("abcdef", 3), "abc...")
        self.assertNotEqual(truncate("abcdef", 3), "abc")

    def test_truncate_exact_limit_is_not_cut(self):
        self.assertEqual(truncate("abcdef", 6), "abcdef")
        self.assertFalse(truncate("abcdef", 6).endswith("..."))

    def test_truncate_limit_plus_one_is_cut(self):
        self.assertEqual(truncate("abcdef", 5), "abcde...")

    def test_truncate_zero_limit_still_marks_the_cut(self):
        self.assertEqual(truncate("abcdef", 0), "...")

    def test_truncate_empty_text_is_not_cut(self):
        self.assertEqual(truncate("", 0), "")

    def test_truncate_cut_result_is_prefix_plus_ellipsis(self):
        text = "abcdef"
        limit = 4
        result = truncate(text, limit)
        self.assertEqual(result, text[:limit] + "...")
        self.assertTrue(result.endswith("..."))
        self.assertEqual(result[: -3], text[:limit])
        self.assertEqual(len(result), limit + 3)


if __name__ == "__main__":
    unittest.main()
