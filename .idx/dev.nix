{ pkgs, ... }: {
  channel = "stable-24.05";

  packages = [
    pkgs.python311
    pkgs.python311Packages.pip
  ];

  env = {};

  idx = {
    extensions = [
      "ms-python.python"
    ];

    previews = {
      enable = true;
    };

    workspace = {
      onCreate = {
        setup = "pip install -r requirements.txt || true";
      };
      onStart = {
        # Optional auto run: python3 devan_runner.py
      };
    };
  };
}
