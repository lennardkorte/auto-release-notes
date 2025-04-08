### New Features

* **feat(workflow):** Added GitHub Actions workflow to automatically generate release notes.  The workflow uses the `lennardkorte/auto-release-notes` action.
* **feat(package):** Created a Python package (`auto-release-notes`) for generating release notes.  This package uses the `litellm` library to interact with LLMs.
* **feat(LLM):** Implemented LLM-based release note generation. The generated notes follow the "Keep a Changelog" style.
* **feat(diff):** Added functionality to extract diffs between Git commits and save them to a "changes" directory.  This allows for easier context analysis by the LLM.
* **feat(prompt):** Added a configurable prompt file (`prompt.txt`) for controlling the LLM's instructions.


### Bug Fixes

* **fix(extractor):** Improved file content extraction to handle binary files and non-UTF-8 encodings more gracefully.  Now reports "Binary file or non-UTF-8 encoding (content not shown)" instead of failing.

### Other Changes

* **chore(deps):** Updated dependencies, including `litellm`.
* **chore(structure):** Reorganized project structure into a Python package.
* **docs(README):** Updated README to reflect new functionality and usage.
* **docs(SECURITY):** Added a SECURITY.md file outlining security reporting procedures.
* **chore(license):** Added a GNU Lesser General Public License (LGPL).
* **chore(gitignore):** Added a `.gitignore` file to exclude common files and directories.
* **chore(manifest):** Added a `MANIFEST.in` to include relevant files in the package.


### Performance Improvements

* **perf(release_notes):** Optimized the `generate_release_notes` function for improved efficiency.




