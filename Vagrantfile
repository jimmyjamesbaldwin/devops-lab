Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.synced_folder 'src', '/tmp/hello-world'

  config.vm.network "forwarded_port", guest: 8080, host: 8010
  config.vm.network :forwarded_port, guest: 22, host: 2230, id: "ssh"
  #ssh vagrant@localhost -i ~/aws-ha-deployment-example/.vagrant/machines/default/virtualbox/private_key -p 2230

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "provision.yml"
  end

  config.vm.provider "virtualbox" do |vb|
    vb.memory = 512
    vb.cpus = 1
  end

end
