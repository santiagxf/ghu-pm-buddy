# Run PM Buddy Action

This GitHub Action runs the PM Buddy project with a given input using the `uv` environment.

## Inputs

### `input`
**Required**: Yes  
**Default**: `'Hello from pm-buddy!'`  
**Description**: Input parameter to pass to the PM Buddy application

## Usage

```yaml
name: Run PM Buddy
on: [workflow_dispatch]

jobs:
  run-pm-buddy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Run PM Buddy
        uses: ./.github/actions/run-pm-buddy
        with:
          input: 'Your custom input message here'
```

## What it does

1. Sets up Python environment using the version specified in `src/.python-version`
2. Installs the `uv` package manager
3. Syncs the project dependencies in the `src/` directory using `uv sync`
4. Runs the PM Buddy application with the provided input

## Example

```yaml
- name: Run PM Buddy with custom input
  uses: ./.github/actions/run-pm-buddy
  with:
    input: 'Process issue #42 in repository owner/repo'
```
