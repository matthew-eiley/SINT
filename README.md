# SINT — Simple Intuitive Notation for Technical Writing

SINT is a custom markup language and interpreter that compiles user-friendly syntax into clean LaTeX. 
It was born from frustration with LaTeX’s clunky syntax—especially when writing long-form technical documents.

With SINT, you can write readable, intuitive syntax like `\BODY{This is a paragraph}` or `\ORDERED{...}` and convert 
it directly into a professionally formatted LaTeX file—ready for Overleaf or PDF generation.

## Features

- 🧠 **Intuitive Syntax**  
  Supports headings (`\H1`–`\H6`), bold/italic/underline/strikethrough, lists, tables, math, code blocks, links, and more.

- 🧾 **Full LaTeX Output**  
  Generates LaTeX documents with proper preamble, formatting, and structure.

- 🧰 **Modular Interpreter**  
  Written in Python with support for clean extensibility and detailed parsing logic.

- 📏 **Nested Support**  
  Supports nested ordered/unordered lists, blockquotes, sub/superscripts, and inline formatting.

## Syntax Reference
Theull syntax guide is available in [syntax.md](syntax.md). It includes:

📖 Document metadata (title, author, date)

📚 Headings & paragraphs

✍️ Text formatting (bold, italic, etc.)

🧮 Math blocks and inline formulas

📦 Code blocks with language support

📝 Lists (ordered & unordered)

📊 Tables, blockquotes, links, and images

