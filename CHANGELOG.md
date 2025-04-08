### Upgrade Steps
* [ACTION REQUIRED] Update your project's dependencies to include the latest version of the `auto-release-notes` package.  Refer to the documentation for installation instructions.


### Breaking Changes
* None

### New Features
* Added a new Python package `auto-release-notes` for automated release note generation.  This package leverages an LLM to generate release notes based on git commit history.
* Implemented a GitHub Actions workflow (`auto_release_notes.yml`) to automatically generate and commit release notes to a `CHANGELOG.md` file.  This workflow uses the new `auto-release-notes` package.
* The `auto-release-notes` package now supports specifying a custom prompt file (`prompt.txt`) for more control over the generated release notes.
* Improved the `get_latest_release_tag` function to correctly identify the latest non-beta tag, preventing the use of the current commit as a baseline if it is already tagged.
* The `get_file_content` function now handles binary files more gracefully, reporting that the content is not shown.
* Added handling of cases where files are not present in one or both commits being compared.

### Bug Fixes
* None

### Performance Improvements
* None

### Other Changes
* Added a `.gitignore` file to ignore various files and directories commonly used in Python projects.
* Added a `SECURITY.md` file outlining the security policy for the project.
* Added a `LICENSE` file (GNU Lesser General Public License v2.1)
* Added a `MANIFEST.in` file to control the files included in the source distribution.
* Refactored the code into a more modular structure, separating concerns into different files.
* Updated the `README.md` file to include information about the GitHub Actions workflow and installation instructions.
* Added a `pyproject.toml` file for project metadata and build configuration.
* Improved the documentation and added examples.



