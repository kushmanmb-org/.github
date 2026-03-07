# Cryptocurrency Consolidation Workflows

This document describes the automated workflows for safely consolidating cryptocurrency assets to the primary address `kushmanmb.base.eth`.

## Overview

The crypto consolidation system provides:
- **Multi-chain balance monitoring** across Ethereum, Base, Polygon, Arbitrum, and Optimism
- **Automated consolidation workflows** with multi-signature approval
- **Security best practices** for handling private keys and sensitive operations
- **Audit trails** with transaction verification and logging

## Target Address

**Primary Consolidation Address**: `kushmanmb.base.eth`

This ENS address resolves on Base L2 chain and serves as the primary destination for all consolidated funds.

## Supported Chains

The consolidation system supports the following networks:

| Chain | Chain ID | RPC Endpoint Variable | Description |
|-------|----------|----------------------|-------------|
| Ethereum Mainnet | 1 | `ETHEREUM_RPC_URL` | Primary L1 network |
| Base | 8453 | `BASE_RPC_URL` | Base L2 (Coinbase) |
| Polygon | 137 | `POLYGON_RPC_URL` | Polygon PoS |
| Arbitrum One | 42161 | `ARBITRUM_RPC_URL` | Arbitrum L2 |
| Optimism | 10 | `OPTIMISM_RPC_URL` | Optimism L2 |

## Workflows

### 1. Balance Monitoring (`balance-monitor.yml`)

Runs on a schedule to check balances across all supported chains:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
```

**Features:**
- Queries native token and ERC-20 balances
- Reports balances via workflow summary
- Triggers consolidation alert if thresholds are met
- Stores balance history as artifacts

### 2. Consolidation Workflow (`crypto-consolidation.yml`)

Manual workflow with approval gates for consolidating funds:

**Workflow Dispatch Parameters:**
- Source chain
- Token contract address (optional, for ERC-20s)
- Amount to consolidate
- Dry-run mode (for testing)

**Security Features:**
- Requires manual approval from authorized personnel
- Multi-signature wallet integration
- Transaction simulation before execution
- Complete audit logging

### 3. Transaction Verification (`tx-verification.yml`)

Runs automatically after consolidation to verify:
- Transaction inclusion on-chain
- Correct destination address
- Expected amount transferred
- Gas costs within limits

## Security Requirements

### GitHub Secrets Required

Store these secrets securely in GitHub repository or organization settings:

```
ETHEREUM_RPC_URL          # Ethereum mainnet RPC (Infura/Alchemy)
BASE_RPC_URL              # Base L2 RPC endpoint
POLYGON_RPC_URL           # Polygon RPC endpoint
ARBITRUM_RPC_URL          # Arbitrum RPC endpoint
OPTIMISM_RPC_URL          # Optimism RPC endpoint
ETHERSCAN_API_KEY         # For transaction verification
MULTISIG_WALLET_ADDRESS   # Address of the multisig wallet
WALLET_PRIVATE_KEY        # Encrypted private key (for signing only)
SLACK_WEBHOOK_URL         # For notifications (optional)
```

### Private Key Management

**CRITICAL SECURITY REQUIREMENTS:**

1. **Never commit private keys** to version control
2. **Use GitHub encrypted secrets** for all sensitive data
3. **Implement hardware wallet integration** where possible
4. **Use multi-signature wallets** for high-value transactions
5. **Enable IP whitelisting** on RPC providers
6. **Rotate credentials regularly** (90-day maximum)
7. **Use separate keys** for different operations
8. **Audit all transactions** before and after execution

### Multi-Signature Approval

For production use, configure the workflows to require:
- **Minimum 2-of-3 signatures** for transactions
- **Manual approval gates** in GitHub Actions
- **Time-locked transactions** for high-value transfers
- **Emergency pause mechanisms**

## Configuration Files

### `crypto-config.json` (gitignored)

Store local configuration in a gitignored file:

```json
{
  "targetAddress": "kushmanmb.base.eth",
  "targetENSResolver": "0x...",
  "chains": {
    "base": {
      "chainId": 8453,
      "name": "Base",
      "enabled": true,
      "minBalanceThreshold": "0.1",
      "consolidationThreshold": "1.0"
    }
  },
  "tokens": {
    "USDC": {
      "ethereum": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
      "base": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "polygon": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
    }
  }
}
```

### `address-whitelist.json` (gitignored)

Whitelist of trusted addresses:

```json
{
  "whitelistedAddresses": [
    {
      "address": "0x...",
      "label": "Cold Storage Wallet 1",
      "purpose": "Long-term holdings",
      "authorized": true
    }
  ]
}
```

## Workflow Usage

### Manual Consolidation

Trigger consolidation manually via GitHub Actions:

```bash
gh workflow run crypto-consolidation.yml \
  --field chain=base \
  --field token=USDC \
  --field amount=100 \
  --field dryRun=true
```

### Automated Monitoring

Balance monitoring runs automatically. To check current status:

```bash
gh run list --workflow=balance-monitor.yml --limit 1
gh run view <run-id>
```

### Transaction Verification

After consolidation, verify the transaction:

```bash
gh workflow run tx-verification.yml \
  --field txHash=0x... \
  --field chain=base
```

## Monitoring and Alerts

### Notification Channels

- **GitHub Actions Summary**: Workflow run summaries
- **Slack Notifications**: Real-time alerts (if configured)
- **Email Alerts**: GitHub notification emails
- **Artifact Storage**: Balance history and transaction logs

### Alert Conditions

Alerts are triggered for:
- Balance exceeds consolidation threshold
- Failed transaction attempts
- Unusual gas prices (>95th percentile)
- Suspicious transaction patterns
- Multi-sig approval timeouts

## Gas Optimization

### Dynamic Gas Pricing

The workflows implement dynamic gas pricing:
- Query current gas prices before transactions
- Wait for favorable gas conditions (if not urgent)
- Use EIP-1559 for Ethereum mainnet (dynamic base fee and priority fee)
- Support EIP-7976 calldata floor pricing (64/64 gas per byte for data-heavy transactions)
- Support EIP-7981 access list pricing (aligned with EIP-7976 floor costs)
- Configure maximum gas price limits

### Best Practices

1. **Consolidate during low-traffic periods** (weekends, early morning UTC)
2. **Batch multiple small transfers** when possible
3. **Use L2 chains** (Base, Arbitrum, Optimism) for lower fees
4. **Monitor mempool** for pending transactions
5. **Set reasonable gas limits** to avoid failures

## Audit and Compliance

### Transaction Logging

All consolidation operations are logged with:
- Timestamp
- Source chain and address
- Destination address (kushmanmb.base.eth)
- Amount and token
- Transaction hash
- Gas used and costs
- Approval signatures

### Audit Trail

Access audit logs via:
- GitHub Actions workflow artifacts
- Transaction verification reports
- Balance history reports

## Disaster Recovery

### Emergency Procedures

If unauthorized access is detected:

1. **Immediately pause** all workflows
2. **Rotate all API keys** and secrets
3. **Review transaction history** for suspicious activity
4. **Contact exchange/wallet providers** if needed
5. **Document the incident** for future prevention

### Backup Procedures

- **Regular backups** of configuration files
- **Multiple signature keys** for recovery
- **Documentation** of all wallet addresses
- **Tested recovery procedures** (quarterly)

## Testing

### Testnet Deployment

Test all workflows on testnets first:
- Sepolia (Ethereum testnet)
- Base Sepolia (Base testnet)
- Mumbai (Polygon testnet)

### Dry-Run Mode

All workflows support dry-run mode:
- Simulates transactions without execution
- Verifies configuration
- Estimates gas costs
- Validates addresses

## Troubleshooting

### Common Issues

**Issue**: Transaction fails with "insufficient funds"
- **Solution**: Check gas token balance (ETH, MATIC, etc.)

**Issue**: ENS resolution fails
- **Solution**: Verify ENS name is correctly registered on the target chain

**Issue**: Multi-sig approval timeout
- **Solution**: Check that required signers are available

**Issue**: High gas prices
- **Solution**: Enable gas price monitoring and wait for favorable conditions

## Additional Resources

- [Security Best Practices](SECURITY_BEST_PRACTICES.md)
- [Multisig Wallet Documentation](MULTISIG_WALLET_README.md)
- [Etherscan API Guide](ETHERSCAN_TOKEN_BALANCE.md)
- [Transaction Hash Verification](TX_HASH_VERIFICATION.md)
- [EIP-7976: Increase Calldata Floor Cost](EIP_7976.md)
- [EIP-7981: Increase Access List Cost](EIP_7981.md)

## Support

For questions or issues:
- Create a GitHub issue
- Contact via [SUPPORT.md](SUPPORT.md)
- Review security policy: [SECURITY.md](SECURITY.md)

---

*Last Updated: 2026-02-13*
*Version: 1.0.0*
