resource "aws_key_pair" "deployer" {
  key_name   = "deployer-key"
  public_key = "${file("/home/seanparadiso/.ssh/id_rsa.pub")}"
}

resource "aws_security_group" "allow-ssh" {
  name        = "allow-ssh"
  description = "Allow ssh access"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags {
    Name = "allow-ssh-sg",
    Billing = "seafile"
  }
}

resource "aws_instance" "seafile_host" {
  ami           = "ami-3ecc8f46"
  instance_type = "t2.micro"
  key_name      = "deployer-key"

  connection {
    type     = "ssh"
    user     = "centos"
  }

  tags {
    Name = "seafile-host-ec2",
    Billing = "seafile"
  }

  volume_tags {
    Name = "seafile-host-volume",
    Billing = "seafile"
  }

  provisioner "remote-exec" {
    script = "../bootstrap/ec2_host_bootstrap.sh"
  }
}

resource "aws_eip" "ip" {
  instance = "${aws_instance.seafile_host.id}"
}
