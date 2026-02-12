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
