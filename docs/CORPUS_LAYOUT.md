# Corpus file layout

## Russian benchmarks (`benchmarks/russian/`)

| File | Split | Notes |
|------|-------|-------|
| `ru.test.conll` | Test, translated | 532 utterances |
| `ru.test_adapt.conll` | Test, adapted | 500 utterances |
| `ru.valid.conll` | Validation, translated | 300 utterances |
| `ru.valid_adapt.conll` | Validation, adapted | 300 utterances |

## Tatar benchmarks (`benchmarks/tatar/`)

| File | Split | Notes |
|------|-------|-------|
| `tt.test.conll` | Test, translated | 500 utterances |
| `tt.test_adapt.conll` | Test, adapted | 500 utterances |
| `tt.valid.conll` | Validation, translated | 300 utterances |
| `tt.valid_adapt.conll` | Validation, adapted | 300 utterances |

> File names may use `tat_` prefix in some internal exports; rename to `tt.*` for consistency with the paper.

## Russian training (`training/russian/`)

| File | Description |
|------|-------------|
| `en.train.reference.conll` | Cleaned English xSID training pool (reference) |
| `ru.train.conll` | Machine-translated Russian training (~37k) |
| `ru.train_adapt.conll` | Culturally adapted training |

## Tatar training (`training/tatar/`)

| File | Description |
|------|-------------|
| `tt.train.conll` | Machine-translated Tatar training |
| `tt.train_adapt.conll` | Culturally adapted Tatar training |

## Audio

Spoken data (7 Russian + 10 Tatar speakers, 800 utterances per language) are **not** stored in this repository due to size. They are released through MERA Multi as **ruSLUn** (Russian) and the Tatar spoken task; see the paper Section 3.4.
