# mkdocs_mcq/plugin.py
import os
import yaml
import re
import textwrap
import markdown
import traceback
import json
import base64
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File


def format_mcq(source, language, css_class, options, md, **kwargs):
    """
    Custom formatter with encoded answers and encoded feedback.
    """
    try:
        source = source.strip()
        if source.startswith("---"):
            _, frontmatter, content = source.split("---", 2)
            config = yaml.safe_load(frontmatter)
        else:
            content, config = source, {}

        mcq_type = config.get("type", "single")
        choices = []
        choice_pattern = re.compile(r"^(\s*)-\s*\[([xX ]?)\]\s*(.*)")

        for line in content.strip().splitlines():
            choice_match = choice_pattern.match(line)
            if choice_match:
                indent_str, checked_char, text_line = choice_match.groups()
                choices.append(
                    {
                        "text_md": text_line,
                        "correct": checked_char.strip() != "",
                        "feedback_md": "",
                        "base_indent": len(indent_str),
                    }
                )
            elif choices:
                last_choice = choices[-1]
                line_indent = len(line) - len(line.lstrip(" "))
                if line.strip() == "" or line_indent > last_choice["base_indent"]:
                    if line.strip().startswith(">"):
                        last_choice["feedback_md"] += line.strip()[1:].strip() + "\n"
                    else:
                        last_choice["text_md"] += "\n" + line

        correct_answer_indices = [
            i for i, choice in enumerate(choices) if choice["correct"]
        ]
        answer_key = json.dumps(correct_answer_indices).encode("utf-8")
        encoded_key = base64.b64encode(answer_key).decode("utf-8")

        # Create a new Markdown instance with the necessary extensions for rendering
        # We need to build extension list from scratch to avoid recursion
        mkdocs_config = options.get('_mkdocs_config', {})
        mdx_configs = mkdocs_config.get('mdx_configs', {})

        # Build a clean list of extension names needed for rendering MCQ content
        extensions_to_use = [
            'pymdownx.highlight',
            'pymdownx.inlinehilite',
            'pymdownx.superfences',
            'pymdownx.tasklist',
            'pymdownx.arithmatex',
        ]

        # Copy extension configs, but modify superfences to exclude custom fences
        extension_configs_to_use = {}
        for ext_name in extensions_to_use:
            if ext_name in mdx_configs:
                if ext_name == 'pymdownx.superfences':
                    # Include superfences but without custom fences to prevent recursion
                    superfences_cfg = mdx_configs[ext_name].copy()
                    superfences_cfg['custom_fences'] = []
                    extension_configs_to_use[ext_name] = superfences_cfg
                else:
                    extension_configs_to_use[ext_name] = mdx_configs[ext_name]
            elif ext_name == 'pymdownx.arithmatex':
                # Always configure arithmatex with generic mode for MCQ content
                extension_configs_to_use[ext_name] = {'generic': True}

        temp_md = markdown.Markdown(
            extensions=extensions_to_use,
            extension_configs=extension_configs_to_use
        )
        question_html = temp_md.convert(
            config.get("question", "Choose the correct answer:")
        )

        choices_html = '<ul class="task-list">'
        for choice in choices:
            choice_text_dedented = textwrap.dedent(choice["text_md"]).strip()
            temp_md.reset()
            choice_html = temp_md.convert(choice_text_dedented)

            # --- NEW: Encode the feedback HTML before adding it to the data attribute ---
            encoded_feedback = ""
            if choice["feedback_md"]:
                temp_md.reset()
                feedback_html = temp_md.convert(textwrap.dedent(choice["feedback_md"]))
                encoded_feedback = base64.b64encode(
                    feedback_html.encode("utf-8")
                ).decode("utf-8")

            choices_html += (
                f'<li class="task-list-item" data-feedback="{encoded_feedback}">'
            )
            choices_html += f'    <label><input type="checkbox"> {choice_html}</label>'
            choices_html += "</li>"
        choices_html += "</ul>"

        return f"""
        <div class="mcq-container" data-mcq-type="{mcq_type}" data-key="{encoded_key}">
            <div class="mcq-question">{question_html}</div>
            <div class="mcq-choices">{choices_html}</div>
        </div>
        """
    except Exception as e:
        error_html = '<div class="mcq-error" style="color: red; border: 1px solid red; padding: 1rem;">'
        error_html += f"<strong>Error processing MCQ:</strong> {e}<br>"
        error_html += f"<pre>{traceback.format_exc()}</pre></div>"
        return error_html


class MCQPlugin(BasePlugin):
    """MkDocs plugin for multiple choice questions"""

    def on_config(self, config):
        config.setdefault("extra_css", []).append("assets/mcq.css")
        config.setdefault("extra_javascript", []).extend([
            "assets/mcq.js",
            "assets/mathjax-config.js",
            "https://polyfill.io/v3/polyfill.min.js?features=es6",
            "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
        ])
        self._configure_superfences(config)
        self._configure_tasklist(config)
        self._configure_arithmatex(config)
        return config

    def _configure_superfences(self, config):
        mdx_configs = config.setdefault("mdx_configs", {})
        superfences_config = mdx_configs.setdefault("pymdownx.superfences", {})
        custom_fences = superfences_config.setdefault("custom_fences", [])
        if not any(f["name"] == "mcq" for f in custom_fences):
            # Pass the config through options so format_mcq can access extensions
            custom_fences.append({
                "name": "mcq",
                "class": "mcq",
                "format": format_mcq,
                "options": {
                    "_mkdocs_config": {
                        "markdown_extensions": config.get("markdown_extensions", []),
                        "mdx_configs": mdx_configs
                    }
                }
            })

    def _configure_tasklist(self, config):
        mdx_configs = config.setdefault("mdx_configs", {})
        tasklist_config = mdx_configs.setdefault("pymdownx.tasklist", {})
        tasklist_config["custom_checkbox"] = True

    def _configure_arithmatex(self, config):
        mdx_configs = config.setdefault("mdx_configs", {})
        arithmatex_config = mdx_configs.setdefault("pymdownx.arithmatex", {})
        arithmatex_config["generic"] = True

    def on_page_content(self, html, page, config, files):
        if '<div class="mcq-container"' in html:
            html = f'<form id="mkdocs-mcq-form">{html}</form>'
            # --- FIX: Added form="mkdocs-mcq-form" to link the button to the form ---
            html += """
            <button type="submit" id="mcq-quiz-submit" form="mkdocs-mcq-form" class="md-button md-button--primary">
                Submit Quiz
            </button>
            """
        return html

    def on_files(self, files, config):
        plugin_dir = os.path.dirname(__file__)
        for asset_file in ["mcq.css", "mcq.js", "mathjax-config.js"]:
            files.append(
                File(
                    path=f"assets/{asset_file}",
                    src_dir=plugin_dir,
                    dest_dir=config["site_dir"],
                    use_directory_urls=config.get("use_directory_urls", True),
                )
            )
        return files
