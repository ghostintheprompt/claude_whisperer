# Claude Whisperer Documentation Map

This docs folder contains both current guidance and older research-era material.

If you only want the current repo story, start with the files below.

## Start Here

- [../README.md](../README.md)
  Top-level repo overview and the best description of what Claude Whisperer is today.
- [GETTING_STARTED.md](GETTING_STARTED.md)
  Fastest path into the repo without pretending everything is a single framework.
- [INSTALLATION.md](INSTALLATION.md)
  Browser-extension installation steps.
- [../extension/README.md](../extension/README.md)
  The current extension surface, UI tabs, and typical workflow.
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
  Honest map of the repo as it exists now.

## Current Working Surface

- `extension/`
  Browser extension for Claude-facing testing and evaluation.
- `patterns/`
  Shared suites and pattern definitions.
- `research/`
  Research notes, templates, and older comparative tooling.

## Mixed-Era Documents

Some files in this folder still reflect earlier repo phases and older model eras. They are useful, but they are not the canonical quickstart for the project today.

Typical signs a doc is historical:
- it is framed as a `Safeguards Framework`
- it is centered on `Claude 3.7` or `Claude 4.0`
- it assumes a single Python launcher or monitor-first workflow

Those files still have research value. They just should not be mistaken for the clean current entry point.

## Useful Supporting Docs

- [SECURITY.md](SECURITY.md)
  Responsible-use guidelines.
- [RESEARCH_METHODOLOGY.md](RESEARCH_METHODOLOGY.md)
  Historical methodology for the research side of the repo.
- [QUICKSTART.md](QUICKSTART.md)
  Short practical setup guide aligned to the current extension-first path.

## If You Are Updating This Repo

When in doubt:
- keep the top-level README honest
- prefer extension-first instructions
- treat older research docs as archive layers unless you are actively modernizing them
- do not describe the repo as a single pristine framework if the codebase itself tells a more mixed story
