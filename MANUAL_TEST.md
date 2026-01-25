# Manual Testing Guide

## Setup

1. Copy your `config.py` to the worktree:
   ```bash
   cp /path/to/main/repo/config.py .worktrees/feature-start-stop/
   ```

2. Ensure dependencies are installed:
   ```bash
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run the bot:
   ```bash
   python movieScraper.py
   ```

## Test Cases

### ✅ Test 1: Startup Behavior

**Expected:**
- Terminal shows: `[INIT] Command listener thread started`
- Terminal shows: `[INIT] Bot started in PAUSED state. Waiting for /start command...`
- Telegram message: `🤖 Bot started! Use /start to begin scraping.`
- Bot is in PAUSED state (not scraping)

**Verify:**
- Check that the script doesn't start scraping immediately
- Check that CPU usage is low (just polling for commands)

---

### ✅ Test 2: Start Command

**Action:** Send `/start` via Telegram

**Expected:**
- Telegram message: `✅ Scraper started!`
- Terminal shows: `[START] Scraper started`
- Bot begins scraping every 10 seconds

**Verify:**
- Wait 10-15 seconds and check terminal for scraping activity
- Check network activity (should see requests to carnivalcinemas.sg)

---

### ✅ Test 3: Status Command (While Running)

**Action:** Send `/status` via Telegram

**Expected:**
- Telegram message: `📊 Status: Running`
- Terminal shows: `[STATUS] Running`

---

### ✅ Test 4: Stop Command

**Action:** Send `/stop` via Telegram

**Expected:**
- Telegram message: `⏸️ Scraper stopped!`
- Terminal shows: `[STOP] Scraper stopped`
- Bot stops scraping (no more network requests to cinema site)

**Verify:**
- Check that scraping stops
- CPU usage should drop

---

### ✅ Test 5: Status Command (While Stopped)

**Action:** Send `/status` via Telegram

**Expected:**
- Telegram message: `📊 Status: Stopped`
- Terminal shows: `[STATUS] Stopped`

---

### ✅ Test 6: Start When Already Running

**Action:** Send `/start` while already running

**Expected:**
- Telegram message: `Scraper is already running`
- Terminal shows: `[START] Already running`
- Bot continues running (no interruption)

---

### ✅ Test 7: Stop When Already Stopped

**Action:** Send `/stop` while already stopped

**Expected:**
- Telegram message: `Scraper is already stopped`
- Terminal shows: `[STOP] Already stopped`
- Bot remains stopped

---

### ✅ Test 8: List Command (Empty)

**Action:** Send `/list` via Telegram (when no movies tracked)

**Expected:**
- Telegram message: `No movies currently tracked`
- Terminal shows: `[LIST] Showing 0 movies`

---

### ✅ Test 9: Start/Stop Multiple Times

**Action:** Alternate `/start` and `/stop` commands

**Expected:**
- Bot toggles between running and stopped states
- Each command gets appropriate confirmation message
- No errors or crashes

---

### ✅ Test 10: Error Handling

**Action:** Disconnect internet, then send `/start`

**Expected:**
- Error notifications via Telegram (existing error handling)
- Bot continues running (doesn't crash)
- Can still respond to `/stop`, `/status` commands

---

## Success Criteria

All of the following should work:

- [ ] Bot starts in PAUSED state
- [ ] `/start` command starts scraping
- [ ] `/stop` command stops scraping
- [ ] `/status` shows correct state
- [ ] `/list` shows movies (or empty message)
- [ ] Duplicate commands are handled gracefully
- [ ] Bot doesn't crash on errors
- [ ] Command listener thread keeps running

## Cleanup

After testing, you can stop the bot with `Ctrl+C`.

To remove the test worktree after merging:
```bash
git worktree remove .worktrees/feature-start-stop
```
