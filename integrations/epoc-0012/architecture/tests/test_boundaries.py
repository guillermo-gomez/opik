import importlib.util
import json
import pathlib
import tempfile
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("checker",ROOT/"check_boundaries.py")
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
class ArchitectureContractTests(unittest.TestCase):
    def test_existing_registry(self):
        self.assertEqual(checker.check(),[])
    def test_unique_writers(self):
        cfg=json.loads((ROOT/"boundaries.json").read_text())
        writers=[w for f in cfg["features"].values() for w in f["writes"]]
        self.assertEqual(len(writers),len(set(writers)))
    def test_dependency_targets_registered(self):
        cfg=json.loads((ROOT/"boundaries.json").read_text())
        for f in cfg["features"].values():
            self.assertTrue(set(f["dependencies"]) <= set(cfg["features"]))
if __name__=="__main__": unittest.main()
