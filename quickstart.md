# Quickstart

This section mentions the prerequisites to run the demo.

## Get the environment ready

Follow this steps to get the environment ready:

1. Open the repository in GitHub Codespaces.
1. Install the AI Toolkit extension:
    - From command pallet type: `Extensions: Install from VSIX`
    - Navigate to the folder `extensions` and install both of the files.
    - Reload the window.
    - The extension is ready to be used.

2. Install `uv` package manager:
    - In the console type `curl -LsSf https://astral.sh/uv/install.sh | sh`
    - Type `uv --version` to confirm `uv` is installed`.

3. Install packages.
    - Move to the folder `pm-buddy`.
    - Restore the project with `uv sync`.