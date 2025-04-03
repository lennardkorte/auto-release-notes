import subprocess
from pathlib import Path
from auto_release_notes import generate_context_string, extract_diff

def get_latest_release_tag():
    """Find the latest non-beta release tag like v1.2.0"""
    result = subprocess.run(
        ['git', 'tag', '--list', 'v[0-9]*', '--sort=-v:refname'],
        capture_output=True, text=True, check=True
    )
    tags = [tag for tag in result.stdout.strip().splitlines() if 'beta' not in tag.lower()]
    return tags[0] if tags else None

def get_current_commit():
    """Get current commit SHA"""
    result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True)
    return result.stdout.strip()

def main():
    last_tag = get_latest_release_tag()
    current_commit = get_current_commit()

    if not last_tag:
        print("No release tag found (e.g. v1.2.0). Please create one first.")
        return

    print(f"\n🟡 Comparing changes from tag `{last_tag}` to commit `{current_commit}`...\n")

    # Optional: Also write files to disk
    extract_diff(last_tag, current_commit)

    # Generate and print the context string for LLM
    context = generate_context_string(last_tag, current_commit)
    print("\n🧠 Generated LLM Context:\n")
    print(context)

if __name__ == "__main__":
    main()
