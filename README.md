# HackatimeBar

A native menubar app for mac which runs cleanly in your menubar, displaying live stats, goals, and estimated stardust from Hackatime.


## Features

- No Configuration Needed: Automatically detects your Hackatime API key from your computer by parsing `~/.wakatime.cfg`
- Live Status Bar Display: Displays your live tracked time directly in the macOS menu bar with no dock icon visible using LSUIElement.
- Automatic Stardust Estimation: Estimates your stardust earnings based off a standard 10x multiplier (I got 10x from Stardacne saying 10 stardust per hour is the average payout; you can change this in app.py)
- Live progress bar: Built-in window that lets you set custom daily hours-of-coding targets, paired with a live ASCII progress bar to reflect it.
- Built in links: Convenient links to Hackatime and Stardance.
- Automatic & Manual refresh: Automatically polls hackatime every 120 seconds and has a button to instantly poll it as well.
- **Emojies!**: Has a nice, bright design with colourful emojies.


# Installation

## Option 1: Easy standard macOS installer
Literally nothing required, just your plain vanilla mac:
1: Head to the google drive (https://drive.google.com/file/d/1GtCrN-tZZCfNzzMMIB5Ab5A4KQOwouV5/view) or the github release page
2: Download HackatimeBar.dmg
3: Open the .dmg and drag HackatimeBar into your Applications folder.
4: Launch the app from Applications or Spotlight like any other mac app!


## Option 2: Run from Source

If for some reason you want to build and run from source code just follow these steps:

Step 1: Clone the repo
git clone https://github.com/Phantom-243/hackatime-menubar.git
cd hackatime-menubar

Step 2: Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

Step 3: Install needed dependencies
pip install -r requirements.txt

Step 4: Run the app
python app.py

**Happy Hacking!**
### Drop me an email at saad.syed.ali11@gmail.com if you have any questions.

**Additional Steps**:

### To build the dmg locally, just paste these commands:
pyinstaller --noconsole --windowed --name "HackatimeBar" --icon=icon.icns --add-data "tracker.py:." app.py
plutil -insert LSUIElement -bool true dist/HackatimeBar.app/Contents/Info.plist
mkdir -p dmg_build
cp -r dist/HackatimeBar.app dmg_build/
ln -s /Applications dmg_build/Applications
hdiutil create -volname "HackatimeBar" -srcfolder dmg_build -ov -format UDZO HackatimeBar.dmg
rm -rf dmg_build