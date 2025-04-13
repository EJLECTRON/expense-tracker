#!/bin/bash

# https://dev.to/tinapyp/installing-and-configuring-mysql-on-arch-linux-11m1
# https://dev.to/sujit-shrc/mariadb-installation-made-easy-a-guide-for-arch-based-linux-users-19o4

# Anything related to shellcheck doesn't impact functionality of script. It is for VS Code extension.
# shellcheck source=/dev/null
# shellcheck disable=SC2154

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR" || exit

source ./styles.sh

is_sql_installed=false

# Check if either MySQL or MariaDB is installed
if command -v mysql >/dev/null 2>&1 || command -v mariadb >/dev/null 2>&1; then
    info "MySQL or MariaDB is already installed. Proceeding to service setup..."
    is_sql_installed=true
else
    info "MySQL or MariaDB not found. Installing MariaDB..."

    # Update and install MariaDB (preferred on Ubuntu)
    sudo apt update
    sudo apt install -y mariadb-server
    handle_error "Failed to install MariaDB."
    info "MariaDB installed successfully."
fi

# Start MariaDB service
sudo systemctl start mariadb
handle_error "Failed to start MariaDB service."
info "MariaDB service started."

# Enable MariaDB to start on boot
sudo systemctl enable mariadb
handle_error "Failed to enable MariaDB service at startup."
info "MariaDB service enabled at startup."

if [ "$is_sql_installed" = false ]; then
    # Secure MariaDB installation
    sudo mysql_secure_installation
    handle_error "Failed to secure MariaDB installation."
    info "MariaDB installation secured."
fi

success "MariaDB successfully set up on Ubuntu."
