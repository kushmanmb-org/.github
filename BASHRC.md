# Bash Configuration

This repository includes a `.bashrc` file with custom bash functions.

## cwhois Function

The `cwhois` function is a custom whois wrapper that queries bgp.tools for network information.

### Usage

To use the `cwhois` function, source the `.bashrc` file in your shell:

```bash
source .bashrc
```

Then you can use the function:

```bash
cwhois <query>
```

### Example

```bash
# Query information about an IP address or AS number
cwhois 8.8.8.8
cwhois AS15169
```

The function automatically adds the `-v` (verbose) flag and queries the bgp.tools whois server.

### How it works

The function is defined as:

```bash
cwhois() {
    whois -h bgp.tools -v $*
}
export -f cwhois
```

This wraps the standard `whois` command to always use the bgp.tools server with verbose output enabled (`-v` flag).

## foundryup Function

The `foundryup` function installs or updates the Foundry toolchain, a blazing fast, portable and modular toolkit for Ethereum application development.

### Usage

To use the `foundryup` function, source the `.bashrc` file in your shell:

```bash
source .bashrc
```

Then you can use the function:

```bash
foundryup
```

### Example

```bash
# Install or update Foundry
foundryup
```

The function downloads and executes the official Foundry installer script from https://foundry.paradigm.xyz.

### How it works

The function is defined as:

```bash
foundryup() {
    curl -fsSL https://foundry.paradigm.xyz | bash
}
export -f foundryup
```

This function downloads the official Foundry installer script and pipes it to bash for execution. The installer will automatically install or update the Foundry toolchain components (forge, cast, anvil, and chisel). The `-fsSL` flags ensure that curl fails silently on errors, operates in silent mode while showing errors, and follows redirects.

## lastcall Function

The `lastcall` function queries the last transaction for an Ethereum address by retrieving its current nonce (transaction count).

### Usage

To use the `lastcall` function, source the `.bashrc` file in your shell:

```bash
source .bashrc
```

Then you can use the function:

```bash
lastcall <address> [rpc_url]
```

### Example

```bash
# Query transaction count for an address using default RPC
lastcall 0x983e3660c0bE01991785F80f266A84B911ab59b0

# Query using a custom RPC endpoint
lastcall 0x983e3660c0bE01991785F80f266A84B911ab59b0 https://eth.llamarpc.com
```

The function returns the nonce (transaction count) for the address, which indicates how many transactions have been sent from this address. This is useful for:
- Determining if an address has made any transactions
- Checking the most recent transaction number
- Verifying address activity

### How it works

The function is defined as:

```bash
lastcall() {
    if [ -z "$1" ]; then
        echo "Usage: lastcall <address> [rpc_url]"
        echo "Example: lastcall 0x983e3660c0bE01991785F80f266A84B911ab59b0"
        return 1
    fi
    
    local address="$1"
    local rpc_url="${2:-https://eth.llamarpc.com}"
    
    # Use cast to get the transaction count (nonce) which helps identify the last transaction
    cast nonce "$address" --rpc-url "$rpc_url"
}
export -f lastcall
```

This function uses Foundry's `cast` tool to query the transaction count (nonce) for an Ethereum address. The nonce represents the number of transactions sent from the address. If no RPC URL is provided, it defaults to `https://eth.llamarpc.com`, a free public Ethereum RPC endpoint.

### Requirements

- **Foundry toolkit** must be installed (use `foundryup` to install)
- **Active internet connection** to query the RPC endpoint
- Valid Ethereum address in hexadecimal format (0x...)
