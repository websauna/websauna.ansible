# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "trusty64"
    config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"

    # TODO: how to port bridge to Travis?
    config.vm.network "public_network", bridge: "en0: Wi-Fi (AirPort)"
    config.ssh.forward_agent = true

    # Expose HTTP to the world for testing
    config.vm.network "forwarded_port", guest: 80, host: 1080

    # Compiling Python extensions with GCC needs more memory
    config.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--memory", "1024"]
      v.customize ["modifyvm", :id, "--cpus", 2]
    end

    config.vm.provision "ansible" do |ansible|
        ansible.playbook = "playbook-vagrant-myapp.yml"
        ansible.extra_vars = {
            public_ip: "0.0.0.0",
            server_name: "vagrant",
            # http://stackoverflow.com/a/22768453/315168
            ansible_ssh_user: 'vagrant',
            ansible_connection: 'ssh',
            ansible_ssh_args: '-o ForwardAgent=yes',
        }

        # http://stackoverflow.com/a/23704069/315168
        ansible.raw_ssh_args = ['-o UserKnownHostsFile=/dev/null']
    end
end