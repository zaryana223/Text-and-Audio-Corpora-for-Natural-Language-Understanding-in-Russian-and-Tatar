# Reorganize repo layout. Run from repo root: .\scripts\reorganize_repo.ps1
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

function Ensure-Dir($Path) {
    if (-not (Test-Path $Path)) { New-Item -ItemType Directory -Force -Path $Path | Out-Null }
}

function Git-Mv($Src, $Dst) {
    $srcNorm = $Src -replace '\\', '/'
    $dstNorm = $Dst -replace '\\', '/'
    if (-not (Test-Path $srcNorm)) { Write-Warning "SKIP missing $srcNorm"; return }
    $parent = Split-Path -Parent $dstNorm
    if ($parent) { Ensure-Dir $parent }
    if (Test-Path $dstNorm) { Remove-Item -Force $dstNorm }
    git mv -- "$srcNorm" "$dstNorm"
    Write-Host "  mv $srcNorm -> $dstNorm"
}

Write-Host "=== Create directories ==="
@(
    "data/russian/text", "data/russian/audio/test", "data/russian/audio/val",
    "data/tatar/text", "data/tatar/audio/test", "data/tatar/audio/val", "data/tatar/audio/asr_transcriptions",
    "experiments/encoders/configs",
    "experiments/encoders/predictions/russian", "experiments/encoders/predictions/tatar",
    "experiments/generative/prompts",
    "experiments/generative/predictions/russian", "experiments/generative/predictions/tatar",
    "code/adaptation", "code/utils"
) | ForEach-Object { Ensure-Dir $_ }

Write-Host "=== Russian text ==="
Git-Mv "training/russian/ru.train.conll"           "data/russian/text/train.conll"
Git-Mv "benchmarks/russian/ru.test.conll"        "data/russian/text/test_translated.conll"
Git-Mv "benchmarks/russian/ru.test_adapt.conll" "data/russian/text/test_adapted.conll"
Git-Mv "benchmarks/russian/ru.valid.conll"       "data/russian/text/val_translated.conll"
Git-Mv "benchmarks/russian/ru.valid_adapt.conll" "data/russian/text/val_adapted.conll"
if (Test-Path "training/russian/ru.train_adapt.conll") {
    Git-Mv "training/russian/ru.train_adapt.conll" "data/russian/text/train_adapted.conll"
}
foreach ($extra in @("ru.train.unique_ids.conll", "en.train.reference.conll", "en.train.unique_ids.conll")) {
    $p = "training/russian/$extra"
    if (Test-Path $p) { Git-Mv $p "data/russian/text/$extra" }
}

Write-Host "=== Tatar text ==="
Git-Mv "training/tatar/tt.train.conll"           "data/tatar/text/train.conll"
Git-Mv "benchmarks/tatar/tt.test.conll"        "data/tatar/text/test_translated.conll"
Git-Mv "benchmarks/tatar/tt.test_adapt.conll"   "data/tatar/text/test_adapted.conll"
Git-Mv "benchmarks/tatar/tt.valid.conll"       "data/tatar/text/val_translated.conll"
Git-Mv "benchmarks/tatar/tt.valid_adapt.conll" "data/tatar/text/val_adapted.conll"
if (Test-Path "training/tatar/tt.train_adapt.conll") {
    Git-Mv "training/tatar/tt.train_adapt.conll" "data/tatar/text/train_adapted.conll"
}
if (Test-Path "benchmarks/tatar/valid_tat.conll") {
    Git-Mv "benchmarks/tatar/valid_tat.conll" "data/tatar/text/val_translated_tat.conll"
}

Write-Host "=== experiments/nlu -> experiments/encoders ==="
if (Test-Path "experiments/nlu") {
    Get-ChildItem "experiments/nlu" -File | ForEach-Object {
        $name = $_.Name
        $src = "experiments/nlu/$name"
        if ($name -match '\.(out|eval)$' -or ($name -match '^(ru\.|nlu\.|cities_)' -and $name -match '\.(conll|raw|txt)$')) {
            Git-Mv $src "experiments/encoders/predictions/russian/$name"
        } else {
            Git-Mv $src "experiments/encoders/$name"
        }
    }
}

Write-Host "=== Russian audio (spoken_test_adapt / spoken_valid_adapt) ==="
if (Test-Path "experiments/nlu/spoken_test_adapt") {
    Get-ChildItem "experiments/nlu/spoken_test_adapt" -Recurse -Filter "*.wav" | ForEach-Object {
        $rel = $_.FullName.Substring($Root.Length + 1) -replace '\\', '/'
        Git-Mv $rel "data/russian/audio/test/$($_.Name)"
    }
}
if (Test-Path "experiments/nlu/spoken_valid_adapt") {
    Get-ChildItem "experiments/nlu/spoken_valid_adapt" -Recurse -Filter "*.wav" | ForEach-Object {
        $rel = $_.FullName.Substring($Root.Length + 1) -replace '\\', '/'
        Git-Mv $rel "data/russian/audio/val/$($_.Name)"
    }
}

Write-Host "=== Tatar audio ==="
if (Test-Path "tatar/data/audio/asr_transcriptions") {
    Get-ChildItem "tatar/data/audio/asr_transcriptions" -File | ForEach-Object {
        Git-Mv "tatar/data/audio/asr_transcriptions/$($_.Name)" "data/tatar/audio/asr_transcriptions/$($_.Name)"
    }
}
Get-ChildItem "tatar/data/audio" -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -ne "asr_transcriptions" } | ForEach-Object {
    Get-ChildItem $_.FullName -Filter "*.wav" | ForEach-Object {
        Git-Mv "tatar/data/audio/$($_.Directory.Name)/$($_.Name)" "data/tatar/audio/test/$($_.Name)"
    }
}

Write-Host "=== code moves ==="
if (Test-Path "code/generative") {
    Get-ChildItem "code/generative" -File | ForEach-Object {
        Git-Mv "code/generative/$($_.Name)" "experiments/generative/$($_.Name)"
    }
}
if (Test-Path "code/preprocessing/translation.py") {
    Git-Mv "code/preprocessing/translation.py" "code/adaptation/translation.py"
}
if (Test-Path "code/preprocessing/clean_up.ipynb") {
    Git-Mv "code/preprocessing/clean_up.ipynb" "code/adaptation/translate.ipynb"
}
if (Test-Path "code/preprocessing/adaptation.ipynb") {
    Git-Mv "code/preprocessing/adaptation.ipynb" "code/adaptation/cultural_adapt.ipynb"
}
if (Test-Path "code/annotation/annotation_labeling.ipynb") {
    Git-Mv "code/annotation/annotation_labeling.ipynb" "code/annotation/manual_annotation.ipynb"
}

Write-Host "=== tatar/scripts -> code/utils + encoders ==="
@("wer_and_cer.py", "soyle.py", "entities.py") | ForEach-Object {
    if (Test-Path "tatar/scripts/$_") { Git-Mv "tatar/scripts/$_" "code/utils/$_" }
}
@("machamp.ipynb", "train_adapted.ipynb") | ForEach-Object {
    if (Test-Path "tatar/scripts/$_") { Git-Mv "tatar/scripts/$_" "experiments/encoders/$_" }
}

Write-Host "=== Merge experiments/encoder README ==="
if (Test-Path "experiments/encoder/README.md") {
    if (-not (Test-Path "experiments/encoders/README.md")) {
        Git-Mv "experiments/encoder/README.md" "experiments/encoders/README_encoder_legacy.md"
    } else {
        git rm -f "experiments/encoder/README.md" 2>$null
    }
}

Write-Host "=== .gitkeep ==="
@(
    "experiments/encoders/predictions/russian/.gitkeep",
    "experiments/encoders/predictions/tatar/.gitkeep",
    "experiments/generative/predictions/russian/.gitkeep",
    "experiments/generative/predictions/tatar/.gitkeep"
) | ForEach-Object {
    if (-not (Test-Path $_)) { New-Item -ItemType File -Path $_ -Force | Out-Null }
}

Write-Host "=== Remove empty legacy trees ==="
@(
    "benchmarks", "training", "tatar", "experiments/nlu", "experiments/encoder",
    "code/generative", "code/preprocessing"
) | ForEach-Object {
    if (Test-Path $_) {
        git rm -rf $_ 2>$null
        if (Test-Path $_) { Remove-Item -Recurse -Force $_ -ErrorAction SilentlyContinue }
    }
}

Write-Host "Done. Run: git status"
