#!/bin/bash
# SILVER LEVEL TEST - Step by Step

echo "=================================="
echo "🥈 TESTING SILVER LEVEL"
echo "=================================="
echo ""

# Activate environment
source venv/bin/activate

# STEP 1: Create a task
echo "STEP 1: Creating a test task..."
echo "Explain what Python is in 2 sentences" > Needs_Action/test_silver.md
echo "✅ Task created!"
echo ""

# STEP 2: Generate plan
echo "STEP 2: Generating plan..."
python -m agent.bronze_planner
echo ""

# STEP 3: Show the plan
echo "STEP 3: Here's the plan that was created:"
echo "---"
cat Plans/test_silver.md
echo "---"
echo ""

# STEP 4: Approve the task
echo "STEP 4: Approving the task..."
sed -i 's/\[ \] Approved/[x] Approved/' Approvals/test_silver.md.approval.md
echo "✅ Task approved!"
echo ""

# STEP 5: Execute the task
echo "STEP 5: Executing the task..."
python -m agent.silver_executor
echo ""

# STEP 6: Show results
echo "STEP 6: RESULTS:"
echo ""
echo "✅ Task moved to Done folder:"
ls -lh Done/test_silver.md
echo ""
echo "✅ Execution log created:"
ls -lh Logs/test_silver.md.execution.log
echo ""
echo "📄 Execution report (first 40 lines):"
head -40 Logs/test_silver.md.execution.log
echo ""
echo "=================================="
echo "✅ SILVER LEVEL TEST COMPLETE!"
echo "=================================="
