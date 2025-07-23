# jarvis.py

from transformers import pipeline
from datetime import datetime
import json
import os

# 🌐 Shared AI Pipelines
lesson_generator = pipeline("text2text-generation", model="google/flan-t5-base")
summarizer = pipeline("summarization")

# 🧠 Jarvis Core Brain
class JarvisCore:
    def __init__(self, style="formal"):
        self.style = style
        self.memory_path = "memory.json"
        self.last_topic = None
        self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.memory_path):
            with open(self.memory_path, "r") as f:
                self.memory = json.load(f)
        else:
            self.memory = {}

    def _save_memory(self):
        with open(self.memory_path, "w") as f:
            json.dump(self.memory, f, indent=2)

    def _update_memory(self, topic, status="explained"):
        self.memory[topic] = {"status": status}
        self.last_topic = topic
        self._save_memory()

    def _generate_lesson(self, topic):
        tone_instructions = {
            "formal": "Use clear academic language.",
            "casual": "Explain like you're chatting with a curious student.",
            "analogy": "Use fun real-life analogies to explain the topic."
        }
        prompt = (
            f"Act as an experienced tutor. Explain the topic: '{topic}'\n"
            f"{tone_instructions.get(self.style, 'Use clear language.')}\n"
            "Include warm-up, examples, simple quiz, and summary."
        )
        result = lesson_generator(prompt, max_new_tokens=512, do_sample=False)
        self._update_memory(topic)
        return result[0]["generated_text"]

    def _summarize_topic(self, topic):
        summary = summarizer(f"The topic is: {topic}", max_length=100, min_length=30, do_sample=False)
        return summary[0]["summary_text"]

    def respond(self, query):
        query_lower = query.lower()

        # 🕒 Time Handling
        if "time" in query_lower:
            now = datetime.now()
            return f"It’s {now.strftime('%I:%M %p on %A, %B %d, %Y')}."

        # 🧑‍🏫 Lesson Style Teaching
        if any(kw in query_lower for kw in ["teach", "lesson", "explain", "how", "what is", "help me understand"]):
            return self._generate_lesson(query)

        # 🔍 General Summary
        if any(kw in query_lower for kw in ["history", "describe", "benefits of", "why"]):
            return self._summarize_topic(query)

        # 🔄 Confusion Handling
        if any(kw in query_lower for kw in ["confusing", "didn’t make sense", "explain better"]):
            if self.last_topic:
                new_explanation = self._generate_lesson(self.last_topic)
                return f"🔁 Let me try again with a clearer explanation:\n\n{new_explanation}"
            else:
                return "I’m not sure what you were referring to — could you repeat the topic?"

        # 🧠 Default Response
        return "I’m still learning — can you rephrase or ask me to teach something specific?"

    def set_style(self, style):
        self.style = style
