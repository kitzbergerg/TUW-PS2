# Programing Languages part 2

The task is to develop an interpreter for a functional language using a dynamically typed language (python).

## Language specification

### Types

* **unit** (represents a missing value, currently used for side effects like `print` where nothing is returned)
* **integer**: Currently only positive can be created like `x = 1`. To get negatives you can `x = minus(0, 10)`.
* **list**: Lists can be defined using `[]`. Lists can contain any values from `[0,1,2]` to `[*,1,+,2,[1,2]]`.
* **function**: See below

### Variables

Only lowercase and underscores are allowed. E.g. `my_func`, `my_var` are valid; `my-func`, `my_var1` are not valid.

### Operations

For operations the following are allowed:

Integer:

* `plus`
* `minus`
* `mult`
* `div` (integers division, there are no floats)
* `mod`

Boolean:

* `eq`
* `not`
* `and`
* `or`
* `less_than`
* `greater_than`

Lists:

* `head`: Returns the first element of the list.
* `tail`: Returns the list apart from the first element.
* `is_empty`: Checks if the list is empty.
* `concat`: Create a new list by concatenating two lists.

Other:

* `print`

## Syntax

The language itself is lazily evaluated. Until a function is called, nothing will happen.

### Control flow

Currently only if statements are supported for control flow.  
They have the following syntax: `if (<expr>) <expr> else <expr>`

### Expressions

Expressions evaluate to something i.e. they have some return value.

They can be:

* integers: `0`, `1`, ...
* lists: `[0,1]`
* variables: `x`
* functions: `<func_name>(<expr>, <expr>)` like `my_func(0, 1)` or `|x,y| plus(x, y)`
* blocks:
  ```
  {
     [<expr1>]
     ...
     <expr>
  }
  ```
  In this case the last block is the returned value.
* control flow elements: `if (<expr>) <expr> else <expr>` like `if (eq(0,0)) 0 else 1` would return `0`

Generally everything has a return value. If there would be no return value like for `print`, instead `unit` is returned.

### Functions

```
<var> = [|<var1>, ...|] <expr>
```

Functions are pure i.e. there are no side effects such as modifying a value passed to the function. This means that all
inputs into a function will be passed by value, there are no references.

The typical definition of a function would be

```
my_func = |x, y| {
    new_x = mult(x, y)
    plus(new_x, y)
}
```

The `||` specifies the parameter count and their naming inside the function.

One thing to consider is captures. To allow easy use of recursions and using functions inside functions, it is allowed
to use variables defined outside the function body. On function creation the environment will be copied to avoid
problems.
In the following example `plus_one` is defined outside the function and even after modifying it, the function works the
same:

```
plus_one = plus(1)
plus_one_squared = |x| {
  x_plus_one = plus_one(x)
  mult(x_plus_one, x_plus_one)
}
print(plus_one_squared(2)) # -> 9
plus_one = plus(2)
print(plus_one_squared(2)) # -> 9
```

Other valid variants are:

* `my_func = plus(0, 1)`
* `my_func = || plus(0, 1)`
* `my_func = { plus(0, 1) }`
* `my_func = || { plus(0, 1) }`
* `my_func = |x| 1`
* `plus_one = plus(1)`
* `plus_one = |x| plus(1, x)`

### Comments

Comments are specified with `#` and hold until the end of the line.

## Examples

### List map

```
map = |list, op| if(is_empty(list)) list else {
  head_l = head(list)
  tail_l = tail(list)
  concat([op(head_l)], map(tail_l, op))
}
my_list = [1,2,3]
times_two = map(my_list, mult(2))
print(times_two)  # [1,2,3]
```
