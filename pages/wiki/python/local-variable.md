---
title: Local Variable
comments: []
---

A **local variable** is a variable that exists only within a function.

<figure class=example>

```python
x = 5

def sum(a, b):
    return a + b
```

In the body of `sum`, `a` and `b` are local variables. Outside of `sum`, `a` and
`b` do not exist.

`x` is a global variable.

</figure>

# Shadowing

It's possible to have a local variable and a global variable with the same name.

<figure class=example>

```python
x = 5

def display_x():
    x = 6
    print(x)
```

Wherever the name `x` appears in the body of `display_x`, it refers to the local
variable, not the global. This is because the local variable **shadows** the
global variable of the same name.

```
>>> display_x()
6
>>> x
5
```

Notice that `print(x)` within `display_x` printed `6` (the value of the *local
variable* `x`), while the *global variable* `x` remained unchanged.

</figure>

# What makes a variable *local*?

A variable is local if it *could be assigned to* anywhere within the function.
When Python first sees the function definition, it scans the whole function to
determine which variables are local. If there is any potential assignment to a
variable within a function, that variable becomes a local variable.

<figure class=example>

```python
def display_x():
    print(x)
```

In `display_x`, `x` is **not** a local variable because there is no assignment
to it within the function.

</figure>

It does not matter whether assignment to the variable actually occurs at
runtime. It is simply the *presence* of an assignment operation within the
function that causes a variable to become local.

<figure class=example>

```python
def banana():
    return "banana"
    x = 6
```

`x` is a local variable in `banana` due to the presence of an assignment
operation in the function. It makes no difference that `x = 6` is never
executed.

</figure>

## Overriding

A function can override Python's decision about whether a variable is local by
using `global` (or `nonlocal`). This statement accepts a list of variable names
and tells Python that those variables should be considered global (or non-local)
instead of local. (*Non-local* is a more complex topic, so we won't address it
here.)

<figure class=example>

```python
x = 5

def display_x():
    global x
    x = 6
```

In `display_x`, `x` is a global variable due to the `global x` statement. The
`x = 6` assignment modifies the global variable.

</figure>

Because `global`/`nonlocal` affect how variable names are interpreted throughout
the whole function, it is best practice to put them at the very top of the
function.

## UnboundLocalError

`UnboundLocalError` means that your code tried to *use* a variable before any
value was assigned to it. It's just like `NameError` but for local
variables.

<figure class=example>

```python
def display_x_error():
    print(x)
    x = 6
```

In `display_x_error`, `x` is a local variable because there is an assignment to
it within the function.

</figure>
