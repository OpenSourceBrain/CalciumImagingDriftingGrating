set -e

convert *0.tiff   -auto-level  -set filename: "%t" ../jpg/%[filename:].jpg
