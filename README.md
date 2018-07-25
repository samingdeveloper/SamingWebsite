





















# Saming ![CI status](https://img.shields.io/badge/release-v0.1-blue.svg)
Welcome to Saming, a programming grading platform, created for FIBO.

## Test Case Syntax

Each test case is a call of `assert_equal(actual, expected, points, [Optional]hidden=False)`

`actual` is the method call, written as `prob.your_method(args)`

`expected` is the expected return value of the method

`points` is the score of the individual test case. In scoring mode, the test cases add up.

`hidden` is whether the test case will be viewable for students

## Importing libraries

use `# lib yourlib` to import libraries your students might need.

## Example

```
assert_equal(prob.foo_bar(9), 8, 7, True)
# lib math
```

