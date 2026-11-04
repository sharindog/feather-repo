# Sharindog Feather Repo

Public AltStore-compatible source for Feather.

Source URL (after GitHub Pages is enabled):

`https://sharindog.github.io/feather-repo/apps.json`

## Setup

1. Create a **public** GitHub repository named `feather-repo` under `sharindog` (without initializing it).
2. Extract this package and run:

```bash
cd feather-repo
git init -b main
git add .
git commit -m "Initialize Feather source"
git remote add origin https://github.com/sharindog/feather-repo.git
git push -u origin main
```

3. In repository Settings → Pages, select **Deploy from a branch**, branch `main`, folder `/ (root)`, and Save.
4. In Settings → Actions → General → Workflow permissions, enable **Read and write permissions** (if available). Alternatively ensure the workflow's `contents: write` is permitted by organization policy.
5. Create a new GitHub Release (not just a tag), attach one or more `.ipa` files and publish. The `Import IPA from release` workflow updates `apps.json` and icons. Use a **unique release tag** for every import.
6. In Feather → Sources, add the Source URL above. Import your certificate/profile in Feather separately.

GitHub Releases asset size limits apply. Do not upload pirated apps or private signing certificates. This public repository exposes IPA files to everyone.

## Limitations

IPA icon extraction supports PNG icons inside the app; apps with only compiled `Assets.car` may receive the default icon. The script requires a standard `Payload/*.app/Info.plist`. IPA versions are indexed by `CFBundleShortVersionString`; uploading two builds with the same version replaces the previous entry. Release deletion is not automatically reflected in the catalog. The GitHub Actions job must have permission to push to `main` (branch protection may prevent it).
