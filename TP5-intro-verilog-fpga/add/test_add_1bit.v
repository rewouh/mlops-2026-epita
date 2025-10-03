`timescale 1ns / 1ps
module stimulus;

    // Inputs
    reg a;
    reg b;
    reg cin;

    // Outputs
    wire s;
    wire cout;

    full_adder uut (
        .a(a),
        .b(b),
        .cin(cin),
        .s(s),
        .cout(cout)
    );

    initial begin
        $dumpfile("test.vcd");
        $dumpvars(0, stimulus);

        a = 0; b = 0; cin = 0; #20;
        a = 0; b = 0; cin = 1; #20;
        a = 0; b = 1; cin = 0; #20;
        a = 0; b = 1; cin = 1; #20;
        a = 1; b = 0; cin = 0; #20;
        a = 1; b = 0; cin = 1; #20;
        a = 1; b = 1; cin = 0; #20;
        a = 1; b = 1; cin = 1; #20;

        #20;
    end

    initial begin
        $monitor("t=%3d a=%d, b=%d, cin=%d => sum=%d, cout=%d", 
                  $time, a, b, cin, s, cout);
    end

endmodule

