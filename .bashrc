#!/bin/bash
# Bash configuration file with custom functions

# cwhois: Custom whois function that queries bgp.tools
# Usage: cwhois <query>
# Arguments:
#   query_target - IP address, domain, or AS number to query
cwhois() {
    local query_target="$@"
    whois -h bgp.tools -v "$query_target"
}
export -f cwhois
