# Mikrus Wiki → Cursor Rules - Installation Guide

One command to get all Mikrus wiki documentation into your Cursor IDE as project rules.

## Quick Install

### Option 1: Direct Download & Run (Recommended)

```bash
curl -sSL https://raw.githubusercontent.com/USER/REPO/main/update_mikrus_rules.py | python3
```

### Option 2: Download Then Run

```bash
# Download the script
curl -O https://raw.githubusercontent.com/USER/REPO/main/update_mikrus_rules.py

# Make it executable (optional)
chmod +x update_mikrus_rules.py

# Run it
python3 update_mikrus_rules.py
```

### Option 3: Clone Repository

```bash
git clone https://github.com/USER/mikrus-cursor-rules.git
cd mikrus-cursor-rules
python3 update_mikrus_rules.py
```

## Usage

```bash
# Check and update if needed (default)
python3 update_mikrus_rules.py

# Force update (ignore cache)
python3 update_mikrus_rules.py --force

# Show help
python3 update_mikrus_rules.py --help

# Show version
python3 update_mikrus_rules.py --version
```

## What It Does

1. **Auto-detects your workspace** - Works from any directory in your project
2. **Downloads latest wiki** - Gets content from GitHub (dev branch)
3. **Creates Cursor rules** - Generates `.mdc` files in `.cursor/rules/`
4. **Checks for updates** - Only downloads if content changed
5. **Cleans up** - Removes temporary files automatically

## Output

Creates 47 `.mdc` files in `.cursor/rules/` directory:
- 46 individual wiki pages (one file per page)
- 1 index file (`00_mikrus_wiki_index.mdc`)

## Requirements

- Python 3.6+ (uses only standard library)
- Internet connection (to download from GitHub)
- Write permissions in your workspace directory

## After Installation

1. **Restart Cursor IDE** to see the rules
2. Check **"Project Rules"** in Cursor settings
3. All Mikrus wiki documentation is now available to Cursor's AI

## Updating

The script automatically checks for updates. Just run it again:

```bash
python3 update_mikrus_rules.py
```

It will only download if the wiki has been updated since your last run.

## Troubleshooting

### "Operation not permitted" error
- On macOS, you may need to grant Terminal/IDE full disk access
- Or run with: `python3 update_mikrus_rules.py` from your workspace root

### Rules not showing in Cursor
- Restart Cursor IDE after running the script
- Check that `.cursor/rules/` directory exists in your workspace root
- Verify files were created: `ls -la .cursor/rules/*.mdc`

### Network/SSL errors
- The script handles SSL issues automatically
- If problems persist, check your internet connection
- Try running with `--force` flag

## Source

- **Wiki**: https://wiki.mikr.us
- **Repository**: https://github.com/Mrugalski-pl/mikrus-dokumentacja
- **Branch**: `dev`

## License

This script is provided as-is for the Mikrus community.

