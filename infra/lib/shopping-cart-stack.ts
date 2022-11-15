import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as apiGateway from "aws-cdk-lib/aws-apigateway";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";

interface ShoppingCartProps extends cdk.StackProps {
  apiGateway: apiGateway.RestApi;
}

export class ShoppingCartStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: ShoppingCartProps) {
    super(scope, id, props);

    const shoppingCartTable = new dynamodb.Table(this, "ShoppingCarts", {
      partitionKey: {
        name: "id",
        type: dynamodb.AttributeType.STRING,
      },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const shoppingCartLambda = new lambda.Function(this, "ShoppingCartApi", {
      runtime: lambda.Runtime.PYTHON_3_9,
      code: lambda.Code.fromAsset("../shopping-cart/app"),
      handler: "shopping_cart_controller.handler",
      environment: {
        TABLE_NAME: shoppingCartTable.tableName,
      },
      timeout: cdk.Duration.seconds(30),
    });

    shoppingCartTable.grantReadWriteData(shoppingCartLambda);

    props?.apiGateway.root
      .addResource("shopping-cart-api")
      .addResource("v1")
      .addProxy({
        defaultIntegration: new apiGateway.LambdaIntegration(
          shoppingCartLambda
        ),
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
    new cdk.CfnOutput(this, "ShoppingCartLambdaArn", {
      value: shoppingCartLambda.functionArn,
    });

    // Output name of the table
    new cdk.CfnOutput(this, "ShoppingCartTableName", {
      value: shoppingCartTable.tableName,
    });
  }
}
