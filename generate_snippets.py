import json
import re
import logging

logging.basicConfig(level=logging.INFO)

PATTERN = re.compile(r"\\snippet\{([\w-]+)\}\{([^\}]+)\}")

# LATEX_CHAR_MAP = {
#     "í": r"\'{i}",
#     "ě": r"\v{e}",
#     "é": r"\'{e}",
#     "ř": r"\v{r}",
#     "č": r"\v{c}",
#     "ý": r"\'{y}",
#     "š": r"\v{s}",
#     "Š": r"\v{S}",
#     "á": r"\'{a}",
#     "ů": r"\r{u}",
#     "Č": r"\v{C}",
#     "ň": r"\v{n}",
#     "Ú": r"\'{U}",
#     "ž": r"\v{z}",
#     "Ž": r"\v{Z}",
#     "ď": r"\v{d}"
# }

# def convert_source_to_latex(source: str) -> str:
#     return "".join([LATEX_CHAR_MAP.get(x, x) for x in source])

if __name__ == "__main__":
    with open("main.ipynb") as fp:
        data = json.load(fp)

        for cell in data["cells"]:
            if cell["cell_type"] != "code":
                continue

            source = cell["source"]
            if len(source) == 0:
                continue

            if r"\snippet-ignore" in source[0]:
                continue

            match = PATTERN.search(source[0])

            if match is not None:
                label = match.group(1)
                caption = match.group(2)

                # r"basicstyle=\small,language=python]" + "\n" + \

                code = r"\begin{lstlisting}" + \
                    r"[label={snip:" + label + r"}," + \
                    r"caption={" + caption + r"}," + \
                    r"basicstyle=\ttfamily\tiny,language=python]" + "\n" + \
                    "".join(source[1:]) + "\n" + \
                    r"\end{lstlisting}" + "\n"
                    # convert_source_to_latex("".join(source[1:])) + "\n" + \

                filepath = "generated/snippets/{}.tex".format(label)

                with open(filepath, "w", encoding='utf-8') as fp:
                    fp.write(code)

            else:
                logging.warning("No snippet tag for:")

                print("".join(source[:5]))

    print("Done.")
