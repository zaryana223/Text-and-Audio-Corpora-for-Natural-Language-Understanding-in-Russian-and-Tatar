import re

import pandas as pd


def parse_annotated_file(filepath):
    data = {}
    current_id = None
    current_intent = None
    current_slots = []
    intent_pattern = re.compile(r"#\s*intent\s*[:=]\s*(.+)", re.IGNORECASE)
    auto_id = 0
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# id:"):
                current_id = line.split(":", 1)[1].strip()
            elif line.startswith("#") and "intent" in line.lower() and current_id is None:
                current_id = f"auto_{auto_id}"
                auto_id += 1
            elif line.lower().startswith("# intent"):
                match = intent_pattern.match(line)
                if match:
                    current_intent = match.group(1).strip()
            elif line and not line.startswith("#"):
                parts = line.split("\t")
                if len(parts) >= 4:
                    current_slots.append(parts[3])
                elif len(parts) >= 3:
                    current_slots.append(parts[-1])
            elif line == "" and current_id is not None:
                data[current_id] = {
                    "intent": current_intent,
                    "slots": " ".join(current_slots),
                }
                current_id = None
                current_intent = None
                current_slots = []
    if current_id is not None:
        data[current_id] = {
            "intent": current_intent,
            "slots": " ".join(current_slots),
        }
    return data


def create_comparison_csv(gold_file, pred_file, output_csv, pred_name=None):
    gold = parse_annotated_file(gold_file)
    pred = parse_annotated_file(pred_file)
    rows = []
    for id_ in gold:
        rows.append(
            {
                "id": id_,
                "intent_gold": gold[id_]["intent"],
                "intent_pred": pred.get(id_, {}).get("intent", ""),
                "slots_gold": gold[id_]["slots"],
                "slots_pred": pred.get(id_, {}).get("slots", ""),
                "model": pred_name or pred_file,
            }
        )
    df = pd.DataFrame(rows).fillna("")
    df.to_csv(output_csv, index=False, encoding="utf-8")
    return df
