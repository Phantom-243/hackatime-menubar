# HackatimeBar

> A native macOS menu bar companion for anyone participating in the Stardance Challenge built with Python, `rumps`, and PyObjC. Tracks daily coding hours, active languages, and Stardust farming targets in real-time right on your desktop.

---

# Features

- **Zero-Configuration Engine**: Automatically detects your Hackatime API key and custom endpoints by parsing `~/.wakatime.cfg` based off standard macOS system paths.
- **Live Status Bar Display**: Renders your real-time tracked time directly in the macOS top status bar with no present dock icon (`LSUIElement`).
- **Calibrated Stardust Estimation**: Estimates your stardust earnings based off a standard 10x multiplier (you can change this in app.py)
- **Interactive Daily Goal Prompt**: Built-in modal window (`rumps.Window`) that lets you set custom daily hour targets on the fly, paired with a dynamic ASCII progress bar.
- **Single-Click Utility**: One-click quick links to the official Hackatime dashboard and Stardance submission portal.
- **Automatic & Manual refresh**: Automatically polls hackatime every 120 seconds and has a button to instantly poll it as well.

---

# Installation

# Option 1: Standalone Installer (Recommended)
No terminal or Python required or any dependancies, just your plain vanilla mac:
1. Head to the **GitHub release page (https://github.com/Phantom-243/hackatime-menubar/releases)**.
2. Download **"HackatimeBar.dmg**.
3. Open the .dmg and drag HackatimeBar into your Applications folder.
4. Launch the app from Applications or Spotlight like any other mac app!

---

# Option 2: Run from Source

If for some reason you want to build and run from source just follow these steps:

```bash
# Step 1: Clone the repo
git clone https://github.com/Phantom-243/hackatime-menubar.git
cd hackatime-menubar

# Step 2: Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Step 3: Install needed dependencies
pip install -r requirements.txt

# Step 4: Run the app
python app.py

**Happy Hacking!**
#Drop me an email at saad.syed.ali11@gmail.com if you have any questions.

*Additional Steps:

#To build the dmg locally, just paste these commands:
pyinstaller --noconsole --windowed --name "HackatimeBar" --icon=icon.icns --add-data "tracker.py:." app.py
plutil -insert LSUIElement -bool true dist/HackatimeBar.app/Contents/Info.plist
mkdir -p dmg_build
cp -r dist/HackatimeBar.app dmg_build/
ln -s /Applications dmg_build/Applications
hdiutil create -volname "HackatimeBar" -srcfolder dmg_build -ov -format UDZO HackatimeBar.dmg
rm -rf dmg_build