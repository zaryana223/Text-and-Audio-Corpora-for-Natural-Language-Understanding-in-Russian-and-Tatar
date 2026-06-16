# Where to cite the repository in the ICNLSP 2026 paper

Replace `ANON_URL` with your real anonymous URL after publishing on GitHub or 4open.science.

Define a macro once in the preamble (already in `icnlsp2026.tex`):

```latex
\newcommand{\anonrepo}{\url{https://anonymous.4open.science/r/ru-tt-nlu-icnlsp2026}}
```

---

## Recommended placements

### 1. Section 3 — Corpora (after statistics) — **primary**

Right after the paragraph on audio (~p. 136), before the span-length table:

> *Code, manually annotated benchmarks, and training CoNLL files are available at \anonrepo{}.*

Reviewers expect data availability in the corpus section.

### 2. Section 5 — Experimental Setup → Metrics

After the first paragraph on intent accuracy / span F1:

> *We provide a reference implementation of all reported metrics at \anonrepo{} (`code/metrics/`).*

### 3. Conclusion — instead of a vague “public release”

Replace:

> *Future work includes expanded generative evaluation and public release.*

With:

> *Future work includes expanded generative evaluation; code and data are publicly available at \anonrepo{}.*

---

## Optional

### Abstract — one line

> *Data and code: \anonrepo{}.*

### Limitations

> *Audio files are distributed via MERA Multi rather than the anonymous repository; see Section 3.4.*

### Camera-ready

- Remove `[review]` from `\usepackage[review]{acl}`
- Replace `\anonrepo` with the final URL (or Zenodo DOI)
- Add the accepted paper bibtex to the repository README

---

## Submission form

**Data availability:** Yes — anonymous repository  
**URL:** `<your ANON_URL>`  
**License:** MIT (code); xSID-derived annotations subject to original xSID terms

---

## Ready-made LaTeX fragments

See `docs/PAPER_SNIPPET.tex` for copy-paste blocks in Overleaf.
