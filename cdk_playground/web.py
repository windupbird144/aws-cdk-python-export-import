from aws_cdk import Stack, CfnOutput, Fn
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

class FrontEndStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, 'vpc', vpc_name='main')

        sg = ec2.SecurityGroup(self,
                    "FrtonendSecurityGroup",
                    vpc=vpc,
                    description="Backend server",
        )

        CfnOutput(self, "FE-SG-ID",
                  value=sg.security_group_id,
                  export_name='FE-SG-ID') 

class BackendStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, 'vpc', vpc_name='main')
        
        frontend_sg = ec2.SecurityGroup.from_security_group_id(
            self,
            'FrontendSG',
            security_group_id=Fn.import_value('FE-SG-ID')    
        )
                
        sg = ec2.SecurityGroup(self,
                    "BackendSecurityGroup",
                    vpc=vpc,
                    description="Backend server",
        )
        sg.add_ingress_rule(
            peer=frontend_sg,
            description='Allow HTTPS connection from frontend',
            connection=ec2.Port.tcp(443)
        )
        sg.add_ingress_rule(
            peer=frontend_sg,
            description='Allow HTTP connection from frontend',
            connection=ec2.Port.tcp(80)
        )