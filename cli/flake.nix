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
        let ocamlPackages = pkgs.ocamlPackages;
        in {
          default = ocamlPackages.buildDunePackage {
            pname = "lentil";
            version = "0.1.0";
            src = ./.;

            buildInputs = with ocamlPackages; [ base core core_unix ];
          };
        });

      devShells = eachSystem (pkgs:
        let ocamlPackages = pkgs.ocamlPackages;
        in {
          default = pkgs.mkShell {
            packages = with ocamlPackages; [
              ocaml
              dune_3
              base
              core
              core_unix
              ocaml-lsp
              ocamlformat
              utop
            ];
          };
        });
    };
}
