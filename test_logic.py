"""
Simple test script to verify start/stop logic without full dependencies.
"""

# Mock the scraper_state
scraper_state = {
    "is_running": False,
    "command": None
}

def start_scraper():
    """Start the scraper if not already running."""
    if not scraper_state["is_running"]:
        scraper_state["is_running"] = True
        print("✅ Scraper started!")
        return True
    else:
        print("⚠️  Scraper is already running")
        return False

def stop_scraper():
    """Stop the scraper if not already stopped."""
    if scraper_state["is_running"]:
        scraper_state["is_running"] = False
        print("⏸️  Scraper stopped!")
        return True
    else:
        print("⚠️  Scraper is already stopped")
        return False

def get_status():
    """Get current status."""
    return "Running" if scraper_state["is_running"] else "Stopped"

# Test sequence
print("=" * 50)
print("Testing Start/Stop Controls")
print("=" * 50)

print("\n1. Initial state:")
print(f"   Status: {get_status()}")
assert get_status() == "Stopped", "Should start stopped"

print("\n2. Testing start:")
result = start_scraper()
assert result == True, "start_scraper() should return True"
assert scraper_state["is_running"] == True, "is_running should be True"
print(f"   Status: {get_status()}")

print("\n3. Testing start when already running:")
result = start_scraper()
assert result == False, "start_scraper() should return False (already running)"
assert scraper_state["is_running"] == True, "is_running should still be True"

print("\n4. Testing stop:")
result = stop_scraper()
assert result == True, "stop_scraper() should return True"
assert scraper_state["is_running"] == False, "is_running should be False"
print(f"   Status: {get_status()}")

print("\n5. Testing stop when already stopped:")
result = stop_scraper()
assert result == False, "stop_scraper() should return False (already stopped)"
assert scraper_state["is_running"] == False, "is_running should still be False"

print("\n6. Testing start again:")
result = start_scraper()
assert result == True, "start_scraper() should return True"
assert scraper_state["is_running"] == True, "is_running should be True"
print(f"   Status: {get_status()}")

print("\n" + "=" * 50)
print("✅ All logic tests passed!")
print("=" * 50)
