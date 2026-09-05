import rumps
import webbrowser
from tracker import fetch_today_stats

STARDUST_MULTIPLIER = 10.0

class HackatimeBarApp(rumps.App):
    def __init__(self):
        super().__init__(
            name="HackatimeBar",
            title="✨ Loading...",
            quit_button="Quit Hackatime Bar"
        )
        
        self.daily_goal_hours = 4.0

        # 1. Define all menu items explicitly first
        self.time_item = rumps.MenuItem("⏱ Today's Coding: Loading...")
        self.stardust_item = rumps.MenuItem("🌟 Farming Stardust: Loading...")
        self.goal_item = rumps.MenuItem("🎯 Daily Goal: ...")
        self.projects_item = rumps.MenuItem("📁 Projects: Loading...")
        self.languages_item = rumps.MenuItem("💻 Languages: Loading...")
        self.set_goal_item = rumps.MenuItem("⚙️ Set Daily Goal...", callback=self.prompt_change_goal)
        self.refresh_item = rumps.MenuItem("🔄 Refresh Now", callback=self.manual_refresh)
        self.web_item = rumps.MenuItem("🌐 Open Hackatime Web", callback=self.open_hackatime)
        self.stardance_item = rumps.MenuItem("🚀 Open Stardance Portal", callback=self.open_stardance)

        # 2. Assemble the macOS dropdown menu
        self.menu = [
            self.time_item,
            self.stardust_item,
            self.goal_item,
            None,  # Separator line
            self.projects_item,
            self.languages_item,
            None,  # Separator line
            self.set_goal_item,
            self.refresh_item,
            self.web_item,
            self.stardance_item,
            None   # Separator line before Quit button
        ]
        
        # 3. Fetch and display stats immediately on launch
        self.update_stats(None)

    # Automatically polls Hackatime every 120 seconds (2 minutes)
    @rumps.timer(120)
    def update_stats(self, _):
        stats = fetch_today_stats()

        if stats.get("error"):
            self.title = "⚠️ Hackatime"
            self.time_item.title = f"Error: {stats['error']}"
            return

        total_text = stats.get("total_text", "0 secs")
        hours = stats.get("hours", 0.0)
        estimated_stardust = round(hours * STARDUST_MULTIPLIER, 1)

        # 1. Update text displayed directly on top Mac Menu Bar
        self.title = f"✨ {total_text}"

        # 2. Update summary details
        self.time_item.title = f"⏱ Today's Coding: {total_text}"
        self.stardust_item.title = f"🌟 Estimated Stardust: ~{estimated_stardust}"

        # 3. Dynamic ASCII progress bar towards daily goal
        if self.daily_goal_hours > 0:
            percent = min(int((hours / self.daily_goal_hours) * 100), 100)
        else:
            percent = 100
        
        filled = int(percent / 10)
        bar = "█" * filled + "░" * (10 - filled)
        self.goal_item.title = f"🎯 Daily Goal: [{bar}] {percent}% ({hours:.1f}/{self.daily_goal_hours:.1f}h)"

        # 4. Update Projects info
        projects = stats.get("projects", [])
        if projects:
            proj_summary = ", ".join([f"{p['name']} ({p['text']})" for p in projects[:2]])
            self.projects_item.title = f"📁 Projects: {proj_summary}"
        else:
            self.projects_item.title = "📁 Projects: None tracked yet today"

        # 5. Update Languages info
        languages = stats.get("languages", [])
        if languages:
            lang_summary = ", ".join([f"{l['name']} ({l['percent']}%)" for l in languages[:3]])
            self.languages_item.title = f"💻 Languages: {lang_summary}"
        else:
            self.languages_item.title = "💻 Languages: None tracked yet today"

    def prompt_change_goal(self, _):
        window = rumps.Window(
            message="Enter your. daily coding goal in hours (e.g. 2, 4, 6.5):",
            title="🎯 Set Daily Goal",
            default_text=f"{self.daily_goal_hours:.1f}",
            ok="Save Goal",
            cancel="Cancel",
            dimensions=(220, 24)
        )
        response = window.run()

        if response.clicked:
            try:
                new_goal = float(response.text.strip())
                if new_goal > 0:
                    self.daily_goal_hours = new_goal
                    self.update_stats(None)
                else:
                    rumps.alert("Invalid Goal", "Please enter a number greater than 0.")
            except ValueError:
                rumps.alert("Invalid Input", "Please enter a valid number (e.g. 4 or 5.5)")

    def manual_refresh(self, _):
        self.title = "🔄 Syncing..."
        self.update_stats(None)

    def open_hackatime(self, _):
        webbrowser.open("https://hackatime.hackclub.com")

    def open_stardance(self, _):
        webbrowser.open("https://stardance.hackclub.com")

if __name__ == "__main__":
    HackatimeBarApp().run()