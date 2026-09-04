# codex-index-aleppo: redirect-host notes

This repository is only a GitHub Pages redirect host. MAM-basics holds the Aleppo
Codex data, readers, procedures, and published pages as of 2026-09-04. Do not
restore removed data or Python here, and do not add published content here.

MAM-basics' frozen manifest
`in/codex_index_aleppo_redirect_pages.json` declares the former URLs. From
`C:/Users/BenDe/GitRepos/MAM-basics`, regenerate the committed source stubs with:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_redirect_stubs.py build --repo codex-index-aleppo --publish
```

Then verify the source tree with:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_redirect_stubs.py check --repo codex-index-aleppo
```

The generator writes stubs and `404.html` but deletes nothing. A redirect-host
update must first change MAM-basics' manifest and target pages, then regenerate and
commit this repository's stubs.
