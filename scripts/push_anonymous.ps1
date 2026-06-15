# Run AFTER you created an empty repo on anonymous GitHub and set the URL below.
param(
  [Parameter(Mandatory=$true)]
  [string]$AnonRemote   # e.g. https://github.com/icnlsp2026-nlu/ru-tt-nlu-resources.git
)

$git = "c:\Users\aleks\diploma\repo_github\_tools\git\cmd\git.exe"
Set-Location "c:\Users\aleks\diploma\anonymous_nlu_release"

& $git add -A
& $git commit -m "Anonymous release: Russian and Tatar NLU corpora (ICNLSP 2026)" 2>$null
& $git branch -M main
& $git remote remove origin 2>$null
& $git remote add origin $AnonRemote
& $git push -u origin main
