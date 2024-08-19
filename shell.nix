{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    python3Packages.boto3
    python3Packages.botocore
  ];

  shellHook = ''
    echo "Python environment for S3 bucket logging script, chill i wont build anything else"
  '';
}
