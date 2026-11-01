# genpark-agentic-commerce-warehouse-slotting-cross-dock-flow-through-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

Distribution center Cross-Dock flow-through staging, inbound-to-outbound trailer turnaround & dock door bottleneck reducer.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `optimize_cross_dock_flow_through`
- **Category**: `agentic_commerce`

### Method Documentation
Optimize warehouse cross-dock staging and direct transfer from inbound unloading doors to outbound outbound trailers without intermediate putaway storage.
Calculates direct flow-through percentage, reduces labor touchpoints from 6 touches to 2 touches, and minimizes dock staging dwell time.

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "optimize_cross_dock_flow_through",
    "arguments": {
    "inbound_pallets": [
        {
            "pallet_id": "PL-01",
            "sku": "SKU-A",
            "destination_order_code": "DEST-CHI",
            "inbound_dock_door": "DOOR-02"
        },
        {
            "pallet_id": "PL-02",
            "sku": "SKU-B",
            "destination_order_code": "DEST-LAX",
            "inbound_dock_door": "DOOR-02"
        },
        {
            "pallet_id": "PL-03",
            "sku": "SKU-C",
            "destination_order_code": "UNALLOCATED_STORAGE",
            "inbound_dock_door": "DOOR-03"
        }
    ],
    "outbound_shipments": [
        {
            "destination_code": "DEST-CHI",
            "outbound_dock_door": "DOOR-24"
        },
        {
            "destination_code": "DEST-LAX",
            "outbound_dock_door": "DOOR-28"
        }
    ]
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
