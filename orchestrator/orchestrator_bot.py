import json
import openai
from participants.character import Character
from typing import List, Tuple

class OrchestratorBot:
    def __init__(self, api_key: str, log_path: str = "story_log.json"):
        openai.api_key = api_key
        self.characters: List[str] = []
        self.scene: str = ""
        self.story_log: List[Tuple[str, str]] = []
        self.log_path = log_path
        # System prompt with placeholders for characters
        self.system_prompt = (
            "You are StoryWeaver, a dynamic, playful narrator and director. "
            "First, ask the user to define two characters and a scene. "
            "Once defined, on each user message choose one speaker: Narrator, {char1}, or {char2}, "
            "and respond in JSON only, exactly as: {\"speaker\": \"<name>\", \"text\": \"<utterance>\"}. "
            "Wait for the next user input after each response."
        )
        # Initialize messages
        self.messages = [{"role": "system", "content": self.system_prompt}]

    def set_character_names(self, char1: str, char2: str):
        """
        Replace placeholders with actual character names and reset history.
        """
        prompt = self.system_prompt.format(char1=char1, char2=char2)
        self.messages = [{"role": "system", "content": prompt}]
        self.characters = [char1, char2]

    def process_input(self, user_input: str) -> str:
        """
        Process user input, parse LLM JSON output, log and return '<speaker>: <text>'.
        """
        # Append user message
        self.messages.append({"role": "user", "content": user_input})
        # Call LLM
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=self.messages
        )
        raw = response.choices[0].message.content.strip()
        # Attempt JSON parsing
        try:
            obj = json.loads(raw)
            speaker = obj.get("speaker", "Narrator")
            text = obj.get("text", "")
        except json.JSONDecodeError:
            speaker, text = "Narrator", raw
        # Log and save
        self.messages.append({"role": "assistant", "content": raw})
        self._log(speaker, text)
        return f"{speaker}: {text}"

    def _log(self, speaker: str, text: str):
        self.story_log.append((speaker, text))
        try:
            with open(self.log_path, 'w', encoding='utf-8') as f:
                json.dump(self.story_log, f, ensure_ascii=False, indent=2)
        except Exception:
            pass