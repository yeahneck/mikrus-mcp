# Pull Request: Add Cursor Rules Installer to Mikrus Wiki Repository

## Summary

This PR adds a Python script that automatically downloads the Mikrus wiki and creates Cursor IDE rule files (`.mdc` format) for easy integration into Cursor projects.

## What This Does

The script (`update_mikrus_rules.py`) allows Cursor IDE users to:
- Get all Mikrus wiki documentation as Cursor project rules with one command
- Auto-update rules when the wiki changes
- Work from any directory (auto-detects workspace)
- No dependencies (pure Python stdlib)

## Files Added

- `update_mikrus_rules.py` - Main installer script
- `INSTALL.md` - Installation and usage instructions

## Suggested Location in Repository

```
mikrus-dokumentacja/
├── content/          # Existing wiki content
├── tools/            # New directory for utility scripts
│   └── cursor-rules/
│       ├── update_mikrus_rules.py
│       └── README.md
└── ...
```

Or alternatively, add to root with clear naming:
```
mikrus-dokumentacja/
├── content/
├── install_cursor_rules.py  # Clear, descriptive name
└── ...
```

## Benefits for Mikrus Community

1. **Better Developer Experience** - Cursor users get instant access to all wiki docs
2. **Always Up-to-Date** - Rules auto-update when wiki changes
3. **Easy Discovery** - Can be linked from main wiki page
4. **Zero Maintenance** - Script is self-contained and works independently

## Usage Example

Users can install with one command:

```bash
curl -sSL https://raw.githubusercontent.com/Mrugalski-pl/mikrus-dokumentacja/dev/tools/cursor-rules/update_mikrus_rules.py | python3
```

Or download and run:

```bash
wget https://raw.githubusercontent.com/Mrugalski-pl/mikrus-dokumentacja/dev/tools/cursor-rules/update_mikrus_rules.py
python3 update_mikrus_rules.py
```

## Integration with Wiki

This could be mentioned in the main wiki page or in a dedicated section:

```markdown
## Cursor IDE Integration

Want all Mikrus documentation in your Cursor IDE? Install with one command:

```bash
curl -sSL https://raw.githubusercontent.com/Mrugalski-pl/mikrus-dokumentacja/dev/tools/cursor-rules/update_mikrus_rules.py | python3
```

This creates Cursor rule files (`.mdc`) in `.cursor/rules/` directory with all wiki content.
```

## Testing

The script has been tested to:
- ✅ Download from GitHub correctly
- ✅ Extract all 46 markdown files
- ✅ Create proper `.mdc` files with YAML frontmatter
- ✅ Auto-detect workspace from any directory
- ✅ Handle updates and caching
- ✅ Clean up temporary files

## Technical Details

- **Language**: Python 3.6+
- **Dependencies**: None (uses only standard library)
- **Size**: ~15KB script
- **Output**: ~110KB of `.mdc` files (47 files)
- **Update Check**: Uses GitHub API to compare commit hashes

## Future Enhancements (Optional)

- Add to Mikrus wiki main page as a featured tool
- Create a dedicated "Tools" section in wiki
- Add installation instructions to wiki FAQ
- Consider adding to NOOBS scripts collection

## Questions for Maintainers

1. Preferred location for the script in the repository?
2. Should this be mentioned in the main wiki page?
3. Any naming conventions to follow?
4. Should we add a "Tools" section to the wiki?

