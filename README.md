# Mikrus Wiki → Cursor Rules Installer

**One command to get all Mikrus wiki documentation into your Cursor IDE as project rules.**

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![No Dependencies](https://img.shields.io/badge/dependencies-none-green.svg)](https://github.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

```bash
# Download and run in one command
curl -sSL https://raw.githubusercontent.com/yeahneck/mikrus-auto-cursor-rules/main/update_mikrus_rules.py | python3
```

Or clone and run:

```bash
git clone https://github.com/yeahneck/mikrus-auto-cursor-rules.git
cd mikrus-auto-cursor-rules
python3 update_mikrus_rules.py
```

## ✨ Features

- ✅ **One Command Install** - Get all 46+ wiki pages as Cursor rules instantly
- ✅ **Auto-Detects Workspace** - Works from any directory in your project
- ✅ **Smart Updates** - Only downloads when wiki content changes
- ✅ **Zero Dependencies** - Pure Python standard library
- ✅ **Auto-Cleanup** - Removes temporary files automatically
- ✅ **Cursor Native** - Creates proper `.mdc` files with YAML frontmatter

## 📖 What It Does

1. Downloads the latest Mikrus wiki from GitHub (`dev` branch)
2. Extracts all Markdown files from the `content/` directory
3. Creates individual `.mdc` rule files in `.cursor/rules/` (one per wiki page)
4. Adds YAML frontmatter with descriptions for Cursor IDE
5. Creates an index file for easy navigation

## 📁 Output

Creates **47 files** in `.cursor/rules/` directory:
- 46+ individual wiki pages (e.g., `Apache_PHP_MySQL.mdc`, `nginx_publikacja_prostej_strony.mdc`)
- 1 index file (`00_mikrus_wiki_index.mdc`)

Total size: ~110 KB

## 🎯 Usage

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

## 🔧 Requirements

- **Python 3.6+** (uses only standard library - no pip install needed)
- **Internet connection** (to download from GitHub)
- **Write permissions** in your workspace directory

## 📝 After Installation

1. **Restart Cursor IDE** to refresh rules
2. Check **"Project Rules"** in Cursor settings
3. All Mikrus wiki documentation is now available to Cursor's AI assistant!

## 🔄 Updating

The script automatically checks for updates by comparing commit hashes. Just run it again:

```bash
python3 update_mikrus_rules.py
```

It will only download if the wiki has been updated since your last run.

## 🛠️ How It Works

### Workspace Detection

The script automatically finds your workspace root by looking for:
- `.cursor/` directory
- `.git/` directory
- Common project files (`package.json`, `requirements.txt`, `Cargo.toml`, etc.)

If none found, it uses the current directory.

### Update Checking

- Compares latest commit hash from GitHub API
- Stores last update info in `.mikrus_rules_update.json`
- Only downloads if commit hash changed (or `--force` used)

### File Structure

```
your-project/
├── .cursor/
│   └── rules/
│       ├── 00_mikrus_wiki_index.mdc
│       ├── Apache_PHP_MySQL.mdc
│       ├── nginx_publikacja_prostej_strony.mdc
│       └── ... (44+ more files)
└── .mikrus_rules_update.json
```

## 🐛 Troubleshooting

### Rules not showing in Cursor

1. **Restart Cursor IDE** after running the script
2. Check that `.cursor/rules/` exists: `ls -la .cursor/rules/`
3. Verify files were created: `ls -la .cursor/rules/*.mdc | wc -l` (should show 47)

### "Operation not permitted" error

- On macOS, grant Terminal/IDE full disk access in System Preferences
- Or run from your workspace root directory

### Network/SSL errors

- The script handles SSL issues automatically
- If problems persist, check your internet connection
- Try running with `--force` flag

## 📚 Source

- **Wiki**: https://wiki.mikr.us
- **Repository**: https://github.com/Mrugalski-pl/mikrus-dokumentacja
- **Branch**: `dev`

## 🤝 Contributing

Found a bug or have a suggestion? Open an issue or submit a PR!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

- **Mikrus Wiki** - https://wiki.mikr.us
- **Mikrus Documentation Repository** - https://github.com/Mrugalski-pl/mikrus-dokumentacja
- **Cursor IDE** - https://cursor.sh

---

**Made for the Mikrus community** 🚀

