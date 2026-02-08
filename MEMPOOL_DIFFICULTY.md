# Bitcoin Difficulty Adjustment API Example

This example demonstrates how to use the [mempool.space](https://mempool.space) JavaScript library to fetch Bitcoin difficulty adjustment data.

## Overview

The `mempool-difficulty-adjustment.html` file shows a simple HTML page that:
- Loads the mempool.js library from mempool.space
- Initializes the mempoolJS client
- Fetches the current Bitcoin difficulty adjustment information
- Displays the result as formatted JSON

## Usage

### Viewing the Example

Simply open the `mempool-difficulty-adjustment.html` file in a web browser. The page will automatically:
1. Connect to the mempool.space API
2. Fetch the current difficulty adjustment data
3. Display the result on the page

### Expected Output

The API returns information about the Bitcoin network's difficulty adjustment, including:
- Current difficulty
- Difficulty change
- Estimated next difficulty adjustment time
- Percentage of progress to next adjustment
- Other related statistics

### Example Response

```json
{
  "progressPercent": 68.45,
  "difficultyChange": 2.34,
  "estimatedRetargetDate": 1707408000000,
  "remainingBlocks": 630,
  "remainingTime": 378000,
  "previousRetarget": -1.23
}
```

## Technical Details

### API Endpoint

The example uses the mempool.space JavaScript library which provides a convenient wrapper around their REST API.

### Dependencies

- **mempool.js**: The official mempool.space JavaScript library
  - Loaded from: `https://mempool.space/mempool.js`
  - Documentation: [https://github.com/mempool/mempool.js](https://github.com/mempool/mempool.js)

### Methods Used

```javascript
const { bitcoin: { difficulty } } = mempoolJS({
  hostname: 'mempool.space'
});

const difficultyAdjustment = await difficulty.getDifficultyAdjustment();
```

## Related Resources

- [Mempool.space Official Website](https://mempool.space)
- [Mempool.space API Documentation](https://mempool.space/docs/api)
- [Bitcoin Difficulty Adjustment Explained](https://en.bitcoin.it/wiki/Difficulty)

## Integration with Other Tools

This example complements the other blockchain utilities in this repository:
- [Blockchain JSON-RPC Server](BLOCKCHAIN_RPC.md)
- [Etherscan Token Balance API](ETHERSCAN_TOKEN_BALANCE.md)

## Notes

- The page requires an internet connection to fetch data from mempool.space
- The API is rate-limited; excessive requests may be throttled
- The displayed data reflects real-time Bitcoin network statistics
