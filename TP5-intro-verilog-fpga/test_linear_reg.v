`timescale 1ns/1ps
module stimulus;

    reg [15:0] size;
    wire [31:0] price;

    linear_reg uut (
        .size(size),
        .price(price)
    );

    initial begin
        $dumpfile("test.vcd");
        $dumpvars(0, stimulus);

        size = 0;      #20;
        size = 1;      #20;
        size = 10;     #20;
        size = 100;    #20;
        size = 500;    #20;
        size = 1000;   #20;

        #20;
    end

    initial begin
        $monitor("t=%3d size=%d => price=%d", $time, size, price);
    end

endmodule

