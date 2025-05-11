import json
import re
import openai
from participants.character import Character

class OrchestratorBot:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.characters = []
        self.scene = None
        self.story_log = []
        self.messages = [
            {"role": "system",
             "content": (
                 "You are the orchestrator of a collaborative storytelling system. "
                 "When the user gives you text, you should only do one of two things:\n"
                 "1) If they’re defining characters and/or a scene, call the function `set_roles_scene` "
                 "with JSON args `roles` (array of strings) and/or `scene` (string).\n"
                 "2) Otherwise, return narrative or facilitation text to drive the story.\n"
                 "Never speak for the characters—they speak for themselves."
             )}
        ]
        self.functions = [
            {
                "name": "set_roles_scene",
                "description": "Extract character roles and an optional scene from user text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "roles": {"type": "array", "items": {"type": "string"}, "description": "Character names"},
                        "scene": {"type": "string", "description": "Scene description"}
                    },
                    "required": []
                }
            }
        ]
        self.story_started = False
        self.current_idx = 0

    def process_input(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        text_input = user_input.strip()
        lower_input = text_input.lower()

        # Setup: parse roles/scene
        if not self.characters or not self.scene:
            resp = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=self.messages,
                functions=self.functions,
                function_call="auto"
            )
            msg = resp.choices[0].message
            if msg.get("function_call"):
                args = json.loads(msg.function_call.arguments)
                out = []
                if args.get("roles"):
                    out.append(self.set_roles(args["roles"]))
                if args.get("scene"):
                    out.append(self.set_scene(args["scene"]))
                return "\n".join(out)
            # Fallback narration during setup
            narration = msg.content.strip()
            self.messages.append({"role": "assistant", "content": narration})
            return narration

        # Begin story: after setup
        if not self.story_started:
            intro = (
                f"The story begins. Scene: {self.scene}. "
                f"Characters: {', '.join(c.role for c in self.characters)}."
            )
            self.story_log.append(("Narrator", intro))
            self.story_started = True
            self.current_idx = 0
            return intro + "\nWho speaks first?"

        # Direct character call via 'Name: dialogue'
        if ":" in text_input:
            name, dialogue = map(str.strip, text_input.split(":", 1))
            for char in self.characters:
                if char.role.lower() == name.lower():
                    return self._char_response(char, dialogue)

        # Direct character call via mention (e.g., 'Hey jellyfish do you...') or choosing who speaks first ('the prawn')
        for char in self.characters:
            # match full role or just last word
            keywords = [char.role.lower(), char.role.lower().split()[-1]]
            for kw in keywords:
                if kw in lower_input:
                    # extract prompt part after keyword
                    parts = re.split(re.escape(kw), text_input, flags=re.IGNORECASE)
                    after = parts[1].strip() if len(parts) > 1 else ""
                    # If no prompt text, treat as first-turn selection
                    if not after:
                        # let the chosen character speak first
                        other = self.characters[(self.characters.index(char) + 1) % len(self.characters)]
                        resp_text = char.interact_with(other, self.scene)
                        self.story_log.append((char.role, resp_text))
                        # set next turn index
                        self.current_idx = (self.characters.index(char) + 1) % len(self.characters)
                        return f"{char.role}: {resp_text}"
                    # otherwise, pass user question to character
                    return self._char_response(char, after)

        # Automatic turn-taking
        speaker = self.characters[self.current_idx]
        other = self.characters[(self.current_idx + 1) % len(self.characters)]
        resp_text = speaker.interact_with(other, self.scene)
        self.story_log.append((speaker.role, resp_text))
        self.current_idx = (self.current_idx + 1) % len(self.characters)
        return f"{speaker.role}: {resp_text}"

    def _char_response(self, char: Character, prompt: str) -> str:
        """
        Helper for character's direct responses.
        """
        char.set_scene(self.scene)
        resp = char.receive_prompt(prompt)
        self.story_log.append((char.role, resp))
        # advance turn to next character
        self.current_idx = (self.characters.index(char) + 1) % len(self.characters)
        return f"{char.role}: {resp}"

    def set_roles(self, roles_list):
        self.characters = [Character(name) for name in roles_list]
        text = f"Roles set: {', '.join(roles_list)}."
        self.messages.append({"role": "assistant", "content": text})
        self.story_log.append(("Narrator", text))
        return text

    def set_scene(self, scene_str):
        self.scene = scene_str
        text = f"Scene set: {scene_str}."
        self.messages.append({"role": "assistant", "content": text})
        self.story_log.append(("Narrator", text))
        return text