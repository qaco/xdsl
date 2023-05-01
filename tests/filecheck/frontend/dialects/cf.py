# RUN: python %s | filecheck %s

from xdsl.frontend.program import FrontendProgram
from xdsl.frontend.context import CodeContext
from xdsl.frontend.dialects.builtin import i1, i32
from xdsl.frontend.exception import CodeGenerationException

p = FrontendProgram()
with CodeContext(p):
    # CHECK: cf.assert(%{{.*}} : !i1) ["msg" = ""]
    def test_assert_I(cond: i1):
        assert cond

    # CHECK: cf.assert(%{{.*}} : !i1) ["msg" = "some message"]
    def test_assert_II(cond: i1):
        assert cond, "some message"


p.compile(desymref=False)
print(p.xdsl())

try:
    with CodeContext(p):
        # CHECK: Expected a string constant for assertion message, found 'ast.Name'
        def test_assert_message_type(cond: i1, a: i32):
            assert cond, a

    p.compile(desymref=False)
    print(p.xdsl())
except CodeGenerationException as e:
    print(e.msg)