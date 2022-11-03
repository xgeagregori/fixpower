#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { ApiStack } from '../lib/api-stack';
import { ProductListingStack } from '../lib/product-listing-stack';
import { ShoppingCartStack } from '../lib/shopping-cart-stack';
import { TransactionStack } from '../lib/transaction-stack';
import { UserStack } from '../lib/user-stack';

const app = new cdk.App();
const api = new ApiStack(app, 'ApiStack');
new ProductListingStack(app, 'ProductListingStack', { apiGateway: api.api });
new ShoppingCartStack(app, 'ShoppingCartStack', { apiGateway: api.api });
new TransactionStack(app, 'TransactionStack', { apiGateway: api.api });
new UserStack(app, 'UserStack', { apiGateway: api.api });
