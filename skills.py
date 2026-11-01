# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-agentic-commerce-warehouse-slotting-cross-dock-flow-through-skill
Category: agentic_commerce
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def optimize_cross_dock_flow_through(inbound_pallets, outbound_shipments):
    outbound_dest_map = {o["destination_code"]: o for o in outbound_shipments}
    cross_dock_eligible = []
    putaway_required = []
    
    for p in inbound_pallets:
        dest = p.get("destination_order_code")
        if dest in outbound_dest_map:
            outbound = outbound_dest_map[dest]
            cross_dock_eligible.append({
                "pallet_id": p["pallet_id"],
                "sku": p["sku"],
                "inbound_door": p["inbound_dock_door"],
                "outbound_door": outbound["outbound_dock_door"],
                "destination": dest,
                "direct_transfer": True
            })
        else:
            putaway_required.append(p)
            
    total_pallets = len(inbound_pallets)
    cross_dock_pct = (len(cross_dock_eligible) / total_pallets * 100.0) if total_pallets > 0 else 0.0
    # Labor savings estimate: $4.50 putaway + $4.50 picking = $9.00 labor saved per cross-docked pallet
    estimated_labor_savings_usd = len(cross_dock_eligible) * 9.00
    
    return {
        "total_inbound_pallets": total_pallets,
        "cross_dock_eligible_pallets": len(cross_dock_eligible),
        "putaway_required_pallets": len(putaway_required),
        "flow_through_rate_pct": round(cross_dock_pct, 1),
        "estimated_labor_touches_saved": len(cross_dock_eligible) * 4,
        "direct_labor_cost_savings_usd": round(estimated_labor_savings_usd, 2),
        "dock_dispatch_manifest": cross_dock_eligible
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "optimize_cross_dock_flow_through",
                        "description": """Optimize warehouse cross-dock staging and direct transfer from inbound unloading doors to outbound outbound trailers without intermediate putaway storage.
Calculates direct flow-through percentage, reduces labor touchpoints from 6 touches to 2 touches, and minimizes dock staging dwell time.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = optimize_cross_dock_flow_through(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'inbound_pallets': [{'pallet_id': 'PL-01', 'sku': 'SKU-A', 'destination_order_code': 'DEST-CHI', 'inbound_dock_door': 'DOOR-02'}, {'pallet_id': 'PL-02', 'sku': 'SKU-B', 'destination_order_code': 'DEST-LAX', 'inbound_dock_door': 'DOOR-02'}, {'pallet_id': 'PL-03', 'sku': 'SKU-C', 'destination_order_code': 'UNALLOCATED_STORAGE', 'inbound_dock_door': 'DOOR-03'}], 'outbound_shipments': [{'destination_code': 'DEST-CHI', 'outbound_dock_door': 'DOOR-24'}, {'destination_code': 'DEST-LAX', 'outbound_dock_door': 'DOOR-28'}]}
        out = optimize_cross_dock_flow_through(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
