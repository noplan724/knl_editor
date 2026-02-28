<img width="692" height="860" alt="gui" src="https://github.com/user-attachments/assets/56dfcad7-89f6-431f-b1ce-6ddc5deb64a0" />


# Kingdom: New Lands - Save Editor

This is just a small hobby project I made to easily tweak savegames in *Kingdom: New Lands* without having to manually edit the `.dat` files. 

It features a simple GUI to add units, get some coins, or make the enemy portals a lot weaker. 

## Features
* **Add Archers:** Spawns new archers on the left or right side.
* **Get Coins:** Maxes out the Banker (999) or your personal Wallet (40).
* **Super Shrines:** Sets the Archer and Worker shrines to last 999 days.
* **Weak Portals:** Reduces all intact portals to 1 HP.

## ⚠️ Important!
Make sure the game is **closed** before you use this tool! If the game is running, your changes won't be saved or the game might overwrite them.
*(Note: The tool automatically creates a backup named `storage_34_AUTO.dat#bckp` the first time you use it, just in case).*

---

## Option 1: Using the Mac App (.app)
If you are on a Mac and don't want to mess with code, you can just use the pre-built app.

1. Download the `KingdomSaveEditor.app.zip` from the Releases section and extract it.
2. Because I'm not a registered Apple Developer, macOS maybe blocks the app if you just double-click it. 
3. **If so: To open it:** **Right-click** (or Control-click) the `.app` file and select **Open**. Click **Open** again in the warning prompt. 
4. Click "Change File" and find your savegame.
   *(Usually located in `~/Library/Application Support/noio/Kingdom/`*.

---

## Option 2: Running from Source (Python)
If you want to run the script yourself, you can use the Python source code.

**Requirements:**
* Python 3 installed
* `customtkinter` package for the GUI

**Run:**
1. Clone this repository or download the `knl_savegame_editor.py` file.
2. Open your terminal / command prompt and install the required UI library:
   ```bash
   pip install customtkinter
   ```
3. Run the script:
   ```bash
   python knl_savegame_editor.py
   ```
4. Select your `storage_34_AUTO.dat` save file and apply the cheats you want.

## Disclaimer
This is just a fun little DIY project. Use it at your own risk!
