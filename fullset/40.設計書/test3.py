from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, AutoScaling
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB, InternetGateway, NATGateway, PrivateSubnet, PublicSubnet, Route53 , CloudFront , ALB
from diagrams.aws.security import WAF, ACM
from diagrams.aws.storage import EFS, S3
from diagrams.aws.general import InternetAlt1

with Diagram("AWS Architecture Diagram", show=False, direction="LR"):
    internet = InternetAlt1("Internet")

    with Cluster("VPC"):
        alb = ALB("ALB")

        with Cluster("Public Subnet"):
            igw = InternetGateway("Internet Gateway")
            nat_gateway = NATGateway("NAT Gateway")
            bastion = EC2("Bastion")

        with Cluster("Private Subnet"):
            efs = EFS("EFS (for AutoScaling Group)")
            rds = RDS("RDS (Database)")

            autoscaling_group = AutoScaling("AutoScaling Group")

    waf = WAF("WAF")
    cloudfront = CloudFront("CloudFront")
    route53 = Route53("example.com")
    acm = ACM("example.com")

    alb >> autoscaling_group
    internet >> cloudfront
    internet >> igw
    igw >> internet

    internet >> route53
    route53 >> internet

    route53 >> acm
    acm >> cloudfront
    acm >> alb

    igw << nat_gateway 
    nat_gateway << autoscaling_group
    autoscaling_group >> rds
    autoscaling_group >> efs
    bastion >> autoscaling_group

    s3 = S3("S3 (Static Hosting)")
    logs_bucket = S3("S3 (Logs Bucket)")
    cloudfront >> s3
    cloudfront >> waf
    cloudfront >> alb
    waf >> cloudfront

    [cloudfront, waf] >>Edge(label="log")>> logs_bucket
    autoscaling_group >>Edge(label="log")>> logs_bucket
    rds >>Edge(label="log")>> logs_bucket

