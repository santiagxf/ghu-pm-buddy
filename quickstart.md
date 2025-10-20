# Quickstart

This section mentions the prerequisites to run the demo.

## Get the environment ready

Follow this steps to get the environment ready:

1. Open the repository in GitHub Codespaces.
1. Install the [AI Toolkit extension](https://github.com/microsoft/Azure-AI-Foundry-Extension-VSCode-Preview/blob/main/extension/vscode-ai-foundry-0.10.1.vsix):
    - From command pallet type: `Extensions: Install from VSIX`
    - Navigate to the folder `extensions` and install both of the files.
    - Reload the window.
    - The extension is ready to be used.

2. Install `uv` package manager:
    - In the console type `curl -LsSf https://astral.sh/uv/install.sh | sh`
    - Type `uv --version` to confirm `uv` is installed.

3. Install packages.
    - Move to the folder `src`.
    - Restore the project with `uv sync`.

4. Configure `uv` environment file:
    - Edit the file `.env.example` and rename it to `.env`.
    - Configure the environment variables indicated there.
    - Edit `~/.bashrc` and add `export UV_ENV_FILE=".env"`.

5. Install the Azure CLI tool:
    - Run `curl -LsSf https://aka.ms/InstallAzureCLIDeb | sudo bash`
    - Login to Azure with `az login`. Use `az login --tenant 7f292395-a08f-4cc0-b3d0-a400b023b0d2`

6. Run the project:

    - `uv run python pm_buddy/workflow.py`