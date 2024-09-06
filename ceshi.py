import execjs

def get_ciphertext():
    with open("test.js", encoding='utf-8') as f:
        code = f.read()
        ctx = execjs.compile(code)
    ciphertext = ctx.call("query", "p1")
    return ciphertext


print(get_ciphertext())
