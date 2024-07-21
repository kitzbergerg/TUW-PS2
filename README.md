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

* plus /2
* minus /2
* mult /2
* div /2 (integers division, there are no floats)
* cond /3 (the first param is a block than will be evaluated as true or false, the second block is returned if true, the
  third if false)

Boolean operators:

* eq /2
* not /1
* and /2
* or /2
* less_than /2
* greater_than /2

## Syntax

Everything in this language can be evaluated as a function. Integers are function that return constants, operations are
functions, blocks are functions, ...

### Blocks

Blocks are expressions that evaluate to something i.e. that have some return value.

Blocks can be:

* integers: `0`, `1`, ...
* operations: `<operation> <block> <block>` like `plus 0 1`, `plus {mult 1 2} 2` or `cond <block> <block> <block>`
* functions: `<func_name> <block> <block>` like `my_func 0 1`
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
    new_x = mult x y
    plus new_x y
}
```

The `||` specifies the parameter count and their naming inside the function.

One thing to consider is captures. To allow easy use of recursions and using functions inside functions, it is allowed
to use functions defined outside the block. On function creation all functions inside will be copied to avoid problems.
In the following example `plus_one` is defined outside the function and even after modifying it the function works the
same:

```
plus_one = plus 1
plus_one_squared = |x| {
  x_plus_one = plus_one x
  mult x_plus_one x_plus_one
}
plus_one_squared 2 # -> 9
plus_one = plus 2
plus_one_squared 2 # -> 9
```

Other valid variants are:

* `my_func = plus 0 1`
* `my_func = || plus 0 1`
* `my_func = { plus 0 1 }`
* `my_func = || { plus 0 1 }`
* `my_func = |x| 1`
* `plus_one = plus 1`
* `plus_one = |x| plus 1 x`

### Lists

Lists can be defined using `[]`. Lists can contain any functions from `[0,1,2]` to `[mult,1,add,2,3]`.

Operations supported for lists are:

* head /1: Returns the first element of the list.
* tail /1: Returns the list apart from the first element.
* is_empty /1: Checks if the list is empty.
* concat /2: Create a new list by concatenating two lists.

## Examples

### Fibonacci

```
fib = |x| {
  cond {eq x 0} {
    0
  } {
    cond {or {eq x 1} {eq x 2}} {
      1 
    } {
      plus {fib {minus x 1}} {fib {minus x 2}}
    }
  } 
}
```

### List map

```
map = |list, op| cond {is_empty list} list {
  head_l = head list
  tail_l = tail list
  concat [{op head_l}] {map tail_l op}
}
my_list = [1,2,3]
times_two = map my_list {mult 2}
```

### List reduce

```
reduce = |acc, op, list| cond {is_empty list} acc {
  head_l = head list
  tail_l = tail list
  acc = op acc head_l
  reduce acc op tail_l
}
reduce_sum = reduce 0 add
my_list = [1,2,3]
sum = reduce_sum my_list
```

### List length

```
reduce_length = reduce 0 {|acc,y| add acc 1}
my_list = [1,2,3]
length = reduce_length my_list
```

### List at_index

```
at_index = |list, i| {
  at_index = |acc, list| {
    cond {eq i acc} {head list} {
      at_index {add acc 1} {tail list}
    }
  }
  at_index 0 list
}
my_list = [1,2,1,5,4]
one = at_index my_list 2
```

## Pitfalls

### Newlines and Blocks

A newline signals the end of a block, the exception being brackets.

Therefore, by slightly modifying the fibonacci example to:

```
fib = |x| {
  cond {eq x 0} {
    0
  }
  {
    cond {or {eq x 1} {eq x 2}} {
      1 
    } {
      plus {fib {minus x 1}} {fib {minus x 2}}
    }
  } 
}
```

the first `cond` will be ignored. `cond` will be passed two blocks, thereby creating a new function that is
however ignored.

It would be evaluated as:

```
fib = |x| {
  _ignored = cond {eq x 0} 0
  
  cond {or {eq x 1} {eq x 2}} {
    1 
  } {
    plus {fib {minus x 1}} {fib {minus x 2}}
  } 
}
```

### Evaluation ordering

Evaluation happens left to right. Since everything is a function you need to be careful with statements
like `plus mult 2 2 1`. This would evaluate to `{{plus mult} 2} 2 1` which errors, since `mult` is a function taking 2
params and `mult + 2` is not defined.
