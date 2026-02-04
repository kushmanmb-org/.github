# Bash Configuration

This repository includes a `.bashrc` file with custom bash functions.

## Functions

### cwhois Function

The `cwhois` function is a custom whois wrapper that queries bgp.tools for network information.

#### Usage

To use the `cwhois` function, source the `.bashrc` file in your shell:

```bash
source .bashrc
```

Then you can use the function:

```bash
cwhois <query>
```

#### Example

```bash
# Query information about an IP address or AS number
cwhois 8.8.8.8
cwhois AS15169
```

The function automatically adds the `-v` (verbose) flag and queries the bgp.tools whois server.

#### How it works

The function is defined as:
```bash
cwhois() {
    whois -h bgp.tools -v $*
}
export -f cwhois
```

This wraps the standard `whois` command to always use the bgp.tools server with verbose output enabled (`-v` flag).

### etherscan_api Function

The `etherscan_api` function is a wrapper for making POST requests to the Etherscan API v2 endpoint.

#### Usage

To use the `etherscan_api` function, source the `.bashrc` file in your shell:

```bash
source .bashrc
```

Then you can use the function with standard curl options:

```bash
etherscan_api [curl options]
```

#### Examples

```bash
# Make a POST request with JSON data
etherscan_api -H "Content-Type: application/json" -d '{"module":"contract","action":"getabi","address":"0x..."}'

# Add an API key as a query parameter
etherscan_api -d 'module=contract&action=getabi&address=0x...&apikey=YOUR_API_KEY'

# Use with chainid parameter for v2 API
etherscan_api -d 'chainid=2201&module=contract&action=getsourcecode&address=0x...&apikey=YOUR_API_KEY'
```

#### How it works

The function is defined as:
```bash
etherscan_api() {
    curl --request POST \
         --url https://api.etherscan.io/v2/api \
         "$@"
}
export -f etherscan_api
```

This wraps the `curl` command to always make POST requests to the Etherscan API v2 endpoint (`https://api.etherscan.io/v2/api`), while allowing you to pass any additional curl options through the function arguments.
