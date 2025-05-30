import asyncio

class Agent:
    def __init__(self, name):
        self.name = name
        self.partner = None

    def set_partner(self, agent):
        self.partner = agent

    async def send(self, message):
        print(f"{self.name} sending: {message}")
        await self.partner.receive(message)

    async def receive(self, message):
        print(f"{self.name} received: {message}")
        response = await self.respond(message)
        if response:
            await self.send(response)

    async def respond(self, message):
        raise NotImplementedError("Each agent must define its own respond method.")


class QuestionAgent(Agent):
    async def start_conversation(self):
        await self.send("What is the capital of France?")

    async def respond(self, message):
        print(f"{self.name} ending conversation.")
        return None  # Stops the loop


class AnswerAgent(Agent):
    async def respond(self, message):
        if "capital of France" in message:
            return "The capital of France is Paris."
        return "I don't know."


async def main():
    q_agent = QuestionAgent("QuestionAgent")
    a_agent = AnswerAgent("AnswerAgent")

    q_agent.set_partner(a_agent)
    a_agent.set_partner(q_agent)

    await q_agent.start_conversation()

asyncio.run(main())
