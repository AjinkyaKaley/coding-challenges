import logging
import argparse
import sys
from enum import Enum

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class JSON_CONSTANTS(str, Enum):
    COMMA = ',',
    LEFT_BRACKET = "{",
    RIGHT_BRACKET = "}"
    LEFT_SQUARE_BRACKET = "["
    RIGHT_SQUARE_BRACKET = "]"
    COLON = ":"
    STRING = "STRING"
    BOOL = "BOOL"
    TRUE = "true"
    FALSE = "false"
    NULL = "null"

class TokenType:
    def __init__(self, _type: str, value: str):
        self.type = _type,
        self.value = value
    
    def __str__(self):
        return self.value
    
def lex(s:str):
    tokens = []
    i = 0

    while i < len(s):
        if s[i] == JSON_CONSTANTS.LEFT_BRACKET.value:
            tokens.append(s[i])
            i+=1
        elif s[i] == JSON_CONSTANTS.LEFT_SQUARE_BRACKET.value:
            tokens.append(s[i])
            i+=1
        elif s[i] == JSON_CONSTANTS.RIGHT_SQUARE_BRACKET.value:
            tokens.append(s[i])
            i+=1
        elif s[i] == JSON_CONSTANTS.RIGHT_BRACKET.value:
            tokens.append(s[i])
            i+=1
        elif s[i] == JSON_CONSTANTS.COMMA.value:
            tokens.append(s[i])
            i+=1
        elif s[i] == JSON_CONSTANTS.COLON.value:
            tokens.append(s[i])
            i+=1
        elif s[i] == '"':
            i+=1
            token = ""
            while i < len(s) and str(s[i]) != '"':
                token += s[i]
                i+=1
            i+=1
            tokens.append(token)
        elif s[i] in (str(i) for i in range(10)):
            token = ""
            while i < len(s) and s[i] in (str(i) for i in range(10)):
                token += s[i]
                i+=1
            tokens.append(token)
        elif (i+4) < len(s) and s[i:i+4] == JSON_CONSTANTS.TRUE.value:
            tokens.append(s[i:i+4])
            i += 4
        elif (i+5) < len(s) and s[i:i+5] == JSON_CONSTANTS.FALSE.value:
            tokens.append(s[i:i+5])
            i += 5
        elif (i+4) < len(s) and s[i:i+4] == JSON_CONSTANTS.NULL.value:
            tokens.append(s[i:i+4])
            i += 4
        elif s[i].isspace():
            i += 1
        elif s[i] == '/^$/':    # new line
            i+=1
        else:
            logger.info(f"Failed at lexical analyser, index {i}, { s[i]}")
            return sys.exit(1)

    return tokens

def parse_object(tokens):
    token = tokens[0]
    json_object = {}

    # right brace for test cases like {}
    if token == JSON_CONSTANTS.RIGHT_BRACKET.value:
        return json_object, tokens[1:]

    while True:
        json_key = tokens[0]                 # first string
        if  type(json_key) is not str:
            logger.info(f"Invalid char {json_key} expecting string data type for key wrapped in double quotes")
            return sys.exit(1)
        
        if json_key in "}]":
            logger.info(f"Invalid char {json_key} expecting string data type for key, but got closing brackets")
            return sys.exit(1)
        
        tokens = tokens[1:]                 # colon delimiter
        if tokens[0] != JSON_CONSTANTS.COLON.value:
            logger.info("Invalid char, expecting COLON :, after key")
            return sys.exit(1)
        
        json_val, tokens = parse(tokens[1:])    # value after colon, could be string, number, array, null, or object
        json_object[json_key] = json_val        # create new object

        token = tokens[0]                        # token has to be "," or closing right brace
        if token == JSON_CONSTANTS.RIGHT_BRACKET.value:
            return json_object, tokens[1:]
        if token != JSON_CONSTANTS.COMMA.value:
            logger.info("Invalid char, expecting Comma")
            return sys.exit(1)                  # comma not found
        
        
        tokens = tokens[1:]                     # comma after key value 

    return sys.exit(1)                          # ending brace is not found   
      
def parse_array(tokens, i=0):
    json_array = []
    token = tokens[0]
    if token == JSON_CONSTANTS.RIGHT_SQUARE_BRACKET.value:
        return json_array, tokens[1:]
    
    while True:
        json, tokens = parse(tokens)
        json_array.append(json)

        token = tokens[0]
        if token == JSON_CONSTANTS.RIGHT_SQUARE_BRACKET.value:
            return json_array, tokens[1:]
        elif token != JSON_CONSTANTS.COMMA.value:
            logger.info("Invalid char, expecting Comma")
            return sys.exit(1)
        
        tokens = tokens[1:]
    
def parse(tokens):
    if not tokens:
        logger.info("No tokens")
        return sys.exit(1)
    token = tokens[0]
    if token == JSON_CONSTANTS.LEFT_BRACKET.value:
        return parse_object(tokens[1:])
    elif token == JSON_CONSTANTS.LEFT_SQUARE_BRACKET.value:
        return parse_array(tokens[1:])
    else:
        return token, tokens[1:]
    
if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="json parser")
    arg_parser.add_argument("file_name")
    arg_parser.add_argument("-d", "--debug", action='store_true')
    args = arg_parser.parse_args()
    file_path = args.file_name
    debug_mode = args.debug
    if debug_mode:
        logger.setLevel(logging.DEBUG)

    with open(file_path, "r") as f:
        content = f.read()
        tokens = lex(content)
        parse(tokens)