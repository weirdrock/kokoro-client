let
    pins = import ./npins;
    pkgs = import pins.nixpkgs {};
in

pkgs.mkShell rec {
    nativeBuildInputs = with pkgs; [
        uv
        python313
        espeak-ng
        portaudio
        linuxPackages.nvidia_x11
        
    ];
    LD_LIBRARY_PATH = "${pkgs.lib.makeLibraryPath nativeBuildInputs}";
    CUDA_PATH = "${pkgs.cudatoolkit}";
}
