# Text and Audio Corpora for NLU in Russian and Tatar

Anonymous release for the ICNLSP 2026 paper.  
**Anonymous view:** [anonymous.4open.science](https://anonymous.4open.science/r/Text-and-Audio-Corpora-for-Natural-Language-Understanding-in-Russian-and-Tatar-0151)

Parallel task-oriented NLU corpora (intent detection + BIO slot filling) for **Russian** and **Tatar**, built on the [xSID]([https://github.com/facebookresearch/xsid](https://github.com/mainlp/xsid.git)) schema.

---

## Repository structure

| Path | Source | Contents |
|------|--------|----------|
| `benchmarks/russian/` | XSID-ru-NLP + manual adaptation | `ru.test.conll`, `ru.valid.conll`, `ru.test_adapt.conll`, `ru.valid_adapt.conll` |
| `benchmarks/tatar/` | Tatar NLU collection | `tt.test.conll`, `tt.valid.conll`, adapted variants |
| `training/russian/` | Development corpus (RU) | `ru.train.conll`, `ru.train_adapt.conll`, English reference |
| `training/tatar/` | Tatar NLU collection | `tt.train.conll`, `tt.train_adapt.conll` |
| `code/metrics/` | Development corpus (RU) | NLU evaluation (`run_metrics.py`, `nlu_metrics/`) |
| `code/preprocessing/` | Development corpus (RU) | MT, cleanup, cultural adaptation notebooks |
| `code/generative/` | Development corpus (RU) | Zero-shot / few-shot LLM evaluation |
| `code/annotation/` | XSID-ru-NLP | Manual annotation notebooks |
| `experiments/nlu/` | NLU (MaChAmp) | Encoder fine-tuning runs, predictions, configs |
| `tatar/` | Tatar NLU collection | Scripts, full `data/` tree (text + audio + ASR transcriptions) |
| `data/errors/` | Development corpus (RU) | Validation metrics and error-analysis spreadsheets |
| `docs/` | Combined | Evaluation docs, generative LLM setup, paper snippets |

---

## Quick start: metrics

```bash
pip install -r requirements.txt
cd code/metrics
python run_metrics.py \
  --gold ../../benchmarks/russian/ru.test_adapt.conll \
  --pred path/to/predictions.conll \
  --model mdeberta_adapt_adapt \
  --output-dir ../../results
```

| Metric | Description |
|--------|-------------|
| Intent Accuracy | Fraction of correct intents |
| Span F1 | BIO span F1 ([seqeval](https://github.com/chakki-works/seqeval)) |
| Slot F1 (/N) | Mean per-utterance BIO F1 (ASR→NLU pipeline) |
| Avg. | `(Intent F1 + Span F1) / 2` |

---

## Corpus statistics

| | Russian | Tatar |
|---|---------|-------|
| Test (translated) | 532 | 500 |
| Test (adapted) | 500 | 500 |
| Validation (per variant) | 300 | 300 |
| Training (deduplicated) | 37,173 | 37,173 |
| Audio (test + val) | 800 | 800 |
