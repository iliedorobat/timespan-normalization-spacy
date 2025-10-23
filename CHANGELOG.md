# Release notes
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).
---

## 2.1.1
### Changed
- Bump spaCy 3.8.7
- Handle language detection exception

### 2.1.0
#### Changed
- Bump TeN Framework 2.1.0
- Escaped special characters when building `regex_matches` in `_retokenize` method
- Improved performance by initializing the Java process at the start of the pipeline and shutting it down only when the pipeline is destroyed.

#### Added
- `input_value` and `prepared_value` fields to `TimeSeries` class
- INP validation tests (`validate_inp_data`)

### 2.0.2
#### Changed
- Improved the log of temporal expressions that are not processed by the TeN Framework.

### 2.0.1
#### Changed
- Updated the text of `Ronec` entities by adding space between the corresponding tokens
- Handled ambiguous or loosely defined expressions, such as "martie -iunie 2013"

### 2.0.0.post2
#### Added
- icon.png.

### 2.0.0.post1
#### Changed
- Minor metadata update after 2.0.0 was withdrawn.

### 2.0.0
#### Added
- Support for [Temporal Expression Normalization Framework v2.0](https://github.com/iliedorobat/timespan-normalization/tree/release/2.0)
- Validation tests
- Code documentation

#### Changed
- `entity._.time_series` now returns a **list of `TimeSeries` objects** instead of a single instance to support multiple temporal interpretations per entity
- Updated the spaCy example to support the new API change

#### Breaking
- ⚠️ API change: `entity._.time_series` was a single `TimeSeries` instance; it is now a list. Code depending on the old behavior must be updated accordingly.

### 1.1.1
#### Changed
- Updated README.md

### 1.1.0
#### Added
- Support for [Temporal Expression Normalization Framework v1.7](https://github.com/iliedorobat/timespan-normalization/tree/release/1.7)
- Standalone example

#### Changed
- The signature of `start_process` and `gateway_conn` to accept plaintext

### 1.0
#### Added
- Initial implementation of the spaCy pipeline of the [Temporal Expression Normalization Framework v1.6](https://github.com/iliedorobat/timespan-normalization/tree/release/1.6)
