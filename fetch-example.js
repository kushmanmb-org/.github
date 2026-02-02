// Simple fetch example for Etherscan API v2
// This demonstrates basic usage of the fetch API to query Etherscan

const options = {method: 'GET'};

fetch('https://api.etherscan.io/v2/api', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
