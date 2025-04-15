# Slippard Keystore Access Extension for Ulauncher

Slippard is [here](https://github.com/coljac/slippard): https://github.com/coljac/slippard

A Ulauncher extension that allows you to quickly access and copy values from your keystore to the clipboard.

## Features

- Lists all keys from your keystore
- Allows filtering keys by typing
- Copies the selected key's value to the clipboard

## Usage

1. Open Ulauncher
2. Type `key` (the default keyword)
3. Optionally type a search term to filter keys
4. Select a key from the list to copy its value to the clipboard

## Requirements

- Ulauncher
- `slpd` command-line tool installed and accessible in your PATH

## Commands Used

- `slpd list` - Lists all keys in the keystore
- `slpd get <key>` - Retrieves the value for a specific key

## Installation

1. Open Ulauncher preferences
2. Go to "Extensions" tab
3. Click "Add extension"
4. Paste the URL of this repository
5. Click "Add"
