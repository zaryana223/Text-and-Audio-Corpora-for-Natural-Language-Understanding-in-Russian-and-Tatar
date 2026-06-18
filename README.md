# Text and Audio Corpora for NLU in Russian and Tatar

Anonymous release for the ICNLSP 2026 paper.  
**Anonymous view:** [anonymous.4open.science](https://anonymous.4open.science/r/Text-and-Audio-Corpora-for-Natural-Language-Understanding-in-Russian-and-Tatar-0151)

Parallel task-oriented NLU corpora (intent detection + BIO slot filling) for **Russian** and **Tatar**, built on the [xSID-0.7](https://github.com/mainlp/xsid) schema.

---

## Repository layout

```
repo/
├── data/                          # all corpora (text + audio)
│   ├── russian/
│   │   ├── text/                  # train + test/val (translated & adapted)
│   │   ├── audio/test/            # 500 wav, 7 speakers
│   │   ├── audio/val/             # 300 wav
│   │   └── speaker_metadata.json
│   └── tatar/
│       ├── text/
│       ├── audio/test/            # 500 wav, 9 speakers
│       ├── audio/val/
│       ├── audio/asr_transcriptions/
│       └── speaker_metadata.json
├── experiments/
│   ├── encoders/                  # MaChAmp fine-tuning, ASR→NLU runs
│   │   ├── configs/
│   │   └── predictions/{russian,tatar}/
│   └── generative/                # zero-/few-shot LLM evaluation
│       ├── prompts/
│       └── predictions/{russian,tatar}/
├── code/
│   ├── adaptation/                # MT, cleanup, cultural adaptation
│   ├── annotation/
│   ├── metrics/                   # run_metrics.py
│   └── utils/                     # ASR helpers (Söyle, WER/CER)
├── docs/
├── scripts/
└── requirements.txt
```

### Text files (`data/{lang}/text/`)

| File | Split |
|------|-------|
| `train.conll` | Training (37,173 utt.) |
| `test_translated.conll` | Test, translated (RU: 532 / TT: 500) |
| `test_adapted.conll` | Test, culturally adapted (500) |
| `val_translated.conll` | Validation, translated (300) |
| `val_adapted.conll` | Validation, adapted (300) |

Extra Russian files: `train_adapted.conll`, `en.train.reference.conll`.  
Extra Tatar file: `train_adapted.conll`, `val_translated_tat.conll`.

---

## Quick start: metrics

```bash
pip install -r requirements.txt
cd code/metrics
python run_metrics.py \
  --gold ../../data/russian/text/test_adapted.conll \
  --pred path/to/predictions.conll \
  --model my_model \
  --output-dir ../../results
```

| Metric | Description |
|--------|-------------|
| Intent Accuracy | Fraction of correct intents |
| Span F1 | BIO span F1 ([seqeval](https://github.com/chakki-works/seqeval)) |
| Slot F1 (/N) | Mean per-utterance BIO F1 (ASR→NLU pipeline) |
| Avg. | `(Intent Acc + Span F1) / 2` |

---

## Corpus statistics

| | Russian | Tatar |
|---|---------|-------|
| Test (translated) | 532 | 500 |
| Test (adapted) | 500 | 500 |
| Validation (per variant) | 300 | 300 |
| Training (deduplicated) | 37,173 | 37,173 |
| Audio (test + val) | 800 | 800 |
