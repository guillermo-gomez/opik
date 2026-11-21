import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
class ContractTests(unittest.TestCase):
    def test_required_files(self):
        for name in ("docker-compose.yml", "prometheus.yml", "alerts.yml", "dashboards/epoc-0012.json"):
            self.assertTrue((ROOT/name).is_file(), name)
    def test_dashboard_panels(self):
        import json
        data=json.loads((ROOT/"dashboards/epoc-0012.json").read_text())
        self.assertEqual(len(data["panels"]), 4)
if __name__ == "__main__":
    unittest.main()
