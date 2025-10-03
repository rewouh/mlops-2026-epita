module linear_reg (
    input  [15:0] size,
    output [31:0] price
);

    wire [31:0] p_result;
    wire [31:0] add_result;

    multiplier16 mult (
        .a(size),
        .b(16'd5000),
        .p(p_result)
    );

    assign price = p_result + 32'd10000;

endmodule

