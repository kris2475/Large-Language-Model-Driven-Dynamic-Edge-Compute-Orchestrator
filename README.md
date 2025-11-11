# 🧠 LLM-DECO: Large Language Model-Driven Dynamic Edge Compute Orchestrator  
*A Context-Aware, Self-Tuning IoT Network for Sustainable Edge Computing*

---

## 🌟 Overview  

**LLM-DECO** (Large Language Model-Driven Dynamic Edge Compute Orchestrator) introduces a genuinely intelligent and adaptive AI management layer for constrained **Internet of Things (IoT)** networks.  

Instead of relying on static or reactive logic, LLM-DECO transforms a distributed network of low-power sensors into a **coordinated, goal-oriented system** that intelligently manages its own energy and compute resources.

At its core, **Dynamic Edge Compute Orchestration (DECO)** is about intelligent, autonomous management of distributed compute and power resources — guided by the reasoning power of an LLM.

---

## 🎯 Core Capabilities  

### 🧩 Goal Translation  
Transforms natural-language mission objectives (e.g.,  
> “Monitor the North Corridor, but conserve 70% battery on Node 5 for the next 12 hours”)  
into **precise, executable system policies**.

### ⚡ Strategic Wake-Up  
Builds on the *Wake-on-Energy-Sensors* paradigm. The LLM instructs the **Control Hub** on which node(s) to wake, when to wake them, and which optimized policy to run — **minimizing energy waste while maintaining mission objectives**.

---

## 🚀 Key Innovations  

- **Strategic Planning** — The LLM balances contradictory human objectives and hardware constraints with contextual reasoning.  
- **Hybrid Optimization** — Combines LLM strategic reasoning with **Bayesian Optimization (BO)** for fine-grained numerical tuning.  
- **Proactive Energy Management** — Schedules tasks dynamically based on real-time or predicted **energy harvesting opportunities** (e.g., solar input).

---

## 🏗️ System Architecture  

LLM-DECO is structured as a **hierarchical control system** with three cooperating layers:

### 1. 🧠 The Commander *(LLM Layer)*  
**Role:** Strategic Planner  
- Receives mission goals and full network telemetry (battery levels, light intensity, RF noise).  
- Generates an **objective function** and **constraints** for the optimizer.  
- Produces a **deterministic JSON command** (e.g., `"Wake Node 4", "Set policy to low-power"`).

### 2. 🔬 The Optimiser *(Bayesian Optimisation)*  
**Role:** Efficiency Engineer  
- Implements probabilistic optimization to search complex parameter spaces (e.g., sampling frequency vs. energy use).  
- Returns optimal numerical settings that satisfy the LLM-defined goals.

### 3. ⚙️ The Executor *(Control Hub + Edge Nodes)*  
**Hub (Master):**  
- Parses the JSON command from the LLM.  
- Issues targeted **Radio Controlii** wake-up signals.  

**Edge Node (Slave):**  
- Wakes on demand.  
- Loads updated sensing or transmission policies.  
- Executes optimized tasks (e.g., BME680 sampling).  
- Transmits data and returns to deep sleep.

---

## 🧪 Simulation Environment  

LLM-DECO includes (or recommends) a **Python-based Digital Twin Simulator** for safe, rapid testing.  
This simulator models **thermal, power, and network dynamics**, enabling realistic evaluation of LLM reasoning and optimization without hardware risk.

| Component | Technology | Role |
|------------|-------------|------|
| **LLM Interface** | Gemini API / OpenAI API | Strategic reasoning, JSON command generation |
| **Optimization** | Python (SciPy / GPyOpt) | Bayesian optimization for parameter tuning |
| **Hub Controller** | Python / C++ | Interface with XBee / Radio Controlii hardware |
| **Edge Hardware** | ATmega4808, ESP32, BME680 | Low-power sensing and energy harvesting |

---

## ⚙️ Getting Started  

### 1️⃣ Clone the Repository  
```bash
git clone [repository-link]
cd LLM-DECO
```

### 2️⃣ Configure the Simulation  
Edit the network model and initial state in:  
```
simulator/config.json
```

### 3️⃣ Add Your LLM API Key  
Insert your API key into `llm_orchestrator.py`:  
```python
LLM_API_KEY = "your_api_key_here"
```

### 4️⃣ Run the Orchestrator  
Execute the main orchestration loop:  
```bash
python main.py
```

You’ll see the LLM dynamically manage the simulated IoT network — balancing mission goals, energy, and compute resources.

---

## 📊 Example Workflow  

1. User issues mission goal in plain English.  
2. LLM-DECO interprets and translates it into an optimization problem.  
3. BO searches parameter space for efficiency.  
4. Control Hub deploys commands to selected edge nodes.  
5. Nodes execute tasks and report telemetry.  

---

## 🌍 Sustainability Impact  

By aligning **intelligent orchestration** with **energy-aware design**, LLM-DECO:  
- Extends network lifetime.  
- Minimizes energy waste.  
- Enables context-aware, low-carbon IoT infrastructure.

---

## 🧭 Future Directions  

- Integration with **real-world solar harvesting nodes**.  
- Federated learning across distributed LLM-DECO clusters.  
- Reinforcement learning for adaptive strategy refinement.  

---

## 🧾 License  
This project is licensed under the **Apache License, Version 2.0 (January 2004)**.  
You may obtain a copy of the License at:  
[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

---

## 👥 Author
K Seunarine

---

> “From passive sensors to proactive agents — LLM-DECO is the cognitive upgrade IoT has been waiting for.”
