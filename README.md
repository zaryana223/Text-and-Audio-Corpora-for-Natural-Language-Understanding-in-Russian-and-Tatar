# Text and Audio Corpora for NLU in Russian and Tatar

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)
![Languages](https://img.shields.io/badge/Languages-Russian%20%7C%20Tatar-orange)
![Paper](https://img.shields.io/badge/Paper-ICNLSP%202026-red)

---

## Abstract

Task-oriented dialogue systems rely on natural language understanding (NLU) to map utterances to intents and slot values. Although voice assistants are widely deployed, Russian and — especially — Tatar remain low-resource for NLU: annotated corpora are scarce and manual cultural adaptation is costly.

To address this gap, we construct parallel Russian and Tatar NLU resources based on the [xSID](https://github.com/mainlp/xsid) benchmark: test and validation splits are manually translated and culturally adapted; the training set is machine-translated with large language models (LLMs) and manually corrected. We additionally record native-speaker audio for both languages and evaluate spoken NLU through automatic speech recognition (ASR)→NLU.

In-language training substantially outperforms English-only fine-tuning; typologically close pivot languages transfer better than distant ones on slot filling; and instruction-tuned generative models achieve strong intent scores but trail fine-tuned encoders on slot extraction.

---

## Repository layout

```
├── data/                    # corpora only (text + audio)
│   ├── russian/
│   └── tatar/
├── code/                    # all pipelines and evaluation
│   ├── adaptation/          # MT, cultural adaptation (russian/ | tatar/)
│   ├── annotation/          # manual benchmark annotation
│   ├── encoders/            # MaChAmp fine-tuning
│   ├── generative/          # zero-/few-shot LLM evaluation
│   ├── asr/                 # speech recognition (russian/ | tatar/)
│   └── metrics/             # NLU scoring (russian/ | tatar/)
├── predictions/             # model outputs (encoder/ | generative/)
│   ├── encoder/
│   └── generative/
└── requirements.txt
```

---

## Data

All annotated material lives under `data/{language}/`. Both languages share the [xSID-0.7](https://github.com/mainlp/xsid) schema: **18 intents**, **44 slot types**, **BIO** tagging.

### Text (`data/{lang}/text/`)

| File | Description | Size |
|------|-------------|------|
| `train.conll` | Machine-translated training corpus (deduplicated) | 37,173 utt. |
| `test_translated.conll` | Manually translated test (calque of English benchmark) | RU 532 / TT 500 |
| `test_adapted.conll` | Manually culturally adapted test | 500 |
| `val_translated.conll` | Manually translated validation | 300 |
| `val_adapted.conll` | Culturally adapted validation | 300 |

**Translated** splits follow the English source literally (foreign place names may remain). **Adapted** splits replace entities with culturally familiar Russian or Tatar equivalents while preserving intents and BIO spans.

Optional extras in `data/russian/text/`: `train_adapted.conll`, `en.train.reference.conll`, `en.train.unique_ids.conll`, `ru.train.unique_ids.conll`.  
Optional in `data/tatar/text/`: `train_adapted.conll`, `english.conll`, `english_normalised.conll`, `söyle_raw.conll`.

**CoNLL format** — one token per line; intent on `# intent:`; slots in BIO:

```
# intent: weather/find
какая    O
погода   O
будет    O
завтра   B-datetime
в        O
Казани   B-location
```

### Audio

| Path | Language | Contents |
|------|----------|----------|
| `data/russian/audio/test/` | Russian | 500 mono WAV (7 speakers) |
| `data/russian/audio/val/` | Russian | 300 mono WAV |
| `data/tatar/audio/test/` | Tatar | 500 mono WAV (9 speakers) |
| `data/tatar/audio/asr_transcriptions/` | Tatar | Söyle ASR hypotheses (`.txt`) |

Speaker demographics and recording conditions: `data/{lang}/speaker_metadata.json`.  
Recordings were made by non-professional native speakers on consumer smartphones in everyday acoustic settings.

### Working with text and audio

1. **Text-only NLU** — load any split from `data/{lang}/text/`, fine-tune an encoder (`code/encoders/`) or run generative prompts (`code/generative/`), score with `code/metrics/{lang}/`.
2. **Adapted vs translated** — use **adapted** test/val when evaluating on localised entities; **translated** train often yields higher slot F1 when train and test variants match.
3. **Spoken NLU** — transcribe WAV with `code/asr/russian/` (GigaAM) or `code/asr/tatar/` (Söyle), then pass CoNLL transcripts to NLU models. Compare ASR output with `wer_and_cer.ipynb`.

---

## Code

All processing and evaluation scripts are under `code/`. Notebooks were used for the ICNLSP 2026 experiments; Python entry points can be extracted from them where noted.

Language-specific folders (`russian/`, `tatar/`) are used for **adaptation**, **asr**, and **metrics**. **annotation**, **encoders**, and **generative** are shared.

### `code/adaptation/` — corpus construction

| Path | Role |
|------|------|
| `russian/translate.ipynb` | Machine translation of the English xSID training pool via LLMs |
| `russian/cultural_adapt.ipynb` | Russian cultural adaptation: entity replacement, morphological fixes |
| `russian/translation.py` | Translation utilities and prompt helpers |
| `tatar/deepseek_translation.ipynb` | DeepSeek-based translation pipeline for Tatar |
| `tatar/train_adapted.ipynb` | Automated entity substitution for Tatar adapted training splits |
| `tatar/entities.py` | Curated replacement lexicons for Tatar adaptation |

The pipeline mirrors the paper: manual translation + adaptation for benchmarks; LLM translation + automatic adaptation at scale for training.

### `code/annotation/` — manual labelling

| File | Role |
|------|------|
| `annotation.ipynb` | Interactive workflow for verifying intents and BIO spans on benchmark utterances |

### `code/encoders/` — fine-tuned NLU models

| File | Role |
|------|------|
| `machamp.ipynb` | [MaChAmp](https://github.com/machamp-nlp/machamp) joint intent classification + BIO slot labeling; mDeBERTa-v3, EuroBERT, XLM-R / Glot500 |

Supports in-language and cross-lingual pivot training described in the paper.

### `code/generative/` — instruction-tuned LLMs

| File | Role |
|------|------|
| `zero_shot+few_shot_version.ipynb` | Zero- and few-shot evaluation of Qwen2.5, Gemma-2, Phi-4-mini, Mistral-7B; JSON `{intent, slots}` output against xSID inventory |

Models are **not** fine-tuned on the corpus; prompts enforce the 16-intent / 33-slot schema at inference time.

### `code/asr/` — speech recognition

| Path | Role |
|------|------|
| `russian/speech_recognition_pipeline.ipynb` | GigaAM v3 ASR→NLU cascade for Russian |
| `russian/wer_and_cer.ipynb` | Word/character error rate for Russian ASR |
| `tatar/soyle.ipynb` | Batch ASR with the Söyle Turkic speech model |
| `tatar/wer_and_cer.ipynb` | WER/CER for Tatar ASR transcripts |

### `code/metrics/` — evaluation

| Path | Role |
|------|------|
| `russian/metrics_evaluation.ipynb` | Batch comparison CSVs and aggregated tables (Russian) |
| `russian/run_metrics.py` | CLI: Intent Accuracy, Span F1 (seqeval), per-slot breakdown |
| `russian/metrics.py`, `csv_builder.py` | Intent Accuracy, Span F1, per-slot breakdown |
| `tatar/run_metrics.py` | CLI: Intent Accuracy, Span F1 (seqeval), per-slot breakdown |
| `tatar/metrics.py`, `csv_builder.py` | Same metric functions for Tatar evaluation |

| Metric | Definition |
|--------|------------|
| Intent Accuracy | Fraction of utterances with correct intent |
| Span F1 | Token-level BIO span F1 ([seqeval](https://github.com/chakki-works/seqeval)) |
| Slot F1 (/N) | Mean per-utterance BIO F1 (for ASR→NLU when lengths differ) |
| Avg. | `(Intent Acc + Span F1) / 2` |

---

## Predictions

Pre-computed model outputs are stored under `predictions/`. Each CSV contains per-utterance intent and slot predictions.

### Encoder predictions (`predictions/encoder/`)

| Path | Description |
|------|-------------|
| `russian/russian_encoder_adapt.zip` | MaChAmp encoder predictions on Russian adapted test |
| `russian/russian_encoder_trans.zip` | MaChAmp encoder predictions on Russian translated test |
| `tatar/tatar_encoder.zip` | MaChAmp encoder predictions on Tatar test |

### Generative predictions (`predictions/generative/`)

Each model has its own subfolder with zero-shot and few-shot result CSVs.

**Russian** (`predictions/generative/russian/`): Gemma-2-2B-it, Gemma-2-9B-it, Mistral-7B-Instruct-v0.3, Phi-4-mini-instruct, Qwen2.5-3B-Instruct, Qwen2.5-7B-Instruct.

**Tatar** (`predictions/generative/tatar/`): Gemma-2-2B-it, Gemma-2-9B-it, Mistral-7B-Instruct-v0.3, Phi-4-mini-instruct, Qwen2.5-3B-Instruct, Qwen2.5-7B-Instruct.

Few-shot configurations: `few_shot_1_popular`, `few_shot_1_problem`, `few_shot_1_slots`, `few_shot_5`, `few_shot_10` — varying the number and selection strategy of in-context examples.

---

## Quick start

```bash
git clone https://github.com/zaryana223/Text-and-Audio-Corpora-for-Natural-Language-Understanding-in-Russian-and-Tatar.git
cd Text-and-Audio-Corpora-for-Natural-Language-Understanding-in-Russian-and-Tatar
pip install -r requirements.txt

cd code/metrics/russian
python run_metrics.py \
  --gold ../../data/russian/text/test_adapted.conll \
  --pred path/to/predictions.out \
  --model my_model \
  --output-dir ../../results
```

---

## Corpus statistics

| Split | Russian (text) | Tatar (text) | Audio (test / val) |
|-------|---------------|--------------|-------------------|
| Train | 37,173 | 37,173 | — |
| Test | 532 / 500* | 500 | 500 |
| Dev | 300 | 300 | 300 |

*532 translated / 500 culturally adapted

---

## License

- **Code**: MIT  
- **Data**: CC BY 4.0  
- **xSID base**: see [xSID license](https://github.com/mainlp/xsid/blob/main/LICENSE)
