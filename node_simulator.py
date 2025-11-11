import json
from dataclasses import dataclass, field
from datetime import datetime
import random

# --- CONFIGURATION CONSTANTS (Can be moved to a separate config file) ---
# Power consumption in Watts (W) for different states
POWER_CONSUMPTION = {
    "SLEEP": 0.00001,      # Ultra-low power sleep (watts)
    "WAKE_LISTEN": 0.05,   # Listening for wake-up signal (Radio Controlii)
    "SENSE_LOW": 0.02,     # Low-fidelity sensing (e.g., basic temperature)
    "SENSE_HIGH": 0.15,    # High-fidelity sensing (e.g., BME680 full scan)
    "TRANSMIT": 0.25,      # XBee radio transmission
}
HARVEST_RATE_MAX = 0.005 # Max possible energy harvested per second (e.g., Solar/Thermal)
MAX_CAPACITY = 3600      # Total battery capacity in Joules (e.g., 1000mAh @ 3.6V = 12960J. Using a smaller value for demonstration)

@dataclass
class NodeState:
    """Dataclass representing the current, real-time status of an IoT node."""
    node_id: str
    battery_joules: float = MAX_CAPACITY
    current_policy: str = "SLEEP"
    last_wake_time: str = datetime.now().isoformat()
    harvest_potential: float = 0.0  # Measured ambient light/heat potential (0.0 to 1.0)
    data_uncertainty: float = 0.5   # Placeholder for BO-derived uncertainty metric (0.0 to 1.0)

class IoTNodeSimulator:
    def __init__(self, node_id: str, initial_capacity: float = MAX_CAPACITY):
        self.state = NodeState(node_id=node_id, battery_joules=initial_capacity)
        self.time_step = 1.0  # Simulate in 1-second increments

    def _calculate_power_change(self) -> float:
        """Calculates energy change (Joules/sec) based on current state and harvest."""
        
        # 1. Consumption based on policy
        P_consume = POWER_CONSUMPTION.get(self.state.current_policy, POWER_CONSUMPTION["SLEEP"])

        # 2. Harvest based on ambient potential (e.g., 0.5 potential = 50% of max harvest)
        P_harvest = self.state.harvest_potential * HARVEST_RATE_MAX
        
        # Total change (Joules/sec)
        return P_harvest - P_consume

    def update_state(self, duration_s: float) -> None:
        """Simulates the passage of time and updates battery level."""
        energy_change_rate = self._calculate_power_change()
        energy_change = energy_change_rate * duration_s
        
        self.state.battery_joules += energy_change

        # Clamp battery level
        self.state.battery_joules = max(0, min(MAX_CAPACITY, self.state.battery_joules))
        self.state.last_wake_time = datetime.now().isoformat()

    def set_policy(self, new_policy: str) -> None:
        """Updates the policy (e.g., after being woken up by the Hub)."""
        if new_policy in POWER_CONSUMPTION:
            self.state.current_policy = new_policy

    def to_json(self) -> str:
        """Returns the current state as a formatted JSON string for the LLM input."""
        # Convert dataclass to a dictionary, then to JSON string
        state_dict = {
            "node_id": self.state.node_id,
            "battery_percent": round((self.state.battery_joules / MAX_CAPACITY) * 100, 2),
            "current_policy": self.state.current_policy,
            "harvest_potential": self.state.harvest_potential,
            "data_uncertainty": round(self.state.data_uncertainty, 4),
            "max_capacity_joules": MAX_CAPACITY
        }
        return json.dumps(state_dict, indent=4)

# --- EXAMPLE USAGE ---
if __name__ == "__main__":
    node1 = IoTNodeSimulator("Node_42")
    
    # 1. Simulate a period of sleep with some harvest
    node1.state.harvest_potential = 0.8
    print(f"[{node1.state.node_id}] Initial State:\n{node1.to_json()}")

    node1.update_state(3600) # One hour of sleep (should gain energy)
    print("\n--- After 1 hour of SLEEP with 80% Harvest ---")
    print(node1.to_json())

    # 2. Simulate a brief high-cost operation after a wake-up
    node1.set_policy("SENSE_HIGH")
    node1.state.harvest_potential = 0.0 # Night time
    node1.update_state(60) # 60 seconds of high-fidelity sensing + transmission (high cost)
    node1.set_policy("SLEEP") # Return to sleep
    print("\n--- After 1 minute of SENSE_HIGH at Night ---")
    print(node1.to_json())