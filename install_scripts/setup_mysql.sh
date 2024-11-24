#!/bin/bash

#Anything related to shellcheck doesn't not impact functionality of script. It is for vscode extension.
#shellcheck source=/dev/null
#shellcheck disable=SC2154

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR" || exit

source ./styles.sh


info_text_is_mysql="MySQL is installed already on your system, proceed to setting up databases..."
info_text_is_not_mysql="MySQL not present."
if type mysql >/dev/null 2>&1 
then
    info "$info_text_is_mysql"
else
    info "$info_text_is_not_mysql"
    sudo pacman -S mysql
    info "Downloaded MySQL service."
    handle_error "Failed to download MySQL service."
    sudo pacman -S mariadb
    info "Downloaded MariaDB service."
    handle_error "Failed to download MariaDB service."
    sudo mysql_install_db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
    info "Initialized MySQL service."
    handle_error "Failed to initialize MySQL service."
fi

sudo systemctl start mysqld
handle_error "Failed to start MySQL service."
info "MySQL service started successfully."

sudo systemctl status mysqld
handle_error "MySQL service is not active."
info "MySQL service is active."

sudo systemctl enable mysqld
handle_error "Failed to enable MySQL service."
info "MySQL service enabled to start on boot."

sudo mysql_secure_installation
handle_error "MySQL secure installation failed."
info "MySQL secure installation completed successfully."

success "MySQL successfully set up."
