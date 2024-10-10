#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_playground.web import BackendStack,FrontEndStack

env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
app = cdk.App()
BackendStack(app, "BackendStack", env=env)
FrontEndStack(app, "FrontendStack", env=env)
app.synth()
