`timescale 1ns / 1ps
module stimulus;

    // Inputs
    reg [7:0] a;
    reg [7:0] b;

    // Output
    wire [15:0] s;

    adder16 uut (
        .a(a),
        .b(b),
        .s(s)
    );

    initial begin
        $dumpfile("test.vcd");
        $dumpvars(0, stimulus);

        a = 8'd0;   b = 8'd0;   #20;
        a = 8'd5;   b = 8'd10;  #20;
        a = 8'd100; b = 8'd50;  #20;
        a = 8'd200; b = 8'd100; #20;
        a = 8'd255; b = 8'd255; #20;

        #20;
    end

    initial begin
        $monitor("t=%3d a=%d, b=%d => sum=%d", $time, a, b, s);
    end

endmodule

