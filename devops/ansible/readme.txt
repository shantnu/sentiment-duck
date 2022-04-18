
create vars/pass.yml, then:

ansible-playbook -i hosts ./main.yml --private-key ~/.ssh/ec2.pem --ask-vault-pass
