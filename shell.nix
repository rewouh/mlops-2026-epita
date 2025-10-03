{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
        python311
        python311Packages.numpy
        gcc
        glibc
        libcxx
        iverilog
        gtkwave
  ];

  LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
}
