// RUN: XDSL_ROUNDTRIP

//===----------------------------------------------------------------------===//
// ArrayType
//===----------------------------------------------------------------------===//

// CHECK: bf16_1D = !emitc.array<1xbf16>
// CHECK-SAME: f32_2D = !emitc.array<4x2xf32>
// CHECK-SAME: f64_1D = !emitc.array<5xf64>
// CHECK-SAME: i1_0D = !emitc.array<0xi1>
// CHECK-SAME: i1_3D = !emitc.array<3x4x5xi1>
// CHECK-SAME: i32_1D = !emitc.array<10xi32>
// CHECK-SAME: index_1D = !emitc.array<1xindex>
"test.op"() {
  bf16_1D = !emitc.array<1xbf16>,
  f32_2D = !emitc.array<4x2xf32>,
  f64_1D = !emitc.array<5xf64>,
  i1_0D = !emitc.array<0xi1>,
  i1_3D = !emitc.array<3x4x5xi1>,
  i32_1D = !emitc.array<10xi32>,
  index_1D = !emitc.array<1xindex>
}: ()->()

//===----------------------------------------------------------------------===//
// LValueType
//===----------------------------------------------------------------------===//

// CHECK: f64 = !emitc.lvalue<f64>
// CHECK-SAME: i32 = !emitc.lvalue<i32>
// CHECK-SAME: index = !emitc.lvalue<index>
// CHECK-SAME: tensor_i32 = !emitc.lvalue<tensor<1xi32>>
// CHECK-SAME: tuple_i32 = !emitc.lvalue<tuple<i32, i32>>
"test.op"() {
  f64 = !emitc.lvalue<f64>,
  i32 = !emitc.lvalue<i32>,
  index = !emitc.lvalue<index>,
  tensor_i32 = !emitc.lvalue<tensor<1xi32>>,
  tuple_i32 = !emitc.lvalue<tuple<i32, i32>>
  // emitc.ptr and emitc.opaque types are not supported yet.
  // Once they are supported, the following lines can be uncommented:
  // ptr_i32 = !emitc.lvalue<!emitc.ptr<i32>>,
  // opaque_int = !emitc.lvalue<!emitc.opaque<"int">>
}: ()->()
