# Folder `data/errors/`: validation and error-analysis spreadsheets

Pre-computed **Excel workbooks** for metric review and error analysis. To recompute from CoNLL predictions, use `code/metrics/` (`run_metrics.py`, `nlu_metrics/`).

---

## 1. `validation_metrics.xlsx`

**Purpose:** summary of **validation** experiments (not test): six encoders, RU/EN training setups, pivot languages, Tatar training runs.

**Main sheets:**

| Sheet | Content |
|-------|---------|
| `RU_EN_6models` | 36 configs: scenario, encoder, intent/slot accuracy, sum, best epoch |
| `Languages_mDeBERTa` | Pivot training by source language → Russian validation |
| `Raw_translated_val` / `Raw_adapted_val` | Raw rows per run (metrics file, epoch) |
| `Pivot_Intent`, `Pivot_Slots`, `Pivot_Sum` | Pivot summary tables |

**Use when:** comparing train/validation scenarios and selecting the best epoch before test evaluation.

---

## 2. `ERRORS_mdeberta_trans_trans_RU_best_val.xlsx`

**Purpose:** error breakdown for mDeBERTa-v3-base on validation (translated train → translated val, Russian).

**Sheets:** Summary · per-intent F1 · intent confusion · intent errors · slot errors · worst utterances.

**Use when:** identifying typical intent confusions and problematic slots before test runs.

---

## 3. `generative_error_analysis_tables.xlsx`

**Purpose:** metrics and errors for **generative LLMs** (zero-shot, few-shot): Qwen, Gemma, Phi, etc.

**Sheet groups:**

| Prefix | Meaning |
|--------|---------|
| `all_runs`, `pivot_*`, `best_*` | Aggregated metrics, best configurations |
| `zs_*` | Zero-shot: confusions, slot hallucinations, BIO vs. span |
| `best_*` | Best run (Gemma-2-9B-it): same breakdowns |

**Use when:** writing the LLM error-analysis section (indirect requests, spurious slots, text normalization).

---

## Quick reference

| Task | File |
|------|------|
| Validation metrics | `validation_metrics.xlsx` |
| mDeBERTa validation errors | `ERRORS_mdeberta_trans_trans_RU_best_val.xlsx` |
| Generative model errors | `generative_error_analysis_tables.xlsx` |
