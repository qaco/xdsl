// RUN: xdsl-opt %s -p 'apply-pdl{pdl_file="%p/pdl_definition.mlir"}' | filecheck %s

func.func @example(%x: i32, %y: i32, %z: i32) -> i32 {
    %a = arith.addi %x, %y : i32
    %b = arith.subi %a, %y : i32
    %c = arith.muli %b, %z : i32
    return %c : i32
}

//CHECK:        builtin.module {
// CHECK-NEXT:     func.func @example(%x : i32, %y : i32, %z : i32) -> i32 {
// CHECK-NEXT:        %0 = arith.constant 0 : i64
// CHECK-NEXT:        %b = arith.addi %x, %0 : i32
// CHECK-NEXT:        %c = arith.muli %b, %z : i32
// CHECK-NEXT:        func.return %c : i32
// CHECK-NEXT:     }
// CHECK-NEXT: }
