# =========================================================================== #
# --------------------------------- IMPORTS --------------------------------- #
# =========================================================================== #

import re
import sys
import textwrap
import inspect

# =========================================================================== #
# ------------------------------- PARSE INPUT ------------------------------- #
# =========================================================================== #

def parse_file(file_path, TEX_PATH):
    with open(file_path, "r") as f:
        text = f.read()
    index = 0
    length = len(text)
    while index < length:
        # Find the next backslash
        if text[index] != '\\':
            index += 1
            continue
        # Extract keyword
        keyword_match = re.match(r'\\(?P<keyword>\w+)', text[index:])
        if not keyword_match:
            index += 1
            continue
        keyword = keyword_match.group('keyword')
        index += keyword_match.end()
        # Skip whitespace after keyword
        while index < length and text[index].isspace():
            index += 1
        if index >= length or text[index] != '{':
            # Invalid syntax (no opening brace)
            continue
        index += 1  # Move past '{'
        # Find matching closing '}' by counting nested braces
        brace_depth = 1
        content_start = index
        while index < length and brace_depth > 0:
            if text[index] == '{':
                brace_depth += 1
            elif text[index] == '}':
                brace_depth -= 1
            index += 1
        content = text[content_start : index-1]  # Content without the final '}'
        content = content.strip()
        # Process the keyword and content
        process_keyword(keyword, content, TEX_PATH)

def process_keyword(keyword, content, TEX_PATH):
    match keyword:
        case "TITLE":
            do_preamble(keyword, do_content(content), TEX_PATH)
        case "AUTHOR":
            do_preamble(keyword, do_content(content), TEX_PATH)
        case "DATE":
            do_preamble(keyword, do_content(content), TEX_PATH)
        case "TOC":
            do_preamble(keyword, do_content(content), TEX_PATH)
        case "H1":
            do_heading("chapter", do_content(content), TEX_PATH)
        case "H2":
            do_heading("section", do_content(content), TEX_PATH)
        case "H3":
            do_heading("subsection", do_content(content), TEX_PATH)
        case "H4":
            do_heading("subsubsection", do_content(content), TEX_PATH)
        case "H5":
            do_heading("paragraph", do_content(content), TEX_PATH)
        case "H6":
            do_heading("subparagraph", do_content(content), TEX_PATH)
        case "BODY":
            do_body(do_content(content), TEX_PATH)
        case "BLOCKQUOTE":
            do_specialty(keyword, do_content(content), TEX_PATH)
        case "HR":
            do_hr(TEX_PATH)
        case "PB":
            do_pb(TEX_PATH)
        case "ORDERED":
            do_list(keyword, do_content(content), TEX_PATH)
        case "UNORDERED":
            do_list(keyword, do_content(content), TEX_PATH)
        case "TABLE":
            do_table(do_content(content), TEX_PATH)
        case "CODE":
            do_specialty(keyword, content, TEX_PATH)
        case "MATH":
            do_specialty(keyword, content, TEX_PATH)
        case "IMAGE":
            do_image(content, TEX_PATH)   
        case _:
            do_invalid_keyword(keyword, content, TEX_PATH)

# =========================================================================== #
# -------------------------------- PREAMBLE --------------------------------- #
# =========================================================================== #

def do_preamble(preamble_tag, content, TEX_PATH):
    with open(TEX_PATH, "r") as f:
        lines = f.readlines()
    target_line = "\\begin{document}\n"
    make_title = "\\maketitle\n"
    title_insert = f"\\title{{{content}}}\n"
    author_insert = f"\\author{{{content}}}\n"
    date_insert = f"\\date{{{content}}}\n"
    toc_insert = "\\tableofcontents\n"
    for (i, line) in enumerate(lines):
        if line == target_line:
            match preamble_tag:
                case "TITLE":
                    lines.insert(i, title_insert)
                    make_title_check(lines, i)
                case "AUTHOR":
                    lines.insert(i, author_insert)
                    make_title_check(lines, i)
                case "DATE":
                    lines.insert(i, date_insert)
                    make_title_check(lines, i)
                case "TOC":
                    if lines[i+1] == make_title:
                        lines.insert(i+2, toc_insert)
                        lines.insert(i+3, "\\newpage\n")
                    else:
                        lines.insert(i+1, toc_insert)
                        lines.insert(i+2, "\\newpage\n")
                    
            break    
    with open(TEX_PATH, "w") as f:
        f.writelines(lines)

# =========================================================================== #
# -------------------------------- HEADINGS --------------------------------- #
# =========================================================================== #

def do_heading(heading_type, content, TEX_PATH):
    with open(TEX_PATH, "a") as f:
        f.write(f"\\{heading_type}{{{content}}}\n")

# =========================================================================== #
# ---------------------------------- BODY ----------------------------------- #
# =========================================================================== #

def do_body(content, TEX_PATH):
    with open(TEX_PATH, "a") as f:
        f.write(f"{content}\\newline\n\n")

def do_hr(TEX_PATH):
    with open(TEX_PATH, "a") as f:
        f.write("\\hrule\n"
                "\\vspace{1em}\n")

def do_pb(TEX_PATH):
    with open(TEX_PATH, "a") as f:
        f.write("\\newpage\n")

# =========================================================================== #
# --------------------------------- LISTS ----------------------------------- #
# =========================================================================== #

def do_list(kind, content, TEX_PATH):
    kind = kind.upper()
    assert kind in {"ORDERED", "UNORDERED"}, "Invalid list type"
    tree = parse_list(content)
    latex = render_list(tree, list_type=kind.lower())
    with open(TEX_PATH, "a") as f:
        f.write(latex)

# =========================================================================== #
# -------------------------------- SPECIALTY -------------------------------- #
# =========================================================================== #

def do_specialty(specialty_tag, content, TEX_PATH):
    with open(TEX_PATH, "a") as f:
        match specialty_tag:
            case "BLOCKQUOTE":
                f.write("\\begin{quote}\n"
                f"{content}\\newline\n\n"
                "\\end{quote}\n")
            case "CODE":
                parts = content.split("\n", 1)
                lang = parts[0]
                content = parts[1]
                cleaned = inspect.cleandoc(content)
                lines = cleaned.splitlines()
                if len(lines) > 1:
                    first, rest = lines[0], lines[1:]
                    rest_indented = ["\t" + line for line in rest]
                    final_code = "\n".join([first] + rest_indented)
                else:
                    final_code = cleaned
                f.write(f"\\begin{{lstlisting}}[language={lang}]\n"
                f"{final_code}\n"
                "\\end{lstlisting}\n\n\\vspace{1em}\n\n")
            case "MATH":
                f.write("\\begin{align*}\n"
                        f"{content}\n"
                        "\\end{align*}\n\n\\vspace{2em}\n\n")

# =========================================================================== #
# ---------------------------------- MISC ----------------------------------- #
# =========================================================================== #

def do_table(content: str, TEX_PATH: str):
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    if not lines:
        return

    title = lines[0]
    rows = []

    for line in lines[1:]:
        cells = [cell.strip() for cell in line.split("|")]
        rows.append(cells)

    num_cols = max(len(row) for row in rows)

    # Build column format: e.g., "|X|X|X|" for 3 columns
    col_format = "|" + "|".join(["Y"] * num_cols) + "|"

    s = "\\begin{table}[h]\n"
    s += "  \\centering\n"
    s += f"  \\caption{{{title}}}\n"
    s += "  \\vspace{0.5em}\n"
    s += f"  \\begin{{tabularx}}{{\\linewidth}}{{{col_format}}}\n"
    s += "    \\hline\n"

    for row in rows:
        padded_row = row + [""] * (num_cols - len(row))
        s += "    " + " & ".join(padded_row) + " \\\\\n"
        s += "    \\hline\n"

    s += "  \\end{tabularx}\n"
    s += "\\end{table}\n\n"

    with open(TEX_PATH, "a") as f:
        f.write(s)

def do_image(content, TEX_PATH):
    splt = content.split("\\")
    img = splt[0].strip()
    caption = splt[1].strip()
    with open(TEX_PATH, "a") as f:
        f.write("\\begin{figure}[h]\n"
                f"\\caption{{{caption}}}\n"
                "\\centering\n"
                f"\\includegraphics[width=0.667\\textwidth]{{{img}}}\n"
                "\\end{figure}\n")

def do_invalid_keyword(keyword, content, TEX_PATH):
    do_pb(TEX_PATH)
    with open(TEX_PATH, "a") as f:
        f.write(f"\\textbf{{INAVLID KEYWORD:}} {keyword} \\\\\n"
                f"\\textbf{{TEXT:}} {content}\n")
    do_pb(TEX_PATH)

# =========================================================================== #
# --------------------------------- CONTENT --------------------------------- #
# =========================================================================== #

def do_content(content):
    reg_ex = r"\\([BIUS^_CML]+)\{([^}]*)\}"
    matches = re.findall(reg_ex, content)
    for keyword, text in matches:
        old_text = f"\\{keyword}{{{text}}}"
        if len(keyword) == 1:
            match keyword:
                case "^":
                    new_text = f"$^{{{text}}}$"
                case "_":
                    new_text = f"$_{{{text}}}$"
                case "C":
                    new_text = f"\\texttt{{{text}}}"
                case "M":
                    new_text = f"${text}$"
                case "B":
                    new_text = f"\\textbf{{{text}}}"
                case "I":
                    new_text = f"\\textit{{{text}}}"
                case "U":
                    new_text = f"\\underline{{{text}}}"
                case "S":
                    new_text = f"\\sout{{{text}}}"
                case "L":
                    splt = text.split("\\")
                    txt = splt[0].strip()
                    url = splt[1].strip()
                    new_text = f"\\href{{{url}}}{{{txt}}}"
            content = content.replace(old_text, new_text)
        else:
            desc = ""
            for char in keyword:
                match char:
                    case "B":
                        desc += f"\\textbf{{"
                    case "I":
                        desc += f"\\textit{{"
                    case "U":
                        desc += f"\\underline{{"
                    case "S":
                        desc += f"\\sout{{"
            num_open_brack = desc.count("{")
            closed_brack = num_open_brack * "}"
            new_text = f"{desc}{text}{closed_brack}"
            content = content.replace(old_text, new_text)
    return content

# =========================================================================== #
# -------------------------------- TEX FILE --------------------------------- #
# =========================================================================== #

def get_tex_path(input_path):
    input_lst = input_path.split("/")[1:]
    tex_name = input_lst[len(input_lst)-1][:-4] + "_tex.txt"
    tex_lst = input_lst[:-1]
    tex_lst.append(f"{tex_name}")
    TEX_PATH = ""
    for part in tex_lst:
        TEX_PATH = TEX_PATH + "/" + part
    return TEX_PATH

def create_tex(TEX_PATH):
    with open(TEX_PATH, "w") as f:
        f.write("\\documentclass[12pt, letterpaper]{report}\n"
                "\\usepackage{graphicx}\n"
                "\\usepackage{titlesec}\n"
                "\\usepackage[normalem]{ulem}\n"
                "\\usepackage{amsmath}\n"
                "\\usepackage{amssymb}\n"
                "\\usepackage{listings}\n"
                "\\usepackage{xcolor}\n"
                "\\usepackage{enumitem}\n"
                "\\usepackage{tabularx}\n"
                "\\usepackage{array}\n"
                "\\usepackage{hyperref}\n"
                "\\hbadness=10000\n"
                "\\setlength{\\parindent}{0pt}\n"
                "\\titleformat{\\chapter}[display]\n"
                "\t{\\normalfont\\huge\\bfseries}\n"
                "\t{}\n"
                "\t{0pt}\n"
                "\t{\\huge}\n"
                "\\titlespacing*{\\chapter}\n"
                "\t{0pt}\n"
                "\t{0pt}\n"
                "\t{30pt}\n"
                "\\lstset{\n"
                "\tbasicstyle=\\ttfamily\\small,\n"
                "\tkeywordstyle=\\color{violet},\n"
                "\tcommentstyle=\\color{gray},\n"
                "\tstringstyle=\\color{blue},\n"
                "\tnumbers=left,\n"
                "\tnumberstyle=\\tiny\\color{gray},\n"
                "\tframe=single,\n"
                "\tbreaklines=true,}\n"
                "\\setlist[itemize,1]{label=$\\bullet$}\n"
                "\\setlist[itemize,2]{label=$\\circ$}\n"
                "\\setlist[itemize,3]{label=$\\cdot$}\n"
                "\\setlist[itemize,4]{label=-}\n"
                "\\newcolumntype{Y}{>{\\centering\\arraybackslash}X}\n"
                "\\hypersetup{\n"
                "\tcolorlinks=true,\n"
                "\tlinkcolor=black,\n"
                "\tfilecolor=blue,\n"
                "\turlcolor=blue,}\n"
                "\\graphicspath{ {./} }\n"
                "\\begin{document}\n")

def end_tex(TEX_PATH):
    with open(TEX_PATH, "a") as f:
        f.write("\n\\end{document}")

# =========================================================================== #
# --------------------------------- HELPERS --------------------------------- #
# =========================================================================== #

def make_title_check(lines, i):
    make_title = "\\maketitle\n"
    if make_title not in lines:
        lines.insert(i+2, make_title)

def parse_list(content):
    items, buf = [], []
    i, n = 0, len(content)
    def flush_buf():
        s = ''.join(buf).strip()
        buf.clear()
        if s and s != "\\":
            items.append(s)
    while i < n:
        for tag in ["ORDERED", "UNORDERED"]:
            if content.startswith(f"{tag}{{", i):
                flush_buf()
                j = i + len(tag) + 1
                depth = 1
                while j < n and depth:
                    if content[j] == "{": depth += 1
                    elif content[j] == "}": depth -= 1
                    j += 1
                inner = content[i + len(tag) + 1 : j - 1]
                items.append((tag.lower(), parse_list(inner)))
                i = j
                break
        else:
            if m := re.match(r'\\\s*\n', content[i:]):
                flush_buf()
                i += m.end()
            else:
                buf.append(content[i])
                i += 1
    flush_buf()
    return items

def render_list(tree, level=0, list_type="unordered"):
    indent = "  " * level
    if list_type == "unordered":
        begin = f"{indent}\\begin{{itemize}}\n"
        end = f"{indent}\\end{{itemize}}\n\n"
    else:  # ordered
        opts = "[label=\\arabic*.]" if level == 0 else "[label*=\\arabic*.]"
        begin = f"{indent}\\begin{{enumerate}}{opts}\n"
        end = f"{indent}\\end{{enumerate}}\n\n"
    s = begin
    for node in tree:
        if isinstance(node, str):
            s += f"{indent}  \\item {node}\n"
        else:
            sub_type, subtree = node
            s += render_list(subtree, level + 1, sub_type)
    s += end
    return s

# =========================================================================== #
# ---------------------------------- MAIN ----------------------------------- #
# =========================================================================== #

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("PROPER USAGE: python3 sint_engine.py path/to/txt/file")
        sys.exit(1)

    input_path = sys.argv[1]
    
    TEX_PATH = ""
    TEX_PATH = get_tex_path(input_path)
    
    print(f"(1) Begin Create Tex")
    create_tex(TEX_PATH)
    print(f"(2) Completed Create Tex")
    
    print(f"(3) Begin Parse File")
    parse_file(input_path, TEX_PATH)
    print(f"(4) Completed Parse File")
    
    print(f"(5) Begin End Tex")
    end_tex(TEX_PATH)
    print(f"(6) Completed End Tex")
    
    print("\nSUCCESS!\n"
          f"Your generated TEX file can be found at {TEX_PATH}\n"
          "Copy content into overleaf to generate a pdf")
    sys.exit(0)

# python3 sint_interpreter.py /Users/mattheweiley/Desktop/SINT/file_name