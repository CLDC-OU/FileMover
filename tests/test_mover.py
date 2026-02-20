import unittest
from src.filemover import Mover
import tempfile
import os

class DummyRenameConfig():
    def apply_rename(self, file_name):
        return f"RENAMED_{file_name}"

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
            "keep_source_behavior": "keep_source",
            "destination_collision_behavior": "ignore",
            "collision_avoidance_behavior": "none",
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

class TestMoverListMatchedFiles(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.source_dir = os.path.join(self.temp_dir.name, "src")
        self.dest_dir = os.path.join(self.temp_dir.name, "dst")
        os.makedirs(self.source_dir)
        os.makedirs(self.dest_dir)
        self.files = [
            "file1.txt",
            "file2.csv",
            "report.xls",
            "notes.txt",
            "data.xlsx",
            "summary.csv",
            "temp_file.txt",
            "final.txt",
            "startfile.txt",
            "endfile.txt",
            "task.done.txt",
            "task.txt",
            "task.done.NOT.txt",
            "startdata.final.txt",
            "data.txt",
            "startdata.md"
        ]
        for fname in self.files:
            with open(os.path.join(self.source_dir, fname), "w") as f:
                f.write("test")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_get_matched_files_file_types(self):
        config = {
            "mover_name": "TestMover",
            "mover_description": "Test Description",
            "file_types": ["txt"],
            "source_directories": [self.source_dir],
            "destination_directories": [self.dest_dir],
            "keep_source_behavior": "keep_source",
            "destination_collision_behavior": "ignore",
            "collision_avoidance_behavior": "none",
            "rename_config": None,
            "recursive": False
        }
        mover = Mover(**config)
        matched = mover.get_matched_files()
        expected = [os.path.join(self.source_dir, f) for f in self.files if f.endswith(".txt")]
        self.assertCountEqual(matched, expected)

    def test_get_matched_files_file_name_contains(self):
        config = {
            "mover_name": "TestMover",
            "mover_description": "Test Description",
            "file_types": None,
            "file_name_contains": "data",
            "source_directories": [self.source_dir],
            "destination_directories": [self.dest_dir],
            "keep_source_behavior": "keep_source",
            "destination_collision_behavior": "ignore",
            "collision_avoidance_behavior": "none",
            "rename_config": None,
            "recursive": False
        }
        mover = Mover(**config)
        matched = mover.get_matched_files()
        expected = [os.path.join(self.source_dir, f) for f in self.files if "data" in os.path.splitext(f)[0]]
        self.assertCountEqual(matched, expected)

    def test_get_matched_files_file_name_regex(self):
        config = {
            "mover_name": "TestMover",
            "mover_description": "Test Description",
            "file_name_regex": r'^task\.done$',
            "source_directories": [self.source_dir],
            "destination_directories": [self.dest_dir],
            "keep_source_behavior": "keep_source",
            "destination_collision_behavior": "ignore",
            "collision_avoidance_behavior": "none",
            "rename_config": None,
            "recursive": False
        }
        mover = Mover(**config)
        matched = mover.get_matched_files()
        # Only "task.done.txt" matches after removing extension
        expected = [os.path.join(self.source_dir, "task.done.txt")]
        self.assertCountEqual(matched, expected)

    def test_get_matched_files_recursive(self):
        sub_dir = os.path.join(self.source_dir, "sub")
        os.makedirs(sub_dir)
        with open(os.path.join(sub_dir, "subfile.txt"), "w") as f:
            f.write("test")
        config = {
            "mover_name": "TestMover",
            "mover_description": "Test Description",
            "file_types": ["txt"],
            "source_directories": [self.source_dir],
            "destination_directories": [self.dest_dir],
            "keep_source_behavior": "keep_source",
            "destination_collision_behavior": "ignore",
            "collision_avoidance_behavior": "none",
            "rename_config": None,
            "recursive": True
        }
        mover = Mover(**config)
        matched = mover.get_matched_files()
        expected = [os.path.join(self.source_dir, f) for f in self.files if f.endswith(".txt")]
        expected.append(os.path.join(sub_dir, "subfile.txt"))
        self.assertCountEqual(matched, expected)

class TestMoverGetDestinationFilesForSource(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.src1 = os.path.join(self.temp_dir.name, "src1")
        self.dest1 = os.path.join(self.temp_dir.name, "dst1")
        self.dest2 = os.path.join(self.temp_dir.name, "dst2")
        os.makedirs(self.src1)
        os.makedirs(self.dest1)
        os.makedirs(self.dest2)
        self.src1_file1 = os.path.join(self.src1, "file.txt")
        with open(self.src1_file1, "w") as f:
            f.write("content")

    def tearDown(self):
        self.temp_dir.cleanup()

    def _base_config(self):
        return {
            "mover_name": "TestMover",
            "mover_description": "Test Description",
            "file_types": ["txt"],
            "source_directories": [self.src1],
            "destination_directories": [self.dest1, self.dest2],
            "keep_source_behavior": "keep_source",
            "destination_collision_behavior": "ignore",
            "collision_avoidance_behavior": "none",
            "rename_config": None,
            "recursive": False
        }

    def test_no_collisions_returns_all_destinations_and_no_collisions(self):
        mover = Mover(**self._base_config())
        destinations, collisions = mover._get_destination_files_for_source(self.src1_file1)
        expected_destinations = [os.path.join(self.dest1, "file.txt"), os.path.join(self.dest2, "file.txt")]
        expected_collisions = []
        self.assertEqual(destinations, expected_destinations)
        self.assertEqual(collisions, expected_collisions)

    def test_with_collision_detects_existing_destination(self):
        # Create a file in dest2 to simulate collision
        existing_path = os.path.join(self.dest2, "file.txt")
        with open(existing_path, "w") as f:
            f.write("exists")
        mover = Mover(**self._base_config())
        destinations, collisions = mover._get_destination_files_for_source(self.src1_file1)
        expected_destinations = [os.path.join(self.dest1, "file.txt"), os.path.join(self.dest2, "file.txt")]
        expected_collisions = [existing_path]
        self.assertEqual(destinations, expected_destinations)
        self.assertEqual(collisions, expected_collisions)

    def test_with_rename_config_applies_rename_to_destinations_and_collisions(self):
        # Create a collision for the renamed name in dest1
        renamed_name = "RENAMED_file.txt"
        existing_renamed = os.path.join(self.dest1, renamed_name)
        with open(existing_renamed, "w") as f:
            f.write("exists")

        config = self._base_config()
        mover = Mover(**config)
        mover.config._rename_config = DummyRenameConfig() # type: ignore
        destinations, collisions = mover._get_destination_files_for_source(self.src1_file1)
        expected_destinations = [os.path.join(self.dest1, renamed_name), os.path.join(self.dest2, renamed_name)]
        expected_collisions = [existing_renamed]
        self.assertEqual(destinations, expected_destinations)
        self.assertEqual(collisions, expected_collisions)

    def test_with_collisions_detects_multiple_existing_destinations(self):
        existing_path_1 = os.path.join(self.dest1, "file.txt")
        with open(existing_path_1, "w") as f:
            f.write("exists")
        existing_path_2 = os.path.join(self.dest2, "file.txt")
        with open(existing_path_2, "w") as f:
            f.write("exists")
        mover = Mover(**self._base_config())
        destinations, collisions = mover._get_destination_files_for_source(self.src1_file1)
        expected_destinations = [os.path.join(self.dest1, "file.txt"), os.path.join(self.dest2, "file.txt")]
        expected_collisions = [existing_path_1, existing_path_2]
        self.assertEqual(destinations, expected_destinations)
        self.assertEqual(collisions, expected_collisions)
