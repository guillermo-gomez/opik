"""EPOC-0012 semantic architecture guardrail; conservative static check."""
import ast
import datetime as dt
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
CARDS = ("feature.json", "entrypoints.json", "contracts.json", "owner.json", "exceptions.json")

def validate(project=None):
    project = pathlib.Path(project) if project else ROOT.parent
    arch = project / "architecture"
    cfg = json.loads((arch / "boundaries.json").read_text(encoding="utf-8"))
    errors, writers = [], {}
    known = cfg["features"]
    for name, rule in known.items():
        for dep in rule.get("allowed_dependencies", []):
            if dep not in known:
                errors.append(f"unknown dependency {name} -> {dep}")
        for resource in rule.get("durable_writes", []):
            if resource in writers:
                errors.append(f"duplicate durable writer {resource}: {writers[resource]} and {name}")
            writers[resource] = name
    feature_root = project / cfg.get("feature_root", "features")
    if feature_root.exists():
        for folder in feature_root.iterdir():
            if not folder.is_dir() or folder.name.startswith("."):
                continue
            name = folder.name
            if name not in known:
                errors.append(f"unregistered feature {name}")
                continue
            for card in CARDS:
                path = folder / card
                if not path.is_file():
                    errors.append(f"missing card {name}/{card}")
                else:
                    try: json.loads(path.read_text(encoding="utf-8"))
                    except (ValueError, UnicodeError): errors.append(f"invalid card {name}/{card}")
            owner = folder / "owner.json"
            if owner.is_file():
                try:
                    declared = set(json.loads(owner.read_text(encoding="utf-8")).get("durable_writes", []))
                    expected = set(known[name].get("durable_writes", []))
                    if declared != expected:
                        errors.append(f"owner card mismatch {name}")
                except (ValueError, UnicodeError): pass
            for path in folder.rglob("*.py"):
                try: tree = ast.parse(path.read_text(encoding="utf-8"))
                except (SyntaxError, UnicodeError):
                    errors.append(f"invalid Python {path}")
                    continue
                for node in ast.walk(tree):
                    imports = [a.name for a in node.names] if isinstance(node, ast.Import) else ([node.module] if isinstance(node, ast.ImportFrom) and node.module else [])
                    for imp in imports:
                        if imp.startswith("features."):
                            dep = imp.split(".")[1].replace("_", "-")
                            if dep != name and dep not in known[name].get("allowed_dependencies", []):
                                errors.append(f"forbidden dependency {name} -> {dep} in {path}")
    registry = project / cfg.get("exception_registry", "architecture/exceptions.json")
    exceptions = json.loads(registry.read_text(encoding="utf-8")).get("exceptions", [])
    for ex in exceptions:
        for field in ("id", "scope", "reason", "jira_issue", "adr_id", "approved_by", "expires"):
            if not ex.get(field): errors.append(f"exception missing {field}: {ex.get('id')}")
        if ex.get("approved_by") in ("agent", "AG-01", "AG-02", "AG-07"):
            errors.append(f"exception lacks human approval: {ex.get('id')}")
        if ex.get("expires"):
            try:
                if dt.date.fromisoformat(ex["expires"]) < dt.date.today():
                    errors.append(f"expired exception: {ex.get('id')}")
            except ValueError:
                errors.append(f"invalid exception expiry: {ex.get('id')}")
    return errors

def check():
    return validate()

if __name__ == "__main__":
    failures = validate()
    for failure in failures: print("FAIL:", failure)
    print("PASS" if not failures else f"{len(failures)} architecture failures")
    sys.exit(bool(failures))
