# Programing Languages part 2

The task is to develop an interpreter for a functional language using a dynamically typed language (python).

## Language specification

The language has the following supported elements:

* integers (for bool expressions 0 will be evaluated to false, everything else is true)
* structured data (lists)
* functions
* named entities (variables, function names, ...)
* operations: plus, minus, mult, div, eq, ...

For named entities only lowercase and underscores are allowed. E.g. `my_func`, `my_var` are valid; `my-func`, `my_var1`
are not valid.

### Operations

For operations the following are allowed:

* `plus`
* `minus`
* `mult`
* `div` (integers division, there are no floats)
* `mod`
* `if` (the first param is a block than will be evaluated as true or false, the second block is returned if true, the
  third if false)

Boolean operators:

* `eq`
* `not`
* `and`
* `or`
* `less_than`
* `greater_than`

Other:

* `print`

## Syntax

The language itself is lazily evaluated. Until a function is called, nothing will happen.

### Blocks

Blocks are expressions that evaluate to something i.e. that have some return value.

Blocks can be:

* integers: `0`, `1`, ...
* functions: `<func_name>(<block>, <block>)` like `my_func(0, 1)` or `|x,y| plus(x, y)`
* brackets:
  ```
  {
     [<expr1>]
     ...
     <block>
  }
  ```
  In this case the last block is the returned value.

### Functions

```
<var> = [|<var1>, ...|] <block>
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
to use functions defined outside the block. On function creation all functions inside will be copied to avoid problems.
In the following example `plus_one` is defined outside the function and even after modifying it, the function works the
same:

```
plus_one = plus(1)
plus_one_squared = |x| {
  x_plus_one = plus_one(x)
  mult(x_plus_one, x_plus_one)
}
plus_one_squared(2) # -> 9
plus_one = plus(2)
plus_one_squared(2) # -> 9
```

Other valid variants are:

* `my_func = plus(0, 1)`
* `my_func = || plus(0, 1)`
* `my_func = { plus(0, 1) }`
* `my_func = || { plus(0, 1) }`
* `my_func = |x| 1`
* `plus_one = plus(1)`
* `plus_one = |x| plus(1, x)`

### Lists

Lists can be defined using `[]`. Lists can contain any values from `[0,1,2]` to `[*,1,+,2,[1,2]]`.

Operations supported for lists are:

* `head`: Returns the first element of the list.
* `tail`: Returns the list apart from the first element.
* `is_empty`: Checks if the list is empty.
* `concat`: Create a new list by concatenating two lists.

## Examples

### List map

```
map = |list, op| if(is_empty(list), list, {
  head_l = head(list)
  tail_l = tail(list)
  concat([op(head_l)], map(tail_l, op))
})
my_list = [1,2,3]
times_two = map(my_list, mult(2))
```
