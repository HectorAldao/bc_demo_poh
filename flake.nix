{
  description = "Plantilla de entorno Python (copiar y rellenar)";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, ... }: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};

    # Cambia aquí la versión de Python para todo el entorno (313, 312, 311...)
    python = pkgs.python313;
  in {
    devShells.${system}.default = pkgs.mkShell {
      packages = [
        # ============================================================
        #  AÑADE TUS PAQUETES AQUÍ
        #  Casi todo lo que hay en PyPI ya está empaquetado en nixpkgs.
        #  Búscalo con:  nix search nixpkgs <nombre>
        #  o en https://search.nixos.org/packages (filtro "Python packages")
        # ============================================================
        (python.withPackages (ps: with ps; [
          # --- paquetes de nixpkgs ---
          # requests
          numpy
          #pandas
	  matplotlib
          # ipykernel   # descomenta para el kernel de VS Code / Jupyter
          # tkinter     # descomenta si necesitas Tk

          # --- paquete de PyPI que NO está en nixpkgs (sdist) ---
          # (buildPythonPackage rec {
          #   pname = "nombre-paquete";
          #   version = "1.2.3";
          #   src = pkgs.fetchPypi {
          #     inherit pname version;
          #     hash = "sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=";
          #     # El hash de arriba es de mentira: ponlo vacío ("") y Nix
          #     # te mostrará el hash correcto al fallar la primera build.
          #   };
          #   pyproject = true;
          #   build-system = [ setuptools wheel ];
          #   # Dependencias Python del paquete:
          #   # propagatedBuildInputs = [ requests ];
          #   # Dependencias nativas (C):
          #   # buildInputs = [ pkgs.openssl ];
          # })

          # --- paquete de PyPI que SOLO existe como wheel binario ---
          # (buildPythonPackage rec {
          #   pname = "nombre-paquete";
          #   version = "1.2.3";
          #   format = "wheel";
          #   src = pkgs.fetchurl {
          #     url = "https://files.pythonhosted.org/packages/.../paquete-1.2.3-cp313-cp313-manylinux_x86_64.whl";
          #     hash = "sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=";
          #   };
          #   nativeBuildInputs = [ pkgs.autoPatchelfHook ];  # repara los enlaces dinámicos
          #   buildInputs = [ pkgs.stdenv.cc.cc.lib pkgs.zlib ];
          #   pythonImportsCheck = [ "nombre_paquete" ];
          # })
        ]))

        # Herramientas de sistema
        pkgs.pkg-config

        # Librerías nativas (descomenta las que necesites; si un paquete
        # Python pide una .so, suele ir aquí, no solo en LD_LIBRARY_PATH)
        # pkgs.openssl
        # pkgs.libffi
        # pkgs.tk
        # pkgs.tcl
      ];

      # Librerías que los binarios/wheels buscan en tiempo de ejecución.
      # Si algo falla con "libX.so not found", añade la librería aquí.
      env.LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
        pkgs.stdenv.cc.cc.lib # libstdc++, libgcc_s
        pkgs.libgcc.lib
        pkgs.zlib              # libz
        pkgs.zeromq            # necesario para el backend de Jupyter
        # pkgs.dbus
        # pkgs.glib
      ];

      shellHook = ''
        # Para que Python encuentre módulos del directorio actual:
        export PYTHONPATH="$PYTHONPATH:$(pwd)"

        # ------------------------------------------------------------
        # VÁLVULA DE ESCAPE: venv + pip (solo para probar rápido)
        # Dentro de este shell, pip SÍ puede funcionar porque
        # LD_LIBRARY_PATH ya apunta a las librerías de Nix:
        #   python -m venv .pyenv
        #   source .pyenv/bin/activate
        #   pip install <paquete>
        # OJO: es reproducible solo en tu máquina. Cuando el paquete te
        # sirva, pásalo al flake (bloque de arriba) y borra el venv.
        # ------------------------------------------------------------
      '';
    };
  };
}
