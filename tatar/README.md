# Tatar NLU data collection

Parallel Tatar resources for intent detection and BIO slot filling (xSID schema).

## Layout

| Path | Description |
|------|-------------|
| `data/audio/` | Recorded utterances; subfolders named by speaker gender and age (`W_<age>`, `M_<age>`) |
| `data/text/` | CoNLL splits (train / valid / test, translated and adapted) |
| `data/audio/asr_transcriptions/` | Söyle ASR outputs (`soyle_results_*.txt`) |
| `scripts/` | Notebooks and utilities for ASR, training, and entity adaptation |

## Key files

| File | Role |
|------|------|
| `scripts/soyle.py` | Batch ASR with the Söyle model |
| `scripts/machamp.ipynb` | MaChAmp fine-tuning workflow |
| `scripts/wer_and_cer.py` | WER / CER between references and ASR transcripts |
| `scripts/train_adapted.ipynb` | Entity substitution for the adapted training split |
| `scripts/entities.py` | Entity lists by slot category |
| `data/text/test/soyle_raw.conll` | Test set aligned with raw ASR text |
| `data/audio/asr_transcriptions/soyle_results_full.txt` | Full-corpus Söyle transcriptions |

Benchmark copies of the test/validation splits also appear under `benchmarks/tatar/` at the repository root.
