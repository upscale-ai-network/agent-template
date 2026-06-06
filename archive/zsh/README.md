# Zsh config archive (macOS → Linux restore)

**Captured from:** Lepton macOS · **User:** `dtundlam`  
**Stack:** Oh My Zsh · Powerlevel10k · zsh-autosuggestions · zsh-syntax-highlighting · **optional** Homebrew (macOS `/opt/homebrew` · Linuxbrew — skipped if absent)

## Contents (`macos/`)

| File | Install as |
|------|------------|
| `.zshrc` | `~/.zshrc` |
| `.zprofile` | `~/.zprofile` |
| `.zshenv` | `~/.zshenv` |
| `.p10k.zsh` | `~/.p10k.zsh` |
| `zsh_history` | `~/.zsh_history` (optional — **may contain secrets**; review before commit/push) |

**Not in repo (install on target):** `~/.oh-my-zsh` · OMZ custom plugins · Powerlevel10k theme files (via brew or git).

## Quick restore (Linux)

```bash
# From repo root after clone
./archive/zsh/restore-linux.sh
```

Manual steps in script: install OMZ + plugins + p10k, copy dotfiles, fix brew path, merge history.

## macOS refresh (re-capture)

```bash
cp ~/.zshrc ~/.zprofile ~/.zshenv ~/.p10k.zsh archive/zsh/macos/
cp ~/.zsh_history archive/zsh/macos/zsh_history
# Review history for tokens before git commit
```

## Security

- **`zsh_history`** can hold passwords, tokens, paths. Scrub or omit before pushing to shared remote.
- **`.zshenv`** uses `$HOME/.local/bin` (uv) — safe to port.

## Related

Oh My Zsh custom plugins on Mac live under `~/.oh-my-zsh/custom/plugins/` — restored by `restore-linux.sh` via git clone (not vendored here).
