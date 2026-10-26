import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from textutil import slugify, truncate


class TextUtilTests(unittest.TestCase):
    def test_slugify_basic(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_slugify_collapses_consecutive_spaces(self):
        # Issue #20: consecutive spaces must not become repeated hyphens.
        self.assertEqual(slugify("Hello  World"), "hello-world")
        self.assertEqual(slugify("a   b   c"), "a-b-c")

    def test_slugify_strips_leading_and_trailing_spaces(self):
        self.assertEqual(slugify(" hello "), "hello")

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
