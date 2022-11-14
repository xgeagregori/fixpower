cdk deploy --all --outputs-file ./cdk-outputs.json --require-approval never

apiGatewayUrl=$(jq -r '.ApiStack.ApiGatewayUrl' ./cdk-outputs.json)

gh secret set AWS_API_GATEWAY_URL -b $apiGatewayUrl

productListingArn=$(jq -r '.ProductListingStack.ProductListingLambdaArn' ./cdk-outputs.json)
shoppingCartArn=$(jq -r '.ShoppingCartStack.ShoppingCartLambdaArn' ./cdk-outputs.json)
transactionArn=$(jq -r '.TransactionStack.TransactionLambdaArn' ./cdk-outputs.json)
userArn=$(jq -r '.UserStack.UserLambdaArn' ./cdk-outputs.json)

gh secret set AWS_PRODUCT_LISTING_LAMBDA_ARN -b $productListingArn
gh secret set AWS_SHOPPING_CART_LAMBDA_ARN -b $shoppingCartArn
gh secret set AWS_TRANSACTION_LAMBDA_ARN -b $transactionArn
gh secret set AWS_USER_LAMBDA_ARN -b $userArn

productListingTableName=$(jq -r '.ProductListingStack.ProductListingTableName' ./cdk-outputs.json)
shoppingCartTableName=$(jq -r '.ShoppingCartStack.ShoppingCartTableName' ./cdk-outputs.json)
transactionTableName=$(jq -r '.TransactionStack.TransactionTableName' ./cdk-outputs.json)
userTableName=$(jq -r '.UserStack.UserTableName' ./cdk-outputs.json)

gh secret set AWS_PRODUCT_LISTING_TABLE_NAME -b $productListingTableName
gh secret set AWS_SHOPPING_CART_TABLE_NAME -b $shoppingCartTableName
gh secret set AWS_TRANSACTION_TABLE_NAME -b $transactionTableName
gh secret set AWS_USER_TABLE_NAME -b $userTableName
