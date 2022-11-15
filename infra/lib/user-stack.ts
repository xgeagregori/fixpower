import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as apiGateway from "aws-cdk-lib/aws-apigateway";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";

interface UserProps extends cdk.StackProps {
  apiGateway: apiGateway.RestApi;
}

export class UserStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: UserProps) {
    super(scope, id, props);

    const userTable = new dynamodb.Table(this, "Users", {
      partitionKey: {
        name: "id",
        type: dynamodb.AttributeType.STRING,
      },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    userTable.addGlobalSecondaryIndex({
      indexName: "username",
      partitionKey: {
        name: "username",
        type: dynamodb.AttributeType.STRING,
      },
      readCapacity: 1,
      writeCapacity: 1,
      projectionType: dynamodb.ProjectionType.ALL,
    });

    const userLambda = new lambda.Function(this, "userApi", {
      runtime: lambda.Runtime.PYTHON_3_9,
      code: lambda.Code.fromAsset("../user/app"),
      handler: "user_controller.handler",
      environment: {
        TABLE_NAME: userTable.tableName,
      },
      timeout: cdk.Duration.seconds(30),
    });

    userTable.grantReadWriteData(userLambda);

    props?.apiGateway.root
      .addResource("user-api")
      .addResource("v1")
      .addProxy({
        defaultIntegration: new apiGateway.LambdaIntegration(userLambda),
      })
      .addCorsPreflight({
        allowHeaders: [
          "Content-Type",
          "X-Amz-Date",
          "Authorization",
          "X-Api-Key",
        ],
        allowMethods: ["OPTIONS", "GET", "POST", "PUT", "PATCH", "DELETE"],
        allowCredentials: true,
        allowOrigins: ["*"],
      });

    // Output arn of the lambda function
    new cdk.CfnOutput(this, "UserLambdaArn", {
      value: userLambda.functionArn,
    });

    // Output name of the table
    new cdk.CfnOutput(this, "UserTableName", {
      value: userTable.tableName,
    });
  }
}
