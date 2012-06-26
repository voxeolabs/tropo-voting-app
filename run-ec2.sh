UBUNTU_AMI="ami-82fa58eb"
INSTANCE_TYPE="t1.micro"
CURDIR=`pwd`

cd ~/.ec2
source dexy-env.sh

ec2-run-instances $UBUNTU_AMI -k $EC2_KEYPAIR -t $INSTANCE_TYPE \
  --instance-initiated-shutdown-behavior stop \
  -f $CURDIR/ubuntu-setup.sh
