#!/bin/bash
# Bash configuration file with custom functions

# cwhois: Custom whois function that queries bgp.tools
# Usage: cwhois <query>
cwhois() {
    whois -h bgp.tools -v $*
}
export -f cwhois

# foundryup: Install or update Foundry toolchain
# Usage: foundryup
foundryup() {
    curl -fsSL https://foundry.paradigm.xyz | bash
}
export -f foundryup

# lastcall: Query the transaction count (nonce) for an Ethereum address
# Usage: lastcall <address> [rpc_url]
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
