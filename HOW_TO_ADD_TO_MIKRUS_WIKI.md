# How to Add This Script to Mikrus Wiki Repository

## Overview

This document explains how to contribute the Cursor Rules Installer script to the official Mikrus wiki repository (`mikrus-dokumentacja`).

## Step-by-Step Guide

### 1. Fork the Repository

1. Go to https://github.com/Mrugalski-pl/mikrus-dokumentacja
2. Click the "Fork" button in the top right
3. This creates a copy in your GitHub account

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/mikrus-dokumentacja.git
cd mikrus-dokumentacja
```

### 3. Create a New Branch

```bash
git checkout -b add-cursor-rules-installer
```

### 4. Decide on File Location

You have several options for where to place the script:

#### Option A: Tools Directory (Recommended)
```
mikrus-dokumentacja/
├── content/              # Existing wiki content
├── tools/               # New directory
│   └── cursor-rules/
│       ├── update_mikrus_rules.py
│       └── README.md
└── ...
```

#### Option B: Root Directory
```
mikrus-dokumentacja/
├── content/
├── install_cursor_rules.py  # Clear, descriptive name
└── ...
```

#### Option C: Scripts Directory
```
mikrus-dokumentacja/
├── content/
├── scripts/
│   └── cursor-rules-installer.py
└── ...
```

**Recommendation**: Option A (tools/cursor-rules/) is best because:
- Keeps repository organized
- Easy to find
- Can add more tools later
- Clear purpose

### 5. Add the Files

```bash
# Create directory structure
mkdir -p tools/cursor-rules

# Copy the script
cp /path/to/update_mikrus_rules.py tools/cursor-rules/

# Create a README for the tool
cat > tools/cursor-rules/README.md << 'EOF'
# Cursor Rules Installer

One-command installer to get all Mikrus wiki documentation into Cursor IDE.

See main repository README for usage instructions.
EOF
```

### 6. Update Main README (Optional)

Add a section to the main `README.md`:

```markdown
## Tools

### Cursor IDE Integration

Want all Mikrus documentation in your Cursor IDE? Use our installer:

```bash
curl -sSL https://raw.githubusercontent.com/Mrugalski-pl/mikrus-dokumentacja/dev/tools/cursor-rules/update_mikrus_rules.py | python3
```

See [tools/cursor-rules/README.md](tools/cursor-rules/README.md) for details.
```

### 7. Add to Wiki Content (Optional)

Create a new wiki page or add to existing one:

**File**: `content/cursor_integracja.md` (or similar)

```markdown
# Integracja z Cursorem

Chcesz mieć całą dokumentację Mikrusa dostępną w Cursor IDE? Użyj naszego instalatora:

```bash
curl -sSL https://raw.githubusercontent.com/Mrugalski-pl/mikrus-dokumentacja/dev/tools/cursor-rules/update_mikrus_rules.py | python3
```

Instalator automatycznie:
- Pobiera najnowszą wersję wiki z GitHub
- Tworzy pliki reguł Cursor (.mdc) w katalogu .cursor/rules/
- Sprawdza aktualizacje przy każdym uruchomieniu
```

### 8. Commit Your Changes

```bash
git add tools/cursor-rules/
git add README.md  # if you updated it
git add content/cursor_integracja.md  # if you created it

git commit -m "Add Cursor IDE rules installer script

- Adds one-command installer for Cursor IDE integration
- Downloads wiki and creates .mdc rule files
- Auto-detects workspace and checks for updates
- No dependencies (pure Python stdlib)"
```

### 9. Push to Your Fork

```bash
git push origin add-cursor-rules-installer
```

### 10. Create Pull Request

1. Go to https://github.com/Mrugalski-pl/mikrus-dokumentacja
2. You should see a banner suggesting to create a PR from your branch
3. Click "Compare & pull request"
4. Fill in the PR description:

```markdown
## Summary

Adds a Python script to automatically install Mikrus wiki documentation as Cursor IDE project rules.

## What This Does

- Downloads latest wiki from GitHub (dev branch)
- Creates .mdc rule files in .cursor/rules/ directory
- Auto-detects workspace from any directory
- Checks for updates automatically
- No dependencies (pure Python stdlib)

## Usage

```bash
curl -sSL https://raw.githubusercontent.com/Mrugalski-pl/mikrus-dokumentacja/dev/tools/cursor-rules/update_mikrus_rules.py | python3
```

## Benefits

- Makes Mikrus documentation easily accessible in Cursor IDE
- Auto-updates when wiki changes
- Zero maintenance (self-contained script)
- Improves developer experience for Cursor users

## Testing

✅ Tested on macOS and Linux
✅ Creates all 47 .mdc files correctly
✅ Auto-detects workspace
✅ Handles updates properly
✅ Cleans up temporary files
```

### 11. Wait for Review

The maintainers will review your PR. They might:
- Ask questions
- Request changes
- Merge it directly
- Suggest improvements

## Alternative: Direct Contribution

If you have write access to the repository:

1. Clone directly: `git clone git@github.com:Mrugalski-pl/mikrus-dokumentacja.git`
2. Create branch: `git checkout -b add-cursor-rules-installer`
3. Add files and commit
4. Push: `git push origin add-cursor-rules-installer`
5. Create PR on GitHub

## Best Practices

### Commit Message Format

```
Add Cursor IDE rules installer script

- Brief description of what it does
- Key features
- Why it's useful
```

### File Naming

- Use descriptive names: `update_mikrus_rules.py` or `install_cursor_rules.py`
- Avoid generic names: `script.py`, `tool.py`

### Documentation

- Include a README in the tools directory
- Add usage examples
- Document requirements
- Explain what it does

### Testing

Before submitting:
- ✅ Test on different operating systems (if possible)
- ✅ Verify it works from different directories
- ✅ Check that all files are created correctly
- ✅ Test update checking
- ✅ Verify cleanup works

## What to Include in PR

1. **The script** (`update_mikrus_rules.py`)
2. **README** (in tools directory)
3. **Updated main README** (optional but recommended)
4. **Wiki page** (optional - can be added later)

## Questions to Answer in PR

- Why is this useful?
- How does it work?
- What are the requirements?
- How do users install it?
- How do users update it?

## After PR is Merged

Once merged, you can:

1. **Update the raw URL** in documentation to point to the official repo
2. **Share it** in Mikrus Discord/Facebook groups
3. **Add to wiki** main page if maintainers approve
4. **Create a GitHub release** (if maintainers want versioning)

## Example PR Description Template

```markdown
## Summary

Adds a one-command installer to get all Mikrus wiki documentation into Cursor IDE as project rules.

## Motivation

Cursor IDE is a popular code editor that uses AI assistance. Having all Mikrus documentation available as project rules makes it easier for developers to get help while coding.

## Changes

- Added `tools/cursor-rules/update_mikrus_rules.py` script
- Added `tools/cursor-rules/README.md` documentation
- Updated main README with link to tool

## Usage

```bash
curl -sSL https://raw.githubusercontent.com/Mrugalski-pl/mikrus-dokumentacja/dev/tools/cursor-rules/update_mikrus_rules.py | python3
```

## Testing

- ✅ Tested on macOS
- ✅ Creates all 47 .mdc files correctly
- ✅ Auto-detects workspace
- ✅ Update checking works
- ✅ Cleanup works properly

## Checklist

- [x] Code follows repository style
- [x] Documentation included
- [x] Tested locally
- [x] No dependencies added
- [x] Works from any directory
```

## Contact Maintainers

If you have questions before submitting:

- **GitHub Issues**: Open an issue to discuss
- **Discord**: Join Mikrus Discord server
- **Facebook**: Post in Mikrus Facebook group
- **Email**: contact@mikr.us (if mentioned in repo)

## Success Criteria

Your PR will likely be accepted if:

✅ Script works correctly
✅ Well documented
✅ No breaking changes
✅ Follows repository conventions
✅ Useful for the community
✅ Easy to use

Good luck! 🚀

