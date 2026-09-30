## MyDef Extension -- MyDef::output_python.pm

This is an extension to [MyDef](https://github.com/hzhou/MyDef) for writing Python code. Use it with `module: python`; pages compile to `.py` (Python 3 by default).

    page: hello
        module: python

        $print Hello World!

`mydef_page hello.def` writes `hello.py`; `mydef_run hello.def` also runs it.

#### Install

MyDef must be installed first, with `MYDEFSRC` pointing to the MyDef source directory (and `PERL5LIB`/`MYDEFLIB` set as in MyDef's install).

    mydef_make
    make
    make install

`make install` installs `MyDef/output_python.pm` into `$PERL5LIB`, `std_python.def` and `python/*.def` into `$MYDEFLIB`, and the `perl_to_python` script into `~/bin`.

To refresh after editing, `make && make install` is enough, unless new `.def` files were added (then rerun `mydef_make` first).

#### Page structure

`std_python.def` is loaded automatically. The page body becomes `def main():` and is called from `if __name__ == "__main__":`. `fncode:` blocks become module-level functions after `main`. Imports and globals are collected at the top of the file.

    page: test
        module: python

        s = get_name()
        $print s = $s

    fncode: get_name
        return "World"

#### Features

In addition to the general macro facilities provided by MyDef, output_python adds:

* **Relaxed syntax** -- the trailing `:` after `if|elif|else|while|for|def` is optional; `print x` becomes `print(x)`; `n++`/`n--` become `n+=1`/`n-=1`.

* **`$if`, `$elif`, `$else`, `$while`** -- the same style as MyDef's Perl/C extensions. `$if !cond` becomes `if not cond:`. `$while cond; step` puts `step` at the end of the loop body.

* **`$for` / `$foreach`**

    | MyDef | Python |
    |-------|--------|
    | `$for i=0:10` | `for i in range(10):` |
    | `$for i=2:10` | `for i in range(2,10):` |
    | `$for N` | `for _i in range(N):` |
    | `$for x in L` | `for x in L:` |
    | `$for a, b in A, B` | `for a, b in zip(A, B):` |
    | `$for i, x in L` | `for i, x in enumerate(L):` |
    | `$for i, a, b in A, B` | `for i, a, b in zip(range(len(A)), A, B):` |

* **`$do`** -- a block you can `break` out of or `continue` to repeat. It compiles to `while 1:` with a `break` at the end.

* **`$def name(params)`** -- an inline `def`; the parentheses may be omitted when there are no parameters.

* **`$print`** -- mixes literal text with `$var` and `${expr}`, as in the C and Perl extensions:

        $print n=$n, root=${sqrt(n)}    # print("n=%s, root=%s" % (n, sqrt(n)))
        $print no newline-              # print("no newline", end='')

    Inside `$(set:print_to=Out)` it prints to that file; with `$(set:print_to=@lines)` it appends the string to the list `lines`. Related: `$dump a, b` prints `a = ..., b = ...`; `$warn msg` prints to `sys.stderr`; `$die msg` raises `Exception`.

* **`$import`, `$try_import`, `$global`** -- place them where they are relevant; they are collected at the top of the file.
    * `$import re`, `$import numpy as np`, `$import sqrt from math` (becomes `from math import sqrt`).
    * `$try_import numpy as np` wraps the import in `try/except ImportError` and sets `has_numpy`.
    * Uses of `re.`, `os.`, `sys.`, `copy.`, `glob.` are imported automatically.
    * `$global cnt = 5` defines `cnt` at module level and emits `global cnt` in the current function.

* **Perl-style regex in conditions** -- with optional capture binding:

        $if s=~/^(\w+) (\w+)/ -> first, second
            $print $second $first
        $elif s !~ /xyz/i
            ...

    A pattern starting with `^` uses `re.match`, otherwise `re.search`; flags `imsx` map to `re.I` etc. A bare `/pattern/` matches against `line` (the loop variable of `open_r`).

* **`$if_match pattern`** -- for writing lexers. It matches at `src_pos` in `src`, advances `src_pos` on success, and leaves the match in `m`. The compiled regexes are placed at `DUMP_STUB regex_compile` (or at the top of the file) to avoid repeated compilation.

#### Standard library

`std_python.def` (autoloaded):

* `&call open_r, fname` -- loop over lines of a file as `line`.
* `&call open_w, fname` / `&call open_W, fname` -- write to file handle `Out`; `open_W` also reports the file name and directs `$print` to it.
* `$call dict_inc, D, key` -- count occurrences in a dict.
* `$(ternary:cond, a, b)` -- `a if cond else b`.
* `$call start_time` / `$call print_time, msg` -- simple timing.
* `$call error, msg` -- raise `Exception`.

Optional, via `include:`:

* `python/parse.def` -- `parse_loop`, `parse_frame`, `if_match_continue`, `if_match_break`, and `parse_operator_precedence` for building parsers.
* `python/tkinter.def` -- a Tkinter main window frame.

Python 2 output can be selected by defining the macro `PYTHON2` (adds `from __future__` imports and uses `raw_input`).

#### perl_to_python

`perl_to_python in.def out.def` converts a MyDef source written for `module: perl` into one for `module: python` (Perl statements such as `my`, `push`, `s///`, `system`, `chomp` are translated; MyDef directives are kept). Wrap Perl-only parts in `/* skip python ... */`.

#### Demo

    page: calc, basic_frame
        module: python

        print calc("1+2*-3")

    fncode: calc(src)
        src_len=len(src)
        src_pos=0

        precedence = {'eof':0, '+':1, '-':1, '*':2, '/':2, 'unary': 99}
        DUMP_STUB regex_compile

        macros:
            type: stack[$1][1]
            atom: stack[$1][0]
            cur_type: cur[1]
            cur_atom: cur[0]

        stack=[]
        $while 1
            #-- lexer ----
            $do
                $if_match \s+
                    continue

                $if_match [\d\.]+
                    num = float(m.group(0))
                    cur=( num, "num")
                    break

                $if_match [-+*/]
                    op = m.group(0)
                    cur = (op, op)
                    break

                $if src_len>=src_pos
                    cur = ('', "eof")
                    break

                #-- error ----
                t=src[0:src_len]+" - "+src[src_len:]
                raise Exception(t)

            #-- reduce ----
            $do
                $if $(cur_type)=="num"
                    break

                $if len(stack)<1 or $(type:-1)!="num"
                    cur = (cur[0], 'unary')
                    break

                $if len(stack)<2
                    break

                $if precedence[$(cur_type)]<=precedence[$(type:-2)]
                    $call reduce
                    continue

            #-- shift ----
            $if $(cur_type)!="eof"
                stack.append(cur)
            $else
                $if len(stack)>0
                    return stack[-1][0]
                $else
                    return None

        subcode: reduce
            $if $(type:-2) == "unary"
                t = -$(atom:-1)
                stack[-2:]=[(t, "num")]
            $map reduce_binary, +, -, *, /

        subcode: reduce_binary(op)
            $elif $(type:-2)=='$(op)'
                t = $(atom:-3) $(op) $(atom:-1)
                stack[-3:]=[(t, "num")]

This prints `-5.0`. More examples are in `test/`.
