import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as apiGateway from "aws-cdk-lib/aws-apigateway";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";

interface ProductListingProps extends cdk.StackProps {
  apiGateway: apiGateway.RestApi;
}

export class ProductListingStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: ProductListingProps) {
    super(scope, id, props);

    const productListingTable = new dynamodb.Table(this, "ProductListings", {
      partitionKey: {
        name: "id",
        type: dynamodb.AttributeType.STRING,
      },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const productListingLambda = new lambda.Function(
      this,
      "ProductListingApi",
      {
        runtime: lambda.Runtime.PYTHON_3_9,
        code: lambda.Code.fromAsset("../product-listing/app"),
        handler: "product_listing_controller.handler",
        environment: {
          TABLE_NAME: productListingTable.tableName,
        },
        timeout: cdk.Duration.seconds(10),
      }
    );

    productListingTable.grantReadWriteData(productListingLambda);

    props?.apiGateway.root
      .addResource("product-listing-api")
      .addResource("v1")
      .addProxy({
        defaultIntegration: new apiGateway.LambdaIntegration(
          productListingLambda
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
    new cdk.CfnOutput(this, "ProductListingLambdaArn", {
      value: productListingLambda.functionArn,
    });

    // Output name of the table
    new cdk.CfnOutput(this, "ProductListingTableName", {
      value: productListingTable.tableName,
    });
  }
}
