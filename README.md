<img width="732" height="930" alt="gui2" src="https://github.com/user-attachments/assets/d4e891c6-11e7-41b0-8767-3611f1796fa8" />

# Kingdom: New Lands - Savegame Editor & Manager 👑🐎

A lightweight, open-source GUI tool to tweak your *Kingdom: New Lands* save files and manage multiple save slots. Designed for rulers who love the game but have a busy life!

## Why I built this
After a few frustrating runs on the higher islands, I was almost ready to give up on *Kingdom: New Lands*. As much as I enjoy the game, it simply takes too much time to balance with a full-time job and family life. I wanted to see the later stages of the game without the massive time sink, so I built this tool to speed things up and safely manage my progress.

---

## ✨ Features

### 💾 Savegame Manager (NEW in v1.1.0)
* **5 Save Slots:** Easily back up your current progress to one of 5 dedicated slots.
* **Auto-Timestamps:** Slots automatically display the date and time (AM/PM format) of your save.
* **Easy Restore:** Messed up a run? Just load your preferred slot and try again without losing everything!

### 🛠️ Quality of Life Tweaks
* **🏹 Add Archers:** Instantly reinforce your left or right side with new units.
* **💰 Max Coins:** Fill the Banker's stash (999) or your personal Wallet (40).
* **⚡ Persistent Shrines:** Set **ALL 4** statues (Archers, Workers, Knights, Building) to last 999 days.
* **🌌 Weak Portals:** Reduce all intact enemy portals to 1 HP for a much faster clear.
* **🛡️ Safety First:** Automatically creates a backup (`storage_v34_AUTO.dat#bckp`) before any changes.

---

## 📂 Where is my Savegame?
The tool modifies the file usually named `storage_v34_AUTO.dat`. It appears after starting and saving a game.
* **Windows:** `%USERPROFILE%\AppData\LocalLow\noio\Kingdom\`
* **macOS:** `~/Library/Application Support/noio/Kingdom/`
* **Linux:** `~/.config/unity3d/noio/Kingdom/`

---

## 📥 Installation & Usage

### 1. Standalone Versions (No Python required)
Go to the [**Releases**](https://github.com/noplan724/Kingdom_NL_Savegame-editor/releases) section on the right and download the latest version for your system:

* **Windows:** Download the `.exe` file. Double-click to run. (If Windows SmartScreen pops up, click "More info" -> "Run anyway").
* **macOS:** Download the Mac `.zip` and extract it. **Right-click** the `.app` and select **Open** to bypass the "Unidentified Developer" warning.
* **Linux:** Download the Linux binary. Make it executable (`chmod +x Linux.KNL.Savegame-editor`) and launch it via terminal (`./Linux.KNL.Savegame-editor`).

### 2. Python Version (Open Source)
If you prefer running the script directly from source:
1. Download `knl_savegame_editor.py`.
2. Install dependencies: `pip install customtkinter`.
3. Run: `python knl_savegame_editor.py`.

---

## ⚠️ Important!
**Make sure the game is completely closed** before using this tool! If the game is running, it might overwrite your changes or fail to load the restored save slots. Always save and quit your game first.

---

## 📜 License
This project is **Open Source** and licensed under the [MIT License](LICENSE). Feel free to check the code, report bugs, or suggest features!

*Disclaimer: Use at your own risk. Always keep a manual backup of your save files if you are worried about your progress.*
