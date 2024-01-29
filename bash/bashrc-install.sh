#!/bin/bash
# Determine the directory in which this script resides.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Determine the correct shell configuration file.
if [ -n "$ZSH_VERSION" ]; then
  SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
  SHELL_RC="$HOME/.bashrc"
else
  SHELL_RC="$HOME/.bashrc"  # Default to bash
fi

# Define the line to append
CUSTOM_BASHRC_SNIPPET="\nif [ -f $SCRIPT_DIR/bashrc ]; then\n    source $SCRIPT_DIR/bashrc\nfi\n"

# Check if the snippet is already present
if grep -Fxq "if [ -f $SCRIPT_DIR/bashrc ]; then" "$SHELL_RC"; then
  echo "Custom bashrc sourcing already exists in $SHELL_RC. Skipping."
else
  # Backup existing shell config
  echo "Backing up existing $SHELL_RC to ${SHELL_RC}.bak"
  cp "$SHELL_RC" "${SHELL_RC}.bak"

  # Append the sourcing command
  echo -e "$CUSTOM_BASHRC_SNIPPET" >> "$SHELL_RC"
  echo "Added bashrc sourcing to $SHELL_RC."
fi

# Reload shell configuration
echo "Reloading $SHELL_RC..."
source "$SHELL_RC"
echo "Done!"

