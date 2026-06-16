"""Rename non-English file and folder names to English (one-off migration)."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# basename replacements (applied anywhere in the tree)
BASENAME_MAP = {
    "Код_для_разметки.ipynb": "annotation_labeling.ipynb",
    "метрики_на_валид_данных.xlsx": "validation_metrics.xlsx",
    "озвучка_test_adapt": "spoken_test_adapt",
    "озвучка_valid_adapt": "spoken_valid_adapt",
    "Автоматические_данные_для_разметки.ipynb": "automatic_labeling_data.ipynb",
    "Курсовая_работа_озвучка.ipynb": "speech_recognition_pipeline.ipynb",
    "Метрики.ipynb": "metrics_evaluation.ipynb",
    "16 лет мужской": "male_16y",
    "20 лет женский_1": "female_20y_1",
    "20 лет женский_2": "female_20y_2",
    "20 лет женский_3": "female_20y_3",
    "21 год женский": "female_21y",
    "36 лет мужской": "male_36y",
    "46 лет женский": "female_46y",
    "söyle.py": "soyle.py",
    "söyle_raw.conll": "soyle_raw.conll",
    "train_adopted.ipynb": "train_adapted.ipynb",
}


def collect_targets() -> list[Path]:
    targets: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        if ".git" in Path(dirpath).parts:
            continue
        for name in dirnames + filenames:
            if name in BASENAME_MAP:
                targets.append(Path(dirpath) / name)
    # empty junk file
    junk = ROOT / "experiments" / "nlu" / "озвучка_valid_adapt" / "ва"
    if junk.is_file() and junk.stat().st_size <= 4:
        targets.append(junk)
    return sorted(targets, key=lambda p: len(p.parts), reverse=True)


def main() -> None:
    for path in collect_targets():
        if path.name == "ва":
            path.unlink()
            continue
        new_name = BASENAME_MAP[path.name]
        new_path = path.with_name(new_name)
        if new_path.exists():
            raise SystemExit(f"target already exists: {new_path}")
        path.rename(new_path)


if __name__ == "__main__":
    main()
