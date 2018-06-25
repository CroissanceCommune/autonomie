Vagrant.configure("2") do |config|
  config.vm.box = "debian/stretch64"
  config.vm.hostname = 'mariadb-server'

  config.vm.network "forwarded_port", guest: 3306, host: 13306

  # Prevent TTY Errors (copied from laravel/homestead: "homestead.rb" file)... By default this is "bash -l".
  config.ssh.shell = "bash"
  config.vm.provision "shell", privileged: true, inline: <<-SHELL
    #!/usr/bin/env bash

    sudo debconf-set-selections <<< 'mariadb-server mariadb-server/root_password password root'
    sudo debconf-set-selections <<< 'mariadb-server mariadb-server/root_password_again password root'
    sudo apt-get update
    sudo apt-get -y install mariadb-server
    sed -i s/127.0.0.1/0.0.0.0/ /etc/mysql/mariadb.conf.d/50-server.cnf
    sudo systemctl restart mariadb

    APP_DB_USER=autonomie
    APP_DB_NAME=autonomie
    APP_DB_PASS=autonomie

    cat << EOF | sudo su -c mysql -- -u root -proot
      SET GLOBAL max_connect_errors=10000;

      DROP USER IF EXISTS $APP_DB_USER;
      DROP DATABASE  IF EXISTS $APP_DB_USER;
      CREATE DATABASE $APP_DB_NAME;
      CREATE USER '$APP_DB_USER' IDENTIFIED BY '$APP_DB_PASS';
      GRANT ALL PRIVILEGES ON $APP_DB_NAME.* TO '$APP_DB_USER';
      FLUSH PRIVILEGES;
EOF
  SHELL
end
