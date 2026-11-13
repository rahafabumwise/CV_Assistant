"""Load config.yaml and apply --set key.sub=value overrides."""
from __future__ import annotations

import argparse
import copy
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _parse_value(text: str):
    # yaml.safe_load turns "1" into 1, "true" into True, "5e-5" into a string,
    # so try float as well.
    value = yaml.safe_load(text)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return value
    return value


def load_config(path: str | Path = "config.yaml", overrides: list[str] | None = None) -> dict:
    path = Path(path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    cfg = copy.deepcopy(cfg)
    for item in overrides or []:
        key, _, raw = item.partition("=")
        if not _:
            raise ValueError(f"Override must look like key.sub=value, got: {item}")
        node = cfg
        parts = key.split(".")
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = _parse_value(raw)
    return cfg


def base_arg_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument(
        "--set", dest="overrides", action="append", default=[],
        metavar="KEY=VALUE", help="Override a config value, e.g. --set cpt.epochs=1",
    )
    return parser


def project_path(relative: str | Path) -> Path:
    """Resolve a path from config.yaml relative to the repository root."""
    p = Path(relative)
    return p if p.is_absolute() else PROJECT_ROOT / p


def results_dirs(cfg: dict) -> list[Path]:
    """Where results are written: the repo's results/ folder and a backup on Drive."""
    return [project_path(cfg["paths"]["results_dir"]),
            Path(cfg["paths"]["output_dir"]) / "results"]


def save_result(cfg: dict, name: str, data) -> None:
    """Write a results file (text, bytes or JSON-able object) to every results folder."""
    import json
    for folder in results_dirs(cfg):
        folder.mkdir(parents=True, exist_ok=True)
        target = folder / name
        if isinstance(data, bytes):
            target.write_bytes(data)
        elif isinstance(data, str):
            target.write_text(data, encoding="utf-8")
        else:
            target.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def resolve_model(cfg: dict, key: str) -> str:
    """Turn models.<key> into a loadable name or path. 'auto' means the checkpoint
    selected by the latest training run of that stage."""
    import json
    value = str(cfg["models"][key])
    if value != "auto":
        return value
    metrics_file = {"cpt": "cpt_metrics.json", "sft": "sft_metrics.json"}[key]
    for folder in results_dirs(cfg):
        f = folder / metrics_file
        if f.exists():
            path = json.loads(f.read_text(encoding="utf-8"))["selected_checkpoint"]
            if Path(path).exists():
                return path
    raise FileNotFoundError(
        f"models.{key} is 'auto' but no finished {key.upper()} run was found "
        f"({metrics_file} in results/ or on Drive). Run train_{key}.py first, "
        f"or put a checkpoint path in config.yaml under models.{key}.")
