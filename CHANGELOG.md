# 0.6.5

* Do not use Hy version ` 1.0aX`

# 0.6.4

* Fix bug with CSV stat export when no VAT on an invoice

# 0.6.3

* Fix bug with `price_formula` and empty string prices

# 0.6.2

* Migrate to Hy `>= 0.26`

# 0.6.1

* Add decimal number format arguments (`--decimals-csv-locale` and `--decimals-csv-format`) to statistics CSV ouput command

# 0.6.0

* Add a parser option `options.price_formula.enabled` in definition to be set to `True` for allowing to set price as formula. The formula starts with `=` and follow with valid Python code. For eg. `prestations.0.price: =1000*0.7` will yield a price of 700 on the first prestation.

# 0.5.0

* Add a `rounding-decimals` kwarg to `parse_invoices` and `parse_quote`, which default to `2`

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
