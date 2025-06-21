# Release notes
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).
---

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
