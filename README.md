## MyDef Extension -- MyDef::output_python.pm

This is an extension to [MyDef](https://github.com/hzhou/MyDef) for writing Python code. 

In addition to the general macro facilities provided by MyDef, output_python adds following features:

* Let's you use `$if`, `$elif`, `$else`, `$while`, `$for`, which fits the styles of MyDef's Perl/C extensions. 

* Let's you optionally omit the trailing `:` after `if|elif|else|while|for|def`.

* `$do`, a sequence construct where you can `break` or `continue`

* `$if_match regex`, let's you use re like in Perl. It will inject re.compile to a global stub (`DUMP_STUB regex_compile`) to avoid repeated compilation. It uses default variable `src`, `src_pos` and uses `re.match`.

* Let's you write `print` without mandatory function call parentheses in Python 3.

* Let's you write all function call statement without parentheses, e.g. `mylist.append: (a, tuple)`.

* Supports `$print` as we did in C and Perl (mixing literal and variables)

* `$import` and `$global`, let's you scatter them to where it is relavant.

* Automatically loads std_python.def, which always calls your main code in `if __name__ == "__main__"`.

#### Install

1. It depends on [MyDef](https://github.com/hzhou/MyDef) -- Hopefully, the instruction there is sufficient.

2. Define environment variable `MYDEFSRC` to the path where you downloaded MyDef.

3. `mydef_make`

4. `touch output_python.def && make`

5. Makefile.PL in `MyDef-output_python/`:

    cd MyDef-output_python
    pmake
    make

6. `mydef_make`  # again to pull the sub Makefile

7. `make install`

8. `sh install_def.sh`

#### Demo

To be added.
