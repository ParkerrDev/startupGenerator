{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.python3Packages.virtualenv
    pkgs.python3Packages.ollama
  ];

  shellHook = ''
    # Create a virtual environment if it doesn't exist
    if [ ! -d ".venv" ]; then
      virtualenv .venv
    fi

    # Activate the virtual environment
    source .venv/bin/activate

    # Install Python dependencies
    pip install -r requirements.txt || true
  '';
}