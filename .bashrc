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
    curl -L https://foundry.paradigm.xyz | bash
}
export -f foundryup
