import unittest
import pytz
from src.rename_config import RenameConfig, RenameRule, AddTimestampConfig, TimestampPosition

class TestRenameConfig(unittest.TestCase):
    def test_rename_rule_repr(self):
        rule = RenameRule("foo", "bar")
        self.assertEqual(repr(rule), "RenameRule(search='foo', replace='bar')")

    def test_timestamp_position_from_string_valid(self):
        self.assertEqual(TimestampPosition.from_string('start'), TimestampPosition.START)
        self.assertEqual(TimestampPosition.from_string('after_prefix'), TimestampPosition.AFTER_PREFIX)
        self.assertEqual(TimestampPosition.from_string('before_suffix'), TimestampPosition.BEFORE_SUFFIX)
        self.assertEqual(TimestampPosition.from_string('end'), TimestampPosition.END)

    def test_timestamp_position_from_string_invalid(self):
        with self.assertRaises(ValueError):
            TimestampPosition.from_string('middle')

    def test_add_timestamp_config_defaults(self):
        cfg = AddTimestampConfig()
        self.assertFalse(cfg.enabled)
        self.assertEqual(cfg.position, TimestampPosition.AFTER_PREFIX)
        self.assertIsInstance(cfg.get_timestamp(), str)

    def test_add_timestamp_config_invalid_timezone(self):
        with self.assertRaises(ValueError):
            AddTimestampConfig(timezone='NotATimezone')
    
    def test_add_timestamp_config_valid_timezone(self):
        cfg = AddTimestampConfig(timezone='UTC')
        self.assertEqual(cfg._timezone, pytz.timezone('UTC'))

    def test_add_timestamp_config_invalid_enabled_type(self):
        with self.assertRaises(TypeError):
            AddTimestampConfig(enabled='yes')

    def test_add_timestamp_config_invalid_format_type(self):
        with self.assertRaises(TypeError):
            AddTimestampConfig(format=123)

    def test_add_timestamp_config_invalid_position(self):
        with self.assertRaises(ValueError):
            AddTimestampConfig(position='middle')
    
    def test_add_timestamp_config_get_timestamp(self):
        cfg = AddTimestampConfig(enabled=True, position='start')
        timestamp = cfg.get_timestamp()
        self.assertIsInstance(timestamp, str)
        self.assertRegex(timestamp, r'^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$')
    
    def test_add_timestamp_config_get_timestamp_with_timezone(self):
        cfg = AddTimestampConfig(enabled=True, position='start', timezone='UTC')
        timestamp = cfg.get_timestamp()
        self.assertIsInstance(timestamp, str)
        self.assertRegex(timestamp, r'^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$')
    
    def test_add_timestamp_config_get_timestamp_custom_format(self):
        cfg = AddTimestampConfig(enabled=True, position='start', format='%Y%m%d_%H%M%S')
        timestamp = cfg.get_timestamp()
        self.assertIsInstance(timestamp, str)
        self.assertRegex(timestamp, r'^\d{8}_\d{6}$')

    def test_rename_config_defaults(self):
        cfg = RenameConfig()
        self.assertFalse(cfg.enabled)
        self.assertEqual(cfg.replace_rules, [])
        self.assertFalse(cfg.case_sensitive)
        self.assertEqual(cfg.prefix, '')
        self.assertEqual(cfg.suffix, '')
        self.assertIsInstance(cfg.add_timestamp, AddTimestampConfig)

    def test_rename_config_apply_rename_disabled(self):
        cfg = RenameConfig(enabled=False)
        self.assertEqual(cfg.apply_rename("file.txt"), "file.txt")

    def test_rename_config_apply_rename_empty_filename(self):
        cfg = RenameConfig(enabled=True)
        with self.assertRaises(ValueError):
            cfg.apply_rename("")

    def test_rename_config_apply_rename_replace_case_insensitive(self):
        cfg = RenameConfig(
            enabled=True,
            replace=[{"search": "foo", "replace": "bar"}],
            case_sensitive=False
        )
        self.assertEqual(cfg.apply_rename("FOO.txt"), "bar.txt")

    def test_rename_config_apply_rename_replace_case_sensitive(self):
        cfg = RenameConfig(
            enabled=True,
            replace=[{"search": "foo", "replace": "bar"}],
            case_sensitive=True
        )
        self.assertEqual(cfg.apply_rename("foo.txt"), "bar.txt")
        self.assertEqual(cfg.apply_rename("FOO.txt"), "FOO.txt")

    def test_rename_config_apply_rename_with_prefix_suffix(self):
        cfg = RenameConfig(
            enabled=True,
            prefix="PRE_",
            suffix="_SUF"
        )
        self.assertEqual(cfg.apply_rename("file.txt"), "PRE_file.txt_SUF")

    def test_rename_config_apply_rename_add_timestamp_after_prefix(self):
        cfg = RenameConfig(
            enabled=True,
            add_timestamp={"enabled": True, "position": "after_prefix"}
        )
        result = cfg.apply_rename("file.txt")
        self.assertRegex(result, r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_file\.txt$")

    def test_rename_config_apply_rename_add_timestamp_before_suffix(self):
        cfg = RenameConfig(
            enabled=True,
            add_timestamp={"enabled": True, "position": "before_suffix"}
        )
        result = cfg.apply_rename("file.txt")
        self.assertRegex(result, r"^file\.txt_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$")

    def test_rename_config_apply_rename_add_timestamp_start(self):
        cfg = RenameConfig(
            enabled=True,
            add_timestamp={"enabled": True, "position": "start"}
        )
        result = cfg.apply_rename("file.txt")
        self.assertRegex(result, r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_file\.txt$")

    def test_rename_config_apply_rename_add_timestamp_end(self):
        cfg = RenameConfig(
            enabled=True,
            add_timestamp={"enabled": True, "position": "end"}
        )
        result = cfg.apply_rename("file.txt")
        self.assertRegex(result, r"^file\.txt_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$")

    def test_rename_config_apply_rename_empty_after_rules(self):
        cfg = RenameConfig(
            enabled=True,
            replace=[{"search": "file", "replace": ""}],
            prefix="",
            suffix=""
        )
        with self.assertRaises(ValueError):
            cfg.apply_rename("file")

if __name__ == "__main__":
    unittest.main()