# MkDocs MCQ Plugin


An interactive plugin for MkDocs to create and display single and multiple-choice quizzes directly within your documentation.

## Features

- **Multiple Question Types:** Supports both single choice (radio buttons) and multiple choice (checkboxes) questions.
- **Rich Content:** Use standard Markdown within questions, answers, and feedback, including inline code, links, bold/italic text, and even multi-line code blocks.
- **Immediate Feedback:** Users get instant results after submitting an answer, with clear visual indicators for CORRECT, INCORRECT, and MISSED states.
- **Explanations/Details:** Provide detailed feedback for any answer choice to help users learn.
- **Theme Agnostic:** Uses embedded SVG icons to ensure a consistent and polished look on any MkDocs theme, not just Material for MkDocs.
- **Quiz Summary:** Automatically calculates and displays a final score in a styled admonition block after submission.

## Installation

Install the plugin using pip:

```bash
pip install mkdocs-mcq
```

**Note**: This plugin requires the following packages to be present in your MkDocs environment.

- mkdocs>=1.5
- pymdown-extensions>=10.0
- pyyaml>=6.0

## Configuration

To use the plugin, add mcq to the plugins section of your `mkdocs.yml` file. The plugin will automatically configure its dependencies.

```yaml
plugins:
  - mcq
```

## Usage: Authoring Quizzes

To create a quiz, use a fenced code block with the language identifier `mcq`.

### Basic Structure

Each quiz block consists of two parts: a YAML configuration block and the question content written in Markdown's task list format.

````md
```mcq
---
type: single
question: Your question text goes here.
---

- [ ] An incorrect answer.
- [x] The correct answer.
- [ ] Another incorrect answer.
```
````

### Configuration Options

- `question` (required): The question to be displayed. You can use Markdown here, like inline code.  
- `type` (required): The type of question. Must be either "**single**" or "**multiple**".

### Choices

Choices are defined using Markdown's task list syntax.

Use `- [ ]` for an incorrect answer.  
Use `- [x]` for a correct answer.

### Adding Feedback

To add detailed feedback to any choice, place it in a blockquote (`>`) immediately following the choice.

```md
- [x] 8
  > Correct! `**` is the exponentiation operator in Python.

- [ ] 6
  > Incorrect. The `**` operator is for exponents, not multiplication.
```

## Examples

Here are some complete examples demonstrating the plugin's features.

### Example 1: Single-Choice Question

This example demonstrates a simple single-choice question with feedback for each option.

````md
```mcq
---
type: single
question: What is the output of `print(2 ** 3)`?
---

- [ ] 6
  > Incorrect. `2 * 3` would be 6.

- [x] 8
  > CORRECT! `**` is the exponentiation operator in Python.

- [ ] 9
- [ ] 5
```
````

### Example 2: Multiple-Choice with Code Blocks

This example shows a multiple-choice question where the options themselves are multi-line code blocks.

````md
```mcq
---
type: multiple
question: Which of the following are valid Python code? (Select all that apply)
---

- [ ]
  ```python
  echo("Hello World!")
  ```
  > `echo` is not a valid Python function

- [x] 
  ```python
  print("Hello World!")
  ```
  > `print` is a valid Python function

- [ ] 
  ```python
  printf("Hello World!")
  ```
  > `printf` is not a valid Python function

- [ ] 
  ```python
  println("Hello World!")
  ```
  > `println` is not a valid Python function
```
````

### Example 3: Fenced-code block question

````md
```mcq
---
type: single
question: |
  What is the error in the following Python code?
  ```python
  a = 10
  b = "5"
  print(a + b)
  ```
---

- [ ] A `SyntaxError`, because the code is improperly formatted.
  > The syntax of the code is valid Python.

- [x] A `TypeError`, because you cannot add an integer and a string.
  > The `+` operator is not defined between the types `int` and `str`, which raises a `TypeError`.

- [ ] No error, it will print `15`.
  > Python does not automatically convert the string `"5"` to a number in this context.

- [ ] No error, it will print `105`.
  > Incorrect. While some languages might concatenate these, Python raises a `TypeError` instead.
```
````

## License

This project is licensed under the MIT License.

