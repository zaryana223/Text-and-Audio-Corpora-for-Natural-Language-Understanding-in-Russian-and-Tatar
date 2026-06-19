import os

import pandas as pd
from seqeval.metrics import classification_report, f1_score as seq_f1
from seqeval.metrics import precision_score as seq_precision
from seqeval.metrics import recall_score as seq_recall
from sklearn.metrics import accuracy_score as sk_accuracy
from sklearn.metrics import f1_score as sk_f1
from sklearn.metrics import precision_score as sk_precision
from sklearn.metrics import recall_score as sk_recall


def _flatten_slots(sequences):
    flat = []
    for seq in sequences:
        flat.extend(seq)
    return flat


def _pair_aligned_sequences(gold, pred):
    gold_aligned, pred_aligned = [], []
    for g_seq, p_seq in zip(gold, pred):
        if len(g_seq) == len(p_seq):
            gold_aligned.append(g_seq)
            pred_aligned.append(p_seq)
    return gold_aligned, pred_aligned


def is_asr_model(model_name: str) -> bool:
    return "gigaam" in model_name.lower()


def slot_f1_competition_mean(gold_slots, pred_slots):
    n_total = len(gold_slots)
    if n_total == 0:
        return 0.0, 0
    slot_sum = 0.0
    n_scored = 0
    for gold_str, pred_str in zip(gold_slots, pred_slots):
        gold = gold_str.split() if isinstance(gold_str, str) else list(gold_str)
        pred = pred_str.split() if isinstance(pred_str, str) else list(pred_str)
        if len(gold) != len(pred):
            continue
        try:
            slot_sum += sk_f1(gold, pred, average="weighted", zero_division=0)
            n_scored += 1
        except ValueError:
            continue
    return slot_sum / n_total, n_scored


def score(df, model_name, save_path="results/metrics_summary.csv"):
    intent_accuracy = sk_accuracy(df["intent_gold"], df["intent_pred"])
    intent_f1_macro = sk_f1(
        df["intent_gold"],
        df["intent_pred"],
        average="macro",
        zero_division=0,
    )
    intent_f1_weighted = sk_f1(
        df["intent_gold"],
        df["intent_pred"],
        average="weighted",
        zero_division=0,
    )
    gold_slots_str = df["slots_gold"].tolist()
    pred_slots_str = df["slots_pred"].tolist()
    gold = [x.split() for x in gold_slots_str]
    pred = [x.split() for x in pred_slots_str]
    asr = is_asr_model(model_name)
    slot_f1_scored_utterances = None
    span_len_matched_utterances = None
    if asr:
        slot_f1, slot_f1_scored_utterances = slot_f1_competition_mean(
            gold_slots_str, pred_slots_str
        )
        gold_aligned, pred_aligned = _pair_aligned_sequences(gold, pred)
        span_len_matched_utterances = len(gold_aligned)
        flat_gold = _flatten_slots(gold_aligned)
        flat_pred = _flatten_slots(pred_aligned)
        if gold_aligned:
            token_precision = sk_precision(
                flat_gold, flat_pred, average="micro", zero_division=0
            )
            token_recall = sk_recall(flat_gold, flat_pred, average="micro", zero_division=0)
            token_f1 = sk_f1(flat_gold, flat_pred, average="micro", zero_division=0)
            span_precision = seq_precision(gold_aligned, pred_aligned)
            span_recall = seq_recall(gold_aligned, pred_aligned)
            span_f1 = seq_f1(gold_aligned, pred_aligned)
        else:
            token_precision = token_recall = token_f1 = 0.0
            span_precision = span_recall = span_f1 = 0.0
        joint_score = (intent_f1_weighted + slot_f1) / 2
    else:
        flat_gold = _flatten_slots(gold)
        flat_pred = _flatten_slots(pred)
        token_precision = sk_precision(
            flat_gold, flat_pred, average="micro", zero_division=0
        )
        token_recall = sk_recall(flat_gold, flat_pred, average="micro", zero_division=0)
        token_f1 = sk_f1(flat_gold, flat_pred, average="micro", zero_division=0)
        span_precision = seq_precision(gold, pred)
        span_recall = seq_recall(gold, pred)
        span_f1 = seq_f1(gold, pred)
        slot_f1 = span_f1
        joint_score = (intent_f1_weighted + span_f1) / 2
    print(f"\n========== {model_name} ==========")
    print("\n========== INTENTS ==========")
    print(f"Intent Accuracy:     {intent_accuracy:.4f}")
    print(f"Intent F1 macro:     {intent_f1_macro:.4f}")
    print(f"Intent F1 weighted:  {intent_f1_weighted:.4f}")
    print("\n====== SLOTS TOKEN-LEVEL ======")
    print(f"Token Precision:     {token_precision:.4f}")
    print(f"Token Recall:        {token_recall:.4f}")
    print(f"Token F1:            {token_f1:.4f}")
    if asr:
        print(
            f"(token/span on {span_len_matched_utterances}/{len(df)} "
            f"length-matched utterances)"
        )
    print("\n====== SLOTS SPAN-LEVEL ======")
    print(f"Span Precision:      {span_precision:.4f}")
    print(f"Span Recall:         {span_recall:.4f}")
    print(f"Span F1:             {span_f1:.4f}")
    if asr:
        print("\n====== SLOT F1 (competition / N) ======")
        print(f"Slot F1 (/ {len(df)}):     {slot_f1:.4f}")
        print(f"Utterances scored:   {slot_f1_scored_utterances}/{len(df)}")
    print("\nJOINT:")
    print(f"{joint_score:.4f}")
    if asr:
        print("(joint uses competition slot F1, not span F1)")
    result_row = {
        "model": model_name,
        "intent_accuracy": intent_accuracy,
        "intent_f1_macro": intent_f1_macro,
        "intent_f1_weighted": intent_f1_weighted,
        "token_precision": token_precision,
        "token_recall": token_recall,
        "token_f1": token_f1,
        "span_precision": span_precision,
        "span_recall": span_recall,
        "span_f1": span_f1,
        "joint_score": joint_score,
        "intent_f1": intent_f1_weighted,
        "slot_precision": span_precision,
        "slot_recall": span_recall,
        "slot_f1": slot_f1,
    }
    if asr:
        result_row["slot_f1_scored_utterances"] = slot_f1_scored_utterances
        result_row["span_len_matched_utterances"] = span_len_matched_utterances
    result_df = pd.DataFrame([result_row])
    if os.path.exists(save_path):
        existing = pd.read_csv(save_path)
        existing = existing[existing["model"] != model_name]
        result_df = pd.concat([existing, result_df], ignore_index=True)
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
    result_df.to_csv(save_path, index=False)
    return result_row


def per_slot_f1(df, model_name):
    gold = [x.split() for x in df["slots_gold"]]
    pred = [x.split() for x in df["slots_pred"]]
    if is_asr_model(model_name):
        gold, pred = _pair_aligned_sequences(gold, pred)
    if not gold:
        return pd.DataFrame(
            columns=["model", "slot", "precision", "recall", "f1", "support"]
        )
    report = classification_report(gold, pred, output_dict=True)
    rows = []
    for label, metrics in report.items():
        if label in ["micro avg", "macro avg", "weighted avg", "accuracy"]:
            continue
        rows.append(
            {
                "model": model_name,
                "slot": label,
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1": metrics["f1-score"],
                "support": metrics["support"],
            }
        )
    return pd.DataFrame(rows)


def save_per_slot(per_slot_df, model_name, output_dir="results"):
    output_path = os.path.join(output_dir, f"per_slot_{model_name}.csv")
    os.makedirs(output_dir, exist_ok=True)
    per_slot_df.to_csv(output_path, index=False)
    print(f"\nSaved per-slot metrics: {output_path}")
