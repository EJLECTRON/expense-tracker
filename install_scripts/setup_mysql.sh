#!/bin/bash

#https://dev.to/tinapyp/installing-and-configuring-mysql-on-arch-linux-11m1
#https://dev.to/sujit-shrc/mariadb-installation-made-easy-a-guide-for-arch-based-linux-users-19o4

#Anything related to shellcheck doesn't not impact functionality of script. It is for vscode extension.
#shellcheck source=/dev/null
#shellcheck disable=SC2154

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR" || exit

source ./styles.sh


info_text_is_mysql="MySQL is installed already on your system, proceed to setting up databases..."
info_text_is_not_mysql="MySQL not present."

if mysqld --version && mariadb --version
then
    info "$info_text_is_mysql"
else
    info "$info_text_is_not_mysql"

    # Install MariaDB
    pacman -Qi mariadb >/dev/null 2>&1 || sudo pacman -S mariadb
    handle_error "Failed to install MariaDB."
    info "MariaDB installed successfully."

    # Initialize MariaDB
    sudo mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mariadb
    handle_error "Failed to initialize MariaDB database."
    info "MariaDB database initialized."

    # Install MySQL
    pacman -Qi mysql >/dev/null 2>&1 || sudo pacman -S mysql
    handle_error "Failed to install MySQL."
    info "MySQL installed successfully."

    # Initialize MySQL
    sudo mysql_install_db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
    handle_error "Failed to initialize MySQL database."
    info "MySQL database initialized."
fi

# Start MySQL service
sudo systemctl start mysqld
handle_error "Failed to start MySQL service."
info "MySQL service started."

# Start MariaDB service
sudo systemctl start mariadb
handle_error "Failed to start MariaDB service."
info "MariaDB service started."

# Enable MySQL service at startup
sudo systemctl enable mysqld
handle_error "Failed to enable MySQL service at startup."
info "MySQL service enabled at startup."

# Enable MariaDB service at startup
sudo systemctl enable mariadb
handle_error "Failed to enable MariaDB service at startup."
info "MariaDB service enabled at startup."

# Secure MySQL installation
sudo mysql_secure_installation
handle_error "Failed to secure MySQL installation."
info "MySQL installation secured."

# Secure MariaDB installation
sudo mariadb-secure-installation
handle_error "Failed to secure MariaDB installation."
info "MariaDB installation secured."

success "MySQL successfully set up."
