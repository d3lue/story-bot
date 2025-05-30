class OrchestratorBot:
    def __init__(self, api_key: str, log_path: str = "story_log.json"):
        openai.api_key = api_key
        # when we call set_character_names, we’ll fill both of these:
        self.character_objs: List[Character] = []
        self.current_idx: int = 0

        self.characters: List[str] = []
        self.scene: str = ""
        self.story_log: List[Tuple[str, str]] = []
        self.log_path = log_path
        # … rest of your existing init …
