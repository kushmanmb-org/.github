# GitHub Secrets Configuration for Crypto Consolidation

This document lists the required GitHub secrets for the cryptocurrency consolidation workflows.

## Required Secrets

Configure these secrets in your GitHub repository or organization settings:

### RPC Endpoints

| Secret Name | Description | Example Value |
|------------|-------------|---------------|
| `ETHEREUM_RPC_URL` | Ethereum mainnet RPC endpoint | `https://mainnet.infura.io/v3/YOUR_PROJECT_ID` |
| `BASE_RPC_URL` | Base L2 RPC endpoint | `https://mainnet.base.org` |
| `POLYGON_RPC_URL` | Polygon RPC endpoint | `https://polygon-rpc.com` |
| `ARBITRUM_RPC_URL` | Arbitrum One RPC endpoint | `https://arb1.arbitrum.io/rpc` |
| `OPTIMISM_RPC_URL` | Optimism RPC endpoint | `https://mainnet.optimism.io` |

### API Keys

| Secret Name | Description | How to Obtain |
|------------|-------------|---------------|
| `ETHERSCAN_API_KEY` | Etherscan API key | [etherscan.io/apis](https://etherscan.io/apis) |
| `BASESCAN_API_KEY` | BaseScan API key | [basescan.org/apis](https://basescan.org/apis) |
| `POLYGONSCAN_API_KEY` | PolygonScan API key | [polygonscan.com/apis](https://polygonscan.com/apis) |
| `ARBISCAN_API_KEY` | Arbiscan API key | [arbiscan.io/apis](https://arbiscan.io/apis) |
| `OPTIMISTIC_ETHERSCAN_API_KEY` | Optimistic Etherscan API key | [optimistic.etherscan.io/apis](https://optimistic.etherscan.io/apis) |

### Wallet Credentials (⚠️ High Security)

| Secret Name | Description | Security Notes |
|------------|-------------|----------------|
| `WALLET_PRIVATE_KEY` | Private key for transaction signing | **CRITICAL**: Use hardware wallet or multisig in production |
| `MULTISIG_WALLET_ADDRESS` | Address of multisig wallet | For additional security on high-value transactions |

### Optional Secrets

| Secret Name | Description | Use Case |
|------------|-------------|----------|
| `SLACK_WEBHOOK_URL` | Slack webhook for notifications | Real-time alerts for transaction status |
| `DISCORD_WEBHOOK_URL` | Discord webhook for notifications | Alternative notification channel |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | Mobile notifications |

## Setting Secrets

### Via GitHub Web Interface

1. Go to repository **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Enter the secret name and value
4. Click **Add secret**

### Via GitHub CLI

```bash
# Set a secret using gh CLI
gh secret set ETHEREUM_RPC_URL --body "https://mainnet.infura.io/v3/YOUR_PROJECT_ID"

# Set multiple secrets from a file
gh secret set ETHERSCAN_API_KEY < etherscan-api-key.txt
```

### Via Terraform (for organizations)

```hcl
resource "github_actions_secret" "ethereum_rpc" {
  repository      = "your-repo"
  secret_name     = "ETHEREUM_RPC_URL"
  plaintext_value = var.ethereum_rpc_url
}
```

## Environment Protection Rules

For production workflows, configure environment protection rules:

1. Go to repository **Settings** → **Environments**
2. Create environment: `production-crypto`
3. Configure protection rules:
   - **Required reviewers**: Add trusted team members (minimum 2)
   - **Wait timer**: 5 minutes (allows time to cancel if needed)
   - **Deployment branches**: Only `main` or `production` branches

## Security Best Practices

### DO:
- ✅ Use separate API keys for each environment (dev, staging, prod)
- ✅ Rotate secrets regularly (every 90 days recommended)
- ✅ Use hardware wallets for high-value operations
- ✅ Enable IP whitelisting on RPC providers
- ✅ Use multisig wallets for production transactions
- ✅ Store backup keys in secure offline storage
- ✅ Use GitHub environment protection rules
- ✅ Enable audit logging for all secret access

### DON'T:
- ❌ Never commit secrets to version control
- ❌ Never share secrets via chat or email
- ❌ Never use production keys in development
- ❌ Never store secrets in plaintext files
- ❌ Never reuse keys across multiple services
- ❌ Never skip testing in testnet environments
- ❌ Never disable approval gates for production

## Verifying Secret Configuration

Run this workflow to verify secrets are configured:

```bash
gh workflow run balance-monitor.yml
```

Check the workflow summary for any missing or misconfigured secrets.

## Rotating Secrets

If a secret is compromised:

1. **Immediately revoke** the compromised credential
2. **Generate new** API key or private key
3. **Update GitHub secret** with new value
4. **Verify** new secret works by running test workflow
5. **Document** the rotation in your security log
6. **Investigate** how the compromise occurred

## Troubleshooting

### Issue: "API key invalid" error

**Solution**: Verify the API key is correct and has proper permissions

```bash
# Test API key manually
curl "https://api.etherscan.io/api?apikey=YOUR_KEY"
```

### Issue: "RPC endpoint not responding"

**Solution**: Check RPC provider status and rate limits

```bash
# Test RPC endpoint
curl -X POST YOUR_RPC_URL \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

### Issue: "Secret not found in workflow"

**Solution**: Ensure secret name matches exactly (case-sensitive)

## Additional Resources

- [GitHub Actions Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Security Best Practices](SECURITY_BEST_PRACTICES.md)
- [Crypto Consolidation Guide](CRYPTO_CONSOLIDATION.md)

---

*Last Updated: 2026-02-13*
*Version: 1.0.0*
