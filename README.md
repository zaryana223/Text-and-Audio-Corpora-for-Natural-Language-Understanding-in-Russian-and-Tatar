# Parallel Russian and Tatar NLU Corpora (Text and Audio)

Anonymous release accompanying the ICNLSP 2026 submission *Text and Audio Corpora for Natural Language Understanding in Russian and Tatar*.

This repository bundles **benchmark CoNLL files**, **large-scale training data**, **evaluation code**, and **experiment scripts** for task-oriented NLU (intent detection + BIO slot filling) in Russian and Tatar, built on the [xSID](https://github.com/facebookresearch/xsid) schema (18 intents, 44 slot types).

> **Anonymous review:** do not link this repository to author identities until acceptance. After de-anonymization, replace the anonymous URL in the paper with the public repository URL.

---

## Repository layout

| Path | Contents |
|------|----------|
| `benchmarks/russian/` | Manually annotated Russian **test** and **validation** splits (`translated` and `adapted` variants) |
| `benchmarks/tatar/` | Manually annotated Tatar **test** and **validation** splits (`translated` and `adapted` variants) |
| `training/russian/` | Russian training corpus (~37k utterances): machine-translated and culturally adapted CoNLL |
| `training/tatar/` | Tatar training corpus (translated + adapted; same pipeline as Russian) |
| `code/metrics/` | Reproducible NLU metrics (intent accuracy/F1, span F1, joint score; ASR-aware slot F1) |
| `code/preprocessing/` | Notebooks and scripts for xSID cleanup, MT, and entity adaptation |
| `code/generative/` | Zero-shot / few-shot evaluation of instruction-tuned LLMs (JSON intent + slots) |
| `experiments/encoder/` | Pointers and configs for MaChAmp fine-tuning (see `README.md` in that folder) |
| `docs/` | Evaluation tables, generative LLM setup, paper citation snippets |

### CoNLL format

Each file follows the xSID / MaChAmp convention:

- Utterance header: `# id: <id>` and `# intent = <label>`
- Token lines: `token\t_\tBIO-tag`
- Blank line between utterances

**Split naming:**

| Suffix / name | Meaning |
|---------------|---------|
| `*_trans` / translated | Manual calque of the English xSID benchmark |
| `*_adapt` / adapted | Culturally localized slot values and rephrasing |
| `ru.train.conll` | Large-scale MT training (translated) |
| `ru.train_adapt.conll` | Large-scale MT + automatic entity adaptation |

---

## Quick start: evaluation metrics

```bash
pip install -r requirements.txt
cd code/metrics
python run_metrics.py \
  --gold ../../benchmarks/russian/ru.test_adapt.conll \
  --pred path/to/model_predictions.conll \
  --model mdeberta_adapt_adapt \
  --output-dir ../../results
```

**Metrics** (aligned with the paper):

| Metric | Description |
|--------|-------------|
| Intent Accuracy | Fraction of utterances with correct intent |
| Intent F1 (weighted) | Weighted F1 over intent classes |
| Span F1 | Span-level slot F1 ([seqeval](https://github.com/chakki-works/seqeval), BIO) |
| Slot F1 (/N) | Mean per-utterance BIO F1 over all test utterances (spoken ASR→NLU pipeline) |
| Avg. / Joint | `(Intent F1 weighted + Span F1) / 2` (encoders); ASR runs use Slot F1 (/N) |

Outputs: `comparison_<model>.csv`, `metrics_summary.csv`, optional `per_slot_<model>.csv`.

---

## Corpus statistics (paper-aligned)

| | Russian | Tatar |
|---|---------|-------|
| Test (translated) | 532 | 500 |
| Test (adapted) | 500 | 500 |
| Validation (per variant) | 300 | 300 |
| Training (deduplicated) | 37,173 | 37,173 |
| Audio (test + val) | 800 | 800 |

Audio recordings and the Russian spoken benchmark **ruSLUn** are distributed separately via [MERA Multi](https://github.com/ai-forever/MERA) (EACL 2026); this repo focuses on **text** benchmarks, training data, and evaluation code.

---

## Preprocessing pipeline

1. **Clean** English xSID training pool (`code/preprocessing/clean_up.ipynb`)
2. **Translate** to Russian/Tatar with LLM APIs (`code/preprocessing/translation.py`)
3. **Adapt** slot entities culturally (`code/preprocessing/adaptation.ipynb`)
4. **Annotate** test/validation manually (benchmark files in `benchmarks/`)

See `docs/CORPUS_LAYOUT.md` for the full file list.

---

## Encoder experiments (MaChAmp)

Fine-tuning uses [MaChAmp](https://github.com/jerbarnes/machamp) on top of multilingual encoders (mBERT, RemBERT, mDeBERTa-v3, EuroBERT, mmBERT). Configuration templates and run logs are documented in `experiments/encoder/README.md`. Pivot-language and cross-lingual transfer experiments follow the setups in Section 5 of the paper.

---

## Generative NLU (zero-shot / few-shot)

Notebook: `code/generative/zero_shot+few_shot_version.ipynb`  
Documentation: `docs/ZERO_SHOT_FEW_SHOT.md`  
Summary tables: `docs/DATA_AND_ERRORS.md` (generative error analysis spreadsheets are listed there).

Models are prompted in Russian (Russian benchmark) or Tatar (Tatar benchmark) to output JSON with `intent` and `slots`.

---

## Assembly

If you cloned only the code, run `scripts/assemble_repo.ps1` (Windows) to copy benchmark and training CoNLL files from local thesis paths or sibling clones of the source repositories.

---

## Citation

If you use these resources, please cite our ICNLSP 2026 paper (citation to be added upon publication) and the original xSID dataset:

```bibtex
@inproceedings{vandergoot2021masked,
  title={Massive Choice, Ample Tasks ({MA}t{AMPA}): A New Dataset for Massive Multilingual {NLU}},
  author={van der Goot, Rob and others},
  booktitle={ACL-IJCNLP},
  year={2021}
}
```

---

## License

MIT — see [LICENSE](LICENSE).  
Benchmark annotations are derived from [xSID](https://github.com/facebookresearch/xsid); respect the original dataset license when redistributing.
