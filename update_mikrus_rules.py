#!/usr/bin/env python3
"""
Mikrus Wiki → Cursor Rules Installer

Extract Mikrus wiki content from GitHub and create Cursor .mdc rule files.
Only keeps the .mdc files, not the full repository.

Usage:
    python3 update_mikrus_rules.py          # Check and update if needed
    python3 update_mikrus_rules.py --force  # Force update
    python3 update_mikrus_rules.py --help   # Show help
    python3 update_mikrus_rules.py --version # Show version

Version: 1.0.0
"""
import os
import subprocess
import tempfile
import shutil
from pathlib import Path
import re
import json
from datetime import datetime
import urllib.request
import zipfile
import sys

VERSION = "1.0.0"
REPO_URL = "https://github.com/Mrugalski-pl/mikrus-dokumentacja.git"
UPDATE_CHECK_FILE = ".mikrus_rules_update.json"

def find_workspace_root():
    """Find workspace root by looking for .git, .cursor, or common project files"""
    current = os.path.abspath(os.getcwd())
    original = current
    
    # Check current directory first
    if os.path.exists(os.path.join(current, '.cursor')):
        return current
    
    # Walk up the directory tree
    while current != os.path.dirname(current):
        # Check for common workspace markers
        markers = ['.git', '.cursor', 'package.json', 'requirements.txt', 
                   'Cargo.toml', 'go.mod', 'pom.xml', 'build.gradle']
        if any(os.path.exists(os.path.join(current, marker)) for marker in markers):
            return current
        current = os.path.dirname(current)
    
    # Fallback: use current directory
    return original

def get_cursor_rules_dir(workspace_root):
    """Get the Cursor rules directory path"""
    return os.path.join(workspace_root, ".cursor", "rules")

def get_latest_commit_hash(repo_url):
    """Get the latest commit hash from GitHub API"""
    try:
        import ssl
        # Convert GitHub URL to API URL
        # https://github.com/user/repo -> https://api.github.com/repos/user/repo/commits/dev
        repo_url_clean = repo_url.rstrip("/").rstrip(".git")
        api_url = repo_url_clean.replace("https://github.com/", "https://api.github.com/repos/")
        api_url = f"{api_url}/commits/dev"
        
        req = urllib.request.Request(api_url)
        req.add_header('Accept', 'application/vnd.github.v3+json')
        
        # Create SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get('sha')
    except Exception:
        # Silently fail - update check is optional
        return None

def get_last_update_info(workspace_root):
    """Get last update information from local file"""
    update_file = os.path.join(workspace_root, UPDATE_CHECK_FILE)
    if os.path.exists(update_file):
        try:
            with open(update_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return None

def save_update_info(workspace_root, commit_hash, timestamp):
    """Save update information to local file"""
    update_file = os.path.join(workspace_root, UPDATE_CHECK_FILE)
    info = {
        'last_commit': commit_hash,
        'last_update': timestamp,
        'repo_url': REPO_URL
    }
    with open(update_file, 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=2)

def download_repo_zip():
    """Download repository as ZIP archive to temporary directory"""
    # Use workspace directory for temp to avoid sandbox issues
    workspace_dir = os.getcwd()
    temp_dir = os.path.join(workspace_dir, ".mikrus_temp")
    
    # Clean up if exists
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    os.makedirs(temp_dir, exist_ok=True)
    zip_path = os.path.join(temp_dir, "repo.zip")
    repo_dir = os.path.join(temp_dir, "mikrus-dokumentacja")
    
    # Download ZIP from GitHub (remove .git if present)
    repo_url_clean = REPO_URL.rstrip("/").rstrip(".git")
    zip_url = f"{repo_url_clean}/archive/refs/heads/dev.zip"
    print(f"📥 Downloading repository as ZIP archive...")
    print(f"   URL: {zip_url}")
    
    try:
        # Create SSL context that doesn't verify certificates (for sandbox environments)
        import ssl
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(zip_url)
        with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
            with open(zip_path, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
        print("✅ Download complete")
        
        # Extract ZIP
        print("📦 Extracting archive...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find the extracted directory (GitHub adds branch name to directory)
        extracted_dirs = [d for d in os.listdir(temp_dir) 
                         if os.path.isdir(os.path.join(temp_dir, d)) and d != "mikrus-dokumentacja"]
        if extracted_dirs:
            extracted_path = os.path.join(temp_dir, extracted_dirs[0])
            # Rename to expected name
            if os.path.exists(repo_dir):
                shutil.rmtree(repo_dir)
            os.rename(extracted_path, repo_dir)
        
        # Clean up ZIP file
        os.remove(zip_path)
        print("✅ Repository extracted successfully")
        return repo_dir
        
    except Exception as e:
        print(f"❌ Error downloading repository:")
        print(f"   {e}")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
        raise

def get_all_markdown_files(content_dir):
    """Get all markdown files from content directory"""
    md_files = []
    content_path = Path(content_dir)
    
    if not content_path.exists():
        raise FileNotFoundError(f"Content directory not found: {content_dir}")
    
    # Find all .md files recursively
    for md_file in content_path.rglob("*.md"):
        # Skip files starting with underscore (Hugo partials)
        if md_file.name.startswith('_'):
            continue
        md_files.append(md_file)
    
    return sorted(md_files)

def read_markdown_file(file_path, content_base):
    """Read and clean markdown file content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get relative path for reference
        rel_path = file_path.relative_to(Path(content_base))
        
        # Extract title from frontmatter if present
        title = None
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', frontmatter, re.MULTILINE)
            if title_match:
                title = title_match.group(1)
            # Remove frontmatter from content
            content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
        
        # Use filename as title if no title found
        if not title:
            title = file_path.stem.replace('_', ' ').replace('-', ' ').title()
        
        return {
            'path': str(rel_path),
            'title': title,
            'content': content.strip()
        }
    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}")
        return None

def clean_markdown_for_rules(content):
    """Clean markdown content to be suitable for Cursor rules"""
    # First, protect code blocks from being modified
    code_blocks = []
    code_block_pattern = r'```[\s\S]*?```'
    
    def replace_code_block(match):
        code_blocks.append(match.group(0))
        return f'__CODE_BLOCK_{len(code_blocks)-1}__'
    
    # Temporarily replace code blocks
    content = re.sub(code_block_pattern, replace_code_block, content)
    
    # Remove markdown links but keep the text
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
    
    # Remove image markdown
    content = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', content)
    
    # Convert headers to plain text (keep the text, remove #)
    content = re.sub(r'^#{1,6}\s+(.+)$', r'\1', content, flags=re.MULTILINE)
    
    # Remove markdown emphasis but keep text
    content = re.sub(r'\*\*([^\*]+)\*\*', r'\1', content)
    content = re.sub(r'\*([^\*]+)\*', r'\1', content)
    content = re.sub(r'__([^_]+)__', r'\1', content)
    content = re.sub(r'_([^_]+)_', r'\1', content)
    
    # Remove backticks from inline code but keep the code
    content = re.sub(r'`([^`]+)`', r'\1', content)
    
    # Remove horizontal rules
    content = re.sub(r'^---+$', '', content, flags=re.MULTILINE)
    
    # Remove "Powrót do strony głównej" links
    content = re.sub(r'\[Powrót do strony głównej\]\([^\)]+\)', '', content)
    
    # Restore code blocks (in reverse order to avoid conflicts)
    for i in range(len(code_blocks) - 1, -1, -1):
        placeholder = f'__CODE_BLOCK_{i}__'
        # Try both with and without underscores
        if placeholder in content:
            content = content.replace(placeholder, code_blocks[i])
        elif f'_CODEBLOCK{i}' in content:
            content = content.replace(f'_CODEBLOCK{i}', code_blocks[i])
        elif f'CODEBLOCK{i}' in content:
            content = content.replace(f'CODEBLOCK{i}', code_blocks[i])
    
    # Normalize whitespace (but preserve code blocks)
    # Split by code blocks, normalize each part, then rejoin
    parts = re.split(r'(```[\s\S]*?```)', content)
    normalized_parts = []
    for part in parts:
        if part.startswith('```'):
            normalized_parts.append(part)  # Keep code blocks as-is
        else:
            # Normalize whitespace in non-code parts
            part = re.sub(r'\n{3,}', '\n\n', part)
            normalized_parts.append(part)
    content = ''.join(normalized_parts)
    
    return content.strip()

def sanitize_filename(filename):
    """Convert filename to safe format for .mdc files"""
    # Remove extension and path separators
    name = os.path.splitext(os.path.basename(filename))[0]
    # Replace invalid characters
    name = re.sub(r'[^\w\-_\.]', '_', name)
    # Limit length
    if len(name) > 100:
        name = name[:100]
    return name

def create_mdc_file(file_data, rules_dir):
    """Create a single .mdc file for a wiki page"""
    if not file_data or not file_data.get('content'):
        return None
    
    path = file_data['path']
    title = file_data.get('title', path)
    content = file_data['content']
    
    # Clean the content for rules format
    content = clean_markdown_for_rules(content)
    
    if not content:
        return None
    
    # Create safe filename
    safe_name = sanitize_filename(path)
    mdc_filename = f"{safe_name}.mdc"
    mdc_path = os.path.join(rules_dir, mdc_filename)
    
    # Create description from first paragraph or title
    description = title
    first_para = content.split('\n\n')[0] if content else ""
    if first_para and len(first_para) < 200:
        description = first_para[:200]
    
    # Create YAML frontmatter
    frontmatter = f"""---
description: "{description.replace('"', "'")}"
source: "https://wiki.mikr.us"
file: "{path}"
---

"""
    
    # Combine frontmatter and content
    mdc_content = frontmatter + f"# {title}\n\n{content}\n"
    
    return mdc_path, mdc_content

def create_cursor_rules(md_files_data, workspace_root):
    """Create .mdc files in .cursor/rules/ directory"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor_rules_dir = get_cursor_rules_dir(workspace_root)
    
    # Create rules directory
    os.makedirs(cursor_rules_dir, exist_ok=True)
    
    created_files = []
    
    for file_data in md_files_data:
        result = create_mdc_file(file_data, cursor_rules_dir)
        if result:
            mdc_path, mdc_content = result
            with open(mdc_path, 'w', encoding='utf-8') as f:
                f.write(mdc_content)
            created_files.append(mdc_path)
    
    # Create a summary/index file
    index_content = f"""---
description: "Mikrus Wiki - Complete Documentation Index"
source: "https://wiki.mikr.us"
last_updated: "{timestamp}"
---

# Mikrus Wiki - Complete Documentation

This directory contains all documentation from https://wiki.mikr.us including all subpages.

**Source**: Official Mikrus Wiki GitHub Repository  
**Repository**: https://github.com/Mrugalski-pl/mikrus-dokumentacja  
**Website**: https://wiki.mikr.us  
**Last Updated**: {timestamp}

All content is extracted from the Markdown files in the repository's `/content` directory.

## Files Included

"""
    
    for file_data in md_files_data:
        if file_data and file_data.get('content'):
            path = file_data['path']
            title = file_data.get('title', path)
            safe_name = sanitize_filename(path)
            index_content += f"- **{title}** (`{safe_name}.mdc`)\n"
    
    index_path = os.path.join(cursor_rules_dir, "00_mikrus_wiki_index.mdc")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    created_files.append(index_path)
    
    return created_files

def show_help():
    """Display help information"""
    print(f"""
Mikrus Wiki → Cursor Rules Installer v{VERSION}

This script downloads the Mikrus wiki from GitHub and creates Cursor rule files
in .cursor/rules/ directory for use in Cursor IDE.

USAGE:
    python3 update_mikrus_rules.py          Check and update if needed
    python3 update_mikrus_rules.py --force Force update (ignore cache)
    python3 update_mikrus_rules.py --help  Show this help message
    python3 update_mikrus_rules.py --version Show version information

FEATURES:
    ✅ Downloads latest Mikrus wiki from GitHub
    ✅ Creates individual .mdc rule files (one per wiki page)
    ✅ Auto-checks for updates (compares commit hashes)
    ✅ Works from any directory (auto-detects workspace)
    ✅ Cleans up temporary files automatically
    ✅ No dependencies (pure Python standard library)

OUTPUT:
    Creates .cursor/rules/*.mdc files in your workspace root directory.

SOURCE:
    Wiki: https://wiki.mikr.us
    Repository: https://github.com/Mrugalski-pl/mikrus-dokumentacja
""")

def extract_and_create_rules(force_update=False):
    """Main function to extract content and create .cursorrules"""
    workspace_root = find_workspace_root()
    cursor_rules_dir = get_cursor_rules_dir(workspace_root)
    
    print("🚀 Mikrus Wiki Rules Updater\n")
    print(f"📁 Workspace: {workspace_root}")
    print(f"📁 Rules directory: {cursor_rules_dir}\n")
    
    # Check for updates
    if not force_update:
        last_info = get_last_update_info(workspace_root)
        latest_commit = get_latest_commit_hash(REPO_URL)
        
        if last_info and latest_commit:
            if last_info.get('last_commit') == latest_commit:
                print(f"✅ Rules are up to date (commit: {latest_commit[:8]}...)")
                print(f"📅 Last updated: {last_info.get('last_update', 'unknown')}")
                return False
        
        if latest_commit:
            print(f"🔄 New updates available (commit: {latest_commit[:8]}...)")
    
    # Download repo to temp directory
    repo_dir = None
    try:
        repo_dir = download_repo_zip()
        content_dir = os.path.join(repo_dir, "content")
        
        # Get all markdown files
        print(f"\n📚 Scanning for Markdown files...")
        md_files = get_all_markdown_files(content_dir)
        print(f"✅ Found {len(md_files)} Markdown files")
        
        # Read all files
        print("\n📖 Reading all files...")
        md_files_data = []
        for md_file in md_files:
            data = read_markdown_file(md_file, content_dir)
            if data and data.get('content'):
                md_files_data.append(data)
                print(f"  ✓ {data['path']}")
        
        # Create .mdc files in .cursor/rules/
        print(f"\n📝 Creating .mdc files in {cursor_rules_dir}/ from {len(md_files_data)} files...")
        created_files = create_cursor_rules(md_files_data, workspace_root)
        
        # Save update info
        latest_commit = get_latest_commit_hash(REPO_URL)
        if latest_commit:
            save_update_info(workspace_root, latest_commit, datetime.now().isoformat())
        
        total_size = sum(os.path.getsize(f) for f in created_files if os.path.exists(f))
        print(f"\n✅ Complete!")
        print(f"📁 Rules directory: {cursor_rules_dir}/")
        print(f"📄 Files created: {len(created_files)}")
        print(f"📊 Total size: {total_size:,} bytes ({total_size/1024:.1f} KB)")
        print(f"📚 Wiki pages included: {len(md_files_data)}")
        print(f"\n💡 Tip: Restart Cursor IDE to see the rules in 'Project Rules'")
        
        return True
        
    finally:
        # Clean up temporary directory
        temp_dir = os.path.join(os.getcwd(), ".mikrus_temp")
        if os.path.exists(temp_dir):
            print(f"\n🧹 Cleaning up temporary files...")
            shutil.rmtree(temp_dir, ignore_errors=True)
            print("✅ Cleanup complete")

def main():
    """Main entry point"""
    import sys
    
    # Handle command line arguments
    if '--help' in sys.argv or '-h' in sys.argv:
        show_help()
        sys.exit(0)
    
    if '--version' in sys.argv or '-v' in sys.argv:
        print(f"Mikrus Wiki → Cursor Rules Installer v{VERSION}")
        sys.exit(0)
    
    force = '--force' in sys.argv or '-f' in sys.argv
    
    try:
        extract_and_create_rules(force_update=force)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

