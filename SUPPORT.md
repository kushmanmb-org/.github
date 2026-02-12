# Support

Thank you for using our blockchain development tools and utilities! We're here to help you get the most out of our projects.

## Getting Help

### Documentation

Before seeking support, please check our comprehensive documentation:

- **[Main README](README.md)** - Overview and quick start guide
- **[Blockchain RPC Documentation](BLOCKCHAIN_RPC.md)** - JSON-RPC server usage
- **[Etherscan Token Balance Guide](ETHERSCAN_TOKEN_BALANCE.md)** - Query ERC-20 token balances
- **[Multisig Wallet Documentation](MULTISIG_WALLET_README.md)** - Ethereum multisig wallet integration
- **[Security Best Practices](SECURITY_BEST_PRACTICES.md)** - Protecting API keys and sensitive data
- **[GPG Key Management](GPG_KEY_MANAGEMENT.md)** - Managing GPG keys and signing commits
- **[Connecting to GitHub with SSH](CONNECTING_TO_GITHUB_WITH_SSH.md)** - SSH setup guide

### Common Issues

#### API Key Issues

If you're having trouble with API keys:

1. **Never commit API keys to version control**

   - Use environment variables: `export ETHERSCAN_API_KEY="your-key"`
   - Use `.gitignore`d configuration files
   - Review [Security Best Practices](SECURITY_BEST_PRACTICES.md)

2. **Getting 401 Unauthorized errors**

   - Verify your API key is valid
   - Check if you're passing the key correctly (--apikey parameter)
   - Ensure you're using the correct API endpoint

3. **Rate limiting errors**

   - Free Etherscan API keys have rate limits
   - Consider upgrading to a paid plan for higher limits
   - Implement exponential backoff in your requests

#### Installation Issues

**Python Scripts:**

```bash
# Install required dependencies
pip install -r requirements.txt

# If you encounter permission errors, use:
pip install --user -r requirements.txt
```

**JavaScript/Node.js Scripts:**

```bash
# Install dependencies
npm install

# Or using yarn
yarn install
```

#### Connection Issues

**RPC Server Won't Start:**

- Check if port 8332 is already in use: `lsof -i :8332`
- Try using a different port: modify `blockchain_rpc_server.py`
- Verify firewall settings aren't blocking the port

**Cannot Connect to APIs:**

- Verify internet connectivity
- Check if API endpoint is accessible: `curl https://api.etherscan.io/v2/api`
- Ensure you're using HTTPS for API requests
- Check if you're behind a corporate firewall or proxy

### Support Channels

#### GitHub Issues

For bug reports, feature requests, or technical questions:

1. **Search existing issues** first to avoid duplicates
2. **Create a new issue** if you don't find an answer:
   - [Bug Report](https://github.com/kushmanmb-org/.github/issues/new?template=bug_report.md)
   - [Feature Request](https://github.com/kushmanmb-org/.github/issues/new?template=feature_request.md)
3. **Provide details**:
   - Clear description of the problem
   - Steps to reproduce
   - Environment information (OS, language version, etc.)
   - Relevant logs or error messages

#### GitHub Discussions

For general questions, ideas, or community discussions:

- Visit our [GitHub Discussions](https://github.com/kushmanmb-org/.github/discussions)
- Ask questions, share ideas, or help others
- Great for "How do I..." questions

#### Stack Overflow

You can also ask questions on Stack Overflow:

- Tag your questions with `blockchain`, `ethereum`, `etherscan-api`, or relevant tags
- Reference our repository in your question
- We monitor these tags and may respond

## Contributing

Want to contribute? That's great!

- Read our [Contributing Guide](CONTRIBUTING.md)
- Check our [Code of Conduct](CODE_OF_CONDUCT.md)
- Look for issues labeled `good first issue` or `help wanted`

## Security Issues

**Do not report security vulnerabilities through public issues.**

For security-related concerns:

- Follow our [Security Policy](SECURITY.md)
- Report vulnerabilities to the [MetaMask HackerOne program](https://hackerone.com/metamask)
- Visit the [MetaMask Security Program](https://metamask.io/security/) page

## Response Times

We're a community-driven project and response times may vary:

- **Critical security issues**: We aim to respond within 24-48 hours
- **Bug reports**: Typically reviewed within 3-7 days
- **Feature requests**: Reviewed during regular planning cycles
- **General questions**: Best effort, community members may respond sooner

Please be patient and respectful. All maintainers and contributors volunteer their time.

## Self-Help Resources

### Example Usage

**Query Token Balance (Bash):**

```bash
./query-token-balance.sh --apikey YOUR_API_KEY
```

**Query Token Balance (Python):**

```bash
./query-token-balance.py --apikey YOUR_API_KEY --pretty
```

**Query Token Balance (JavaScript):**

```bash
node query-token-balance.js --apikey YOUR_API_KEY --pretty
```

**Start RPC Server:**

```bash
python3 blockchain_rpc_server.py
```

**Test RPC Server:**

```bash
python3 blockchain_rpc_client.py \
  --tx 08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898 \
  --height 172165 \
  --pretty
```

### Troubleshooting Tips

1. **Enable verbose output** - Many scripts support `-v` or `--verbose` flags
2. **Check logs** - Look for error messages in console output
3. **Verify dependencies** - Ensure all required packages are installed
4. **Test with curl** - Use curl to test API endpoints directly
5. **Read error messages** - They often contain helpful information
6. **Update dependencies** - Make sure you're using compatible versions

## Additional Resources

- **Etherscan API Documentation**: <https://docs.etherscan.io/>
- **Ethereum Developer Docs**: <https://ethereum.org/developers>
- **Python Requests Library**: <https://requests.readthedocs.io/>
- **Node.js Fetch API**: <https://nodejs.org/docs/latest/api/globals.html#fetch>

## Thank You

Thank you for using our tools and being part of our community. Your feedback helps us improve and build better blockchain development utilities!

---

**Need help?** Don't hesitate to reach out through any of the channels above. We're here to help! 🚀
