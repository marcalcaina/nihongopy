import json
import os
import random
from collections import defaultdict
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.columns import Columns
from rich.table import Table
from rich import box
import questionary

console = Console()


class N5Trainer:
    def __init__(self):
        self.files = {
            "Hiragana": "hiragana.json",
            "Katakana": "katakana.json",
            "Kanji": "kanji.json",
            "Grammar": "grammar.json"
        }
        self.score = 0
        self.lang = "en"
        self.ui = {}

        # Estilo personalizado para Questionary
        self.custom_style = questionary.Style([
            ('qmark', 'fg:#5fafff bold'),
            ('question', 'bold white'),
            ('answer', 'fg:#af00ff bold'),
            ('pointer', 'fg:#ffff00 bold'),
            ('highlighted', 'fg:#00ffff bold'),
            ('selected', 'fg:#00ff00'),
        ])

    def load_json(self, filename):
        if not os.path.exists(filename):
            return None
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_ui(self, key):
        return self.ui.get(self.lang, {}).get(key, key)

    def get_common_ui(self, key):
        return self.ui.get("common", {}).get(key, key)

    def get_mode_label(self, mode):
        return self.get_ui(f"mode_{mode.lower()}") if mode else ""

    def header(self, subtitle=""):
        console.clear()
        title = Text(f" {self.get_ui('app_title')} ", style="bold white on blue")
        status = Text(f" [ {self.get_ui('score')}: {self.score} ] ", style="bold black on yellow")

        console.print(Columns([title, status], expand=True, align="center"))

        console.print(Panel(
            Align.center(f"[bold cyan]{subtitle}[/bold cyan]"),
            border_style="magenta",
            box=box.ROUNDED
        ))
        console.print("")

    def run(self):
        self.ui = self.load_json("interface.json") or {}

        self.lang = questionary.select(
            self.get_common_ui("language_prompt"),
            choices=[
                {"name": self.get_common_ui("language_en"), "value": "en"},
                {"name": self.get_common_ui("language_es"), "value": "es"}
            ],
            style=self.custom_style,
            instruction=self.get_common_ui("menu_instruction")
        ).ask()

        if not self.lang:
            return

        while True:
            self.header(self.get_ui("welcome"))

            practice_modes = ["Hiragana", "Katakana", "Kanji", "Grammar"]
            review_modes = ["Hiragana", "Katakana", "Kanji"]
            menu_choices = [
                questionary.Separator(self.get_ui("menu_section_practice")),
                *[
                    questionary.Choice(
                        title=f"📖 {self.get_mode_label(mode)}",
                        value=("practice", mode)
                    )
                    for mode in practice_modes
                ],
                questionary.Separator(self.get_ui("menu_section_review")),
                *[
                    questionary.Choice(
                        title=f"📖 {self.get_mode_label(mode)}",
                        value=("review", mode)
                    )
                    for mode in review_modes
                ],
                questionary.Separator(),
                questionary.Choice(title=f"❌ {self.get_ui('exit')}", value="exit")
            ]

            choice = questionary.select(
                "",
                choices=menu_choices,
                style=self.custom_style,
                instruction=self.get_ui("menu_instruction")
            ).ask()

            if choice == "exit" or choice is None:
                console.print(f"\n[bold cyan]{self.get_ui('goodbye')}[/bold cyan]")
                break

            action, mode = choice
            data = self.load_json(self.files[mode])
            if not data:
                continue

            if action == "review":
                if mode == "Kanji":
                    self.show_kanji_chart(data)
                else:
                    self.show_kana_chart(data, mode)
            else:
                self.start_training(data, mode)

    def show_kana_chart(self, data, mode):
        category_titles = {
            "gojuuon": self.get_ui("category_gojuuon"),
            "dakuten": self.get_ui("category_dakuten"),
            "handakuten": self.get_ui("category_handakuten"),
            "yoon": self.get_ui("category_yoon")
        }

        grouped = defaultdict(list)
        for item in data:
            grouped[item.get("type", "other")].append(item)

        order = ["gojuuon", "dakuten", "handakuten", "yoon"]

        while True:
            self.header(f"{self.get_ui('study_mode')} - {self.get_mode_label(mode)}")

            for category in order:
                items = grouped.get(category, [])
                if not items:
                    continue

                table = Table(
                    title=category_titles.get(category, category.title()),
                    box=box.ROUNDED,
                    border_style="cyan",
                    show_header=True,
                    header_style="bold magenta",
                    expand=True
                )
                table.add_column(self.get_ui("char_prompt"), justify="center", style="bold white", no_wrap=True)
                table.add_column(self.get_ui("romaji_col"), justify="center", style="bold green")

                for item in items:
                    table.add_row(item["char"], item["romaji"])

                console.print(table)
                console.print("")

            questionary.press_any_key_to_continue(
                message=f"\n {self.get_ui('continue')}",
                style=self.custom_style
            ).ask()
            return

    def show_kanji_chart(self, data):
        while True:
            self.header(f"{self.get_ui('study_mode')} - {self.get_mode_label('Kanji')}")

            table = Table(
                title=self.get_ui("learn_kanji"),
                box=box.ROUNDED,
                border_style="cyan",
                show_header=True,
                header_style="bold magenta",
                expand=True
            )
            table.add_column(self.get_ui("kanji_col"), justify="center", style="bold white", no_wrap=True)
            table.add_column(self.get_ui("reading_col"), justify="center", style="bold green")
            table.add_column(self.get_ui("romaji_col"), justify="center", style="green")
            table.add_column(self.get_ui("meaning_col"), style="yellow")

            suffix = "_es" if self.lang == "es" else ""
            for item in data:
                meaning = item.get("meaning" + suffix, item.get("meaning", ""))
                table.add_row(
                    item.get("kanji", ""),
                    item.get("reading", ""),
                    item.get("romaji", ""),
                    meaning
                )

            console.print(table)
            console.print("")

            questionary.press_any_key_to_continue(
                message=f"\n {self.get_ui('continue')}",
                style=self.custom_style
            ).ask()
            return

    def start_training(self, data, mode):
        self.score = 0
        active = True
        suffix = "_es" if self.lang == "es" else ""

        while active:
            item = random.choice(data)

            if mode == "Grammar":
                q_text = item["sentence"]
                correct = item["answer"]
                options = item["distractors"] + [correct]
                hint = item.get('meaning' + suffix, item.get('meaning', ''))
            elif mode == "Kanji":
                q_text = f"{self.get_ui('reading_prompt')}: {item['kanji']}"
                correct = item["reading"]
                others = [i["reading"] for i in data if i["reading"] != correct]
                options = random.sample(others, min(3, len(others))) + [correct]
                hint = item.get('meaning' + suffix, item.get('meaning', ''))
            else:  # Hiragana / Katakana
                q_text = f"{self.get_ui('character_prompt')}: {item['char']}"
                correct = item["romaji"]
                others = [i["romaji"] for i in data if i["romaji"] != correct]
                options = random.sample(others, min(3, len(others))) + [correct]
                hint = self.get_ui("select_correct_romaji")

            random.shuffle(options)

            self.header(f"{self.get_mode_label(mode)} - {self.get_ui('practice_mode')}")
            console.print(Panel(
                Align.center(f"[bold white]{q_text}[/bold white]"),
                title=self.get_ui("question"),
                border_style="yellow",
                box=box.ROUNDED
            ))
            console.print(Align.center(f"[italic dim]{hint}[/italic dim]"))
            console.print("")

            user_answer = questionary.select(
                f"❯ {self.get_ui('select')}",
                choices=options,
                style=self.custom_style,
                qmark="?",
                instruction=self.get_ui("menu_instruction")
            ).ask()

            if user_answer == correct:
                self.score += 1
            else:
                active = False
                self.show_fail_screen(item, correct, mode, suffix)

    def show_fail_screen(self, item, correct, mode, suffix):
        console.clear()
        console.print(Panel(
            Align.center(f"[bold white on red] {self.get_ui('failed')} [/bold white on red]"),
            border_style="red",
            box=box.HEAVY
        ))

        expl = item.get("explanation" + suffix, item.get("explanation", self.get_ui("no_explanation")))

        results_text = Text.assemble(
            (f"{self.get_ui('wrong_ans')}\n", "white"),
            (f"{self.get_ui('right_ans')}: ", "white"),
            (f"{correct}\n\n", "bold green"),
            (f"💡 {self.get_ui('explanation')}: ", "yellow bold"),
            (f"{expl}", "yellow italic")
        )

        console.print(Panel(
            results_text,
            title=f"{self.get_ui('final_score')}: {self.score}",
            border_style="red",
            box=box.ROUNDED
        ))

        questionary.press_any_key_to_continue(
            message=f"\n {self.get_ui('continue')}",
            style=self.custom_style
        ).ask()


if __name__ == "__main__":
    try:
        trainer = N5Trainer()
        trainer.run()
    except KeyboardInterrupt:
        console.print(f"\n[bold cyan]{trainer.get_ui('goodbye')}[/bold cyan]")
