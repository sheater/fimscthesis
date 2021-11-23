import json
import re
import logging

logging.basicConfig(level=logging.INFO)

pattern = re.compile(r"\\snippet\{([\w-]+)\}\{([^\}]+)\}")

if __name__ == "__main__":
    with open("main.ipynb") as fp:
        data = json.load(fp)

        for cell in data["cells"]:
            if cell["cell_type"] != "code":
                continue

            source = cell["source"]
            if r"\snippet-ignore" in source[0]:
                continue

            logging.info("-" * 30)

            match = pattern.search(source[0])

            if match is not None:
                label = match.group(1)
                caption = match.group(2)

                code = r"\begin{lstlisting}" + \
                    r"[label={snip:" + label + r"}," + \
                    r"caption={" + caption + r"}," + \
                    r"basicstyle=\tiny,language=python]" + "\n" + \
                    "".join(source[1:]) + "\n" + \
                    r"\end{lstlisting}" + "\n"

                filepath = "generated/snippets/{}.tex".format(label)

                with open(filepath, "w") as fp:
                    fp.write(code)

            else:
                logging.warning("No snippet tag for:")

                print("".join(source))
