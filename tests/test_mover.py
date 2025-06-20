import unittest
from src.filemover import Mover

class DummyRenameConfig:
    def apply_rename(self, name):
        return name

class TestMoverShouldMoveFile(unittest.TestCase):
    def setUp(self):
        self.default_config = {
            "mover_name": "TestMover",
            "mover_description": "Test Description",
            "file_types": None,
            "file_type_regex": None,
            "file_type_exclude_regex": None,
            "file_names": None,
            "file_name_regex": None,
            "file_name_exclude_regex": None,
            "file_name_contains": None,
            "file_name_starts_with": None,
            "file_name_ends_with": None,
            "source_directories": [""],
            "destination_directories": [""],
            "keep_source": True,
            "rename_config": None
        }
        mover_config = self.default_config.copy()
        mover_config["file_types"] = "csv"

        self.mover = Mover(**mover_config)

    def test_none_file_name(self):
        self.assertFalse(self.mover._should_move_file(None))

    def test_empty_file_name(self):
        self.assertFalse(self.mover._should_move_file(""))

    def test_file_types(self):
        config = self.default_config.copy()
        config["file_types"] = ['txt', 'md']
        mover = Mover(**config)
        self.assertTrue(mover._should_move_file("file.txt"))
        self.assertFalse(mover._should_move_file("file.pdf"))

    def test_file_type_regex(self):
        config = self.default_config.copy()
        config["file_type_regex"] = r'xl(s|t)x?$'
        mover = Mover(**config)
        self.assertTrue(mover._should_move_file("report.xls"))
        self.assertTrue(mover._should_move_file("data.xlsx"))
        self.assertFalse(mover._should_move_file("notes.txt"))
        self.assertFalse(mover._should_move_file("summary.csv"))

    def test_file_type_exclude_regex(self):
        config = self.default_config.copy()
        config["file_type_exclude_regex"] = r'.*bak$'
        mover = Mover(**config)
        self.assertFalse(mover._should_move_file("data.bak"))
        self.assertTrue(mover._should_move_file("data.txt"))

    def test_file_names(self):
        config = self.default_config.copy()
        config["file_names"] = ["keep", "important"]
        mover = Mover(**config)
        self.assertTrue(mover._should_move_file("keep.txt"))
        self.assertFalse(mover._should_move_file("other.txt"))

    def test_file_name_regex(self):
        config = self.default_config.copy()
        config["file_name_regex"] = r'^report_\d+$'
        mover = Mover(**config)
        self.assertTrue(mover._should_move_file("report_123.csv"))
        self.assertFalse(mover._should_move_file("summary.csv"))

    def test_file_name_exclude_regex(self):
        config = self.default_config.copy()
        config["file_name_exclude_regex"] = r'^temp_.*'
        mover = Mover(**config)
        self.assertFalse(mover._should_move_file("temp_file.txt"))
        self.assertTrue(mover._should_move_file("final.txt"))

    def test_file_name_contains(self):
        config = self.default_config.copy()
        print(config["file_types"])
        config["file_name_contains"] = "data"
        mover = Mover(**config)
        self.assertTrue(mover._should_move_file("mydata.txt"))
        self.assertFalse(mover._should_move_file("report.txt"))

    def test_file_name_starts_with(self):
        config = self.default_config.copy()
        config["file_name_starts_with"] = "start"
        mover = Mover(**config)
        self.assertTrue(mover._should_move_file("startfile.txt"))
        self.assertFalse(mover._should_move_file("endfile.txt"))

    def test_file_name_ends_with(self):
        config = self.default_config.copy()
        config["file_name_ends_with"] = ".done"
        mover = Mover(**config)
        self.assertTrue(mover._should_move_file("task.done.txt"))
        self.assertFalse(mover._should_move_file("task.txt"))
        self.assertFalse(mover._should_move_file("task.done.NOT.txt"))

    def test_all_conditions_met(self):
        config = self.default_config.copy()
        config["file_types"] = ["txt"]
        config["file_name_contains"] = "data"
        config["file_name_starts_with"] = "start"
        config["file_name_ends_with"] = ".final"
        mover = Mover(**config)
        self.assertTrue(mover._should_move_file("startdata.final.txt"))
        self.assertFalse(mover._should_move_file("data.txt"))
        self.assertFalse(mover._should_move_file("startdata.md"))

if __name__ == "__main__":
    unittest.main()