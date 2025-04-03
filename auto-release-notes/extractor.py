#!/usr/bin/env python3
import os
import subprocess
import sys

def get_changed_files(last_release_tag, current_commit):
    """Return a list of files changed between last_release_tag and current_commit."""
    result = subprocess.run(
        ['git', 'diff', '--name-only', last_release_tag, current_commit],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip().splitlines()

def get_file_content(commit, file_path):
    """Return file content for a given commit and file path. Return None if file does not exist."""
    try:
        result = subprocess.run(
            ['git', 'show', f'{commit}:{file_path}'],
            capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return None

def sanitize_filename(file_path):
    """Sanitize the file path to create a safe directory name."""
    return file_path.replace('/', '_').replace(' ', '_')

def main():
    # Check for environment variables; allow command line override.
    last_release_tag = os.environ.get("LAST_RELEASE_TAG")
    current_commit = os.environ.get("GITHUB_SHA")
    
    if len(sys.argv) > 1:
        last_release_tag = sys.argv[1]
    if len(sys.argv) > 2:
        current_commit = sys.argv[2]

    if not last_release_tag or not current_commit:
        print("Error: LAST_RELEASE_TAG and GITHUB_SHA must be set (or provided as arguments).", file=sys.stderr)
        sys.exit(1)

    os.makedirs("changes", exist_ok=True)
    
    try:
        changed_files = get_changed_files(last_release_tag, current_commit)
    except subprocess.CalledProcessError as e:
        print("Error running git diff:", e, file=sys.stderr)
        sys.exit(1)
    
    if not changed_files:
        print(f"No changes detected between {last_release_tag} and {current_commit}.")
        sys.exit(0)

    for file_path in changed_files:
        safe_name = sanitize_filename(file_path)
        change_dir = os.path.join("changes", safe_name)
        os.makedirs(change_dir, exist_ok=True)

        # Get "before" content from the last release
        before_content = get_file_content(last_release_tag, file_path)
        before_file = os.path.join(change_dir, "before")
        with open(before_file, "w") as bf:
            if before_content is not None:
                bf.write(before_content)
            else:
                bf.write("File not present in last release")

        # Get "after" content from the current commit
        after_content = get_file_content(current_commit, file_path)
        after_file = os.path.join(change_dir, "after")
        with open(after_file, "w") as af:
            if after_content is not None:
                af.write(after_content)
            else:
                af.write("File not present in current commit")
                
    print(f"Extracted changes for {len(changed_files)} file(s) into the 'changes' directory.")

if __name__ == "__main__":
    main()
