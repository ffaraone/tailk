# TailK

![pyversions](https://img.shields.io/pypi/pyversions/tailk.svg) [![PyPi Status](https://img.shields.io/pypi/v/tailk.svg)](https://pypi.org/project/tailk/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/tailk) ![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/ffaraone/tailk/test.yml?branch=master) ![Codecov](https://img.shields.io/codecov/c/github/ffaraone/tailk)

## Introduction

`TaikK` is a small utility to tail logs from multiple Kubernetes pods.

## Installation

`TailK` requires Python 3.8+ and `kubectl` available in your shell.

### Using pip

```
$ pip install tailk
```

### Using Homebrew

```
$ brew update
$ brew tap ffaraone/birre
$ brew install ffaraone/birre/tailk
```


## Usage

### Basic usage

```
$ tailk pattern1 [...]
```

where `pattern1` is any valid Python regular expression.

> Multiple patterns are combined with a logical `OR`.


### Advanced usage

You may want to highlight portions of the log. In this case you can provide highlighting patterns in the following way:

```
$ tailk pattern1 --highlight hl-pattern-1 [--highlight hl-pattern-2]
```

where `hl-pattern-1` is any valid Python regular expression.

You can also customize the style for highlight. In this case your patterns must be specified using named capturing groups

```
$ tailk pattern1 --highlight "(?P<hello>HELLO)" --style "hello:underline magenta"
```

## License

`TailK` is released under the [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
