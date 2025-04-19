import mistune
from mistune import BaseRenderer


def extract_markdown_section(md_text, heading_name, heading_level=None):
    markdown = mistune.create_markdown(renderer=None)
    ast = markdown(md_text)

    collecting = False
    current_level = None
    result = []

    for i, node in enumerate(ast):
        if node["type"] == "heading":
            text = "".join(
                child["raw"] for child in node["children"] if child["type"] == "text"
            )

            level = node["attrs"]["level"]

            if collecting:
                # If we hit a heading of same or higher level, stop
                if level <= current_level:
                    break

            if text.strip().lower() == heading_name.lower():
                collecting = True
                current_level = level
                heading_level = level  # save for external use too if passed as None
                continue

        if collecting:
            result.append(node)

    return result  # still in AST, can convert to markdown or HTML if needed


class MarkdownRenderer:
    def __call__(self, tokens, state=None, level=0):
        return "".join([self.render_token(token, level) for token in tokens])

    def render_token(self, token, level=0):
        t = token["type"]
        if t == "text":
            return token["raw"]
        elif t == "paragraph":
            return self(token["children"], level)
        elif t == "block_text":
            return self(token["children"], level)
        elif t == "strong":
            return f"**{self(token['children'], level)}**"
        elif t == "emphasis":
            return f"*{self(token['children'], level)}*"
        elif t == "link":
            text = self(token["children"], level)
            return f"[{text}]({token['attrs']['url']})"

        elif t == "list":
            depth = token["attrs"].get("depth", 0)
            return "".join(
                self.render_list_item(item, depth) for item in token["children"]
            )
        elif t == "heading":
            return (
                f"{'#' * token['attr']['level']} {self(token['children'], level)}\n\n"
            )
        elif t == "code_block":
            return f"```\n{token['text']}\n```\n\n"
        elif t == "inline_code":
            return f"`{token['text']}`"
        elif t == "blockquote":
            return "> " + self(token["children"], level).replace("\n", "\n> ") + "\n\n"
        else:
            breakpoint()
            return f"<{t}>"

    def render_list_item(self, token, depth):
        indent = "    " * depth
        child_tokens = token["children"]

        # Separate text (block_text, paragraph, etc) from nested lists
        text_tokens = []
        nested_lists = []
        for child in child_tokens:
            if child["type"] == "list":
                nested_lists.append(child)
            else:
                text_tokens.append(child)

        text = self(text_tokens).strip()
        nested = "".join(self.render_token(t) for t in nested_lists).rstrip()

        # Add newline between top-level text and nested list (if present)
        if nested:
            return f"{indent}- {text}\n{nested}\n"
        else:
            return f"{indent}- {text}\n"


if __name__ == "__main__":
    # Example usage
    md_text = """'\n## Inbox\n\n## Todo\n\n## Ideas\n\n## Journal\n\n## Bookmarks\n- Cool personal assistant with single SQLite table and some cron jobs [Stevens: a hackable AI assistant using a single SQLite table and a handful of cron jobs](https://www.geoffreylitt.com/2025/04/12/how-i-made-a-useful-ai-assistant-with-one-sqlite-table-and-a-handful-of-cron-jobs)\n\t- Implementation: [stevensDemo/README.md | Val Town](https://www.val.town/x/geoffreylitt/stevensDemo/code/README.md)\n- Valtown a very interesting platform for deploying simple apis / cron jobs / etc... [val.town](https://www.val.town/)\n\t- Examples: [Val Town](https://www.val.town/explore/use-cases)\n\t\t- Standup bot\n\t\t- slack notifications\n\t\t- simple blog\n\t\t- framer integrations \n\t\t\t- [Introduction - Framer Developers](https://www.framer.com/developers/fetch-introduction)\n\t\t- replicate app:\n\t\t\t- [Build a webhook notifier with Val Town - Replicate docs](https://replicate.com/docs/guides/build-a-webhook-notifier-with-val-town)\n\t\t- etc..\n\t- Cron job example: [Your first cron val | Docs | Val Town](https://docs.val.town/quickstarts/first-cron/)\n\t- Use with local editor: [GitHub - val-town/vt: CLI to work with projects in the Val Town platform](https://github.com/val-town/vt)\n- Steel headless web browser for web agents [Steel | Open-source Headless Browser API](https://steel.dev/#pricing)\n\t- With Val integration [Overview | Overview](https://docs.steel.dev/overview/integrations/valtown/overview)\n- Internals of pytorch\n\n## Other'"""

    ast = extract_markdown_section(md_text, "Bookmarks")

    # markdown = mistune.create_markdown(renderer=None)
    # ast = markdown(md_text)

    renderer = MarkdownRenderer()
    markdown_again = renderer(ast)
    print(markdown_again)
