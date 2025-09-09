from .helpers import HTMLHelper, PDFHelper

html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Sample Document</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.5; margin: 20px; }
        h1, h2, h3 { color: #2c3e50; }
        p { margin-bottom: 10px; }
        a { color: #2980b9; text-decoration: none; }
        a:hover { text-decoration: underline; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        ul, ol { margin-bottom: 15px; }
        blockquote { border-left: 4px solid #ccc; padding-left: 10px; color: #555; font-style: italic; }
        .highlight { background-color: #ffeb3b; }
        .sup { vertical-align: super; font-size: smaller; }
        .sub { vertical-align: sub; font-size: smaller; }
    </style>
</head>
<body>
    <h1>Sample PDF Test Document</h1>
    <h2>Introduction</h2>
    <p>This is a large sample HTML document used for testing PDF conversion. It contains various <strong>text styles</strong>, <em>emphasis</em>, <u>underlines</u>, <s>strikeouts</s>, and links like <a href="https://www.example.com">Example Site</a>.</p>
    
    <h2>Lists</h2>
    <p>Unordered list:</p>
    <ul>
        <li>Apples</li>
        <li>Bananas</li>
        <li>Cherries</li>
    </ul>
    
    <p>Ordered list:</p>
    <ol>
        <li>Step one</li>
        <li>Step two</li>
        <li>Step three</li>
    </ol>
    
    <h2>Tables</h2>
    <table>
        <tr>
            <th>Name</th>
            <th>Age</th>
            <th>City</th>
        </tr>
        <tr>
            <td>Alice</td>
            <td>28</td>
            <td>Melbourne</td>
        </tr>
        <tr>
            <td>Bob</td>
            <td>34</td>
            <td>Sydney</td>
        </tr>
        <tr>
            <td>Charlie</td>
            <td>22</td>
            <td>Brisbane</td>
        </tr>
    </table>
    
    <h2>Blockquotes</h2>
    <blockquote>
        “This is a blockquote. It should stand out visually in the PDF.”
    </blockquote>
    
    <h2>Inline Styles</h2>
    <p>This text has <span class="highlight">highlighting</span> and some <span style="color: red;">red text</span> for testing.</p>
    
    <h2>Superscript & Subscript</h2>
    <p>Water formula: H<span class="sub">2</span>O and Einstein's formula: E = mc<span class="sup">2</span>.</p>
    
    <h2>Conclusion</h2>
    <p>This sample document is designed to stress-test PDF conversion. It contains enough content to produce a multi-page PDF, including headings, tables, lists, and styled text.</p>
    
    <p>Visit <a href="https://www.google.com">Google</a> for more information.</p>
</body>
</html>
"""

PDFHelper().write(HTMLHelper().to_pdf(html), "out.pdf")