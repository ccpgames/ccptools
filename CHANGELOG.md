# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [1.1.0] - 2024-04-08

### Added

- a new `enum_eval` method that turns any reasonable value into an instance 
  of the supplied Enum class _(i.e. string names or ints or whatever)_.
- a new enum base class, `EnumEx` that extends `enum.Enum` by adding a 
  `from_any` class method that uses `enum_eval` to initialize a new instance 
  of whatever class extends `EnumEx` from any sensible value
- the new `EnumEx` class to the base `ccptools.structs` import

### Changed

- how `int_eval` tries to cast strings and bytes since failed try/except's 
  are much faster than evaluating the content of a string first


## [1.0.0] - 2024-04-05

### Added

- This entire Project