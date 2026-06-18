# Notebook `zero_shot+few_shot_version.ipynb`

Zero-shot and few-shot evaluation of **generative LLMs** on Russian NLU without fine-tuning. The model receives a prompt and returns JSON `{intent, slots}`. The test split is `ru.test.conll` (532 utterances after filtering to the `INTENTS` list).

Results are aggregated in `data/errors/generative_error_analysis_tables.xlsx`.

---

## 1. Experiment modes

| Mode | Flag | Model input | Goal |
|------|------|-------------|------|
| **Zero-shot** | `RUN_ZERO_SHOT = True` | `SYSTEM_PROMPT` + utterance only | Baseline LLM capability without examples |
| **Few-shot** | `RUN_FEWSHOT = True` | Prompt + 1–10 train pairs (query → JSON) + test utterance | Whether in-domain demos from `ru.train.conll` help |

Global settings at the top of the notebook:

| Parameter | Purpose |
|-----------|---------|
| `ACTIVE_MODEL` | Model key in `MODEL_REGISTRY` (e.g. `Phi-4-mini-instruct`) |
| `DEFAULT_QUANT` | Quantization: `4bit` or `fp16` |
| `SMOKE_N` | If > 0, use only the first N test utterances (smoke test) |
| `SAVE_DIR` | Output directory for logs and metrics (Colab: Google Drive `nlu_results`) |

---

## 2. Models (`MODEL_REGISTRY`)

| Notebook key | Hugging Face ID | Chat template |
|--------------|-----------------|---------------|
| `Qwen2.5-3B-Instruct` | Qwen/Qwen2.5-3B-Instruct | qwen |
| `Qwen2.5-7B-Instruct` | Qwen/Qwen2.5-7B-Instruct | qwen |
| `google/gemma-2-2b-it` | google/gemma-2-2b-it | gemma |
| `google/gemma-2-9b-it` | google/gemma-2-9b-it | gemma |
| `Phi-4-mini-instruct` | microsoft/Phi-4-mini-instruct | qwen |
| `Mistral-7B-Instruct-v0.3` | mistralai/Mistral-7B-Instruct-v0.3 | qwen |

For **Gemma**, the system prompt is folded into a single user message; for Qwen/Mistral/Phi, separate `system` and `user` roles are used.

---

## 3. Zero-shot pipeline

| Step | Function / block | Action |
|------|------------------|--------|
| 1 | `SYSTEM_PROMPT` | 16 intents, slot types, JSON output rules |
| 2 | `parse_conll_to_dicts` | Read `ru.test.conll` → text, gold intent, gold slots, BIO |
| 3 | `load_model` | Load LLM (4-bit via `bitsandbytes`, GPU) |
| 4 | `_build_messages_zeroshot(text)` | Chat messages without examples |
| 5 | `_generate` → `_parse_output` | `model.generate` → parse JSON intent/slots |
| 6 | `generate_prediction_zeroshot(text)` | Single-utterance wrapper |
| 7 | `run_evaluation(..., "zero_shot")` | Full test run + metrics |

**Single run:**

```python
run_evaluation(generate_prediction_zeroshot, "zero_shot", model_name=MODEL_NAME)
```

---

## 4. Few-shot pipeline

| Step | Function / block | Action |
|------|------------------|--------|
| 1 | `FEWSHOT_CONFIGS` | Intent set for demonstration mining |
| 2 | `get_fewshot_examples(intents)` | One slot-rich train example per intent from `ru.train.conll` |
| 3 | `_build_messages_fewshot(text, examples)` | Chat history: user → assistant (JSON) per demo, then test |
| 4 | `generate_prediction_fewshot(text, examples)` | Generation with demonstrations |
| 5 | `run_evaluation(...)` | Separate output folder per configuration |

### Few-shot configurations

| Experiment ID (`exp_type`) | Demo intents | Rationale |
|----------------------------|--------------|-----------|
| `few_shot_1_popular` | `weather/find` | Most frequent intent |
| `few_shot_1_problem` | `SearchScreeningEvent` | Error-prone intent |
| `few_shot_1_slots` | `BookRestaurant` | Slot-rich intent |
| `few_shot_5` | 5 intents (weather, restaurant, movie, alarm, reminder) | Short set |
| `few_shot_10` | 10 distinct intents | Extended set |

On-disk layout: `{SAVE_DIR}/{exp_type}/{MODEL_NAME}/`.

---

## 5. Zero-shot vs. few-shot

| | Zero-shot | Few-shot |
|---|-----------|----------|
| Examples in prompt | No | 1–10 train utterances |
| Output folder | `zero_shot/<model>/` | `few_shot_* /<model>/` |
| Extra file | — | `fewshot_examples.json` |
| Typical effect | Baseline | Small intent gains; slots still weaker than encoders |

---

## 6. Metrics (`run_evaluation`)

| Metric | Level | Description |
|--------|-------|-------------|
| Intent Accuracy | utterance | Fraction of correct intents |
| Intent F1 macro / weighted | utterance | sklearn `f1_score` over classes |
| Slot Precision / Recall / F1 | span (type + value) | Exact span set match |
| Slot F1 (seqeval) | BIO sequence | Token-level span F1 (same as encoders) |
| Joint (paper) | — | `(Intent F1 weighted + Span F1) / 2` from `metrics_summary.json` |

Rare intents/slots in train (threshold 500) are flagged as weak categories.

---

## 7. Output files (per run)

| File | Content |
|------|---------|
| `metrics_summary.json` | Aggregated metrics |
| `results.csv` | Per utterance: text, gold/pred intent, slots, confidence |
| `log.txt` | Verbose log |
| `per_slot_bio.csv` | Per-slot F1 (seqeval) |
| `per_slot_span.csv` | Per-slot F1 (strict span match) |
| `fewshot_examples.json` | Few-shot only: demonstration texts |
| `checkpoint.json` | Resume checkpoint every 10 utterances |

Model-level summary: `summary_<MODEL_NAME>.csv` under `SAVE_DIR`.

---

## 8. Dependencies

`transformers`, `accelerate`, `bitsandbytes`, `torch`, `pandas`, `seqeval`, `scikit-learn`, `tqdm`. GPU recommended (notebook targets Colab L4). Gated models require a Hugging Face token (`HF_TOKEN`).

---

## Repository links

| Artifact | Location |
|----------|----------|
| Experiment notebook | [experiments/generative/zero_shot+few_shot_version.ipynb](../experiments/generative/zero_shot+few_shot_version.ipynb) |
| LLM error tables | [data/errors/generative_error_analysis_tables.xlsx](../data/errors/generative_error_analysis_tables.xlsx) |
| Encoder metrics code | [code/metrics/nlu_metrics/](../code/metrics/nlu_metrics/), [code/metrics/run_metrics.py](../code/metrics/run_metrics.py) |
