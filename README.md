# StreamCo DevOps Lab

Technical assessment for DevOps candidates.

Nobody asked me to do this but I was bored.

<img src="https://i0.wp.com/www.awsomeblog.com/wp-content/uploads/2014/05/photo.png" width="100"><img src="https://s3.amazonaws.com/hashicorp-marketing-web-assets/brand/Vagrant_VerticalLogo_FullColor.rkvQk0Hax.svg" width="100"><img src="https://www.datocms-assets.com/2885/1506457192-blog-packer-list.svg" width="100"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/2000px-Python-logo-notext.svg.png" width="100">

## Overview
Summary: Using AWS Cloudformation, automate the deployment of secure, publicly available HA Load-Balanced Web Servers. [More details](https://github.com/StreamCo/devops-lab)

## Solution
I wanted to use [Packer](https://www.packer.io) for this task, so I build an AMI based on Ubuntu which is then provisioned by Ansible. Ansible executes a hardening role courtesy of [dev-sec.io](https://dev-sec.io), then installs the dependencies for the web application. Local development is enabled by using Vagrant, which allows for consistency as local dev will use the same provisioning mechanism that will end up in the finished AMI. The provisioning process installs python dependencies, creates a local account to run the application, checks out the application source, and sets up [Supervisord](http://supervisord.org/) to configure the application launch. The CloudFormation stack creates multiple EC2 instances using the Packer image, behind an ELB for resiliency, which handles SSL termination and makes use of a selfsigned certificates. The EC2 instances run a small Flask api to serve content.

## Build
### Deploying on AWS
Deploying on AWS is simple and requires generating a certificate before running the CloudFormation template to setup the infrastructure. You can generate and deploy a certificate to AWS using the following commands assuming you have aws-cli installed:

```
openssl genrsa -des3 -out domain.key 1024
openssl req -nodes -newkey rsa:2048 -keyout domain.key -out domain.csr
cp domain.key domain.key.password
openssl rsa -in domain.key.password -out domain.key
openssl x509 -req -days 365 -in domain.csr -signkey domain.key -out domain.crt

aws iam upload-server-certificate \
--server-certificate-name mysslcert \
--certificate-body file://domain.crt \
--private-key file://domain.key
```

Now run Packer and generate your AMI:
```
ansible-galaxy install -r requirements.yml
./packer build packer.json
```

You can now run the CloudFormation template, fill in the requested variables, and it will output the DNS alias of the load balancer endpoint when deployment is complete:

![hello-world](https://media.giphy.com/media/fsc7c6t2RAOadx27gG/giphy.gif)


### Local Development
You can try out the build locally on your machine simply by running
```
ansible-galaxy install -r requirements.yml
vagrant up
```
and heading to localhost:8010. You can ssh onto the box if you want to fiddle around, using the following command:

`ssh vagrant@localhost -i .vagrant/machines/default/virtualbox/private_key -p 2230`. Provisioning the machine takes a couple of minutes because of the hardening process.

### To Do
* Come up with a better software deployment mechanism; something that would allow easier deploys and blue/green deployment


