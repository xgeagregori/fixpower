import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as apiGateway from "aws-cdk-lib/aws-apigateway";

export class ApiStack extends cdk.Stack {
  public readonly api: apiGateway.RestApi;

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const api = new apiGateway.RestApi(this, "RestApi", {
      restApiName: "FixNPower REST Api",
    });

    this.api = api;

    // Output stage prod url for the API
    new cdk.CfnOutput(this, "ApiGatewayUrl", {
      value: api.url
    });
  }
}
