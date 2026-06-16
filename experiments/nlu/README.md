# Russian NLU experiments (encoders, ASR, metrics)

Notebooks, CoNLL exports, and comparison CSVs used for Russian encoder and ASR→NLU experiments in the ICNLSP 2026 paper.

## Data files

| File | Description |
|------|-------------|
| `ru.test_adapt.conll` | 500 adapted test utterances (xSID-ru) |
| `ru.valid_adapt.conll` | 300 adapted validation utterances |
| `xSID-ru/` | Russian xSID test/validation CoNLL (translated from [xSID](https://github.com/mainlp/xsid/tree/main/data/xSID)) |
| `spoken_test_adapt/` | Recorded adapted **test** audio (500 utterances); used in `speech_recognition_pipeline.ipynb` |
| `spoken_valid_adapt/` | Recorded adapted **validation** audio (150 utterances); used for Vosk and GigaAM comparison |
| `cities_test_adapt.conll` | 1,125 city-name examples (generated with `automatic_labeling_data.ipynb`) |
| `cities_test_adapt.raw.txt` | Same dataset in raw-text form |
| `cities_test_adapt.raw_0.conll` | mDeBERTa-v3-base predictions |

## Prediction and metric artifacts

| File | Description |
|------|-------------|
| `comparison_cities.csv` | Gold vs. predicted (cities); scored with `metrics_evaluation.ipynb` |
| `comparison_gigaAM.csv` | Test set via GigaAM ASR → NLU |
| `comparison_test_adapt.csv` | Adapted test: gold vs. mDeBERTa predictions |
| `comparison_vosk.csv` | Test set via Vosk ASR → NLU |
| `metrics_epoch_15.json` | Best-epoch accuracy snapshot |
| `nlu.xsid_test_adapt.out` | mDeBERTa-v3-base test predictions |
| `nlu.xsid_test_adapt.out.eval` | Aggregated test evaluation |
| `ru.test_vosk.raw.conll` | Vosk transcripts in raw CoNLL form |
| `ru.test_vosk.raw_0.conll` | NLU predictions on Vosk text |
| `ru_GigaAM_0.raw.txt` | GigaAM transcripts (raw) |
| `ru_GigaAM.raw_0.conll` | NLU predictions on GigaAM text |

## Notebooks

| Notebook | Purpose |
|----------|---------|
| `xSID.ipynb` | [MaChAmp](https://github.com/machamp-nlp/machamp) fine-tuning |
| `automatic_labeling_data.ipynb` | Synthetic city dataset: gap filling, case agreement, entity replacement |
| `speech_recognition_pipeline.ipynb` | Speech-to-text with [GigaAM](https://github.com/salute-developers/GigaAM) and [Vosk](https://alphacephei.com/vosk/models); WER/CER for model selection |
| `metrics_evaluation.ipynb` | Restore utterance IDs, build comparison CSVs, compute Intent Accuracy |

## Recorded audio layout (`spoken_test_adapt/`)

Speaker subfolders use English names: `male_16y`, `male_36y`, `female_20y_1`, `female_20y_2`, `female_20y_3`, `female_21y`, `female_46y`.
