---
hide:
  - toc
---

# Test Your Knowledge

Test your Python skills with the quiz below.

### Question 1

```mcq
---
type: single
question: What is the output of `#!python print(2 ** 3)`?
---

- [ ] 6
- [x] 8 
  > `**` is the exponentiation operator in Python

- [ ] 9
- [ ] 5
```

### Question 2

```mcq
---
type: multiple
question: Which of the following are valid dictionary methods in Python? (Select all that apply)
---

- [x] `keys()` 
  > Returns a view object displaying a list of all the keys

- [x] `values()` 
  > Returns a view object displaying a list of all the values

- [x] `items()` 
  > Returns a view object displaying a list of dictionary's key-value tuple pairs

- [ ] `elements()` 
  > `elements` is not a valid dictionary method
```

### Question 3

```mcq
---
type: multiple
question: Which of the following are valid Python code? (Select all that apply)
--- 

- [x] 
  ```python
  a = 25
  b = 30
  print(a + b)
  ```

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

### Question 4

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

### Question 5

```mcq
---
type: single
question: Which query correctly handles potential NULL values in string concatenation?
---

- [ ]
  ```sql
  SELECT first_name + ' ' + last_name AS full_name 
  FROM guest 
  WHERE guest_id IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
  ```

- [x]
  ```sql
  SELECT COALESCE(first_name, 'Unknown') + ' ' + COALESCE(last_name, 'Guest') AS full_name 
  FROM guest 
  WHERE registration_date >= '2023-01-01' AND status = 'active';
  ```
  > COALESCE handles NULL values by replacing them with default strings

- [ ]
  ```sql
  SELECT ISNULL(first_name + ' ' + last_name, 'Unknown Guest') AS full_name 
  FROM guest 
  WHERE email IS NOT NULL AND phone_number IS NOT NULL;
  ```

- [ ]
  ```sql
  SELECT CONCAT(IFNULL(first_name, ''), ' ', IFNULL(middle_name, ''), ' ', IFNULL(last_name, '')) AS full_name 
  FROM guest_table 
  WHERE created_at > NOWD() - INTERVAL 30 DAY;
  ```
```

### Question 6

```mcq
---
type: single
question: |
  What is the derivative of 
  
  $$
  f(x) = x^2 + 3x + 5
  $$
---

- [ ] $f'(x) = x + 3$
  > You need to apply the power rule to each term.

- [x] $f'(x) = 2x + 3$
  > Using the power rule: $\frac{d}{dx}(x^2) = 2x$ and $\frac{d}{dx}(3x) = 3$

- [ ] $f'(x) = 2x^2 + 3x$
  > Remember, the derivative reduces the power by 1.

- [ ] $f'(x) = x^2 + 3$
  > This is not how differentiation works.
```

### Question 7

```mcq
---
type: multiple
question: Which of the following integrals are correctly evaluated? (Select all that apply)
---

- [x]
  $$\int_0^1 x^2 dx = \frac{1}{3}$$
  > Using the power rule for integration: $\int x^2 dx = \frac{x^3}{3}$, evaluated from 0 to 1.

- [ ]
  $$\int_0^{\pi} \sin(x) dx = 0$$
  > This is incorrect. The integral equals 2.

- [x]
  $$\int_1^e \frac{1}{x} dx = 1$$
  > This equals $\ln(e) - \ln(1) = 1 - 0 = 1$

- [ ]
  $$\int_{-1}^{1} x dx = 1$$
  > This integral equals 0 because the function is odd and the limits are symmetric.
```
