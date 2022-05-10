# 0.4.3

* Fix `setup.py` to include `tqwgp_parser.files` module files

# 0.4.2

* Missing `__init__.py` for module `tqwgp_parser.files` (wrong fix)

# 0.4.1

* Fix missing dependencies

# 0.4.0

* Introduce statistics feature, allowing to parse a directory of invoices and generating revenue statistics (experimental)
    * To use it, run `tqwgp stats <project(s)_dir>`, `tqwgp show <project(s)_dir>` or `tqwgp csv --extract=invoices <project(s)_dir>`

# 0.3.0

* Migrate to [Hy 1.0a4](https://github.com/hylang/hy/releases/tag/1.0a4) and support Python 3.10

# 0.2.2

* Fix counts optional prestations inside sections for `optional_prestations`

# 0.2.1

* Fix inverted `price` and `optional_price` in `document.sections`)

# 0.2.0

* Each section (`document.sections`) return now both a `price` and `optional_price` properties, which decompose VAT: `total_vat_excl`, `total_vat_incl` and `vat`

# 0.1.0

* Requires Hy `>=1.0a1`

# 0.0.5

* Works with Hy `0.20.0`
