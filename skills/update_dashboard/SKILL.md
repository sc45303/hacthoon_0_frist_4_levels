# Update Dashboard Skill

**Purpose:** Update Dashboard.md with current system status and metrics

**Category:** Bronze Tier - System Monitoring
**Version:** 1.0
**Last Updated:** 2026-02-16

---

## Usage

```bash
/update-dashboard
```

**No parameters required** - automatically collects all metrics.

---

## What This Skill Does

This skill keeps Dashboard.md up-to-date with real-time system status and metrics.

### Step-by-Step Process:
1. **Count Tasks** - Scans all folders for task counts
2. **Check System Status** - Verifies cron jobs and processes
3. **Read Logs** - Extracts recent activity from logs
4. **Calculate Metrics** - Computes daily/weekly/all-time stats
5. **Update Dashboard** - Writes updated Dashboard.md
6. **Timestamp** - Records last update time

---

## Inputs

### Context Files Read:
- `Needs_Action/*.md` - Pending tasks count
- `Approvals/*.md.approval.md` - Approval status
- `Done/*.md` - Completed tasks count
- `Plans/*.md` - Plans created count
- `Logs/*.execution.log` - Execution history
- `Memory/linkedin_posts.log` - LinkedIn activity
- `Memory/cron_logs/*.log` - System health

---

## Outputs

### Files Updated:

**Dashboard.md** - Complete system overview
```markdown
# AI Employee Dashboard

**Last Updated:** 2026-02-16 21:30:00

## 🎯 System Status
| Component | Status | Last Run |
|-----------|--------|----------|
| Gmail Watcher | 🟢 Running | 2 minutes ago |
| LinkedIn Poster | 🟢 Running | 15 minutes ago |
| Bronze Planner | 🟢 Running | 3 minutes ago |
| Silver Executor | 🟢 Running | 1 minute ago |

## 📊 Today's Activity
- 📧 Emails processed: 3
- ✅ Tasks completed: 2
- 📱 LinkedIn posts: 1
- ⏳ Pending approvals: 1

## 📈 All-Time Stats
- Total Emails: 45
- Total Tasks: 17
- Total Posts: 4
- System Uptime: 99.5%
```

---

## Metrics Collected

### Task Metrics:
- **Needs Action count** - Tasks awaiting planning
- **Plans created** - Total plans generated
- **Pending approvals** - Tasks awaiting human decision
- **Completed today** - Tasks finished today
- **Completed all-time** - Total tasks ever completed

### System Health:
- **Cron job status** - Running/stopped for each job
- **Last run times** - When each component last executed
- **Error count** - Errors in last 24 hours
- **API quota** - Gemini API usage

### Activity Metrics:
- **Emails processed** - Today and all-time
- **LinkedIn posts** - Today and all-time
- **Approvals given** - Human approval rate
- **Average response time** - Time from detection to completion

---

## System Status Detection

### Component Health Check:
```python
def check_component_status(component_name):
    log_file = f'Memory/cron_logs/{component_name}.log'
    last_line = read_last_line(log_file)
    last_run = extract_timestamp(last_line)

    if time_since(last_run) < expected_interval:
        return '🟢 Running'
    elif time_since(last_run) < 2 * expected_interval:
        return '🟡 Delayed'
    else:
        return '🔴 Stopped'
```

### Status Indicators:
- 🟢 **Running** - Last run within expected interval
- 🟡 **Delayed** - Last run overdue but recent
- 🔴 **Stopped** - No activity for extended period
- ⚠️ **Error** - Recent errors detected

---

## Dashboard Sections

### 1. System Status
Shows health of all components (watchers, planners, executors)

### 2. Today's Activity
Current day metrics (resets at midnight)

### 3. Current Tasks
Lists tasks in each stage of workflow

### 4. Business Goals
Progress toward weekly/monthly objectives

### 5. Alerts
Important notifications (quota limits, errors, etc.)

### 6. All-Time Stats
Cumulative metrics since system start

### 7. Quick Links
Obsidian links to key folders and files

---

## Update Frequency

### Automatic Updates:
- After each task execution
- After each plan creation
- After each LinkedIn post
- Every 5 minutes (via cron)

### Manual Updates:
- On demand via `/update-dashboard`
- After system configuration changes
- During troubleshooting

---

## Performance Metrics

- **Update time:** < 2 seconds
- **Accuracy:** 100% (direct file counting)
- **Updates per day:** ~300 (every 5 min)

---

## Error Handling

### Common Issues:
- **Dashboard.md locked** → Retry after 1 second
- **Folder not accessible** → Log warning, use cached count
- **Log file corrupted** → Skip that metric, continue
- **Permission denied** → Alert human

---

## Example Output

### Before Update:
```markdown
**Last Updated:** 2026-02-16 21:00:00
- Tasks completed: 15
```

### After Update:
```markdown
**Last Updated:** 2026-02-16 21:30:00
- Tasks completed: 17
```

---

## Integration Points

### Used By:
- All other skills (update after their actions)
- Cron job (periodic updates)
- Orchestrator (after each workflow cycle)

### Uses:
- File system (counts files)
- Log parsers (extracts metrics)
- Time utilities (calculates intervals)

---

## Dashboard Template

### Minimal Dashboard:
```markdown
# AI Employee Dashboard
**Last Updated:** {{timestamp}}

## System Status
{{component_status_table}}

## Today's Activity
{{daily_metrics}}

## Current Tasks
{{task_counts}}
```

### Full Dashboard:
Includes all sections: status, activity, tasks, goals, alerts, stats, links

---

## Customization

### Add New Metrics:
1. Define metric calculation function
2. Add to metrics collection
3. Update dashboard template
4. Test update cycle

### Add New Sections:
1. Create section template
2. Add data collection logic
3. Insert in dashboard layout
4. Verify formatting

---

## Related Skills

- `plan_task` - Calls this after creating plans
- `execute_task` - Calls this after execution
- `linkedin_post` - Calls this after posting
- `check_approvals` - Provides approval counts

---

## Maintenance Notes

### When to Update This Skill:
- New metrics are needed
- Dashboard layout changes
- New components are added
- Performance optimization needed

### Version History:
- v1.0 (2026-02-16) - Initial creation for hackathon

---

**This skill keeps your AI Employee's dashboard current and informative.**
