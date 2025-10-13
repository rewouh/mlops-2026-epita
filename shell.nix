{ pkgs ? import <nixpkgs> {
    config = {
      cudaSupport = true;
      allowUnfreePredicate = pkg:
        builtins.elem (pkgs.lib.getName pkg) [
          "cuda_cudart"
          "libcublas"
          "cuda_cccl"
          "cuda_nvcc"
        ];
    };
  }
}:

pkgs.mkShell {
  buildInputs = with pkgs; [
        python311
        gcc
        glibc
        glibc.bin
        libcxx
        iverilog
        gtkwave
  ];

  shellHook = ''
    export LD_LIBRARY_PATH=/run/opengl-driver/lib:${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
  '';
}
