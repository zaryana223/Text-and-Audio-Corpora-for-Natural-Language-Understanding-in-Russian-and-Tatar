# One-click upload (anonymous review)

The release is ready in this folder. **You** must create the anonymous hosting account (we cannot do that for you).

## Fastest: anonymous.4open.science

1. Open https://anonymous.4open.science and sign up (use an email not tied to your name in the paper).
2. **New repository** → name: `ru-tt-nlu-icnlsp2026`
3. Upload the zip file from your Desktop:
   `ru-tt-nlu-icnlsp2026.zip` (created next to this project)
4. Copy the URL shown on the site, e.g.  
   `https://anonymous.4open.science/r/ru-tt-nlu-icnlsp2026-Ab12Cd`
5. Paste into `icnlsp2026.tex`:
   ```latex
   \newcommand{\anonrepo}{\url{https://anonymous.4open.science/r/ru-tt-nlu-icnlsp2026-Ab12Cd}}
   ```

## Alternative: anonymous GitHub account

1. New GitHub user (no real name / HSE / links to personal repos).
2. New public repo `ru-tt-nlu-resources`.
3. Push this folder (see `scripts/push_anonymous.ps1` after setting `ANON_REMOTE`).

## What is included

- Russian & Tatar benchmarks (`benchmarks/`)
- Training CoNLL (`training/`, ~30 MB per language)
- Metrics code, preprocessing notebooks, generative evaluation notebook
- No audio (released via MERA Multi)
