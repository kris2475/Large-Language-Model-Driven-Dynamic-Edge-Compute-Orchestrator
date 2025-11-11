import json
from typing import List, Dict, Any
from node_simulator import IoTNodeSimulator, MAX_CAPACITY # Import necessary components

# --- LLM OUTPUT JSON SCHEMA (The critical command format) ---
# This schema dictates the exact JSON the LLM MUST return.
LLM_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "description": "The high-level action to take. Must be 'WAKE_NODE' or 'DO_NOTHING'."
        },
        "target_node_id": {
            "type": "string",
            "description": "The Node_ID (e.g., 'Node_42') to send the wake-up signal to. Required if action is WAKE_NODE."
        },
        "new_policy": {
            "type": "string",
            "description": "The sensing policy the node should run after waking. Must be 'SENSE_LOW' or 'SENSE_HIGH'."
        },
        "bo_parameters": {
            "type": "object",
            "description": "Optimal numerical settings found by Bayesian Optimization.",
            "properties": {
                "sampling_interval_s": {"type": "number", "description": "The optimised sampling interval in seconds."},
                "tx_power_dbm": {"type": "number", "description": "The optimised transmission power in dBm."}
            }
        },
        "reasoning": {
            "type": "string",
            "description": "A brief explanation of the decision based on mission goal, energy, and uncertainty."
        }
    },
    "required": ["action", "reasoning"]
}

def generate_llm_prompt(network_state_json: str, mission_goal: str) -> str:
    """Constructs the full prompt passed to the LLM."""
    prompt = f"""
    You are the Large Language Model-Driven Dynamic Edge Compute Orchestrator (LLM-DECO).
    Your task is to analyse the current state of the IoT network and determine the optimal single action.
    Your goal is to satisfy the MISSION GOAL while prioritising network longevity.

    ---
    MISSION GOAL: "{mission_goal}"
    ---
    CURRENT NETWORK STATE (JSON Array):
    {network_state_json}
    ---

    INSTRUCTIONS:
    1. Analyse the 'data_uncertainty' and 'battery_percent' for all nodes.
    2. Select ONE node to wake if necessary ('action': 'WAKE_NODE'), or 'DO_NOTHING'.
    3. If WAKE_NODE, choose 'new_policy' ('SENSE_LOW' or 'SENSE_HIGH'). Prioritise nodes with high 'harvest_potential' for 'SENSE_HIGH'.
    4. Provide the output ONLY as a JSON object that strictly adheres to the provided JSON Schema.
    5. The 'bo_parameters' should contain the final numerical output from your internal Bayesian Optimisation routine (use plausible, realistic numbers).
    """
    return prompt

def simulate_llm_api_call(network_state_json: str, mission_goal: str) -> Dict[str, Any]:
    """
    Simulates the call to the LLM API to get the structured JSON command.
    The logic is now hardcoded to follow the mission goal constraints.
    """
    
    # Parse the input state from the JSON string
    network_state = json.loads(network_state_json)
    
    # Logic: Find the node with the highest uncertainty that meets the battery constraint (>= 20%)
    best_candidate = None
    max_uncertainty = -1
    MIN_BATTERY_PERCENT = 20.0 # Constraint from mission goal
    
    for node in network_state:
        # Check battery constraint
        battery_ok = node.get('battery_percent', 0) >= MIN_BATTERY_PERCENT
        
        # Check uncertainty level
        uncertainty = node.get('data_uncertainty', 0)
        
        if battery_ok and uncertainty > max_uncertainty:
            max_uncertainty = uncertainty
            best_candidate = node
            
    # Decision Point: Only act if uncertainty is high enough (e.g., > 0.6) and a candidate exists
    if best_candidate and max_uncertainty > 0.6: 
        
        # Determine the best policy based on harvest potential
        if best_candidate.get('harvest_potential', 0) > 0.7:
            # High harvest potential means we can afford SENSE_HIGH for better data
            policy = "SENSE_HIGH"
            # BO suggests aggressive parameters to maximize data quality
            bo_params = {"sampling_interval_s": 5.0, "tx_power_dbm": 10.0} 
            
            reason = (
                f"{best_candidate['node_id']} has the highest uncertainty ({max_uncertainty}) and meets the {MIN_BATTERY_PERCENT}% battery minimum. "
                f"It also has high harvest potential ({best_candidate['harvest_potential']}), justifying the energy-intensive {policy} policy to rapidly meet the mission goal."
            )
        else:
            # Low harvest potential, use the lower-cost policy
            policy = "SENSE_LOW"
            # BO suggests conservative parameters
            bo_params = {"sampling_interval_s": 30.0, "tx_power_dbm": 5.0} 
            
            reason = (
                f"{best_candidate['node_id']} has the highest uncertainty ({max_uncertainty}) and meets the {MIN_BATTERY_PERCENT}% battery minimum. "
                f"We are using the energy-efficient {policy} policy due to low ambient harvest potential."
            )
            
        return {
            "action": "WAKE_NODE",
            "target_node_id": best_candidate['node_id'],
            "new_policy": policy,
            "bo_parameters": bo_params,
            "reasoning": reason
        }
    
    # Fallback to DO_NOTHING
    return {
        "action": "DO_NOTHING",
        "reasoning": "No node requires critical action. All high-uncertainty nodes are either below the 20% critical battery threshold or all uncertainty is currently acceptable."
    }

# --- MAIN EXECUTION LOGIC ---
if __name__ == "__main__":
    
    # 1. GATHER NETWORK STATE (using our simulator)
    
    # Node 42: High battery, low uncertainty
    node_a = IoTNodeSimulator("Node_42", initial_capacity=MAX_CAPACITY * 0.8333)
    node_a.state.harvest_potential = 0.0
    node_a.state.data_uncertainty = 0.5
    
    # Node 11: Low battery, HIGH uncertainty, HIGH harvest potential -> TARGET NODE
    node_b = IoTNodeSimulator("Node_11", initial_capacity=MAX_CAPACITY * 0.2778) 
    node_b.state.harvest_potential = 0.9 
    node_b.state.data_uncertainty = 0.8 
    
    # Convert nodes to the format expected by the LLM
    network_state = [json.loads(node_a.to_json()), json.loads(node_b.to_json())]
    network_state_json = json.dumps(network_state, indent=4)

    # 2. DEFINE THE MISSION GOAL
    mission = "Reduce the highest data uncertainty in the network, but do not wake any node with less than 20% battery."

    print("## Input Network State (for LLM) ##")
    print(network_state_json)
    print(f"\n## Mission Goal ##\n{mission}")
    print("\n-------------------------------------------------\n")

    # 3. CALL LLM AND GET STRUCTURED COMMAND
    final_command = simulate_llm_api_call(network_state_json, mission)

    # 4. OUTPUT FINAL JSON
    print("## LLM-DECO Final Command (JSON for Control Hub) ##")
    final_command_json = json.dumps(final_command, indent=4)
    print(final_command_json)