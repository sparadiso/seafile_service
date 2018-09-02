
resource "aws_instance" "seafile_host" {
  ami           = "ami-3ecc8f46"
  instance_type = "t2.micro"

  provisioner "remote-exec" {
    script = "../bootstrap/ec2_host_bootstrap.sh"
  }
}

resource "aws_eip" "ip" {
  instance = "${aws_instance.seafile_host.id}"
}
