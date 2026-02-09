
try:
    from portal.badge_history import timeline
except Exception:
    def timeline(agent=None):
        return []

def feed(base_url="http://localhost"):
    return "<?xml version='1.0'?><rss></rss>"
