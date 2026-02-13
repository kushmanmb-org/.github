# Quick Start: Crypto Consolidation to kushmanmb.base.eth

This guide helps you quickly set up and use the crypto consolidation system.

## Prerequisites

- GitHub repository access with Actions enabled
- RPC endpoints for blockchain networks
- API keys for block explorers
- (Optional) Private key for transaction signing

## Step 1: Configure Secrets

Set up required secrets in GitHub repository settings:

```bash
# Using GitHub CLI
gh secret set ETHEREUM_RPC_URL --body "https://mainnet.infura.io/v3/YOUR_PROJECT_ID"
gh secret set BASE_RPC_URL --body "https://mainnet.base.org"
gh secret set ETHERSCAN_API_KEY --body "YOUR_ETHERSCAN_KEY"
gh secret set BASESCAN_API_KEY --body "YOUR_BASESCAN_KEY"
```

See [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md) for complete list.

## Step 2: Set Up Environment Protection

1. Go to **Settings** → **Environments**
2. Create environment: `production-crypto`
3. Add required reviewers (minimum 2)
4. Set wait timer: 5 minutes
5. Save changes

## Step 3: Monitor Balances

Check balances across all chains:

```bash
gh workflow run balance-monitor.yml
```

View results:
```bash
gh run list --workflow=balance-monitor.yml --limit 1
gh run view $(gh run list --workflow=balance-monitor.yml --limit 1 --json databaseId --jq '.[0].databaseId')
```

## Step 4: Test Consolidation (Dry Run)

Always test with dry run first:

```bash
gh workflow run crypto-consolidation.yml \
  --field sourceChain=base \
  --field amount=0.1 \
  --field dryRun=true
```

## Step 5: Execute Consolidation (Production)

After successful dry run:

```bash
gh workflow run crypto-consolidation.yml \
  --field sourceChain=base \
  --field amount=0.1 \
  --field dryRun=false \
  --field requiresApproval=true
```

**Important**: This requires manual approval from configured reviewers.

## Step 6: Verify Transaction

After consolidation completes:

```bash
gh workflow run tx-verification.yml \
  --field txHash=0xYOUR_TX_HASH \
  --field chain=base \
  --field expectedDestination=kushmanmb.base.eth
```

## Common Commands

### Check Workflow Status
```bash
# List recent runs
gh run list --limit 10

# View specific run
gh run view RUN_ID

# Watch run in progress
gh run watch RUN_ID
```

### View Artifacts
```bash
# Download verification report
gh run download RUN_ID
```

### Cancel Running Workflow
```bash
gh run cancel RUN_ID
```

## Troubleshooting

### Issue: "Secret not found"
**Solution**: Verify secrets are set correctly
```bash
gh secret list
```

### Issue: "Approval timeout"
**Solution**: Check environment reviewers are available and notified

### Issue: "RPC endpoint error"
**Solution**: Test RPC endpoint manually
```bash
curl -X POST YOUR_RPC_URL \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

## Safety Checklist

Before production use:
- [ ] All secrets configured and tested
- [ ] Environment protection rules set up
- [ ] Dry run tested successfully
- [ ] Reviewers know approval process
- [ ] Target address verified: kushmanmb.base.eth
- [ ] Backup of current configuration
- [ ] Emergency contacts identified

## Target Address

**Primary Consolidation Address**: `kushmanmb.base.eth`

Always verify this address before approving transactions!

## Need Help?

- 📖 Full documentation: [CRYPTO_CONSOLIDATION.md](CRYPTO_CONSOLIDATION.md)
- 🔒 Secrets setup: [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md)
- 🛡️ Security: [SECURITY_BEST_PRACTICES.md](SECURITY_BEST_PRACTICES.md)
- 📋 Implementation: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

## Support

For issues or questions:
- Create a GitHub issue
- Review [SUPPORT.md](SUPPORT.md)
- Check [SECURITY.md](SECURITY.md) for security concerns

---

**Remember**: Always use dry-run mode first and verify the target address before executing production transactions!

*Last Updated: 2026-02-13*
