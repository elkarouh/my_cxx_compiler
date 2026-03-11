# CXX — Experimental Programming Language

> *Within C++, there is a much smaller and cleaner language struggling to get out.*
> — Bjarne Stroustrup

> *There are two ways of constructing a software design: one way is to make it so simple
> that there are obviously no deficiencies, and the other way is to make it so complicated
> that there are no obvious deficiencies. The first method is far more difficult.*
> — C.A.R. Hoare

---

CXX is an experimental programming language / transpiler to C, developed since 2012.
It is **statically typed, object-oriented, and imperative**, with the goal of being:

- **As safe as Ada** — visibility levels, constrained types, mandatory null checks
- **As performant as C** — output is clean C99, compiled with a C compiler
- **As productive as Python** — Python-style syntax, generators, RAII, docstrings

The design philosophy is to stay C-like at the low level while infusing Python idioms at
the high level — making it approachable to Python users without sacrificing performance.

---

## Table of Contents

- [Design Philosophy](#design-philosophy)
- [Visibility Levels](#visibility-levels)
- [Language Features](#language-features)
  - [Classes and Objects](#classes-and-objects)
  - [Memory Management](#memory-management)
  - [Generators and Coroutines](#generators-and-coroutines)
  - [Namespaces](#namespaces)
  - [Error Handling](#error-handling)
  - [C and C++ Interoperability](#c-and-c-interoperability)
- [Standard Library](#standard-library)
- [Roadmap / TODO](#roadmap--todo)
- [Known Bugs](#known-bugs)

---

## Design Philosophy

The most important goal when coding is to keep code from collapsing under the weight of
its own complexity. CXX addresses this by:

- **No forward declarations** — order of definitions is not significant; you can group
  definitions logically rather than in the order the compiler demands.
- **Python-style syntax** — indentation-based blocks, `for x in collection`, `yield`,
  named parameters, docstrings, default parameters.
- **Transparent C output** — the transpiler produces readable C99. You can inspect,
  debug, and profile the generated code directly.
- **Clean-C compatibility** — output is C99 and also compatible with C++ (no designated
  initialisers or compound literals in C++ mode, using `extern "C"` headers).

---

## Visibility Levels

Every class declaration is preceded by a visibility keyword. A newline must precede it.

| Keyword             | Effect                                                                 |
|---------------------|------------------------------------------------------------------------|
| `public class`      | All internals are made public in the generated `.h` file               |
| `protected class`   | Only an opaque type is exported; accessors must be defined explicitly  |
| `private class`     | The type is visible only within its own module                         |

---

## Language Features

### Classes and Objects

```python
# Static class members
class A:
    static int counter = 0

# Designated construction
myobj := new Obj(.a=1, .b=5)
# ==> Obj* myobj = DESIGNATE_NEW(Obj, .a=1, .b=5)

# Polymorphic calls use =>
shape => draw()

# If a child class has no __del__, the parent destructor is called automatically.

# Properties (getters / setters)
class Cat:
    char name[100]:
        get:
            return name
        set:
            strcpy(name, value)
```

### Memory Management

```python
# Heap allocation
a1 = new int[12]
# ==> int *a1 = malloc(12 * sizeof(int))

# 2D arrays
arr = new TYPE[ROWS][COLS]
# ==> TYPE *arr_p = calloc(ROWS*COLS, sizeof(TYPE))
#     TYPE (*arr)[COLS] = (TYPE(*)[COLS])arr_p

# RAII — automatic cleanup on scope exit
RAII volatile fp := new File(...)
# ==> File* fp __attribute__((cleanup(File_free))) = File_new()

RAII volatile fp := new double
# ==> double* fp __attribute__((cleanup(free))) = malloc(sizeof(*fp))

# Scoped allocation with 'with'
with new char[255] as buf:
    ...
# ==> for (char* buf=malloc(255), enter=1; enter; free(buf), enter=0)

# Array reshaping
b := reshape(a, 2, 5)
# ==> int (*b)[5] = (int(*)[5])a_p

# Multi-value return
int {x, y} = function(...)
# ==> volatile int* res = function(...); int x=res[0], y=res[1]
```

### Generators and Coroutines

CXX supports generator functions via `yield`. The `next` method may contain `yield`
statements; control resumes just after the yield on the next call.

```python
# Iterating a generator
for int x in gen:
    ...
# ==> while (not gen->exhausted) { int x = gen->next(); ... }

# Delegating yield
data = yield from generator()
# ==> data = generator->next()
#     if (not generator->exhausted) yield data
```

**Ground rules for generators:**
- All local variables that survive across a `yield` must be declared as instance members.
- No local variables may be declared in a function that uses labels (due to C label scoping).
- Never put two `yield` statements on the same source line.
- Use `yield None` to produce output that should be ignored by the caller.

#### Pipeline syntax (planned)

Transformers (pure functions) and filters (stateful generators) can be composed:

```python
newsource = source >> filter1 | transformer | filter2
```

### Namespaces

```python
namespace G:
    int a = 8
    ...
# ==> struct { int a; ... } G = {.a = 8}

# Anonymous namespaces are supported within named namespaces (uses anonymous structs).
```

### Error Handling

`try/except/else` translates into an idiomatic C short-circuit error chain:

```python
try:
    SSLFreeBuffer(&hashCtx)
    ReadyHash(&SSLHashSHA1, &hashCtx)
    SSLHashSHA1.update(&hashCtx, &clientRandom)
    SSLHashSHA1.update(&hashCtx, &serverRandom)
    SSLHashSHA1.final(&hashCtx, &hashOut)
except:
    whatever
else:
    finish
```

Transpiles to:

```c
if (!((err = SSLFreeBuffer(&hashCtx))                        ||
      (err = ReadyHash(&SSLHashSHA1, &hashCtx))              ||
      (err = SSLHashSHA1.update(&hashCtx, &clientRandom))    ||
      (err = SSLHashSHA1.update(&hashCtx, &serverRandom))    ||
      (err = SSLHashSHA1.final(&hashCtx, &hashOut)))) {
    finish;
fail:
    whatever;
}
```

### C and C++ Interoperability

**Using a CXX class from C++** — generate a `.hxx` file that produces a `.hpp` for
C++ consumption:

```python
public extern "C":
    #include "buf.h"

public klass mybuf : public Buf:
    mybuf(int x, int y):
        Buf::constructor(self, x, y)
    void clear():
        Buf::clear(self)
    bool append(const char* p, unsigned c):
        return Buf::append(self, p, c)
```

All generated C headers use `extern "C"`. C code is compiled to object files with a C
compiler; C++ code and `main` are compiled with a C++ compiler and linked together.

**Using a C++ class from CXX** — create a thin `extern "C"` wrapper:

```cpp
// qtklass_wrapper.h
#include "qtklass.h"
extern "C" Qtclass* Qtclass_new(int x)                { return new Qtclass(x); }
extern "C" int      Qtclass_foo(Qtclass* self, int i) { return self->foo(i); }
extern "C" void     Qtclass_del(Qtclass* self)        { delete self; }
```

---

## Standard Library

Planned modules (to be distributed in a zip, extracted as needed):

| Module                | Contents                                      |
|-----------------------|-----------------------------------------------|
| `linkedlist.cxx`      | Linked list                                   |
| `CircularBuffer.cxx`  | Circular buffer                               |
| `hek_string.cxx`      | Python-like string operations                 |
| `hek_thread.cxx`      | Threading + channel (merge with `Channel.cxx`)|
| `hek_mem.cxx`         | Memory utilities, `nullfree`, `recalloc`      |
| `heapq.cxx`           | Priority queue                                |
| `cxx_dict.cxx`        | Hash map (via uthash)                         |
| `epoll_reactor.cxx`   | Event loop / reactor                          |
| `preprocessor.h`      | Shared preprocessor macros                    |

Python-style collection wrappers are planned (`PYSTRING`, `PYLIST`, `PYDICT`) that
translate slice and iteration syntax into the appropriate C calls.

---

## Roadmap / TODO

### Transpiler

- [ ] Separate the transpiler from Makefile generation
- [ ] Implement a symbol table (for string slicing and type-aware operations)
- [ ] Populate symbol table from function parameters, including imported modules
- [ ] Refactor internals to use the `rxe` regex module
- [ ] Extract Python unittest code to a separate file
- [ ] Inline functions support
- [ ] Handle overloaded functions
- [ ] Labeled `break`
- [ ] `repeat … until` construct
- [ ] `for int i in [a:b]` → `for (int i=a; i<b; i++)`
- [ ] `for i in range(n)` → `for (int i=0; i<n; i++)`
- [ ] Replace `case::` with `case:`
- [ ] Implement PEP 531 (existential operator `?=`)
- [ ] Implement `Either` type: `Either<Exception, int>`
- [ ] Generics / templates: `List<int, 10> mylist`
- [ ] Smart pointers with reference counting
- [ ] Currying
- [ ] `delegate` objects for the `G` global struct
- [ ] User-defined literals: `1m`, `3s`, `4m_s`
- [ ] `assert a > 0, "message"` → replace `,` with `&&`
- [ ] POD struct inheritance and general struct inheritance
- [ ] `reset(self)` method pattern
- [ ] Ada-style constrained types: `int x constraint 0 < x < 9`
- [ ] Anonymous blocks: `::` introduces a `{ }` scope
- [ ] First `/* … */` comment in a file treated as module docstring
- [ ] `uint16_t` → `uint_fast16_t` (C99)
- [ ] Default parameters for virtual methods
- [ ] Default constructor generation in derived classes
- [ ] `sig in [SIGTERM, SIGINT]` → `sig==SIGTERM || sig==SIGINT`
- [ ] `clone` method
- [ ] Convert `delete[]` → `free`
- [ ] PlantUML integration
- [ ] Generator `reset` method
- [ ] `add_s` support in array macros

### Build / Tooling

- [ ] Replace Makefiles with [qo](https://github.com/andlabs/qo)
- [ ] Embed compile options and directives in source files
- [ ] Fix Makefile generation for split-main-functionality projects
- [ ] `pkg-config` support in generated Makefiles
- [ ] SWIG integration + type annotations in `.cxx` files
- [ ] Python interpreter embedding
- [ ] C++ wrapper generation (with corresponding Makefile)
- [ ] Use CMake for the standard library

### Memory Safety

- [ ] Use `nullfree` in destructors (enforce: only `NULL` pointers may be passed to
  `malloc`; only non-`NULL` pointers may be passed to `realloc`)
- [ ] Add assertions before/after every pointer dereference (annotated arrays)
- [ ] `insert` / `get_and_delete` macros and tests

### Demo Programs

- [ ] Tetris
- [ ] Pacman
- [ ] Sunfish chess engine
- [ ] TCL interpreter
- [ ] Toy search engine

---

## Known Bugs

- `__init__` declaration must currently be on a single line.
- Doc strings may not contain empty lines.
- A single quote `'` inside a `/* … */` block comment breaks parsing.
- `typedef` handling is broken (see `currying` test file).
- The constructor of a class intended to be derived from must be `public`, especially
  when the class contains virtual methods.

---

## Miscellaneous Notes

- **Numeric literals** — underscores (`1_000_000`) are stripped to plain integers.
- **String comparison** — `var == "ffff"` and `var.startswith("ffff")` both transpile
  to the appropriate `strncmp` call.
- **Advice** — use SDL for games, Qt for GUIs.
- **C++ template parsing ambiguity** — `f(a<b, c>d)` is the canonical example of why
  C++ templates are a parsing nightmare. CXX avoids this entirely.
