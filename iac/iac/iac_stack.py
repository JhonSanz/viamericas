from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as elbv2,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
)


class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "MyVpc", max_azs=2)

        cluster = ecs.Cluster(self, "MyCluster", vpc=vpc)

        backend_task_role = iam.Role(
            self,
            "BackendTaskRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        )

        backend_task = ecs.FargateTaskDefinition(
            self, "BackendTask", task_role=backend_task_role
        )
        backend_container = backend_task.add_container(
            "BackendContainer",
            image=ecs.ContainerImage.from_registry("jhonsanz/viamericas:latest"),
            memory_limit_mib=512,
            cpu=256,
            logging=ecs.LogDriver.aws_logs(stream_prefix="backend"),
        )
        backend_container.add_port_mappings(ecs.PortMapping(container_port=8000))

        lb = elbv2.ApplicationLoadBalancer(self, "LB", vpc=vpc, internet_facing=True)

        listener = lb.add_listener("PublicListener", port=80, open=True)

        backend_service = ecs.FargateService(
            self,
            "BackendService",
            cluster=cluster,
            task_definition=backend_task,
            desired_count=1,
            assign_public_ip=True,  # Asigna una IP pública
        )

        # Create backend target group explicitly
        backend_target_group = listener.add_targets(
            "BackendTarget",
            port=8000,
            targets=[backend_service],
            health_check=elbv2.HealthCheck(
                path="/health",
                interval=Duration.seconds(30),
                timeout=Duration.seconds(10),
                unhealthy_threshold_count=3,
                healthy_threshold_count=2,
            ),
        )
