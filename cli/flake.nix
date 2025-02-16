{
  description = "OCaml CLI project";

  inputs = { nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable"; };

  outputs = { self, nixpkgs }:
    let
      systems =
        [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      eachSystem = f:
        nixpkgs.lib.genAttrs systems
        (system: f (import nixpkgs { inherit system; }));
    in {
      packages = eachSystem (pkgs:
        let ocamlPackages = pkgs.ocaml-ng.ocamlPackages_5_1;
        in {
          default = ocamlPackages.buildDunePackage {
            pname = "lentil";
            version = "0.1.0";
            src = ./.;

            buildInputs = with ocamlPackages; [ base core core_unix ];
          };
        });

      devShells = eachSystem (pkgs:
        let
          ocamlPackages = pkgs.ocaml-ng.ocamlPackages_5_1;
          ocamlDeps = with ocamlPackages; [
            ocaml
            dune_3
            base
            core
            core_unix
            ocaml-lsp
            ocamlformat
            utop
            merlin
            cohttp
            async
            cohttp-async
            yojson
            ppx_deriving_yojson
          ];
          pythonDeps = with pkgs.python3.pkgs; [ numpy pip ];
          otherDeps = with pkgs; [
            uv
            stdenv.cc.cc.lib
            gcc
            python3
          ];
          allPackages = ocamlDeps ++ pythonDeps ++ otherDeps;
        in { default = pkgs.mkShell { packages = allPackages; }; });
    };
}
