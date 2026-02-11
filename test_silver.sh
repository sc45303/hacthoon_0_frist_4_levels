#!/bin/bash

echo "🧪 Testing Silver Level AI Employee"
echo "===================================="
echo ""

# Activate virtual environment
source venv/bin/activate

echo "📝 Step 1: Creating a test task..."
cat > Needs_Action/test_task.md << 'EOF'
Create a simple greeting message that says "Hello from Silver AI Employee!"
EOF

echo "✅ Task created: Needs_Action/test_task.md"
echo ""

echo "🧠 Step 2: Running planner to generate plan..."
python -m agent.bronze_planner
echo ""

echo "📋 Step 3: Check the generated plan..."
if [ -f "Plans/test_task.md" ]; then
    echo "✅ Plan created successfully!"
    echo "Plan content:"
    cat Plans/test_task.md
else
    echo "❌ Plan not found"
    exit 1
fi
echo ""

echo "✋ Step 4: Check approval request..."
if [ -f "Approvals/test_task.md.approval.md" ]; then
    echo "✅ Approval request created!"
    cat Approvals/test_task.md.approval.md
else
    echo "❌ Approval request not found"
    exit 1
fi
echo ""

echo "👉 Step 5: Approve the task..."
cat > Approvals/test_task.md.approval.md << 'EOF'
# Approval Request

Task: test_task.md

Decision:
[x] Approved
[ ] Rejected

Notes:
Testing Silver level execution
EOF

echo "✅ Task approved!"
echo ""

echo "🚀 Step 6: Execute the approved task..."
python -m agent.silver_executor
echo ""

echo "📊 Step 7: Verify results..."
echo ""

if [ -f "Done/test_task.md" ]; then
    echo "✅ Task moved to Done folder"
else
    echo "❌ Task not in Done folder"
fi

if [ -f "Logs/test_task.md.execution.log" ]; then
    echo "✅ Execution log created"
    echo ""
    echo "Log preview:"
    head -20 Logs/test_task.md.execution.log
else
    echo "❌ Execution log not found"
fi

echo ""
echo "🎉 Silver Level Test Complete!"
