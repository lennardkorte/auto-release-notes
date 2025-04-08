### New Features

* Added a new Python package `auto-release-notes` for generating release notes.  The package leverages an LLM to generate release notes from git commit diffs.
* Created GitHub Actions workflows (`auto_release_notes.yml` and `release_notes.yml`) to automate the generation and publishing of release notes.  These workflows use the new package and require a GEMINI_API_KEY secret.


### Bug Fixes

* Improved the `get_file_content` function to handle binary files and non-UTF-8 encodings more robustly.  It now returns a message indicating a binary file or encoding issue if the decoding fails.


### Other Changes

* Added a `.gitignore` file to exclude various files and directories.
* Added a `LICENSE` file (GNU Lesser General Public License v2.1).
* Added a `MANIFEST.in` file to specify which files to include in the package distribution.
* Added a `README.md` file with instructions and a link to the GitHub workflow.
* Added a `SECURITY.md` file outlining the security policy and disclosure guidelines.
* Updated `pyproject.toml` to include build system configurations and dependencies.
* Refactored code into a more structured package with modules for different functionalities.
* Added a `prompt.txt` file containing the prompt for the LLM.
* Added a `run.py` file to run the release notes generation script.

### Upgrade Steps

* Add a `GEMINI_API_KEY` secret to your GitHub repository settings.  This secret is required for the GitHub Actions workflows to function.
* If upgrading from a previous version, manually delete the `CHANGELOG.md` file.  The workflow will automatically regenerate it.



