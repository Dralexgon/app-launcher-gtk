{
  description = "A flake for a GTK4 development environment with Python bindings";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }:
  let
    pkgs = nixpkgs.legacyPackages."x86_64-linux";
  in
  {
    devShell."x86_64-linux" = pkgs.mkShell
    {
      packages = [
        pkgs.gtk4
        pkgs.cairo #if venv
        pkgs.pkg-config #if venv
        (pkgs.python3.withPackages (python-pkgs: [
          python-pkgs.pygobject3
        ]))
      ];

      shellHook = ''
        echo "Nix develop successful !"
      '';
    };
  };
}
