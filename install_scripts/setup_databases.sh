#!/bin/bash

#Anything related to shellcheck doesn't not impact functionality of script. It is for vscode extension.
#shellcheck source=/dev/null
#shellcheck disable=SC2154

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR" || exit

source ./styles.sh


success "Databases created successfully."
