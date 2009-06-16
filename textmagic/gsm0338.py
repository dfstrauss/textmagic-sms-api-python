"""
GSM 03.38 character set mapping to Unicode is specified here:
 http://unicode.org/Public/MAPPINGS/ETSI/GSM0338.TXT
This code was translated from the C++ snippet at:
 http://stackoverflow.com/questions/27599/reliable-sms-unicode-gsm-encoding-in-php
contributed by Magnus Westin:
 http://stackoverflow.com/users/2957/magnus-westin

"""

UCS2_TO_GSM_LOOKUP_TABLE_SIZE   = 0x100
NON_GSM                         = 0x80
UCS2_GCL_RANGE                  = 24
UCS2_GREEK_CAPITAL_LETTER_ALPHA = 0x0391
EXTEND                          = 0x001B
# note that the ` character is mapped to ' so that all characters that can be typed on
# a standard north american keyboard can be converted to the GSM default character set
ucs2_to_gsm = [
# +0x0        +0x1        +0x2        +0x3        +0x4        +0x5        +0x6        +0x7
  NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,  # 0x00
  NON_GSM,    NON_GSM,    0x0a,       NON_GSM,    NON_GSM,    0x0d,       NON_GSM,    NON_GSM,  # 0x08
  NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,  # 0x10
  NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,  # 0x18
  0x20,       0x21,       0x22,       0x23,       0x02,       0x25,       0x26,       0x27,     # 0x20
  0x28,       0x29,       0x2a,       0x2b,       0x2c,       0x2d,       0x2e,       0x2f,     # 0x28
  0x30,       0x31,       0x32,       0x33,       0x34,       0x35,       0x36,       0x37,     # 0x30
  0x38,       0x39,       0x3a,       0x3b,       0x3c,       0x3d,       0x3e,       0x3f,     # 0x38
  0x00,       0x41,       0x42,       0x43,       0x44,       0x45,       0x46,       0x47,     # 0x40
  0x48,       0x49,       0x4a,       0x4b,       0x4c,       0x4d,       0x4e,       0x4f,     # 0x48
  0x50,       0x51,       0x52,       0x53,       0x54,       0x55,       0x56,       0x57,     # 0x50
  0x58,       0x59,       0x5a,       EXTEND,     EXTEND,     EXTEND,     EXTEND,     0x11,     # 0x58
  0x27,       0x61,       0x62,       0x63,       0x64,       0x65,       0x66,       0x67,     # 0x60
  0x68,       0x69,       0x6a,       0x6b,       0x6c,       0x6d,       0x6e,       0x6f,     # 0x68
  0x70,       0x71,       0x72,       0x73,       0x74,       0x75,       0x76,       0x77,     # 0x70
  0x78,       0x79,       0x7a,       EXTEND,     EXTEND,     EXTEND,     EXTEND,     NON_GSM,  # 0x78
  NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,  # 0x80
  NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,  # 0x88
  NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,  # 0x90
  NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,  # 0x98
  NON_GSM,    0x40,       NON_GSM,    0x01,       0x24,       0x03,       NON_GSM,    0x5f,     # 0xA0
  NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,  # 0xA8
  NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,  # 0xB0
  NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    0x60,     # 0xB8
  NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    0x5b,       0x0e,       0x1c,       0x09,     # 0xC0
  NON_GSM,    0x1f,       NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    0x60,     # 0xC8
  NON_GSM,    0x5d,       NON_GSM,    NON_GSM,    NON_GSM,    NON_GSM,    0x5c,       NON_GSM,  # 0xD0
  0x0b,       NON_GSM,    NON_GSM,    NON_GSM,    0x5e,       NON_GSM,    NON_GSM,    0x1e,     # 0xD8
  0x7f,       NON_GSM,    NON_GSM,    NON_GSM,    0x7b,       0x0f,       0x1d,       NON_GSM,  # 0xE0
  0x04,       0x05,       NON_GSM,    NON_GSM,    0x07,       NON_GSM,    NON_GSM,    NON_GSM,  # 0xE8
  NON_GSM,    0x7d,       0x08,       NON_GSM,    NON_GSM,    NON_GSM,    0x7c,       NON_GSM,  # 0xF0
  0x0c,       0x06,       NON_GSM,    NON_GSM,    0x7e,       NON_GSM,    NON_GSM,    NON_GSM   # 0xF8
]

ucs2_gcl_to_gsm = [
  0x41,  # Alpha A
  0x42,  # Beta B
  0x13,  # Gamma
  0x10,  # Delta
  0x45,  # Epsilon E
  0x5A,  # Zeta Z
  0x48,  # Eta H
  0x19,  # Theta
  0x49,  # Iota I
  0x4B,  # Kappa K
  0x14,  # Lambda
  0x4D,  # Mu M
  0x4E,  # Nu N
  0x1A,  # Xi
  0x4F,  # Omicron O
  0x16,  # Pi
  0x50,  # Rho P
  NON_GSM,
  0x18,  # Sigma
  0x54,  # Tau T
  0x59,  # Upsilon Y
  0x12,  # Phi
  0x58,  # Chi X
  0x17,  # Psi
  0x15   # Omega
]

def not_gsm(char):
    result = True
    ordinal = ord(char)
    if(ordinal < UCS2_TO_GSM_LOOKUP_TABLE_SIZE):
        result = (ucs2_to_gsm[ordinal] == NON_GSM)
    elif((ordinal >= UCS2_GREEK_CAPITAL_LETTER_ALPHA) and
                        (ordinal <= (UCS2_GREEK_CAPITAL_LETTER_ALPHA + UCS2_GCL_RANGE))):
        result = (ucs2_gcl_to_gsm[ordinal - UCS2_GREEK_CAPITAL_LETTER_ALPHA] == NON_GSM)
    elif(ordinal == 0x20AC):  # Euro sign
        result = False;
    return result;

def is_gsm(string):
    assert isinstance(string, basestring)
    for ch in string:
        if (not_gsm(ch)):
            return False
    return True
