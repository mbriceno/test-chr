# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  # config.vm.boot_timeout = 960

  # config.ssh.forward_agent = true
  # config.vm.network "forwarded_port", guest: 22, host:2222, id: "ssh", auto_correct: true
  config.vm.network "forwarded_port", guest: 80, host: 80
  config.vm.network "forwarded_port", guest: 8001, host: 8001
  config.vm.network "forwarded_port", guest: 5432, host: 5433
  # config.vm.network "forwarded_port", guest: 6379, host: 6379

  config.vm.network "private_network", ip: "192.168.56.13"

  config.vm.provider "virtualbox" do |vb|
    # vb.gui = true
    vb.cpus = 2
    # Customize the amount of memory on the VM:
    vb.memory = "2048"
  end

end
