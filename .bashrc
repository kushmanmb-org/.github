#!/bin/bash
# Bash configuration file with custom functions

# cwhois: Custom whois function that queries bgp.tools
# Usage: cwhois <query>
cwhois() {
    whois -h bgp.tools -v $*
}
export -f cwhois

# etherscan_api: Make POST requests to Etherscan API v2
# Usage: etherscan_api [options]
# Example: etherscan_api -d '{"module":"contract","action":"getabi","address":"0x..."}'
etherscan_api() {
    curl --request POST \
         --url https://api.etherscan.io/v2/api \
         "$@"
}
export -f etherscan_api
