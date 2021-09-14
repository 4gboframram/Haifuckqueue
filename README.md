# Haifuckqueue
- A stack-based esoteric programming language that is based on the haiku (wip)

## Specifications of the language 
### General Info
- Lines must follow the following pattern 5 characters, 7 characters, 5 characters. This is the most important part.
  - A newline should be between each group of 3 lines (or stanza), and the interpreter/compiler may or may not enforce it
    

- Multiple argument input is supported. Arguments must be separated by null bytes
- All numbers and strings must be terminated on the same line. 
  
- Values on the stack must be signed and at least 2 bytes. This implementation uses 2 bytes.
- The stack size remains constant throughout the entirety of the program  
- Stack size should be adjustable easily in some way.
- THERE US NO NOOP INSTRUCTION 


### Operations
| Operations | Arguments | Effects | 
| :----: | :----:| :----:
|`.` | `Number`|Go to that line number if the top of the stack is not 0. 
|`+-*/&^o ` | `None` | Perform the corresponding operation on the top 2 items of the stack and set the third item on the stack to the result. Division is floor division.
|`~`| `None`| Change the top of the stack's value to it's binary not.
| &#x7c; | `Number` | Set tos to that `Number`
| `$` | `Number` | Print the top `Number` items on the stack as their character and pop them from the stack. NO NEWLINE.
| `d` | `Number` | Print value of `Number`th item of the stack as digits
| `c` | `Number` | Print value of `Number`th item of the stack as a character
| `s` | `Number` | Swap the value of the top of the stack with the `Number`th item on the stack
| `!` | `None` | Sets every value on the stack to 0
| `#` | `None` | Pops the top of the stack
| `)(` | `None` | Increment/Decrement the top of the stack
| `a` | `None` | Sets top of stack's value to the value of the next byte of the input
| `p` | `None` | Push a zero on top of the stack

### Strings
- {`string`} 
  - Set the top len(`string`) items on the stack to be the values of the characters of the string.
  - Has to be terminated on the same line.

    
### Varying constants based on state 
- A
    - Total byte count of sys.argv, including null bytes. Can be used in place of `Number`
- @
    - Represents the number of non-zero items on the stack. Can be used in place of a `Number`   
  
### Commandline
- This implementation uses command line arguments for config
- To see the entire usage, run `python3 main.py -h`
- File extension should be `.hfqbruh` for files
- Usage `python3 main.py [file] --args [input]`


