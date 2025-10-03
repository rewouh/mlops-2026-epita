`timescale 1ns / 1ps
module stimulus;

    // Inputs
    reg [15:0] a;
    reg [15:0] b;

    // Output
    wire [31:0] p;

    multiplier16 uut (
        .a(a),
        .b(b),
        .p(p)
    );

    initial begin
        $dumpfile("test.vcd");
        $dumpvars(0, stimulus);

        a = 16'd0;     b = 16'd0;     #20;
        a = 16'd5;     b = 16'd10;    #20;
        a = 16'd123;   b = 16'd45;    #20;
        a = 16'd1000;  b = 16'd2000;  #20;
        a = 16'd65535; b = 16'd2;     #20;
        a = 16'd65535; b = 16'd65535; #20;

        #20;
    end

    initial begin
        $monitor("t=%3d a=%d, b=%d => product=%d", 
                  $time, a, b, p);
    end

endmodule

