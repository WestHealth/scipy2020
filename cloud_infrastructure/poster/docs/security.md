# Security and Compliance

## Encryption in Transit

![Encryption in Transit](encryption-in-transit.svg)


Be sure all communications is encrypted

  * All communications from outside to ALB
  * All communications from ALB to ECS instances
  * All communication from ECS instances to shared drives

## Encryption at Rest

![Encryption in Transit](encryption-at-rest.svg)

Be sure all storage devices are encrypted

  * All shared drives (EFS or ObjectiveFS) especially NFS
  * All drives connected to the ECS instances (EBS)
  * All Amazon Machine Instances (AMI)

## Access Control

  * Use [AWS Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html)
  * Use Firewall to control container outbound traffic
  * Direct outbound traffic to a proxy
  * Block access to AWS's metadata ip addresses

Example IP Tables can be found [here](https://github.com/WestHealth/scipy2020/tree/master/cloud_infrastructure/supplemental_code/iptables). Sample of how to set the proxy environemnt is given [here](https://github.com/WestHealth/scipy2020/tree/master/cloud_infrastructure/supplemental_code/docker_proxy).


## Auditing

   * Use the ALB logging to track access
   * Use a logging agent to track potential privilege escalation
   * ALB logs to an S3 bucket, use a log management tool for easier analysis
   * Put the target bucket in a separate AWS account so it cannot be deleted by the logger
   * Supplement monitoring by installing logging agents on each EC2 instance
   * Use a log management tool to provide alarms when severe incidents.

## Other Useful Agents

![Other Agents](agents.svg)

   * Keep ECS Agent up to date
   * AWS Systems Manager (SSM) makes it easier to manage the EC2
   * Make sure anti-virus agents are container aware 
   * an intrusion detection agent can look for high risk
   
