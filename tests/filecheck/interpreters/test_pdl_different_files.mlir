// RUN: xdsl-opt %s -p 'apply-pdl{pdl_file="%p/pdl_definition.mlir"}' | filecheck %s

func.func @example(%x: i32, %y: i32, %z: i32) -> i32 {
    %a = arith.addi %x, %y : i32
    %b = arith.subi %a, %y : i32
    %c = arith.muli %b, %z : i32
    return %c : i32
}
