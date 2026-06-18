# Corpus file layout

## Russian (`data/russian/text/`)

| File | Split | Notes |
|------|-------|-------|
| `train.conll` | Training | 37,173 utterances |
| `test_translated.conll` | Test, translated | 532 utterances |
| `test_adapted.conll` | Test, adapted | 500 utterances |
| `val_translated.conll` | Validation, translated | 300 utterances |
| `val_adapted.conll` | Validation, adapted | 300 utterances |
| `train_adapted.conll` | Training, adapted | optional |
| `en.train.reference.conll` | English reference | optional |

## Tatar (`data/tatar/text/`)

| File | Split | Notes |
|------|-------|-------|
| `train.conll` | Training | 37,173 utterances |
| `test_translated.conll` | Test, translated | 500 utterances |
| `test_adapted.conll` | Test, adapted | 500 utterances |
| `val_translated.conll` | Validation, translated | 300 utterances |
| `val_adapted.conll` | Validation, adapted | 300 utterances |
| `train_adapted.conll` | Training, adapted | optional |

## Audio

| Language | Path | Notes |
|----------|------|-------|
| Russian | `data/russian/audio/test/`, `val/` | 500 + 300 mono WAV |
| Tatar | `data/tatar/audio/test/`, `val/` | 500 + 300 mono WAV |
| Tatar ASR | `data/tatar/audio/asr_transcriptions/` | Söyle outputs |

Speaker metadata: `data/{lang}/speaker_metadata.json`
