# 🕐 Cron Scheduling Guide

## Overview

Automated scheduling for the Personal AI Employee using cron jobs. This ensures your watchers and posters run automatically without manual intervention.

## What Gets Scheduled

### 1. Gmail Watcher
- **Frequency**: Every 2 minutes
- **Purpose**: Monitor inbox for important emails
- **Script**: `cron_gmail_watcher.sh`
- **Log**: `Memory/cron_logs/gmail_watcher.log`

### 2. LinkedIn Poster
- **Frequency**: Every hour
- **Purpose**: Post queued content to LinkedIn
- **Script**: `cron_linkedin_poster.sh`
- **Log**: `Memory/cron_logs/linkedin_poster.log`

### 3. Log Cleanup
- **Frequency**: Daily at midnight
- **Purpose**: Remove logs older than 7 days
- **Keeps**: Last 7 days of logs

## Setup Instructions

### Step 1: Run Setup Script

```bash
./setup_cron.sh
```

This creates:
- Wrapper scripts for each task
- Crontab entries file
- Log directory structure

### Step 2: Install Cron Jobs

**Option A: Automatic Installation**
```bash
crontab -l > /tmp/current_cron 2>/dev/null || true
cat crontab_entries.txt >> /tmp/current_cron
crontab /tmp/current_cron
rm /tmp/current_cron
```

**Option B: Manual Installation**
```bash
crontab -e
```
Then paste the contents of `crontab_entries.txt`

### Step 3: Verify Installation

```bash
# View installed cron jobs
crontab -l

# Check cron service status
service cron status
```

## Cron Schedule

```
# Gmail Watcher - Every 2 minutes
*/2 * * * * /path/to/cron_gmail_watcher.sh

# LinkedIn Poster - Every hour
0 * * * * /path/to/cron_linkedin_poster.sh

# Daily cleanup - Midnight
0 0 * * * find /path/to/logs -name "*.log" -mtime +7 -delete
```

## Monitoring

### View Live Logs

```bash
# Gmail watcher
tail -f Memory/cron_logs/gmail_watcher.log

# LinkedIn poster
tail -f Memory/cron_logs/linkedin_poster.log
```

### Check Last Run

```bash
# Gmail watcher
ls -lh Memory/cron_logs/gmail_watcher.log

# LinkedIn poster
ls -lh Memory/cron_logs/linkedin_poster.log
```

### View Recent Activity

```bash
# Last 20 lines of Gmail watcher
tail -20 Memory/cron_logs/gmail_watcher.log

# Last 20 lines of LinkedIn poster
tail -20 Memory/cron_logs/linkedin_poster.log
```

## Troubleshooting

### Cron Jobs Not Running

**Check if cron service is running:**
```bash
service cron status
```

**Start cron service:**
```bash
sudo service cron start
```

**Enable cron on boot (systemd):**
```bash
sudo systemctl enable cron
```

### Scripts Not Executing

**Check script permissions:**
```bash
ls -l cron_*.sh
# Should show: -rwxr-xr-x
```

**Make executable if needed:**
```bash
chmod +x cron_gmail_watcher.sh
chmod +x cron_linkedin_poster.sh
```

### No Logs Generated

**Check log directory exists:**
```bash
ls -ld Memory/cron_logs/
```

**Create if missing:**
```bash
mkdir -p Memory/cron_logs
```

**Check cron execution:**
```bash
grep CRON /var/log/syslog | tail -20
```

### WSL-Specific Issues

**Cron doesn't start automatically in WSL:**
```bash
# Start manually
sudo service cron start

# Or add to .bashrc for auto-start
echo 'sudo service cron start 2>/dev/null' >> ~/.bashrc
```

## Customizing Schedule

### Change Gmail Watcher Frequency

Edit crontab and change the interval:
```bash
# Every 5 minutes instead of 2
*/5 * * * * /path/to/cron_gmail_watcher.sh

# Every 10 minutes
*/10 * * * * /path/to/cron_gmail_watcher.sh
```

### Change LinkedIn Poster Frequency

```bash
# Every 2 hours
0 */2 * * * /path/to/cron_linkedin_poster.sh

# Twice daily (9 AM and 5 PM)
0 9,17 * * * /path/to/cron_linkedin_poster.sh

# Business hours only (9 AM - 5 PM, hourly)
0 9-17 * * * /path/to/cron_linkedin_poster.sh
```

## Disabling Cron Jobs

### Temporarily Disable

```bash
# Comment out in crontab
crontab -e
# Add # at start of line to disable
```

### Remove All Jobs

```bash
crontab -r
```

### Remove Specific Job

```bash
crontab -e
# Delete the specific line
```

## Log Management

### View Log Size

```bash
du -sh Memory/cron_logs/
```

### Manual Cleanup

```bash
# Remove all logs
rm Memory/cron_logs/*.log

# Remove logs older than 3 days
find Memory/cron_logs/ -name "*.log" -mtime +3 -delete
```

### Rotate Logs

```bash
# Archive current logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz Memory/cron_logs/
rm Memory/cron_logs/*.log
```

## Testing

### Test Individual Scripts

```bash
# Test Gmail watcher
./cron_gmail_watcher.sh

# Test LinkedIn poster
./cron_linkedin_poster.sh
```

### Test Cron Execution

```bash
# Add a test job that runs every minute
* * * * * echo "Test at $(date)" >> /tmp/cron_test.log

# Wait 2 minutes, then check
cat /tmp/cron_test.log
```

## Best Practices

1. **Monitor Logs Regularly**
   - Check for errors weekly
   - Ensure tasks are running as expected

2. **Keep Logs Clean**
   - Automatic cleanup runs daily
   - Manual cleanup if logs grow large

3. **Test After Changes**
   - Always test scripts manually first
   - Verify cron syntax before installing

4. **Backup Crontab**
   ```bash
   crontab -l > crontab_backup_$(date +%Y%m%d).txt
   ```

## Success Criteria

Cron scheduling is working when:
- ✅ `crontab -l` shows installed jobs
- ✅ Log files are being updated
- ✅ Gmail watcher runs every 2 minutes
- ✅ LinkedIn poster runs every hour
- ✅ No errors in logs

---

**Automated Scheduling Complete!** 🎉

Your Personal AI Employee now runs automatically in the background.
