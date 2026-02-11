"""
Platinum Level - Agent Coordinator
Orchestrates multiple agents working together
"""

from agent.specialized_agents import ResearcherAgent, WriterAgent, AnalystAgent, CoderAgent
from agent.task_decomposer import TaskDecomposer
from agent.agent_registry import get_registry
from agent.communication_bus import get_communication_bus
from typing import Dict, Any, List
import time

class AgentCoordinator:
    """Coordinates multiple agents to complete complex tasks"""

    def __init__(self):
        self.decomposer = TaskDecomposer()
        self.registry = get_registry()
        self.comm_bus = get_communication_bus()

        # Initialize specialized agents
        self.agents = {
            'Researcher': ResearcherAgent(),
            'Writer': WriterAgent(),
            'Analyst': AnalystAgent(),
            'Coder': CoderAgent()
        }

    def execute_complex_task(self, task_description: str) -> Dict[str, Any]:
        """Execute a complex task using multiple agents"""

        print("\n" + "="*60)
        print("💎 PLATINUM LEVEL - Multi-Agent Collaboration")
        print("="*60)
        print(f"\n📋 Task: {task_description}\n")

        # Step 1: Decompose task
        decomposition = self.decomposer.decompose_task(task_description)

        if not decomposition['requires_collaboration']:
            print("ℹ️  Simple task - single agent execution")
            return self._execute_single_agent(decomposition)

        print(f"\n🤝 Collaboration required - {len(decomposition['subtasks'])} agents needed\n")

        # Step 2: Execute subtasks
        results = {}
        execution_order = decomposition['execution_order']

        for subtask_id in execution_order:
            subtask = next(s for s in decomposition['subtasks'] if s['subtask_id'] == subtask_id)

            # Check dependencies
            if subtask['depends_on']:
                print(f"⏳ Waiting for dependencies: {subtask['depends_on']}")
                # In a real system, we'd wait for these to complete
                # For now, we'll pass their results

            # Execute subtask
            print(f"\n🎯 Executing subtask {subtask_id}: {subtask['description']}")

            agent_type = subtask['agent_type']
            agent = self.agents.get(agent_type)

            if not agent:
                print(f"⚠️  Agent type {agent_type} not found")
                continue

            # Prepare task with context from previous results
            task_data = {
                'description': subtask['description'],
                'previous_results': results
            }

            # Add specific data based on dependencies
            if subtask['depends_on']:
                for dep_id in subtask['depends_on']:
                    if dep_id in results:
                        dep_result = results[dep_id]
                        if 'findings' in dep_result:
                            task_data['research_data'] = dep_result['findings']
                        if 'analysis' in dep_result:
                            task_data['data'] = dep_result['analysis']

            # Execute
            result = agent.execute_task(task_data)
            results[subtask_id] = result

            # Notify other agents
            self.comm_bus.broadcast_message(
                agent.agent_id,
                'notification',
                {'event': 'task_completed', 'subtask_id': subtask_id}
            )

        # Step 3: Aggregate results
        print("\n" + "="*60)
        print("📦 Aggregating results from all agents...")
        print("="*60 + "\n")

        final_result = self._aggregate_results(task_description, results, decomposition)

        return final_result

    def _execute_single_agent(self, decomposition: Dict) -> Dict[str, Any]:
        """Execute a simple task with a single agent"""
        subtask = decomposition['subtasks'][0]
        agent_type = subtask['agent_type']
        agent = self.agents.get(agent_type)

        if not agent:
            return {"status": "failed", "error": f"Agent type {agent_type} not found"}

        task_data = {'description': subtask['description']}
        result = agent.execute_task(task_data)

        return {
            "task": subtask['description'],
            "collaboration": False,
            "result": result,
            "status": "completed"
        }

    def _aggregate_results(self, original_task: str, results: Dict, decomposition: Dict) -> Dict[str, Any]:
        """Aggregate results from multiple agents into final output"""

        # Compile all agent outputs
        agent_outputs = []
        for subtask_id, result in results.items():
            subtask = next(s for s in decomposition['subtasks'] if s['subtask_id'] == subtask_id)

            output = {
                "subtask": subtask['description'],
                "agent": result.get('agent_type'),
                "status": result.get('status')
            }

            # Add the actual content
            if 'findings' in result:
                output['output'] = result['findings']
            elif 'content' in result:
                output['output'] = result['content']
            elif 'analysis' in result:
                output['output'] = result['analysis']
            elif 'code' in result:
                output['output'] = result['code']

            agent_outputs.append(output)

        # Create final aggregated result
        final_result = {
            "original_task": original_task,
            "collaboration": True,
            "agents_involved": len(results),
            "subtasks_completed": len(results),
            "agent_outputs": agent_outputs,
            "status": "completed"
        }

        # Print summary
        for output in agent_outputs:
            print(f"\n{'='*60}")
            print(f"🤖 {output['agent']} Agent - {output['subtask']}")
            print(f"{'='*60}")
            print(output.get('output', 'No output')[:500] + "..." if len(output.get('output', '')) > 500 else output.get('output', 'No output'))

        return final_result

    def get_agent_status(self) -> List[Dict]:
        """Get status of all agents"""
        return [
            {
                "agent_id": agent.agent_id,
                "type": agent.agent_type,
                "capabilities": agent.capabilities
            }
            for agent in self.agents.values()
        ]
