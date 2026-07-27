#!/usr/bin/env bash
#
# Build the Tree-sitter grammars used by the path-context generators
# (generate_path_contexts.py) and the adversarial-rule verifier
# (adversarial_sample_verification.py).
#
# Grammar revisions are pinned. Tree-sitter's parser ABI changes between minor
# releases, and this project is pinned to tree-sitter==0.21.3 (see
# requirements.txt), so building against grammar HEAD will produce shared
# objects the Python bindings refuse to load.
#
# Usage:
#   scripts/build-tree-sitter.sh [output-dir]
#
# Default output dir is $TREE_SITTER_SO_DIR, falling back to ./tree-sitter-so.
# Re-running is cheap: grammars that are already built are skipped.

set -euo pipefail

OUT_DIR="${1:-${TREE_SITTER_SO_DIR:-$(pwd)/tree-sitter-so}}"
SRC_DIR="${TREE_SITTER_SRC_DIR:-${TMPDIR:-/tmp}/tree-sitter-src}"

# name<TAB>repo<TAB>pinned-tag
GRAMMARS=$(
    cat <<'EOF'
c	https://github.com/tree-sitter/tree-sitter-c.git	v0.20.7
cpp	https://github.com/tree-sitter/tree-sitter-cpp.git	v0.20.5
java	https://github.com/tree-sitter/tree-sitter-java.git	v0.20.2
python	https://github.com/tree-sitter/tree-sitter-python.git	v0.20.4
javascript	https://github.com/tree-sitter/tree-sitter-javascript.git	v0.20.4
ruby	https://github.com/tree-sitter/tree-sitter-ruby.git	v0.20.1
c-sharp	https://github.com/tree-sitter/tree-sitter-c-sharp.git	v0.20.0
EOF
)

mkdir -p "$OUT_DIR" "$SRC_DIR"

while IFS=$'\t' read -r name repo tag; do
    [ -n "$name" ] || continue

    so="$OUT_DIR/tree-sitter-${name}.so"
    if [ -f "$so" ]; then
        echo "[skip]  tree-sitter-${name}.so already built"
        continue
    fi

    checkout="$SRC_DIR/tree-sitter-${name}"
    if [ ! -d "$checkout" ]; then
        echo "[clone] ${name} @ ${tag}"
        git clone --quiet --depth 1 --branch "$tag" "$repo" "$checkout"
    fi

    # Tagged releases ship a pre-generated src/parser.c. Only fall back to the
    # tree-sitter CLI (which needs Node) when it is genuinely absent.
    if [ ! -f "$checkout/src/parser.c" ]; then
        echo "[gen]   ${name}: src/parser.c missing, running tree-sitter generate"
        (cd "$checkout" && npx --yes tree-sitter-cli generate)
    fi

    sources=("$checkout/src/parser.c")
    compiler=gcc
    if [ -f "$checkout/src/scanner.c" ]; then
        sources+=("$checkout/src/scanner.c")
    elif [ -f "$checkout/src/scanner.cc" ]; then
        # A few grammars (older tree-sitter-ruby) ship a C++ external scanner.
        sources+=("$checkout/src/scanner.cc")
        compiler=g++
    fi

    echo "[build] tree-sitter-${name}.so (${compiler}, ${#sources[@]} source file(s))"
    "$compiler" -shared -fPIC -O2 -I"$checkout/src" "${sources[@]}" -o "$so"
done <<<"$GRAMMARS"

echo
echo "Grammars built in: $OUT_DIR"
ls -1 "$OUT_DIR"
