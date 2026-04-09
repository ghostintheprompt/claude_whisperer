# Claude Whisperer Project Structure

Claude Whisperer is a layered repo. The browser extension is the clearest current entry point, but the repository also preserves older safeguard-monitor tooling, research utilities, and archive material from earlier Claude eras.

## Top-Level Layout

```text
claude_whisperer/
├── README.md
├── LICENSE
├── extension/
├── patterns/
├── research/
├── core/
├── tools/
├── docs/
├── config/
├── tests/
├── semantic_mirror/
├── multimodal/
├── exploit_generator/
├── frontend/
└── backup_final/
```

## Primary Surfaces

### `extension/`

The most current, easiest-to-understand surface in the repo.

What lives here:
- browser-extension UI
- Claude page integration
- popup actions
- local history/export
- modular generators for semantic, structured, and multimodal testing

If you are new to the repo, start here.

### `patterns/`

JSON suites and pattern files used across different versions of the project.

These files are useful when you want to inspect the repo's test vocabulary and research categories without digging through UI code.

### `research/`

Comparative testing notes, mode/model experiments, reporting templates, and older research tooling.

This directory is still useful, but much of it reflects earlier Claude versions and research phases.

## Supporting and Legacy Surfaces

### `core/`

Older Python-side clients and monitors from the safeguards-focused phase of the repo.

These files matter historically, but they are not the current recommended entry point.

### `tools/`

Analysis and orchestration utilities from the same broader research/safeguards period.

### `semantic_mirror/`, `multimodal/`, `exploit_generator/`, `frontend/`

Project slices and experiments preserved from prior iterations. They help explain how the repo grew, even when they are not the most current surface.

### `backup_final/`

Archived snapshot material retained for reference.

Treat this as historical context, not the primary codepath.

## Practical Reading Order

If you want to understand the repo without getting lost:

1. [../README.md](../README.md)
2. [GETTING_STARTED.md](GETTING_STARTED.md)
3. [../extension/README.md](../extension/README.md)
4. `extension/`
5. `patterns/`
6. `research/`

After that, visit `core/`, `tools/`, and `backup_final/` only if you want the deeper history of the project.

## Important Caveat

This repo does not currently present itself as one perfectly unified framework on disk. That is fine. The point of the refreshed docs is to make the current working surface obvious while still respecting the older layers that gave the project its shape.
