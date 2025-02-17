from __future__ import annotations

from collections.abc import Sequence

from xdsl.dialects.builtin import FunctionType, StringAttr
from xdsl.dialects.utils import (
    parse_func_op_like,
)
from xdsl.dialects.x86.ops import X86AsmOperation, X86Instruction
from xdsl.ir import Attribute, Dialect, Operation, Region
from xdsl.irdl import (
    attr_def,
    irdl_op_definition,
    opt_attr_def,
    region_def,
    traits_def,
)
from xdsl.parser import Parser
from xdsl.printer import Printer
from xdsl.traits import (
    CallableOpInterface,
    HasParent,
    IsolatedFromAbove,
    IsTerminator,
    SymbolOpInterface,
)


class FuncOpCallableInterface(CallableOpInterface):
    @classmethod
    def get_callable_region(cls, op: Operation) -> Region:
        assert isinstance(op, FuncOp)
        return op.body

    @classmethod
    def get_argument_types(cls, op: Operation) -> tuple[Attribute, ...]:
        assert isinstance(op, FuncOp)
        return op.function_type.inputs.data

    @classmethod
    def get_result_types(cls, op: Operation) -> tuple[Attribute, ...]:
        assert isinstance(op, FuncOp)
        return op.function_type.outputs.data


@irdl_op_definition
class FuncOp(X86AsmOperation):
    """x86 function definition operation"""

    name = "x86_func.func"
    sym_name = attr_def(StringAttr)
    body = region_def()
    function_type = attr_def(FunctionType)
    sym_visibility = opt_attr_def(StringAttr)

    traits = traits_def(
        SymbolOpInterface(),
        FuncOpCallableInterface(),
        IsolatedFromAbove(),
    )

    def __init__(
        self,
        name: str,
        region: Region,
        function_type: FunctionType | tuple[Sequence[Attribute], Sequence[Attribute]],
        visibility: StringAttr | str | None = None,
    ):
        if isinstance(function_type, tuple):
            inputs, outputs = function_type
            function_type = FunctionType.from_lists(inputs, outputs)
        if isinstance(visibility, str):
            visibility = StringAttr(visibility)
        attributes: dict[str, Attribute | None] = {
            "sym_name": StringAttr(name),
            "function_type": function_type,
            "sym_visibility": visibility,
        }

        super().__init__(attributes=attributes, regions=[region])

    @classmethod
    def parse(cls, parser: Parser) -> FuncOp:
        visibility = parser.parse_optional_visibility_keyword()
        (name, input_types, return_types, region, extra_attrs, arg_attrs, res_attrs) = (
            parse_func_op_like(
                parser,
                reserved_attr_names=("sym_name", "function_type", "sym_visibility"),
            )
        )
        if arg_attrs:
            raise NotImplementedError("arg_attrs not implemented in x86_func")
        if res_attrs:
            raise NotImplementedError("res_attrs not implemented in x86_func")
        func = FuncOp(name, region, (input_types, return_types), visibility)
        if extra_attrs is not None:
            func.attributes |= extra_attrs.data
        return func

    def print(self, printer: Printer):
        if self.sym_visibility:
            visibility = self.sym_visibility.data
            printer.print_string(f" {visibility}")

        printer.print(f" @{self.sym_name.data}")
        printer.print_function_type(
            self.function_type.inputs.data, self.function_type.outputs.data
        )
        if self.body.blocks:
            printer.print(" ")
            printer.print_region(self.body, False, False)

    def assembly_line(self) -> str | None:
        if self.body.blocks:
            return f"{self.sym_name.data}:"
        else:
            return None


@irdl_op_definition
class RetOp(X86Instruction):
    """
    Return from subroutine.
    """

    name = "x86_func.ret"

    assembly_format = "attr-dict"

    traits = traits_def(IsTerminator(), HasParent(FuncOp))

    def __init__(
        self,
        *,
        comment: str | StringAttr | None = None,
    ):
        if isinstance(comment, str):
            comment = StringAttr(comment)

        super().__init__(
            attributes={
                "comment": comment,
            },
        )

    def assembly_line_args(self):
        return ()


X86_FUNC = Dialect(
    "x86_func",
    [
        FuncOp,
        RetOp,
    ],
)
