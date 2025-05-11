import openai

class Character:
    def __init__(self, role: str):
        self.role = role
        self.context = []
        self.system_prompt = (
            f"You are {self.role}, a story character. "
            "Speak in first-person as yourself. "
            "Do not narrate events or describe other characters or the scene."
        )
        self.context.append({"role": "system", "content": self.system_prompt})

    def set_scene(self, scene_description: str):
        self.context.append({"role": "system", "content": f"Scene context: {scene_description}"})

    def receive_prompt(self, user_input: str) -> str:
        self.context.append({"role": "user", "content": user_input})
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.context
        )
        reply = resp.choices[0].message.content.strip()
        self.context.append({"role": "assistant", "content": reply})
        return reply

    def interact_with(self, other: "Character", scene: str) -> str:
        prompt = (
            f"You are {self.role}. You interact with {other.role}. "
            f"Scene: {scene}. What do you say or do next in first person?"
        )
        msgs = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": f"Scene: {scene}"},
            {"role": "user", "content": prompt}
        ]
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=msgs
        )
        reply = resp.choices[0].message.content.strip()
        self.context.append({"role": "assistant", "content": reply})
        return reply