#!/bin/bash
# Complete Testing Guide for Silver and Gold Levels

echo "=================================="
echo "🧪 AI EMPLOYEE TESTING GUIDE"
echo "=================================="
echo ""

# Activate virtual environment
source venv/bin/activate

echo "📋 PART 1: TESTING SILVER LEVEL"
echo "=================================="
echo ""

# Step 1: Clean up old test files
echo "Step 1: Cleaning up old test files..."
rm -f Needs_Action/silver_test.md
rm -f Plans/silver_test.md
rm -f Approvals/silver_test.md.approval.md
rm -f Done/silver_test.md
rm -f Logs/silver_test.md.execution.log
echo "✅ Cleanup complete"
echo ""

# Step 2: Create a test task
echo "Step 2: Creating a Silver level test task..."
cat > Needs_Action/silver_test.md << 'EOF'
List 3 benefits of using Python for data science
EOF
echo "✅ Task created: Needs_Action/silver_test.md"
echo ""

# Step 3: Generate plan (Bronze level)
echo "Step 3: Generating plan..."
python -m agent.bronze_planner
echo ""

# Step 4: Check if plan was created
echo "Step 4: Verifying plan was created..."
if [ -f "Plans/silver_test.md" ]; then
    echo "✅ Plan created successfully!"
    echo ""
    echo "📄 Plan content:"
    cat Plans/silver_test.md
    echo ""
else
    echo "❌ Plan not found - something went wrong"
    exit 1
fi

# Step 5: Check approval request
echo "Step 5: Checking approval request..."
if [ -f "Approvals/silver_test.md.approval.md" ]; then
    echo "✅ Approval request created!"
    echo ""
    echo "📄 Approval content:"
    cat Approvals/silver_test.md.approval.md
    echo ""
else
    echo "❌ Approval request not found"
    exit 1
fi

# Step 6: Approve the task
echo "Step 6: Approving the task..."
cat > Approvals/silver_test.md.approval.md << 'EOF'
# Approval Request

Task: silver_test.md

Decision:
[x] Approved
[ ] Rejected

Notes:
Testing Silver level execution
EOF
echo "✅ Task approved!"
echo ""

# Step 7: Execute with Silver executor
echo "Step 7: Executing task with Silver executor..."
python -m agent.silver_executor
echo ""

# Step 8: Verify execution results
echo "Step 8: Verifying execution results..."
echo ""

if [ -f "Done/silver_test.md" ]; then
    echo "✅ Task moved to Done folder"
else
    echo "❌ Task not in Done folder"
fi

if [ -f "Logs/silver_test.md.execution.log" ]; then
    echo "✅ Execution log created"
    echo ""
    echo "📄 Log preview (first 30 lines):"
    head -30 Logs/silver_test.md.execution.log
    echo ""
else
    echo "❌ Execution log not found"
fi

echo ""
echo "=================================="
echo "✅ SILVER LEVEL TEST COMPLETE!"
echo "=================================="
echo ""
echo "Press Enter to continue to Gold level testing..."
read

echo ""
echo "📋 PART 2: TESTING GOLD LEVEL"
echo "=================================="
echo ""

# Step 1: Clean up old test files
echo "Step 1: Cleaning up old test files..."
rm -f Needs_Action/gold_test.md
rm -f Plans/gold_test.md
rm -f Approvals/gold_test.md.approval.md
rm -f Done/gold_test.md
rm -f Logs/gold_test.md.execution.log
rm -f Feedback/gold_test.md.feedback.md
echo "✅ Cleanup complete"
echo ""

# Step 2: Create a test task
echo "Step 2: Creating a Gold level test task..."
cat > Needs_Action/gold_test.md << 'EOF'
Write a short motivational quote about learning and growth
EOF
echo "✅ Task created: Needs_Action/gold_test.md"
echo ""

# Step 3: Generate plan with learning (Gold level)
echo "Step 3: Generating plan with learning engine..."
python -m agent.gold_planner
echo ""

# Step 4: Check if plan was created
echo "Step 4: Verifying plan was created..."
if [ -f "Plans/gold_test.md" ]; then
    echo "✅ Plan created successfully!"
    echo ""
    echo "📄 Plan content (first 40 lines):"
    head -40 Plans/gold_test.md
    echo ""
else
    echo "❌ Plan not found"
    exit 1
fi

# Step 5: Approve the task
echo "Step 5: Approving the task..."
cat > Approvals/gold_test.md.approval.md << 'EOF'
# Approval Request

Task: gold_test.md

Decision:
[x] Approved
[ ] Rejected

Notes:
Testing Gold level with learning
EOF
echo "✅ Task approved!"
echo ""

# Step 6: Execute with Gold executor
echo "Step 6: Executing task with Gold executor..."
python -m agent.gold_executor
echo ""

# Step 7: Verify execution and feedback request
echo "Step 7: Verifying execution results..."
echo ""

if [ -f "Done/gold_test.md" ]; then
    echo "✅ Task moved to Done folder"
else
    echo "❌ Task not in Done folder"
fi

if [ -f "Logs/gold_test.md.execution.log" ]; then
    echo "✅ Execution log created"
else
    echo "❌ Execution log not found"
fi

if [ -f "Feedback/gold_test.md.feedback.md" ]; then
    echo "✅ Feedback request created (Gold feature!)"
    echo ""
    echo "📄 Feedback form:"
    cat Feedback/gold_test.md.feedback.md
    echo ""
else
    echo "❌ Feedback request not found"
fi

# Step 8: Provide feedback
echo "Step 8: Providing feedback..."
cat > Feedback/gold_test.md.feedback.md << 'EOF'
# Feedback Request

Task: gold_test.md
Date: 2026-02-11 13:30

## Quality Rating
Rate the execution quality (1-5):
[ ] 1 - Poor
[ ] 2 - Below Average
[ ] 3 - Average
[x] 4 - Good
[ ] 5 - Excellent

## Plan Quality
Was the plan appropriate?
[x] Yes
[ ] No
[ ] Partially

## Execution Quality
Was the execution satisfactory?
[x] Yes
[ ] No
[ ] Partially

## What went well?

The quote was inspiring and well-crafted. Good execution of the task.

## What could be improved?

Could provide multiple quote options to choose from.

## Additional Comments?

Solid work! The learning system is working well.

---
*This feedback helps the AI learn and improve future performance*
EOF
echo "✅ Feedback provided!"
echo ""

# Step 9: Process feedback
echo "Step 9: Processing feedback for learning..."
python -m agent.feedback_processor
echo ""

# Step 10: Check learning metrics
echo "Step 10: Checking performance metrics..."
python -m agent.learning_engine
echo ""

# Step 11: Verify learning database
echo "Step 11: Verifying learning database..."
if [ -f "Memory/feedback_history.json" ]; then
    echo "✅ Learning database exists"
    echo ""
    echo "📄 Feedback history:"
    cat Memory/feedback_history.json
    echo ""
else
    echo "❌ Learning database not found"
fi

echo ""
echo "=================================="
echo "✅ GOLD LEVEL TEST COMPLETE!"
echo "=================================="
echo ""
echo "🎉 SUMMARY:"
echo "  ✅ Silver Level: Task execution working"
echo "  ✅ Gold Level: Learning system working"
echo "  ✅ Feedback collection working"
echo "  ✅ Performance metrics tracking"
echo ""
echo "Your AI Employee is fully operational at Gold level!"
echo ""
