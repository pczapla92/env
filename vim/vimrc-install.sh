#!/bin/bash
# Determine the directory in which this script resides.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Verify that the vimrc exists in the script directory.
if [ ! -f "$SCRIPT_DIR/vimrc" ]; then
  echo "Error: vimrc not found in $SCRIPT_DIR. Aborting installation."
  exit 1
fi

# Backup existing ~/.vimrc if it exists.
if [ -e "$HOME/.vimrc" ]; then
  echo "Backing up existing ~/.vimrc to ~/.vimrc.bak"
  mv "$HOME/.vimrc" "$HOME/.vimrc.bak"
fi

# Create a symlink from the repository's vimrc to ~/.vimrc.
ln -sf "$SCRIPT_DIR/vimrc" "$HOME/.vimrc"
echo "Symlink created: $HOME/.vimrc now points to $SCRIPT_DIR/vimrc"
