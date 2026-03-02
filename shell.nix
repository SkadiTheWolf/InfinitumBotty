let
    pkgs = import <nixpkgs> {};
in pkgs.mkShell {
    packages = [
        (pkgs.python3.withPackages (python-pkgs: [
            python-pkgs.virtualenv
            python-pkgs.requests
            python-pkgs.wikipedia
            python-pkgs.cython
            ]))
        ];
    }
