import os
import subprocess

def get_changed_files(last_release_tag, current_commit):
    """Return a list of files changed between last_release_tag and current_commit."""
    result = subprocess.run(
        ['git', 'diff', '--name-only', last_release_tag, current_commit],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip().splitlines()

def get_file_content(commit, file_path):
    """Return file content for a given commit and file path. 
    Return None if the file does not exist at that commit."""
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

def extract_diff(last_release_tag, current_commit, output_dir="changes"):
    """
    Extract diffs between two Git references and write before/after contents to disk.
    (Original functionality)
    """
    os.makedirs(output_dir, exist_ok=True)

    changed_files = get_changed_files(last_release_tag, current_commit)
    if not changed_files:
        print(f"No changes detected between {last_release_tag} and {current_commit}.")
        return

    for file_path in changed_files:
        safe_name = sanitize_filename(file_path)
        change_dir = os.path.join(output_dir, safe_name)
        os.makedirs(change_dir, exist_ok=True)

        before_content = get_file_content(last_release_tag, file_path)
        before_file = os.path.join(change_dir, "before")
        with open(before_file, "w") as bf:
            bf.write(before_content if before_content is not None else "File not present in last release")

        after_content = get_file_content(current_commit, file_path)
        after_file = os.path.join(change_dir, "after")
        with open(after_file, "w") as af:
            af.write(after_content if after_content is not None else "File not present in current commit")

    print(f"Extracted changes for {len(changed_files)} file(s) into the '{output_dir}' directory.")

def generate_context_string(last_release_tag, current_commit):
    """
    Generate a single context string representing the before/after changes
    of every modified file. This is especially useful for feeding context into an LLM.
    """
    changed_files = get_changed_files(last_release_tag, current_commit)
    if not changed_files:
        return f"No changes detected between {last_release_tag} and {current_commit}."

    context_pieces = []
    for file_path in changed_files:
        # Grab "before" and "after" contents from the repo
        before_content = get_file_content(last_release_tag, file_path)
        after_content = get_file_content(current_commit, file_path)

        # Default text if file doesn’t exist in one commit or the other
        if before_content is None:
            before_content = "File not present in last release"
        if after_content is None:
            after_content = "File not present in current commit"

        # Construct the per-file context
        file_context = (
            f"=== File: {file_path} ===\n"
            f"--- BEFORE ---\n{before_content}\n"
            f"--- AFTER ----\n{after_content}\n"
            "====================\n"
        )
        context_pieces.append(file_context)

    # Join all file contexts into one big string
    return "\n".join(context_pieces)
