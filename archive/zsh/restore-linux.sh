#!/usr/bin/env bash
# Restore zsh dotfiles from archive/zsh/macos/ on Linux (or macOS refresh).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="$ROOT/macos"
ZSH_CUSTOM="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"

echo "==> Source: $SRC"

if [[ ! -f "$SRC/.zshrc" ]]; then
  echo "Missing $SRC/.zshrc — run from repo with archive present." >&2
  exit 1
fi

# Oh My Zsh
if [[ ! -d "$HOME/.oh-my-zsh" ]]; then
  echo "==> Installing Oh My Zsh..."
  RUNZSH=no CHSH=no sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
fi

# Powerlevel10k theme (OMZ custom themes)
if [[ ! -d "$ZSH_CUSTOM/themes/powerlevel10k" ]]; then
  echo "==> Cloning Powerlevel10k..."
  git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "$ZSH_CUSTOM/themes/powerlevel10k"
fi

# Plugins
clone_plugin() {
  local name="$1" url="$2"
  if [[ ! -d "$ZSH_CUSTOM/plugins/$name" ]]; then
    echo "==> Cloning $name..."
    git clone --depth=1 "$url" "$ZSH_CUSTOM/plugins/$name"
  fi
}
clone_plugin zsh-autosuggestions https://github.com/zsh-users/zsh-autosuggestions
clone_plugin zsh-syntax-highlighting https://github.com/zsh-users/zsh-syntax-highlighting

# Dotfiles (backup existing)
stamp="$(date +%Y%m%d-%H%M%S)"
for f in .zshrc .zprofile .zshenv .p10k.zsh; do
  if [[ -f "$HOME/$f" ]]; then
    cp -a "$HOME/$f" "$HOME/${f}.bak.$stamp"
    echo "==> Backed up ~/$f"
  fi
  cp "$SRC/$f" "$HOME/$f"
  echo "==> Installed ~/$f"
done

# Dotfiles use optional brew detection (macOS + Linuxbrew); no sed patch needed.

# History (optional; skipped in GLUON_ZOMBIE_BOOTSTRAP unless GLUON_ZOMBIE_ZSH_HISTORY=1)
if [[ -f "$SRC/zsh_history" ]]; then
  do_history=0
  if [[ "${GLUON_ZOMBIE_ZSH_HISTORY:-0}" == "1" ]]; then
    do_history=1
  elif [[ "${GLUON_ZOMBIE_BOOTSTRAP:-0}" != "1" ]]; then
    read -r -p "Merge zsh_history from archive? [y/N] " ans
    if [[ "${ans,,}" == "y" ]]; then
      do_history=1
    fi
  fi
  if [[ "$do_history" -eq 1 ]]; then
    if [[ -f "$HOME/.zsh_history" ]]; then
      cp -a "$HOME/.zsh_history" "$HOME/.zsh_history.bak.$stamp"
      cat "$SRC/zsh_history" "$HOME/.zsh_history" | sort -u > "$HOME/.zsh_history.merged"
      mv "$HOME/.zsh_history.merged" "$HOME/.zsh_history"
    else
      cp "$SRC/zsh_history" "$HOME/.zsh_history"
    fi
    echo "==> History installed/merged"
  fi
fi

echo "==> Done. Open a new terminal or: exec zsh"
