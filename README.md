# 🧠 Wumpus World AI Agent

### Propositional Logic + Resolution Refutation + Interactive Visualization

This project implements a **knowledge-based AI agent** that operates in the classic **Wumpus World environment** using **propositional logic and resolution inference**.

Unlike basic implementations, this system includes a **custom resolution engine**, **dynamic knowledge base**, and a **real-time web interface** to visualize the agent's reasoning process.

---

## 🚀 Features

* ✅ Custom **Resolution Refutation Engine**
* ✅ Knowledge Base with CNF clause management
* ✅ Logical inference for:

  * Pit detection
  * Wumpus detection
  * Safe cell prediction
* ✅ Interactive **Flask Web Interface**
* ✅ Real-time metrics:

  * Inference steps
  * Knowledge base size
  * Agent percepts
* ✅ Dynamic grid with:

  * Hidden hazards
  * Agent exploration
  * Visual feedback

---

## 🧩 Core Concepts

This project demonstrates:

* Propositional Logic
* CNF (Conjunctive Normal Form)
* Resolution-based inference
* Knowledge-based agents
* Rule-based reasoning under uncertainty

---

## 🏗️ System Architecture

```
User Interface (HTML/CSS/JS)
        ↓
Flask Backend (API Layer)
        ↓
Knowledge Base (Logical Clauses)
        ↓
Resolution Engine (Inference)
        ↓
Wumpus World Simulation
```

---

## 🎮 How It Works

1. The agent starts at position (0,0) — guaranteed safe.
2. It perceives:

   * `breeze` → nearby pit
   * `stench` → nearby Wumpus
   * `glitter` → gold
3. These percepts are added to the **Knowledge Base**.
4. The **Resolution Engine**:

   * Converts KB to CNF
   * Applies resolution to infer new facts
5. The agent queries:

   * Is a cell safe?
   * Can it move without risk?

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/wumpus-world-ai.git
cd wumpus-world-ai
```

### 2. Install dependencies

```bash
pip install flask flask-cors
```

### 3. Run the server

```bash
python app.py
```

### 4. Open in browser

```
http://localhost:5000
```

---

## 📊 API Endpoints

| Endpoint              | Description                  |
| --------------------- | ---------------------------- |
| `/api/new_game`       | Initialize new environment   |
| `/api/move`           | Move agent                   |
| `/api/get_safe_cells` | Infer safe neighboring cells |

---

## 🧠 Example Inference

If:

* Breeze at (x, y)

Then:

* At least one adjacent cell contains a pit

Using resolution:

* The agent eliminates impossible locations
* Infers safe cells logically

---

## 📌 Limitations

* Resolution can be computationally expensive (O(n²) clause pairing)
* No heuristic optimization (pure logic-based reasoning)
* Limited to propositional logic (no probabilistic reasoning)

---

## 🔮 Future Improvements

* Heuristic-guided inference
* Probabilistic reasoning (Bayesian approach)
* Path planning (A* or BFS integration)
* Smarter agent (utility-based decisions)
* Performance optimization for resolution

---

## 🧑‍💻 Tech Stack

* Python
* Flask
* HTML/CSS/JavaScript
* Logic Programming Concepts

---

## 📷 Preview

> Interactive grid showing agent movement, hazards, and inferred safe cells.

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 💡 Why This Project Matters

Most Wumpus World implementations rely on hardcoded rules.
This project instead demonstrates a **true logic-based inference system**, making it closer to **real AI reasoning systems**.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss.

---

## ⭐ Support

If you find this project useful, consider giving it a star!
