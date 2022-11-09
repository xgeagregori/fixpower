import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as apiGateway from "aws-cdk-lib/aws-apigateway";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";

interface TransactionProps extends cdk.StackProps {
  apiGateway: apiGateway.RestApi;
}

export class TransactionStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: TransactionProps) {
    super(scope, id, props);

    const transactionTable = new dynamodb.Table(this, "Transactions", {
      partitionKey: {
        name: "id",
        type: dynamodb.AttributeType.STRING,
      },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const transactionLambda = new lambda.Function(this, "transactionApi", {
      runtime: lambda.Runtime.PYTHON_3_9,
      code: lambda.Code.fromAsset("../transaction/app"),
      handler: "transaction_controller.handler",
      environment: {
        TABLE_NAME: transactionTable.tableName,
      },
      timeout: cdk.Duration.seconds(10),
    });

    transactionTable.grantReadWriteData(transactionLambda);

    props?.apiGateway.root
      .addResource("transaction-api")
      .addResource("v1")
      .addProxy({
        defaultIntegration: new apiGateway.LambdaIntegration(transactionLambda),
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
    new cdk.CfnOutput(this, "TransactionLambdaArn", {
      value: transactionLambda.functionArn,
    });

    // Output name of the table
    new cdk.CfnOutput(this, "TransactionTableName", {
      value: transactionTable.tableName,
    });
  }
}
