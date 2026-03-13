import unittest
from src.filemover.match_files_config import FileMatchRule, FileMatchType, FileNameMatchMode, FileMatchType
import tempfile
import os

class TestFileMatchRuleMatchesFile(unittest.TestCase):
    def setUp(self):
        self.filename = "exact_value"
        self.filename_with_multiple_dot = self.filename.replace("_", ".")  # exact.value
        self.filename_with_space = self.filename.replace("_", " ")  # exact value
        self.filename_with_capitalization = self.filename.title()  # Exact_value
        self.filename_with_caps_and_space = self.filename.replace("_", " ").title()  # Exact Value
        self.filename_with_multiple_dots_and_space = "exa.ct value"
        self.filename_with_caps_multiple_dots_and_space = self.filename_with_multiple_dots_and_space.title()  # Exa.ct Value
        filename_parts = self.filename.split("_")
        filename_parts.reverse()
        self.filename_parts_reversed = "_".join(filename_parts)  # value_exact

        self.filename_no_extension = self.filename
        self.filename_txt = f"{self.filename}.txt"  # exact_value.txt
        self.filename_with_multiple_dot_txt = f"{self.filename_with_multiple_dot}.txt"  # exact.value.txt
        self.filename_with_space_txt = f"{self.filename_with_space}.txt"  # exact value.txt
        self.filename_with_capitalization_txt = f"{self.filename_with_capitalization}.txt"  # Exact_value.txt
        self.filename_with_caps_and_space_txt = f"{self.filename_with_caps_and_space}.txt"  # Exact Value.txt
        self.filename_with_multiple_dots_and_space_txt = f"{self.filename_with_multiple_dots_and_space}.txt"  # exa.ct value.txt
        self.filename_with_caps_multiple_dots_and_space_txt = f"{self.filename_with_caps_multiple_dots_and_space}.txt"  # Exa.ct Value.txt
        self.filename_parts_reversed_txt = f"{self.filename_parts_reversed}.txt"  # value_exact.txt

    def tearDown(self):
        pass

    def test_missing_all_throws_error(self):
        config = {
            "enabled": True,
        }
        with self.assertRaises(ValueError):
            rule = FileMatchRule(**config)

    def test_missing_type_and_mode_throws_error(self):
        config = {
            "enabled": True,
            "value": self.filename
        }
        with self.assertRaises(ValueError):
            rule = FileMatchRule(**config)

    def test_missing_type_throws_error(self):
        config = {
            "enabled": True,
            "mode": FileNameMatchMode.SINGLE_EXACT.value,
            "value": self.filename
        }
        with self.assertRaises(ValueError):
            rule = FileMatchRule(**config)

    def test_missing_mode_throws_error(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "value": self.filename
        }

        with self.assertRaises(ValueError):
            rule = FileMatchRule(**config)

    def test_invalid_file_mode_throws_error(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": "INVALID",
            "value": self.filename
        }

        with self.assertRaises(ValueError):
            rule = FileMatchRule(**config)

    def test_initialize_with_valid_config(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.SINGLE_EXACT.value,
            "value": self.filename
        }
        rule = FileMatchRule(**config)
        self.assertIsNotNone(rule)

    def test_missing_value_throws_error(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.SINGLE_EXACT.value,
            "value": ""
        }
        with self.assertRaises(ValueError):
            rule = FileMatchRule(**config)
    
    def test_number_type_value_throws_error(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.SINGLE_EXACT.value,
            "value": 2
        }
        with self.assertRaises(ValueError):
            rule = FileMatchRule(**config)
    def test_none_type_value_throws_error(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.SINGLE_EXACT.value,
            "value": None
        }
        with self.assertRaises(ValueError):
            rule = FileMatchRule(**config)

    def test_list_value_for_non_list_mode_throws_error(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.SINGLE_EXACT.value,
            "value": [self.filename]
        }
        with self.assertRaises(ValueError):
            rule = FileMatchRule(**config)
    
    def test_non_list_value_for_list_mode_throws_error(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.MULTIPLE_EXACT.value,
            "value": self.filename
        }
        with self.assertRaises(ValueError):
            rule = FileMatchRule(**config)

    def test_matches_single_exact(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.SINGLE_EXACT.value,
            "value": self.filename
        }

        rule = FileMatchRule(**config)
        self.assertTrue(rule.matches_filename(self.filename_no_extension))
        self.assertTrue(rule.matches_filename(self.filename_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_multiple_dot_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_capitalization_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_caps_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_multiple_dots_and_space_txt))

    def test_matches_single_exact_case_insensitive(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.SINGLE_EXACT.value,
            "value": self.filename_with_capitalization,
            "case_sensitive": False
        }

        rule = FileMatchRule(**config)
        self.assertTrue(rule.matches_filename(self.filename_no_extension))
        self.assertTrue(rule.matches_filename(self.filename_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_multiple_dot_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_space_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_capitalization_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_caps_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_multiple_dots_and_space_txt))

    def test_matches_single_exact_with_multiple_dots(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.SINGLE_EXACT.value,
            "value": self.filename_with_multiple_dot
        }

        rule = FileMatchRule(**config)
        self.assertFalse(rule.matches_filename(self.filename_no_extension))
        self.assertFalse(rule.matches_filename(self.filename_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_multiple_dot_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_capitalization_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_caps_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_multiple_dots_and_space_txt))

    def test_matches_multiple_exact(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.MULTIPLE_EXACT.value,
            "value": [self.filename, self.filename_with_multiple_dot, self.filename_with_caps_and_space]
        }
        rule = FileMatchRule(**config)

        self.assertTrue(rule.matches_filename(self.filename_no_extension))
        self.assertTrue(rule.matches_filename(self.filename_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_multiple_dot_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_capitalization_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_caps_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_multiple_dots_and_space_txt))

    def test_matches_multiple_exact_insensitive(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.MULTIPLE_EXACT.value,
            "value": [self.filename, self.filename_with_multiple_dot, self.filename_with_caps_and_space],
            "case_sensitive": False
        }
        rule = FileMatchRule(**config)

        self.assertTrue(rule.matches_filename(self.filename_no_extension))
        self.assertTrue(rule.matches_filename(self.filename_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_multiple_dot_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_space_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_capitalization_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_caps_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_multiple_dots_and_space_txt))

    def test_file_name_contains(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.CONTAINS.value,
            "value": self.filename.split("_")[0]
        }
        rule = FileMatchRule(**config)

        self.assertTrue(rule.matches_filename(self.filename_no_extension))
        self.assertTrue(rule.matches_filename(self.filename_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_multiple_dot_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_capitalization_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_caps_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_multiple_dots_and_space_txt))
        self.assertTrue(rule.matches_filename(self.filename_parts_reversed_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_caps_multiple_dots_and_space_txt))
    def test_file_name_contains_case_insensitive(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.CONTAINS.value,
            "value": self.filename.split("_")[0],
            "case_sensitive": False
        }
        rule = FileMatchRule(**config)

        self.assertTrue(rule.matches_filename(self.filename_no_extension))
        self.assertTrue(rule.matches_filename(self.filename_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_multiple_dot_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_space_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_capitalization_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_caps_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_multiple_dots_and_space_txt))
        self.assertTrue(rule.matches_filename(self.filename_parts_reversed_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_caps_multiple_dots_and_space_txt))

    def test_file_name_starts_with(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.STARTS_WITH.value,
            "value": self.filename.split("_")[0]
        }
        rule = FileMatchRule(**config)

        self.assertTrue(rule.matches_filename(self.filename_no_extension))
        self.assertTrue(rule.matches_filename(self.filename_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_multiple_dot_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_capitalization_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_caps_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_multiple_dots_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_caps_multiple_dots_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_parts_reversed_txt))
    def test_file_name_starts_with_case_insensitive(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.STARTS_WITH.value,
            "value": self.filename.split("_")[0],
            "case_sensitive": False
        }
        rule = FileMatchRule(**config)

        self.assertTrue(rule.matches_filename(self.filename_no_extension))
        self.assertTrue(rule.matches_filename(self.filename_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_multiple_dot_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_space_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_capitalization_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_caps_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_multiple_dots_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_caps_multiple_dots_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_parts_reversed_txt))

    def test_file_name_ends_with(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.ENDS_WITH.value,
            "value": self.filename.split("_")[1]
        }
        rule = FileMatchRule(**config)

        self.assertTrue(rule.matches_filename(self.filename_no_extension))
        self.assertTrue(rule.matches_filename(self.filename_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_multiple_dot_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_capitalization_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_caps_and_space_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_multiple_dots_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_caps_multiple_dots_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_parts_reversed_txt))
    def test_file_name_ends_with_case_insensitive(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.ENDS_WITH.value,
            "value": self.filename.split("_")[1],
            "case_sensitive": False
        }
        rule = FileMatchRule(**config)

        self.assertTrue(rule.matches_filename(self.filename_no_extension))
        self.assertTrue(rule.matches_filename(self.filename_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_multiple_dot_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_space_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_capitalization_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_caps_and_space_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_multiple_dots_and_space_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_caps_multiple_dots_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_parts_reversed_txt))

    def test_file_name_regex_include_dot_in_middle_lowercase(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.REGEX_INCLUDE.value,
            "value": r'^([a-z])+\.([a-z])+'
        }
        rule = FileMatchRule(**config)

        self.assertFalse(rule.matches_filename(self.filename_no_extension))
        self.assertFalse(rule.matches_filename(self.filename_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_multiple_dot_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_capitalization_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_caps_and_space_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_multiple_dots_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_caps_multiple_dots_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_parts_reversed_txt))

    def test_file_name_regex_include_case_sensitive_has_no_effect(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.REGEX_INCLUDE.value,
            "value": r'^([a-z])+\.([a-z])+',
            "case_sensitive": False
        }
        rule = FileMatchRule(**config)

        self.assertFalse(rule.matches_filename(self.filename_no_extension))
        self.assertFalse(rule.matches_filename(self.filename_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_multiple_dot_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_capitalization_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_caps_and_space_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_multiple_dots_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_caps_multiple_dots_and_space_txt))  # if this test fails, the case_sensitive option applies to regex, which shouldn't be the case
        self.assertFalse(rule.matches_filename(self.filename_parts_reversed_txt))

    def test_file_name_regex_exclude_dot_in_middle_lowercase(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.REGEX_EXCLUDE.value,
            "value": r'^([a-z])+\.([a-z])+'
        }
        rule = FileMatchRule(**config)

        self.assertTrue(rule.matches_filename(self.filename_no_extension))
        self.assertTrue(rule.matches_filename(self.filename_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_multiple_dot_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_space_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_capitalization_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_caps_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_multiple_dots_and_space_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_caps_multiple_dots_and_space_txt))
        self.assertTrue(rule.matches_filename(self.filename_parts_reversed_txt))
    def test_file_name_regex_exclude_case_sensitive_has_no_effect(self):
        config = {
            "enabled": True,
            "type": FileMatchType.FILE_NAME.value,
            "mode": FileNameMatchMode.REGEX_EXCLUDE.value,
            "value": r'^([a-z])+\.([a-z])+',
            "case_sensitive": False
        }
        rule = FileMatchRule(**config)

        self.assertTrue(rule.matches_filename(self.filename_no_extension))
        self.assertTrue(rule.matches_filename(self.filename_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_multiple_dot_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_space_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_capitalization_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_caps_and_space_txt))
        self.assertFalse(rule.matches_filename(self.filename_with_multiple_dots_and_space_txt))
        self.assertTrue(rule.matches_filename(self.filename_with_caps_multiple_dots_and_space_txt))
        self.assertTrue(rule.matches_filename(self.filename_parts_reversed_txt))