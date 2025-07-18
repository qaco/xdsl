# RUN: python %s | filecheck %s

from xdsl.dialects import bigint, builtin
from xdsl.frontend.pyast.context import CodeContext
from xdsl.frontend.pyast.program import FrontendProgram
from xdsl.frontend.pyast.utils.block import block
from xdsl.frontend.pyast.utils.const import Const
from xdsl.frontend.pyast.utils.exceptions import FrontendProgramException

p = FrontendProgram()
p.register_type(int, bigint.bigint)
p.register_type(bool, builtin.i1)
#      CHECK: Cannot compile program without the code context
# CHECK-NEXT:     p = FrontendProgram()
# CHECK-NEXT:     with CodeContext(p):
# CHECK-NEXT:         # Your code here.
try:
    p.compile(desymref=False)
except FrontendProgramException as e:
    print(e.msg)

#      CHECK: Cannot print the program IR without compiling it first. Make sure to use:
# CHECK-NEXT:     p = FrontendProgram()
# CHECK-NEXT:     with CodeContext(p):
# CHECK-NEXT:         # Your code here.
# CHECK-NEXT:     p.compile()
with CodeContext(p):

    def foo():
        return


try:
    print(p.textual_format())
except FrontendProgramException as e:
    print(e.msg)

try:
    with CodeContext(p):

        def foo():
            return

        # CHECK: Function 'foo' is already defined
        def foo():
            return

    p.compile(desymref=False)
    print(p.textual_format())
except FrontendProgramException as e:
    print(e.msg)

try:
    with CodeContext(p):

        def foo():
            # CHECK-NEXT: Cannot have an inner function 'bar' inside the function 'foo'.
            def bar():
                return

            return

    p.compile(desymref=False)
    print(p.textual_format())
except FrontendProgramException as e:
    print(e.msg)

try:
    with CodeContext(p):

        def foo():
            @block
            def bb1():
                # CHECK-NEXT: Cannot have a nested function 'foo' inside the block 'bb1'.
                def foo():
                    return

                return

            return bb1()

    p.compile(desymref=False)
    print(p.textual_format())
except FrontendProgramException as e:
    print(e.msg)

try:
    with CodeContext(p):

        def foo():
            @block
            def bb0():
                # CHECK-NEXT: Cannot have a nested block 'bb1' inside the block 'bb0'.
                @block
                def bb1():
                    return

                return bb1()

            return bb0()

    p.compile(desymref=False)
    print(p.textual_format())
except FrontendProgramException as e:
    print(e.msg)

try:
    with CodeContext(p):

        def foo():
            @block
            def bb0():
                return bb0()

            # CHECK-NEXT: Block 'bb0' is already defined
            @block
            def bb0():
                return

            return bb0()

    p.compile(desymref=False)
    print(p.textual_format())
except FrontendProgramException as e:
    print(e.msg)

try:
    with CodeContext(p):

        def test():
            a: Const[int] = 23
            # CHECK-NEXT: Constant 'a' is already defined and cannot be assigned to.
            a = 3
            return

    p.compile(desymref=False)
    print(p.textual_format())
except FrontendProgramException as e:
    print(e.msg)

try:
    with CodeContext(p):
        a: Const[int] = 23

        # CHECK-NEXT: Constant 'a' is already defined.
        def test():
            a: int = 3
            return

    p.compile(desymref=False)
    print(p.textual_format())
except FrontendProgramException as e:
    print(e.msg)

try:
    with CodeContext(p):
        b: Const[int] = 23

        def test():
            @block
            def bb0():
                # CHECK-NEXT: Constant 'b' is already defined and cannot be assigned to.
                b = 3
                return

            return bb0()

    p.compile(desymref=False)
    print(p.textual_format())
except FrontendProgramException as e:
    print(e.msg)

try:
    with CodeContext(p):
        c: Const[int] = 23

        def foo():
            # CHECK-NEXT: Constant 'c' is already defined and cannot be assigned to.
            c = 2
            return

    p.compile(desymref=False)
    print(p.textual_format())
except FrontendProgramException as e:
    print(e.msg)

try:
    with CodeContext(p):
        c: Const[int] = 23

        def foo():
            # CHECK-NEXT: Constant 'c' is already defined.
            c: int = 2
            return

    p.compile(desymref=False)
    print(p.textual_format())
except FrontendProgramException as e:
    print(e.msg)

try:
    with CodeContext(p):
        c: Const[int] = 23

        # CHECK-NEXT: Constant 'c' is already defined and cannot be used as a function/block argument name.
        def foo(c: int):
            return

    p.compile(desymref=False)
    print(p.textual_format())
except FrontendProgramException as e:
    print(e.msg)

try:
    with CodeContext(p):
        d: Const[int] = 23

        def foo():
            @block
            def bb0():
                # CHECK-NEXT: Constant 'd' is already defined and cannot be assigned to.
                d = 2
                return

            return bb0()

    p.compile(desymref=False)
    print(p.textual_format())
except FrontendProgramException as e:
    print(e.msg)

with CodeContext(p):
    # CHECK-NEXT: Expected non-zero number of return types in function 'foo', but got 0.
    def foo() -> int:
        return


try:
    p.compile(desymref=False)
    print(p.textual_format())
except FrontendProgramException as e:
    print(e.msg)


try:
    # CHECK-NEXT: Cannot re-register type name 'int'
    p.register_type(int, bigint.bigint)
except FrontendProgramException as e:
    print(e.msg)


try:
    # CHECK-NEXT: Cannot re-register function 'int.__add__'
    p.register_function(int.__add__, bigint.AddOp)
    p.register_function(int.__add__, bigint.AddOp)
except FrontendProgramException as e:
    print(e.msg)


try:
    # CHECK-NEXT: Cannot register multiple source types for IR type '!bigint.bigint'
    p.register_type(float, bigint.bigint)
except FrontendProgramException as e:
    print(e.msg)


try:
    # CHECK-NEXT: Cannot register multiple source types for IR type '!bigint.bigint'
    p.register_type(float, bigint.bigint)
except FrontendProgramException as e:
    print(e.msg)

try:
    with CodeContext(p):
        # CHECK: Expected non-zero number of return types in function 'test_no_return_type', but got 0.
        def test_no_return_type(a: int) -> int:
            return

    p.compile(desymref=False)
    exit(1)
except FrontendProgramException as e:
    print(e.msg)

try:
    with CodeContext(p):
        # CHECK: Type signature and the type of the return value do not match at position 0: expected i1, got !bigint.bigint.
        def test_wrong_return_type(a: bool, b: int) -> bool:
            return b

    p.compile(desymref=False)
    exit(1)
except FrontendProgramException as e:
    print(e.msg)

try:
    with CodeContext(p):
        # CHECK: Expected no return types in function 'test_wrong_return_type'.
        def test_wrong_return_type(a: int):
            return a

    p.compile(desymref=False)
    exit(1)
except FrontendProgramException as e:
    print(e.msg)

try:
    with CodeContext(p):
        # CHECK: Expected the same types for binary operation 'Add', but got !bigint.bigint and i1.
        def bin_op_type_mismatch(a: int, b: bool) -> int:
            return a + b

    p.compile(desymref=False)
    exit(1)
except FrontendProgramException as e:
    print(e.msg)

try:
    with CodeContext(p):
        # CHECK: Expected the same types for comparison operator 'Lt', but got !bigint.bigint and i1.
        def cmp_op_type_mismatch(a: int, b: bool) -> bool:
            return a < b

    p.compile(desymref=False)
    exit(1)
except FrontendProgramException as e:
    print(e.msg)
