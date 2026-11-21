import importlib.util
import json
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("checker", ROOT / "check_boundaries.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

class ArchitectureContractTests(unittest.TestCase):
    def test_existing_registry(self):
        self.assertEqual(checker.validate(), [])

    def test_unique_writers(self):
        cfg = json.loads((ROOT / "boundaries.json").read_text(encoding="utf-8"))
        writers = [w for f in cfg["features"].values() for w in f["durable_writes"]]
        self.assertEqual(len(writers), len(set(writers)))

    def test_dependency_targets_registered(self):
        cfg = json.loads((ROOT / "boundaries.json").read_text(encoding="utf-8"))
        for f in cfg["features"].values():
            self.assertTrue(set(f["allowed_dependencies"]) <= set(cfg["features"]))

    def test_negative_duplicate_writer(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = pathlib.Path(tmp)
            (base / "architecture").mkdir()
            cfg = json.loads((ROOT / "boundaries.json").read_text(encoding="utf-8"))
            cfg["features"]["solver-engine"]["durable_writes"] = ["telemetry_exports"]
            (base / "architecture" / "boundaries.json").write_text(json.dumps(cfg))
            (base / "architecture" / "exceptions.json").write_text('{"exceptions":[]}')
            self.assertTrue(any("duplicate durable writer" in e for e in checker.validate(base)))

    def test_negative_forbidden_dependency(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = pathlib.Path(tmp)
            (base / "architecture").mkdir()
            cfg = json.loads((ROOT / "boundaries.json").read_text(encoding="utf-8"))
            (base / "architecture" / "boundaries.json").write_text(json.dumps(cfg))
            (base / "architecture" / "exceptions.json").write_text('{"exceptions":[]}')
            folder = base / "features" / "solver-engine"
            folder.mkdir(parents=True)
            for card in checker.CARDS:
                (folder / card).write_text(json.dumps({"durable_writes":["simulation_results"]} if card=="owner.json" else {}))
            (folder / "module.py").write_text("from features.observability import telemetry\n")
            self.assertTrue(any("forbidden dependency" in e for e in checker.validate(base)))

if __name__ == "__main__":
    unittest.main()
