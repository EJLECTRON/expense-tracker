#!/bin/bash

#line for vscode extension shellcheck
#shellcheck source=/dev/null

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR" || exit

source ./styles.sh


bash setup_mysql.sh
bash setup_databases.sh

success "Installation succeed! Enjoy using expence tracker. You can contribute to my project on GitHub: https://github.com/EJLECTRON/expence-tracker.git"
