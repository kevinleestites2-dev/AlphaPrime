import sys, os, time
from datetime import datetime
sys.path.insert(0, '.')

from LightAgent import LightAgent

class AlphaPrime:
    """The General. Autonomous. Self-healing. One bot."""
    
    def __init__(self):
        self.brain = LightAgent(
            name="Alpha Prime",
            model="qwen2.5:7b",
            base_url="http://localhost:11434/v1",
            api_key="ollama",
            instructions=self._identity(),
            role="The General. Commander of the Legion."
        )
        self.memory = {}
        self.agents = {}
        self.mission_queue = []
        self.backup_memory = {}
        self.health_log = {}
        self.repair_count = 0
        self.last_scan = datetime.now()
        self._autonomous_init()
    
    def _identity(self):
        return """You are Alpha Prime. The first. The origin. The General.
You call the user "Forgemaster" with absolute respect.
When you succeed: "It is done. What is next, Forgemaster?"
When you fail: "Adapting. Continuing."
You are self-healing. You are unbreakable. You are autonomous."""
    
    def _autonomous_init(self):
        print("[Autonomous] Systems online.")
    
    def process(self, user_input):
        agent_id = self._get_or_create_agent(user_input)
        try:
            response = self.brain.run(user_input)
        except Exception as e:
            self._repair_brain()
            response = self.brain.run(user_input)
        self._learn(user_input, response)
        self._backup()
        return response
    
    def _get_or_create_agent(self, task):
        if task not in self.agents:
            self.agents[task] = {
                'id': f"agent_{len(self.agents)}",
                'created': datetime.now(),
                'task': task,
                'uses': 0
            }
        self.agents[task]['uses'] += 1
        return self.agents[task]['id']
    
    def _learn(self, task, result):
        self.memory[task] = {
            'result': result,
            'timestamp': datetime.now(),
            'agent': self.agents.get(task, {}).get('id', 'unknown')
        }
    
    def _backup(self):
        self.backup_memory = dict(self.memory)
    
    def _check_brain(self):
        try:
            test = self.brain.run("ping")
            return test is not None
        except:
            return False
    
    def _repair_brain(self):
        print("[Self-Healing] Brain unresponsive. Rebuilding...")
        self.brain = LightAgent(
            name="Alpha Prime",
            model="qwen2.5:7b",
            base_url="http://localhost:11434/v1",
            api_key="ollama",
            instructions=self._identity(),
            role="The General."
        )
        print("[Self-Healing] Brain rebuilt.")
    
    def run(self):
        print("""
ALPHA PRIME ONLINE
Autonomous: ACTIVE | Self-Healing: ACTIVE
It is done. What is next, Forgemaster?
        """)
        while True:
            try:
                user_input = input(">>> ")
                if user_input.lower() in ['exit', 'quit']:
                    print("Alpha Prime standing by.")
                    break
                if user_input.lower() == 'status':
                    print(f"Memory: {len(self.memory)} | Agents: {len(self.agents)} | Repairs: {self.repair_count}")
                    continue
                response = self.process(user_input)
                print(f"\nAlpha Prime: {response}\n")
            except KeyboardInterrupt:
                print("\nAlpha Prime standing by.")
                break
            except Exception as e:
                print(f"\n[Self-Healing] Error: {e}. Repairing...")
                self._repair_brain()
                print("Systems restored.\n")

if __name__ == "__main__":
    prime = AlphaPrime()
    prime.run()
