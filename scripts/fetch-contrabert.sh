#!/usr/bin/env bash
#
# Download the ContraBERT_C and ContraBERT_G checkpoints.
#
# Unlike every other model in the study, ContraBERT is not on the Hugging Face
# Hub — the authors distribute it through Google Drive. run-contrabert_c-cv.sh
# and run-contrabert_g-cv.sh expect the checkpoints at ./ContraBERT_C and
# ./ContraBERT_G in the repository root, which is where this script puts them.
#
# Usage:
#   scripts/fetch-contrabert.sh
#
# Google Drive folder downloads need an interactive consent step, so this uses
# gdown. If it fails (quota, or Drive asking for a captcha), download the two
# folders by hand from the links in ContraBERT.md and unpack them to the paths
# above; nothing else in the pipeline depends on how they got there.

set -euo pipefail

cd "$(dirname "$0")/.."

CONTRABERT_C_FOLDER="1F-yIS-f84uJhOCzvGWdMaOeRdLsVWoxN"
CONTRABERT_G_FOLDER="1t8VX6aYchpJolbH4mkhK3IQGzyHrDD3C"

if ! python -c "import gdown" 2>/dev/null; then
    echo "Installing gdown (not part of requirements.txt: only this script uses it)..."
    python -m pip install --quiet gdown
fi

fetch() {
    local name="$1" folder_id="$2"

    if [ -d "$name" ] && [ -n "$(ls -A "$name" 2>/dev/null)" ]; then
        echo "[skip]  ./${name} already present"
        return
    fi

    echo "[fetch] ${name} from Google Drive..."
    if ! python -m gdown --folder "https://drive.google.com/drive/folders/${folder_id}" -O "$name"; then
        echo
        echo "Automated download of ${name} failed." >&2
        echo "Download it manually — see the links in ContraBERT.md — and unpack it to ./${name}" >&2
        return 1
    fi
}

status=0
fetch ContraBERT_C "$CONTRABERT_C_FOLDER" || status=1
fetch ContraBERT_G "$CONTRABERT_G_FOLDER" || status=1

if [ "$status" -eq 0 ]; then
    echo
    echo "ContraBERT checkpoints ready. Fine-tune them with:"
    echo "  cd LeetCode/ContraBERT_C && ../../run-contrabert_c-cv.sh 10"
fi

exit "$status"
