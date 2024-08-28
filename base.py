ascii_dict = {
    1: '\x01', 2: '\x02', 3: '\x03', 4: '\x04', 5: '\x05', 6: '\x06', 7: '\x07', 8: '\x08',
    9: '\t', 10: '\n', 11: '\x0b', 12: '\x0c', 13: '\r', 14: '\x0e', 15: '\x0f', 16: '\x10',
    17: '\x11', 18: '\x12', 19: '\x13', 20: '\x14', 21: '\x15', 22: '\x16', 23: '\x17', 24: '\x18',
    25: '\x19', 26: '\x1a', 27: '\x1b', 28: '\x1c', 29: '\x1d', 30: '\x1e', 31: '\x1f', 32: ' ',
    33: '!', 34: '"', 35: '#', 36: '$', 37: '%', 38: '&', 39: "'", 40: '(', 41: ')', 42: '*',
    43: '+', 44: ',', 45: '-', 46: '.', 47: '/', 48: '0', 49: '1', 50: '2', 51: '3', 52: '4',
    53: '5', 54: '6', 55: '7', 56: '8', 57: '9', 58: ':', 59: ';', 60: '<', 61: '=', 62: '>',
    63: '?', 64: '@', 65: 'A', 66: 'B', 67: 'C', 68: 'D', 69: 'E', 70: 'F', 71: 'G', 72: 'H',
    73: 'I', 74: 'J', 75: 'K', 76: 'L', 77: 'M', 78: 'N', 79: 'O', 80: 'P', 81: 'Q', 82: 'R',
    83: 'S', 84: 'T', 85: 'U', 86: 'V', 87: 'W', 88: 'X', 89: 'Y', 90: 'Z', 91: '[', 92: '\\',
    93: ']', 94: '^', 95: '_', 96: '`', 97: 'a', 98: 'b', 99: 'c', 100: 'd', 101: 'e', 102: 'f',
    103: 'g', 104: 'h', 105: 'i', 106: 'j', 107: 'k', 108: 'l', 109: 'm', 110: 'n', 111: 'o',
    112: 'p', 113: 'q', 114: 'r', 115: 's', 116: 't', 117: 'u', 118: 'v', 119: 'w', 120: 'x',
    121: 'y', 122: 'z', 123: '{', 124: '|', 125: '}', 126: '~', 127: '\x7f'
}

base64_dict = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H',
    8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P',
    16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X',
    24: 'Y', 25: 'Z', 26: 'a', 27: 'b', 28: 'c', 29: 'd', 30: 'e', 31: 'f',
    32: 'g', 33: 'h', 34: 'i', 35: 'j', 36: 'k', 37: 'l', 38: 'm', 39: 'n',
    40: 'o', 41: 'p', 42: 'q', 43: 'r', 44: 's', 45: 't', 46: 'u', 47: 'v',
    48: 'w', 49: 'x', 50: 'y', 51: 'z', 52: '0', 53: '1', 54: '2', 55: '3',
    56: '4', 57: '5', 58: '6', 59: '7', 60: '8', 61: '9', 62: '+', 63: '/'
}

reverse_base64_dict = {v: k for k, v in base64_dict.items()}
reverse_ascii_dict = {v: k for k, v in ascii_dict.items()}

def ascii_convert(input_string):
    ascii_values = []
    for char in input_string:
        if char in reverse_ascii_dict:
            ascii_values.append(reverse_ascii_dict[char])
    return ascii_values

def dec2bin(number):
    binary = ""
    while number > 0:
        binary = str(number % 2) + binary
        number = number // 2
    return binary.zfill(8)

def split_binary(binary_string):
    parts = []
    for i in range(0, len(binary_string), 6):
        part = binary_string[i:i+6]
        if len(part) < 6:
            part = part.ljust(6, '0')
        parts.append(part)
    return parts

def binary_to_decimal(binary_str):
    decimal = 0
    power = 0
    for digit in reversed(binary_str):
        if digit == '1':
            decimal += 2 ** power
        power += 1
    return decimal

def base64_convert(decimal_parts):
    base64_string = ""
    for decimal in decimal_parts:
        base64_string += base64_dict[decimal]
    return base64_string

def decode_base64(base64_string):
    base64_string = base64_string.rstrip('=')
    binary_string = ""
    
    for char in base64_string:
        decimal = reverse_base64_dict[char]
        binary_string += dec2bin(decimal)[2:]  # Skip the first 2 bits as they are padding in base64 binary representation
    
    ascii_chars = []
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        if len(byte) == 8:
            ascii_chars.append(chr(int(byte, 2)))
    
    return "".join(ascii_chars)

def encode_string(input_string):
    ascii_values = ascii_convert(input_string)

    binary_values = []
    for value in ascii_values:
        binary_values.append(dec2bin(value))

    binarystring = ""
    for binary in binary_values:
        binarystring += binary

    binary_parts = split_binary(binarystring)

    decimal_parts = []
    for part in binary_parts:
        decimal_parts.append(binary_to_decimal(part))

    base64_string = base64_convert(decimal_parts)

    padding_needed = len(input_string) % 3
    if padding_needed > 0:
        padding = '=' * (3 - padding_needed)
        base64_string += padding

    return base64_string

choice = input("Would you like to encode or decode? (e/d): ").strip().lower()
if choice == 'e':
    input_string = input("Enter the string to encode: ")
    encoded_string = encode_string(input_string)
    print(f"Encoded string: {encoded_string}")
elif choice == 'd':
    input_string = input("Enter the Base64 string to decode: ")
    decoded_string = decode_base64(input_string)
    print(f"Decoded string: {decoded_string}")
else:
    print("Invalid choice. Please enter 'e' to encode or 'd' to decode.")
