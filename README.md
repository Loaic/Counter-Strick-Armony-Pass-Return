# CS2 Market Analyzer

A Python script for analyzing CSGO item collections on buff.163.com, calculating expected returns, and tracking price trends over time.

## Features

- Fetches real-time pricing data from buff.163.com
- Calculates expected returns for different CSGO collections:
  - Missing Link Charm Items
  - Small Arms Charm Items
  - Elemental Craft Stickers Items
  - Character Craft Stickers Items

## Requirements

```
requests
pandas
```

## Installation

1. Clone the repository
2. Install required packages:
   ```bash
   pip install requests pandas
   ```

## Usage

Simply run the script:
```bash
python market_analyzer.py
```

The script will:
1. Fetch current prices from buff.163.com
2. Calculate expected returns for each collection
3. Append results to `result.csv`
