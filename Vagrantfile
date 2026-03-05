Vagrant.configure("2") do |config|
  # Box
  config.vm.box = "ubuntu/bionic64"

  # Configuración de VirtualBox
  config.vm.provider "virtualbox" do |vb|
   vb.memory = "2048"
   vb.cpus = 1
  end

  # Redireccionar puerto para acceder a FastAPI desde el host
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  # Provisión para instalar Docker y Docker Compose
  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y docker.io docker-compose
    sudo usermod -aG docker vagrant
  SHELL
end