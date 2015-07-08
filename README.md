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
                stack.append: cur
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
                

