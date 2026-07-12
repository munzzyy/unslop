## 0.3.0

Fixed the retry loop that hung when the server sent a 429 with no Retry-After header.
Added a --timeout flag. The config parser now prints the line number on a syntax error
instead of just failing with a stack trace.

## 0.2.1

Packed the wheel with the data file that was missing from 0.2.0. Sorry about that.
