# Changelog

All notable changes to **pydd-web** are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/).

## [0.2.4] - 2026-08-12

### Added
- Bilingual documentation site (English + فارسی) on GitHub Pages — FastAPI / Flask / Django guides

### Changed
- Project URLs: Homepage / Documentation → https://ardavanshamroshan.github.io/pydd/
- README links to docs, PyPI, and GitHub
- Require `pydump-dd>=0.2.4`

## [0.2.3] - 2026-08-12

### Fixed
- README install docs: use PyPI packages `pydd-web` and `pydump-dd` instead of local path deps
- Require `pydump-dd>=0.2.3`

## [0.2.2] - 2026-08-12

### Added
- HTML dumps show `$variable · kind · type` tips (via pydump metadata)
- MIT `LICENSE` file

### Changed
- PyPI distribution renamed to **`pydd-web`** (`import pydd` unchanged)
- Depends on **`pydump-dd>=0.2.2`** from PyPI (removed local path source)

## [0.2.1] - 2026-07-23

### Added
- Laravel-style global helpers: `import pydd` injects web-aware `dd` / `dump` into builtins (overrides pydump)
- `install_helpers()` to re-install builtins explicitly

### Fixed
- Boot `dd` no longer auto-opens browser; refresh existing tab instead
- `dd(var)` outside request no longer hijacked via `last_app()` fallback
- Multiple HTML dumps no longer merge visually (`pre.sf-dump` bottom margin)
- `// file:line` tip after `[▼` when expanded, after `]` when collapsed (`[▶] // file`)
- Terminal tips no longer resolve to `pydd/api.py` (skip pydd package)

### Changed
- Document Editor/linter setup for builtin helpers (Ruff, Pyright, PyCharm; no `builtins.pyi`)

### Notes
- Package version aligned with GitHub tag/release `v0.2.1`

## [0.2.0] - 2026-07-23

### Notes
- Tag/release `v0.2.0` exists; prefer `v0.2.1` for current code

## [0.1.0] - 2026-07-22

### Added
- Initial release: HTML `dd` for FastAPI / Flask / Django on pydump

---

[Unreleased]: https://github.com/ardavanshamroshan/pydd/compare/v0.2.4...HEAD
[0.2.4]: https://github.com/ardavanshamroshan/pydd/releases/tag/v0.2.4
[0.2.3]: https://github.com/ardavanshamroshan/pydd/releases/tag/v0.2.3
[0.2.2]: https://github.com/ardavanshamroshan/pydd/releases/tag/v0.2.2
[0.2.1]: https://github.com/ardavanshamroshan/pydd/releases/tag/v0.2.1
[0.2.0]: https://github.com/ardavanshamroshan/pydd/releases/tag/v0.2.0
[0.1.0]: https://github.com/ardavanshamroshan/pydd/releases/tag/v0.1.0

See also: [Upgrade guide](upgrade.md) · [PyPI](https://pypi.org/project/pydd-web/) · [GitHub](https://github.com/ardavanshamroshan/pydd)
