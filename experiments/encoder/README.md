# Encoder fine-tuning (MaChAmp)

This folder documents how to reproduce encoder experiments from the paper. Full training configs and prediction files are maintained in a separate MaChAmp workflow repository to keep this release focused on **data + metrics**.

## Setup

1. Install [MaChAmp](https://github.com/jerbarnes/machamp) and dependencies.
2. Point MaChAmp to CoNLL files under `benchmarks/` and `training/`.
3. Use the xSID task definition (intent + BIO slots).

## Configurations (Section 5.2)

Six fine-tuning setups per language:

| Train data | Eval benchmark |
|------------|----------------|
| English xSID | Translated test |
| English xSID | Adapted test |
| In-language translated | Translated test |
| In-language translated | Adapted test |
| In-language adapted | Translated test |
| In-language adapted | Adapted test |

## Models

- mBERT, RemBERT, mDeBERTa-v3-base, EuroBERT, mmBERT (Russian and Tatar)
- Pivot training: 11 xSID languages → Russian/Tatar validation
- Cross-lingual: Russian ↔ Tatar transfer (symmetric)

## Evaluation

Export MaChAmp predictions as CoNLL and score with:

```bash
cd code/metrics
python run_metrics.py --gold ../../benchmarks/russian/ru.test_adapt.conll \
  --pred /path/to/predictions.conll --model mdeberta_adapt_adapt
```

Validation metric spreadsheets referenced in the paper are described in `docs/DATA_AND_ERRORS.md`.
