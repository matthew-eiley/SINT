# Sint Syntax

This document contains the comprehensive syntax documentation for the Sint language.

## Preliminary Info
### Title
```
\TITLE {Title}
```
This will display `Title` as the title of the document.
### Author
```
\AUTHOR {Matthew Eiley}
```
This will display `Matthew Eiley` as the author of the document.
### Date
```
\DATE {April 27, 2025}
```
This will display `April 27, 2025` as the date of the document.

### Table of Contents
```
\TOC {}
```
This will display a table of contents.

## Headings
```
\H1 {Heading 1}
```
This will display `Heading 1` as an H1 (the most ephasized heading) H1-H6 are supported.

## Paragraph Formatting
### Paragraphs
```
\BODY {Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sapien nulla, tincidunt in mi eget, imperdiet dictum tortor. Donec in mi aliquam, faucibus sem quis, feugiat justo. Curabitur sodales, purus id sagittis lobortis, lectus augue pretium massa, at condimentum urna tortor in lectus. Etiam sollicitudin turpis interdum ipsum ultricies semper. Nam orci massa, dignissim eu euismod nec, blandit a ligula. Donec purus nunc, eleifend eget aliquam efficitur, consequat eleifend mauris. In suscipit odio ut est auctor, vehicula consequat augue semper. Donec tincidunt odio eu purus ullamcorper pharetra.}
```
This will display all of the text within the curly brackets as a paragraph. Writing in a different `BODY` block will start a new paragraph. To break the line within a body paragraph, simply insert ` \\ ` wherever you want the newline to be
### Blockquotes
```
\BLOCKQUOTE {Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sapien nulla, tincidunt in mi eget, imperdiet dictum tortor. Donec in mi aliquam, faucibus sem quis, feugiat justo. Curabitur sodales, purus id sagittis lobortis, lectus augue pretium massa, at condimentum urna tortor in lectus. Etiam sollicitudin turpis interdum ipsum ultricies semper. Nam orci massa, dignissim eu euismod nec, blandit a ligula. Donec purus nunc, eleifend eget aliquam efficitur, consequat eleifend mauris. In suscipit odio ut est auctor, vehicula consequat augue semper. Donec tincidunt odio eu purus ullamcorper pharetra.}
``` 
This will display a blockquote containing the text. This is essentially the same as a body, just indented on both margins, so that it appears distinct. Additionally, a newline can be achieved using ` \\ `
### Horizontal Rules
To make a horizontal rule, write `\HR {}`.
### Page Breaks
To make a page break, write `\PB {}`.


## Emphasis
### Bold
Within another block, putting `\B{text}` will make that text appear in bold.
### Italic
Similarly, `\I{text}` will make the text appear in italics.
### Underline
Similarly, `\U{text}` will display the text underlined.
### Strikethrough
Similarly, `\S{text}` will display the text with a strikethrough.
### Combinations
Any combination (in any order) is valid, so for example, `\BI{text}` and `\IB{text}` will both display the text bold and underlined. Similarly, `\SBU{text}` will show the text with a strikethrough, in bold, and underlined. 
### Subscript
`\_{a}` will display `a` as a subscript.
### Superscript
Similarly, `\^{b}` will display `b` as a superscript.

## Lists
### Ordered Lists
```
\ORDERED    {This should be entry 1\
            This should be entry 2\
            \ORDERED{This should be entry 2,1\
                    This should be entry 2,2\
                    \ORDERED{This should be entry 2,2,1\
                            This should be entry 2,2,2}
                    This should be entry 2,3}
            This should be entry 3}
```
### Unordered Lists
```
\UNORDERED {
    this is the first entry.\
    This is the second unordered line.\
    \UNORDERED{this is a nested entry.}\
    \UNORDRED{\UNORDERED{this is a doubly-nested line}}\
    This is back to normal entry
}
```
## Tables
```
\TABLE {This is the Table Title
    0,0 | 1,0 | 2,0 \
    0,1 | 1,1 | 2,1 \
    0,2 | 1,2 | 2,2
}
```
Will display the table
```
This is the Table Title
-------------
|0,0|1,0|2,0|
-------------
|0,1|1,1|2,1|
-------------
|0,2|1,2|2,2|
-------------
```

## Code and Math
### Blocks
Similar to how you would declare a `BODY` block, declare a code or math block as follows:
```
\CODE {Python
    def foo():
        return "Hello World"
}
```
Which will display the code in a block with Python colouring.
```
\MATH {
    \frac{420}{a} = b + c \\
    x = \sqrt{y} - z + pq
}
```
### In-Text
Within a block like `BODY`, use `\C{code}` and `\M{math}` to display code and math respectively in-text.

## Links
Within a block like `BODY`, `\L{click here \ https://www.google.ca/}` will direct you to the link, by clicking the text "click here". To link to a file, rather than using a URL on the right side of the `\`, write it as follows: `\L{click here \ run:./filename}`. The `run:./` is necessary to specify that the link is to a file rather than a URL, and the `filename` is to be used as the file must be in the same directory as the pdf to generate the link properly.

## Images
```
\IMAGE { image_name \ caption}
```
Will display the image with `image_name`, and the caption "caption." For the image to be processed properly, add the image (with the name `image_name`) into the overleaf project before generating the pdf. Then download the pdf normally and there is no need to save or access the image locally.