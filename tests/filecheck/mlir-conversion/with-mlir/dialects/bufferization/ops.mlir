// RUN: xdsl-opt %s | mlir-opt --mlir-print-op-generic | xdsl-opt | filecheck %s


%t = bufferization.alloc_tensor() : tensor<10x20x30xf64>
%m = "test.op"() : () -> memref<30x20x10xf32>
%m_t = bufferization.to_tensor %m restrict writable : memref<30x20x10xf32>
%t_m = bufferization.to_memref %m_t read_only : memref<30x20x10xf32>

%tensor1 = "test.op"() : () -> tensor<2x2xf64>
%tensor2 = "test.op"() : () -> tensor<2x2xf64>
%b = bufferization.materialize_in_destination %tensor1 in %tensor2 : (tensor<2x2xf64>, tensor<2x2xf64>) -> tensor<2x2xf64>


// CHECK:       builtin.module {
// CHECK-NEXT:    %0 = bufferization.alloc_tensor() : tensor<10x20x30xf64>
// CHECK-NEXT:    %1 = "test.op"() : () -> memref<30x20x10xf32>
// CHECK-NEXT:    %2 = bufferization.to_tensor %1 restrict writable : memref<30x20x10xf32>
// CHECK-NEXT:    %3 = bufferization.to_memref %2 read_only : memref<30x20x10xf32>
// CHECK-NEXT:    %4 = "test.op"() : () -> tensor<2x2xf64>
// CHECK-NEXT:    %5 = "test.op"() : () -> tensor<2x2xf64>
// CHECK-NEXT:    %6 = bufferization.materialize_in_destination %4 in %5 : (tensor<2x2xf64>, tensor<2x2xf64>) -> tensor<2x2xf64>
// CHECK-NEXT:  }
