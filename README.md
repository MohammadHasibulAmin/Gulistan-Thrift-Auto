# 🏙️ Gulistan Thrift Auto

A medium-scale OpenGL-based city simulation game built using **Python and PyOpenGL**, featuring a 2D road network with 3D buildings, roaming NPCs, pickpocket mechanics, multiple weapons, drivable vehicles, and interactive city elements.

---

## 📌 Overview

**Gulistan Thrift Auto** is a third-person / first-person hybrid city simulation where the player navigates an urban environment, interacts with NPCs, pickpockets them under time constraints, engages in combat using multiple weapon types, and drives different vehicles. The project emphasizes real-time interaction, camera control, and basic AI behavior.

---

## 👥 Authors
**Group Members**
- [Mohammad Hasibul Amin](https://github.com/MohammadHasibulAmin)
- [Fabiha Tarannum Areena](https://github.com/FabihaTarannumA)
- [Md. Mushfiqur Rahman](https://github.com/mMushfiqurR)

CSE423 Section 13 Fall'25  
Department of Computer Science and Engineering, BRAC University  

## 🏗️ Environment Design

- **2D Road Network**
  - Main road and intersections rendered on the XY-plane
  - Sidewalks and river included for environmental detail

- **3D Buildings**
  - Procedurally generated buildings along sidewalks
  - Variable heights and colors
  - Special interaction buildings:
    - **Black building** – Purchase sniper rifle
    - **Brown building** – Purchase automatic rifle
    - **Pink building** – Change player t-shirt color

- **Skybox**
  - Large enclosed sky environment for visual immersion

---

## 🧍 NPC System

- 2–3 roaming NPCs dynamically move around the city
- NPC behavior includes:
  - Autonomous roaming
  - Player pursuit
  - Distance-based interaction detection
- NPCs interact with the player through combat and pickpocket mechanics

---

## 🕵️ Pickpocketing Mechanic

- Activated when the player is **within 20–40 units** of an NPC
- A **2-second time window** is provided
- Press **X** within the time limit to successfully pickpocket
- **Successful pickpocket**
  - Player gains in-game money
  - NPC respawns at a random location
- **Failure conditions**
  - Time window expires
  - Player moves out of range
  - NPC reaches the player and attacks, reducing hit points

---

## 🔫 Weapons System

Three distinct weapon types are implemented:

### 🔹 Pistol
- Default weapon
- One click → one bullet
- Moderate fire rate

### 🔹 Automatic Rifle
- Purchased using in-game money
- Continuous firing while holding left mouse button
- Higher fire rate

### 🔹 Sniper Rifle
- Purchased using in-game money
- High damage output
- Zoom functionality:
  - Right-click to zoom in
  - Dynamic camera repositioning
  - Field-of-view (FOV) reduction

### Weapon Controls
| Key | Weapon |
|----|-------|
| 1 | Pistol |
| 2 | Automatic Rifle |
| 3 | Sniper Rifle |

---

## 🚗 Vehicle System

- Three vehicle types:
  - Sport
  - Sedan
  - SUV
- Vehicles differ in:
  - Speed
  - Height
  - Body proportions
- Vehicles roam autonomously when not controlled

### Player Interaction
- Press **F** near a vehicle to enter
- Player movement is transferred to the vehicle
- Press **F** again to exit

---

## 🎥 Camera System

- **Third-Person View (TPP)** – Default camera mode
- **First-Person View (FPV)** – Activated during sniper zoom
- Smooth camera positioning using `gluLookAt`
- Dynamic FOV adjustments for scoped gameplay

---

## 🎮 Controls

### Movement
| Key | Action |
|----|-------|
| W | Move forward |
| S | Move backward |
| A | Rotate left |
| D | Rotate right |

### Combat
| Input | Action |
|------|-------|
| Left Click | Fire weapon |
| Right Click | Sniper zoom |
| 1 | Pistol |
| 2 | Automatic rifle |
| 3 | Sniper rifle |

### Interaction
| Key | Action |
|----|-------|
| X | Pickpocket NPC |
| F | Enter / Exit vehicle |

---

## 🧠 Game Logic Highlights

- Bullet physics using trigonometric direction vectors
- Collision detection:
  - Bullets vs NPCs
  - Player vs NPC proximity
  - Player vs vehicles
- Cooldown-based weapon firing system
- Time-based pickpocketing mechanic
- Procedural city layout generation

---

## 🛠️ Technologies Used

- Python 3
- PyOpenGL
- GLUT
- OpenGL (Immediate Mode)

---

## ▶️ How to Run

### Requirements
```bash
pip install PyOpenGL PyOpenGL_accelerate
```

### Run The Game
```bash
python S13_G4.py
```

### 📄 License

This project is intended for educational purposes only.

