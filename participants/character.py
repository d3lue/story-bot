import openai
from typing import List, Dict

class Character:
    def __init__(self, role: str):
        self.role = role
        self.context: List[Dict[str, str]] = []
        # Character-specific prompt
        self.system_msg = (
            f"You are {self.role}, a story character. "
            "Respond in first-person as yourself; do not narrate the scene or other characters."
        )
        self.context.append({"role": "system", "content": self.system_msg})

    def set_scene(self, scene_description: str):
        """
        Inform character of the scene context.
        """
        self.context.append({"role": "system", "content": f"Scene context: {scene_description}"})

    def receive_prompt(self, user_input: str) -> str:
        """
        Non-streaming character response to direct user input.
        """
        self.context.append({"role": "user", "content": user_input})
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.context
        )
        reply = resp.choices[0].message.content.strip()
        self.context.append({"role": "assistant", "content": reply})
        return reply

    def interact_with(self, other: "Character", scene: str) -> str:
        """
        Generate a response when this character interacts with another character in the given scene.
        """
        prompt = (
            f"You are {self.role}. You are interacting with {other.role}. "
            f"Scene: {scene}. What do you say or do next? Speak in first person."
        )
        msgs = [
            {"role": "system", "content": self.system_msg},
            {"role": "system", "content": f"Scene context: {scene}"},
            {"role": "user", "content": prompt}
        ]
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=msgs
        )
        reply = resp.choices[0].message.content.strip()
        self.context.append({"role": "assistant", "content": reply})
        return reply
