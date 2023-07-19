repru = []
strg = u"\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652\u0670"
strg = u"\u202a\u202b\u202c"
for c in strg:
	code_point = ord(c)  # Unicode code point
	utf8_bytes = chr(code_point).encode('utf-8')
	utf8_representation = ''.join([f'\\x{byte:02x}' for byte in utf8_bytes])
	repru.append(utf8_representation)
print('|'.join(repru))
