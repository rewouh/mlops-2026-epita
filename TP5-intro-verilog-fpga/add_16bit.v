module adder16 (
    input  [7:0] a,
    input  [7:0] b,
    output [15:0] s
);

    assign s = a + b;

endmodule

