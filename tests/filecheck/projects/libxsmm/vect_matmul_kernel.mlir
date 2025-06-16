// RUN: xdsl-opt -p convert-vector-to-x86{arch=avx2},convert-vector-to-ptr,convert-ptr-to-x86{arch=avx2},reconcile-unrealized-casts,reconcile-unrealized-casts

// func to x86 func: need to support the lowering of shaped function parameters
// arith.constant: need to support the lowering to x86
// arith.addi: need to support the lowering to x86
// ptr_xdsl.to_ptr: need to support the lowering to x86

func.func @matmul(
  %A: memref<4x8xf32>,
  %B: memref<8x4xf32>,
  %C: memref<4x4xf32>
) {
  %i0 = arith.constant 0: index
  %i1 = arith.constant 1: index
  %i2 = arith.constant 2: index
  %i3 = arith.constant 3: index
  %i4 = arith.constant 4: index
  %i5 = arith.constant 5: index
  %i6 = arith.constant 6: index
  %i7 = arith.constant 7: index
  %f0 = arith.constant 0.0: f32
  %init_acc = vector.broadcast %f0: f32 to vector<8xf32>

  // Let i be 0 and j be 0

  // Load lines of A for i = 0, k ∈ [0,7]
  %a0 = vector.load %A[%i0,%i0]: memref<4x8xf32>, vector<8xf32>
  %a1 = vector.load %A[%i0,%i1]: memref<4x8xf32>, vector<8xf32>
  %a2 = vector.load %A[%i0,%i2]: memref<4x8xf32>, vector<8xf32>
  %a3 = vector.load %A[%i0,%i3]: memref<4x8xf32>, vector<8xf32>
  %a4 = vector.load %A[%i0,%i4]: memref<4x8xf32>, vector<8xf32>
  %a5 = vector.load %A[%i0,%i5]: memref<4x8xf32>, vector<8xf32>
  %a6 = vector.load %A[%i0,%i6]: memref<4x8xf32>, vector<8xf32>
  %a7 = vector.load %A[%i0,%i7]: memref<4x8xf32>, vector<8xf32>
  // Load points from B for j = 0, k ∈ [0,7]
  %b0_scal = memref.load %B[%i0, %i0] : memref<8x4xf32>
  %b1_scal = memref.load %B[%i1, %i0] : memref<8x4xf32>
  %b2_scal = memref.load %B[%i2, %i0] : memref<8x4xf32>
  %b3_scal = memref.load %B[%i3, %i0] : memref<8x4xf32>
  %b4_scal = memref.load %B[%i4, %i0] : memref<8x4xf32>
  %b5_scal = memref.load %B[%i5, %i0] : memref<8x4xf32>
  %b6_scal = memref.load %B[%i6, %i0] : memref<8x4xf32>
  %b7_scal = memref.load %B[%i7, %i0] : memref<8x4xf32>
  // Broadcast points from B
  %b0 = vector.broadcast %b0_scal: f32 to vector<8xf32>
  %b1 = vector.broadcast %b1_scal: f32 to vector<8xf32>
  %b2 = vector.broadcast %b2_scal: f32 to vector<8xf32>
  %b3 = vector.broadcast %b3_scal: f32 to vector<8xf32>
  %b4 = vector.broadcast %b4_scal: f32 to vector<8xf32>
  %b5 = vector.broadcast %b5_scal: f32 to vector<8xf32>
  %b6 = vector.broadcast %b6_scal: f32 to vector<8xf32>
  %b7 = vector.broadcast %b7_scal: f32 to vector<8xf32>
  // Fmas along k
  %acc0 = vector.fma %a0, %b0, %init_acc: vector<8xf32>
  %acc1 = vector.fma %a1, %b1, %acc0: vector<8xf32>
  %acc2 = vector.fma %a2, %b2, %acc1: vector<8xf32>
  %acc3 = vector.fma %a3, %b3, %acc2: vector<8xf32>
  %acc4 = vector.fma %a4, %b4, %acc3: vector<8xf32>
  %acc5 = vector.fma %a5, %b5, %acc4: vector<8xf32>
  %acc6 = vector.fma %a6, %b6, %acc5: vector<8xf32>
  %acc7 = vector.fma %a7, %b7, %acc6: vector<8xf32>
  // Store the result of the reduction to
  vector.store %acc7, %C[%i0,%i0]: memref<4x4xf32>, vector<8xf32>
  
  return
}
