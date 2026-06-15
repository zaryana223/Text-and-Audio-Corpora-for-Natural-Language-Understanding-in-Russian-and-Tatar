# Где вставить ссылку на репозиторий в статье (ICNLSP 2026)

Замените `ANON_URL` на ваш реальный анонимный URL после публикации на GitHub / 4open.science.

В LaTeX удобно один раз определить макрос в преамбуле (уже добавлено в `icnlsp2026.tex`):

```latex
\newcommand{\anonrepo}{\url{https://anonymous.4open.science/r/ru-tt-nlu-icnlsp2026}}
```

---

## Обязательные места (рекомендуем)

### 1. Section 3 — Corpora (после статистики) — **главное место**

Сразу после абзаца про audio (стр. ~136), перед Table span-length:

> **English:**  
> *Code, manually annotated benchmarks, and training CoNLL files are available at \anonrepo{}.*

> **Русский смысл:** код, ручные test/val и обучающие CoNLL выложены по ссылке.

Рецензенты ожидают data availability именно в разделе про корпус.

### 2. Section 5 — Experimental Setup → Metrics

После первого абзаца про intent accuracy / span F1:

> *We provide a reference implementation of all reported metrics at \anonrepo{} (`code/metrics/`).*

### 3. Conclusion — вместо голого "public release"

Было: `Future work includes expanded generative evaluation and public release.`

Стало:

> *Future work includes expanded generative evaluation; code and data are publicly available at \anonrepo{}.*

---

## Дополнительно (по желанию)

### Abstract — короткая сноска

Только если есть место (1 строка):

> *Data and code: \anonrepo{}.*

### Limitations

> *Audio files are distributed via MERA Multi rather than the anonymous repository; see Section 3.4.*

### Camera-ready / после рецензии

- Убрать `[review]` из `\usepackage[review]{acl}`
- Заменить `\anonrepo` на финальный URL (или Zenodo DOI)
- В README репозитория добавить bibtex принятой статьи

---

## Что писать рецензентам в submission form

**Data availability:** Yes — anonymous repository  
**URL:** `<ваш ANON_URL>`  
**License:** MIT (code); xSID-derived annotations subject to original xSID terms

---

## Файл с готовыми LaTeX-фрагментами

См. `docs/PAPER_SNIPPET.tex` — можно копировать блоки в Overleaf.
