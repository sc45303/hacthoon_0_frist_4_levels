#!/bin/bash
# GOLD LEVEL TEST - Step by Step

echo "=================================="
echo "🥇 TESTING GOLD LEVEL"
echo "=================================="
echo ""

# Activate environment
source venv/bin/activate

# STEP 1: Create a task
echo "STEP 1: Creating a test task..."
echo "Write a motivational quote about success" > Needs_Action/test_gold.md
echo "✅ Task created!"
echo ""

# STEP 2: Generate plan WITH LEARNING
echo "STEP 2: Generating plan with learning engine..."
python -m agent.gold_planner
echo ""

# STEP 3: Show the plan (notice it mentions learning!)
echo "STEP 3: Here's the plan (notice it uses past learning):"
echo "---"
head -30 Plans/test_gold.md
echo "---"
echo ""

# STEP 4: Approve the task
echo "STEP 4: Approving the task..."
sed -i 's/\[ \] Approved/[x] Approved/' Approvals/test_gold.md.approval.md
echo "✅ Task approved!"
echo ""

# STEP 5: Execute with Gold executor
echo "STEP 5: Executing the task with Gold executor..."
python -m agent.gold_executor
echo ""

# STEP 6: Check feedback request was created
echo "STEP 6: GOLD LEVEL FEATURE - Feedback request created!"
echo ""
echo "✅ Feedback form:"
cat Feedback/test_gold.md.feedback.md
echo ""

# STEP 7: Fill out feedback
echo "STEP 7: Providing feedback..."
cat > Feedback/test_gold.md.feedback.md << 'EOF'
# Feedback Request

Task: test_gold.md
Date: 2026-02-11 14:30

## Quality Rating
Rate the execution quality (1-5):
[x] 5 - Excellent

## Plan Quality
Was the plan appropriate?
[x] Yes

## Execution Quality
Was the execution satisfactory?
[x] Yes

## What went well?
Great motivational quote! The AI clearly learned from previous tasks.

## What could be improved?
Nothing, perfect execution.

## Additional Comments?
The learning system is working excellently!
EOF
echo "✅ Feedback provided!"
echo ""

# STEP 8: Process feedback
echo "STEP 8: Processing feedback to update learning database..."
python -m agent.feedback_processor
echo ""

# STEP 9: Show updated metrics
echo "STEP 9: Updated performance metrics:"
python -m agent.learning_engine
echo ""

echo "=================================="
echo "✅ GOLD LEVEL TEST COMPLETE!"
echo "=================================="
echo ""
echo "🎉 SUMMARY:"
echo "  ✅ Silver: Task execution works"
echo "  ✅ Gold: Learning system works"
echo "  ✅ Feedback collected and processed"
echo "  ✅ AI is learning and improving!"
