# Changelog

The releases this repository pins, newest first, in the form of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). A pin move is recorded here, not in decisions/.

## [Unreleased]

### Changed

- Pinned reader-ergonomics v1.24.5 (`030e4f2`), from v1.24.2 (`65e4247`): a SICI DOI is read whole and a server that refuses the checker is a warning, so the weekly online run does not fail on a reference that exists.

### Added

- The tool roles `cadquery-part`, `comfyui-graph-check`, `unity-batch-build` and `runpod-pod-guard`, each with a reference pipeline run twice from an empty folder, its judge and its refused faults, in the form of decision 0003.
- The literature review of roles, with its baseline B1, in `evidence/roles-review/`.
- Pinned reader-ergonomics v1.24.2 (`65e4247`), the commit its release tag points to, in both workflows.
