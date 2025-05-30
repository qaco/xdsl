// RUN: XDSL_ROUNDTRIP

// CHECK: f32_2D = !emitc.array<4x2xf32>
// CHECK-SAME: i32_1D = !emitc.array<10xi32>
// CHECK-SAME: f64_1D = !emitc.array<5xf64>
// CHECK-SAME: i1_3D = !emitc.array<3x4x5xi1>
"test.op"() {
  f32_2D = !emitc.array<4x2xf32>,
  i32_1D = !emitc.array<10xi32>,
  f64_1D = !emitc.array<5xf64>,
  i1_3D = !emitc.array<3x4x5xi1>
}: ()->()
