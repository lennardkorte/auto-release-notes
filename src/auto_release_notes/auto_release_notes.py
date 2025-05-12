#!/usr/bin/env python3

from importlib.resources import files
import os
import subprocess
from auto_release_notes.gen_notes import generate

def get_changed_files(last_release_tag, current_commit, path="."):
    """Return a list of files changed between last_release_tag and current_commit,
    excluding CHANGELOG.md, limited to the given path."""
    result = subprocess.run(
        ['git', 'diff', '--name-only', last_release_tag, current_commit, '--', path],
        capture_output=True, text=True, check=True
    )
    changed_files = result.stdout.strip().splitlines()
    # Exclude CHANGELOG.md
    return [f for f in changed_files if f != "CHANGELOG.md"]

def get_file_content(commit, file_path):
    """Return file content for a given commit and file path.
    Return None if the file does not exist at that commit or is binary."""
    try:
        result = subprocess.run(
            ['git', 'show', f'{commit}:{file_path}'],
            capture_output=True, check=True
        )
        # Try decoding safely
        try:
            return result.stdout.decode("utf-8")
        except UnicodeDecodeError:
            return "Binary file or non-UTF-8 encoding (content not shown)"
    except subprocess.CalledProcessError:
        return None

def sanitize_filename(file_path):
    """Sanitize the file path to create a safe directory name."""
    return file_path.replace('/', '_').replace(' ', '_')

def extract_diff(last_release_tag, current_commit, output_dir="changes", path="."):
    """
    Extract diffs between two Git references and write before/after contents to disk,
    but only for files under the given path.
    """
    os.makedirs(output_dir, exist_ok=True)

    changed_files = get_changed_files(last_release_tag, current_commit, path)
    if not changed_files:
        print(f"No changes detected between {last_release_tag} and {current_commit} in {path}.")
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

def generate_context_string(last_release_tag, current_commit, path="."):
    """
    Generate a single context string representing the before/after changes
    of every modified file under the given path. Useful for LLM context.
    """
    changed_files = get_changed_files(last_release_tag, current_commit, path)
    if not changed_files:
        return f"No changes detected between {last_release_tag} and {current_commit} in {path}."

    context_pieces = []
    for file_path in changed_files:
        before_content = get_file_content(last_release_tag, file_path)
        after_content = get_file_content(current_commit, file_path)

        if before_content is None:
            before_content = "File not present in last release"
        if after_content is None:
            after_content = "File not present in current commit"

        file_context = (
            f"=== File: {file_path} ===\n"
            f"--- BEFORE ---\n{before_content}\n"
            f"--- AFTER ----\n{after_content}\n"
            "====================\n"
        )
        context_pieces.append(file_context)

    return "\n".join(context_pieces)

def get_current_commit():
    """Get the current commit SHA."""
    result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True)
    return result.stdout.strip()

def get_latest_release_tag():
    """
    Returns the latest non-beta release tag that does not point to the current commit.
    """
    current_commit = get_current_commit()
    result = subprocess.run(
        ['git', 'tag', '--list', 'v[0-9]*', '--sort=-v:refname'],
        capture_output=True, text=True, check=True
    )
    tags = [tag for tag in result.stdout.strip().splitlines() if 'beta' not in tag.lower()]
    for tag in tags:
        tag_commit = subprocess.run(
            ['git', 'rev-list', '-n', '1', tag],
            capture_output=True, text=True, check=True
        ).stdout.strip()
        if tag_commit != current_commit:
            return tag
    return None

def generate_release_notes(
    prompt_file_path="prompt.txt",
    output_dir="changes",
    model="gemini/gemini-1.5-flash",
    apikey=None,
    path="."
):
    """
    High-level function that:
      1. Finds the latest tag + current commit
      2. Extracts diffs to `output_dir` for the given path
      3. Generates a single context string
      4. Reads a prompt file
      5. Calls the wrapped LLM generate function
      6. Returns the release notes text
    """
    last_tag = get_latest_release_tag()
    current_commit = get_current_commit()
    if not last_tag:
        return "No valid release tag found (like 'v1.0.0'). Please create one."

    extract_diff(last_tag, current_commit, output_dir=output_dir, path=path)
    context = generate_context_string(last_tag, current_commit, path=path)

    data_path = files("auto_release_notes").joinpath(prompt_file_path)
    prompt_text = data_path.read_text()

    release_notes = generate(
        changes=context,
        prompt=prompt_text,
        model=model,
        apikey=apikey
    )

    return release_notes
