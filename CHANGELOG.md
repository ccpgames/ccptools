# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [1.2.1] - 2024-22-05

### Added

- Super basic unittests for `instant_to_datetime` and `timestamp_to_datetime` 
  cause there was a super dumb error which those would have caught 


### Changed

- The unittest for `any_to_datetime` to account for "instant"


### Fixed

- The `any_to_datetime` call where it's accidentally casting "instants" to 
  "timestamps"


## [1.2.0] - 2024-22-05

### Added

- The `logging` package to the `ccptools.structs._base`
- Methods for casting between Datetime and timestamp (number of seconds since 
  UNIX Epoch as a float) that work even on Windows when the built in 
  `datetime.timestamp()` and `datetime.fromtimestamp()` methods fail for 
  negative values and more
- Methods for casting between Datetime and "instant" (number of milliseconds 
  since UNIX Epoch as an int)


### Changed

- How `any_to_datetime` handles "ambiguous" numeric values when deciding between
  "timestamp", "instant" and "filetime"
- How `any_to_datetime` handles strings such that if a given string is a simple 
  int or float, it's cast and treated as such


### Removed

- The `utc` argument from `any_to_datetime`


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