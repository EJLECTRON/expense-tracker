#!/bin/bash

#Anything related to shellcheck doesn't not impact functionality of script. It is for vscode extension.
#shellcheck source=/dev/null
#shellcheck disable=SC2154
#shellcheck disable=SC2024

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR" || exit

source ./styles.sh

SQL_FILE="set_up_database.sql"

if sudo mariadb -u "root" -p < "$SQL_FILE"
then
    success "Databases created successfully."
else
    error "Databases didn't create successfully."
fi
