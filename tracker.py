import os
import base64
import configparser
import requests

def get_hackatime_config():
    """
    Smart Auto-Detector:
    Searches all standard Hackatime / WakaTime file locations on macOS
    and robustly parses credentials without requiring manual setup.
    """
    candidate_paths = [
        os.path.expanduser("~/.wakatime.cfg"),
        os.path.expanduser("~/.wakatime/wakatime.cfg"),
        os.path.expanduser("~/.config/wakatime/wakatime.cfg"),
    ]

    api_key = None
    api_url = "https://hackatime.hackclub.com/api/hackatime/v1"
    detected_path = None

    for path in candidate_paths:
        if os.path.isfile(path):
            # Method A: Try standard INI parser
            try:
                cfg = configparser.ConfigParser()
                cfg.read(path)
                for section in cfg.sections():
                    if cfg.has_option(section, "api_key"):
                        api_key = cfg.get(section, "api_key").strip().strip('"').strip("'")
                    if cfg.has_option(section, "api_url"):
                        api_url = cfg.get(section, "api_url").strip().strip('"').strip("'")
            except Exception:
                pass

            # Method B: Fallback line-by-line search (handles missing headers / weird formatting)
            if not api_key:
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            clean_line = line.strip()
                            if clean_line.startswith("#") or clean_line.startswith(";"):
                                continue
                            if "=" in clean_line:
                                key, val = clean_line.split("=", 1)
                                key = key.strip().lower()
                                val = val.strip().strip('"').strip("'")
                                if key in ["api_key", "apikey"]:
                                    api_key = val
                                elif key in ["api_url", "apiurl"]:
                                    api_url = val
                except Exception as e:
                    print(f"Could not read {path}: {e}")

            if api_key:
                detected_path = path
                break

    if detected_path:
        print(f"✅ Auto-detected config from: {detected_path}")

    # Ensure api_url has no trailing slash
    if api_url and api_url.endswith("/"):
        api_url = api_url[:-1]

    return api_key, api_url

def fetch_today_stats():
    """Queries Hackatime API and computes hours, projects, languages, and Stardust."""
    api_key, api_url = get_hackatime_config()

    if not api_key:
        return {
            "error": "No Hackatime config found",
            "total_text": "No Key",
            "hours": 0.0,
            "stardust_est": 0.0,
            "projects": [],
            "languages": []
        }

    auth_header = "Basic " + base64.b64encode(api_key.encode("utf-8")).decode("utf-8")
    headers = {
        "Authorization": auth_header,
        "User-Agent": "HackatimeMenuBar/1.0"
    }

    endpoints = [
        f"{api_url}/users/current/statusbar/today",
        f"{api_url}/users/current/status_bar/today"
    ]
    if not any(v in api_url for v in ["/v1", "/hackatime"]):
        endpoints.insert(0, f"{api_url}/hackatime/v1/users/current/statusbar/today")

    data = None
    last_err = None

    for url in endpoints:
        try:
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code == 200:
                data = resp.json().get("data", {})
                break
            else:
                last_err = f"HTTP {resp.status_code}"
        except requests.RequestException:
            last_err = "Network error"

    if data is None:
        return {
            "error": last_err or "Offline",
            "total_text": "Offline",
            "hours": 0.0,
            "stardust_est": 0.0,
            "projects": [],
            "languages": []
        }

    grand_total = data.get("grand_total", {})
    total_text = grand_total.get("text", "0 secs")
    total_seconds = grand_total.get("total_seconds", 0.0)
    hours = total_seconds / 3600.0

    projects = [
        {
            "name": p.get("name", "Unknown"),
            "text": p.get("text", "0 mins"),
            "percent": round(p.get("percent", 0.0), 1)
        }
        for p in data.get("projects", [])
    ]

    languages = [
        {
            "name": l.get("name", "Unknown"),
            "text": l.get("text", "0 mins"),
            "percent": round(l.get("percent", 0.0), 1)
        }
        for l in data.get("languages", [])
    ]

    return {
        "error": None,
        "total_text": total_text,
        "hours": hours,
        "stardust_est": round(hours, 2),
        "projects": projects,
        "languages": languages
    }

if __name__ == "__main__":
    print("Testing Hackatime Smart Auto-Detector...")
    stats = fetch_today_stats()
    print("Result:", stats)