module multiplier32 (
    input  [31:0] a,
    input  [31:0] b,
    output [63:0] p
);

    assign p = a * b;

endmodule

