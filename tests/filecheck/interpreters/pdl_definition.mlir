pdl.pattern : benefit(1) {
    %in_type = pdl.type: i32
    %x = pdl.operand : %in_type
    %y = pdl.operand : %in_type
    %root_addi = pdl.operation "arith.addi" (%x,%y: !pdl.value, !pdl.value)  -> (%in_type: !pdl.type)
    %a = pdl.result 0 of %root_addi
    %root_subi = pdl.operation "arith.subi" (%a,%y: !pdl.value, !pdl.value)  -> (%in_type: !pdl.type)
    pdl.rewrite %root_subi {
      %zero_attr = pdl.attribute = 0
      %zero_op = pdl.operation "arith.constant" {"value" = %zero_attr} -> (%in_type: !pdl.type)
      %zero = pdl.result 0 of %zero_op
      %new_addi = pdl.operation "arith.addi" (%x,%zero: !pdl.value, !pdl.value)  -> (%in_type: !pdl.type)
      pdl.replace %root_subi with %new_addi
      pdl.erase %root_addi
    }
}
