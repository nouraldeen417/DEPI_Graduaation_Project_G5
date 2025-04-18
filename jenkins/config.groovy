// repo/jenkins/JenkinsVarFile.groovy
def config = [
    HOST_SUBSET_ONPREM = 'on_prems' , // Define the host subset in ansible inventory
    HOST_SUBSET_AWS = 'aws_ec2'  ,// Define the host subset in ansible inventory 
    CREDENTIALS_AWS_ACCOUNT = 'aws-credentials', // AWS credentials ID
    CREDENTIALS_AWS_SSH = 'aws_ec2_ssh_key' ,// AWS credentials ID        
    CREDENTIALS_ONPREM_SERVER = 'jenkins-remote-credentials' // Jenkins remote credentials ID
    CREDENTIALS_KUBECONFIG = 'kubeconfig-secret' ,// Kubeconfig secret ID
    CREDENTIALS_DOCKERHUB = 'dockerhub', // Docker Hub credentials ID
    CREDENTIALS_SLACK = 'slack' ,// Slack credentials ID
    DOCKER_REGISTRY = 'your-docker-registry', // e.g., Docker Hub
    IMAGE_NAME = "nouraldeen152/networkapp",
    IMAGE_TAG =  "${params.CUSTOM_BUILD_NUMBER}" ,// Use custom build number or default to BUILD_NUMBER
    REMOTE_USER = 'jenkins-remote',
    REMOTE_HOST = '192.168.1.150',
    REMOTE_DIR = "/home/jenkins-remote/",
    KUBECONFIG = "${WORKSPACE}/.kube/config",
    AWS_SSH_KEY = "${WORKSPACE}/.ssh/ssh_key.pem",
    SLACK_CHANNEL = "#team-project" // Slack channel to send notifications

]
return config