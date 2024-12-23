# Command Definitions for the Custom Language

# System Commands
EXIT    = "exit"      # Exit the program
COMMENT = "//"        # Comment a line
PASS    = "pass"      # Pass a line

# Examples
# EXIT
# // This is a comment
# PASS

# Variable Handling
SET     = "set"       # Set a variable

# Examples
# SET [x] = 10

# Input and Output
OUT     = "out"       # Output a value
INP     = "inp"       # Input a value

# Examples
# SET [y] = 20
# OUT "Hello, World"
# OUT [y]
# INP str [z]

# String Manipulation
LOWER   = "lower"     # Convert string to lowercase
UPPER   = "upper"     # Convert string to uppercase
FUPPER  = "fupper"    # Capitalize first letter
LUPPER  = "lupper"    # Capitalize last letter
FLOWER  = "flower"    # Lowercase first letter
LLOWER  = "llower"    # Lowercase last letter
REVERSE = "reverse"   # Reverse the string

# Examples
# SET [string] = "lOL, tHIs Is HAha"
# LOWER [string]
# UPPER [string]
# FUPPER [string]
# LUPPER [string]
# FLOWER [string]
# LLOWER [string]
# REVERSE [string]

# Arithmetic Operations
ADD     = "add"       # Add numbers
SUB     = "sub"       # Subtract numbers
MUL     = "mul"       # Multiply numbers
DIV     = "div"       # Divide numbers

# Examples
# SET [a] = 10
# SET [b] = 30
# ADD [a] = [b] [a]
# SUB [c] = [a] [b]
# MUL [b] = [b] [c]
# DIV [c] = [b] [a]

# Functions
FUNC    = "func"      # Define a function
CALL    = "call"      # Call a function

# Math and Random
ABS     = "abs"       # Absolute value
ROUND   = "round"     # Round a float
RANDOM  = "random"    # Get a random number between two numbers

# Control Flow
LOOP    = "loop"      # Loop through a block
IF      = "if"        # Conditional check

# Timing
WAIT    = "wait"      # Wait for a specific time (in seconds)

# Type Casting
STR     = "str"       # Convert variable to string
INT     = "int"       # Convert variable to integer
FLT     = "flt"       # Convert variable to float
BOL     = "bol"       # Convert variable to boolean

# Argument Handling
ARG     = "arg"       # Get arguments from the command line

# Type Checking
ISSTR   = "isstr"     # Check if variable is a string
ISINT   = "isint"     # Check if variable is an integer
ISFLT   = "isflt"     # Check if variable is a float
ISBOL   = "isbol"     # Check if variable is a boolean
