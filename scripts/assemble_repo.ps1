# Assemble full anonymous release from local thesis paths and optional git clones.
# Run from repo root:  .\scripts\assemble_repo.ps1

$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot

function Copy-IfExists($Src, $Dst) {
    if (Test-Path $Src) {
        $dir = Split-Path -Parent $Dst
        if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
        Copy-Item -Force $Src $Dst
        Write-Host "  OK $Dst"
    } else {
        Write-Host "  SKIP (missing) $Src"
    }
}

Write-Host "=== Russian benchmarks ==="
$ruBench = Join-Path $Root "benchmarks\russian"
Copy-IfExists "c:\Users\aleks\diploma\data\ru.test_adapt.conll" (Join-Path $ruBench "ru.test_adapt.conll")
Copy-IfExists "c:\Users\aleks\diploma\results\data\ru.test.conll" (Join-Path $ruBench "ru.test.conll")

# From XSID-ru-NLP clone (if present)
$xsidRu = "$env:USERPROFILE\XSID-ru-NLP"
Copy-IfExists (Join-Path $xsidRu "ru.test.conll") (Join-Path $ruBench "ru.test.conll")
Copy-IfExists (Join-Path $xsidRu "ru.valid.conll") (Join-Path $ruBench "ru.valid.conll")
Copy-IfExists (Join-Path $xsidRu "ru.test_adapt.conll") (Join-Path $ruBench "ru.test_adapt.conll")
Copy-IfExists (Join-Path $xsidRu "ru.valid_adapt.conll") (Join-Path $ruBench "ru.valid_adapt.conll")

Write-Host "=== Tatar benchmarks ==="
$ttBench = Join-Path $Root "benchmarks\tatar"
$ttRepo = "$env:USERPROFILE\-Data-collection-for-natural-language-understanding-NLU-tasks-in-the-Tatar-language"
Get-ChildItem -Path $ttRepo -Filter "*.conll" -ErrorAction SilentlyContinue | ForEach-Object {
    Copy-IfExists $_.FullName (Join-Path $ttBench $_.Name)
}

Write-Host "=== Tatar training ==="
$ttTrain = Join-Path $Root "training\tatar"
Get-ChildItem -Path "c:\Users\aleks\diploma" -Recurse -Filter "*tat*adapt*.conll" -ErrorAction SilentlyContinue | Select-Object -First 3 | ForEach-Object {
    Copy-IfExists $_.FullName (Join-Path $ttTrain "tt.train_adapt.conll")
}

Write-Host "=== Russian training (refresh) ==="
$ruTrain = Join-Path $Root "training\russian"
Copy-IfExists "c:\Users\aleks\diploma\_github_push\ru.train.conll" (Join-Path $ruTrain "ru.train.conll")
Copy-IfExists "c:\Users\aleks\diploma\_github_push\ru.train_adapt.conll" (Join-Path $ruTrain "ru.train_adapt.conll")

Write-Host "Done. Check benchmarks/ and training/ folders."
