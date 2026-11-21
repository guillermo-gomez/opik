"""Minimal executable EPOC-0012 semantic boundary checks. Not a full dependency analyzer."""
import ast
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
def check():
    cfg = json.loads((ROOT / "boundaries.json").read_text(encoding="utf-8"))
    errors, writers = [], {}
    for name, rule in cfg["features"].items():
        for dep in rule["dependencies"]:
            if dep not in cfg["features"]:
                errors.append(f"{name}: unknown dependency {dep}")
        for resource in rule["writes"]:
            if resource in writers:
                errors.append(f"duplicate writer {resource}: {writers[resource]} and {name}")
            writers[resource] = name
    features = ROOT.parent / "features"
    if features.exists():
        for folder in features.iterdir():
            if not folder.is_dir(): continue
            name = folder.name
            if name not in cfg["features"]:
                errors.append(f"unregistered feature {name}")
                continue
            for card in ("feature.json","entrypoints.json","contracts.json","owner.json","exceptions.json"):
                path = folder / card
                if not path.exists():
                    errors.append(f"missing card {name}/{card}")
                else:
                    try: json.loads(path.read_text(encoding="utf-8"))
                    except (ValueError, UnicodeError): errors.append(f"invalid card {name}/{card}")
            for path in folder.rglob("*.py"):
                try: tree=ast.parse(path.read_text(encoding="utf-8"))
                except (SyntaxError, UnicodeError):
                    errors.append(f"invalid Python {path}")
                    continue
                for node in ast.walk(tree):
                    imports = [x.name for x in node.names] if isinstance(node,ast.Import) else ([node.module] if isinstance(node,ast.ImportFrom) and node.module else [])
                    for imp in imports:
                        if imp.startswith("features."):
                            target=imp.split(".")[1].replace("_","-")
                            if target!=name and target not in cfg["features"][name]["dependencies"]:
                                errors.append(f"forbidden dependency {name} -> {target} in {path}")
    for ex in cfg.get("exceptions",[]):
        for key in ("id","scope","reason","adr","jira","expires","approved_by"):
            if not ex.get(key): errors.append(f"exception missing {key}")
        if ex.get("approved_by") in ("AG-01","AG-02","AG-07","agent"):
            errors.append(f"exception lacks independent human approval: {ex.get('id')}")
    return errors
if __name__ == "__main__":
    failures=check()
    for item in failures: print("FAIL:",item)
    print("PASS" if not failures else f"{len(failures)} architecture failures")
    sys.exit(bool(failures))
