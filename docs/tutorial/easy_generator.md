# Easy Generator

Generating random values, passwords, QR codes, UUIDs, API keys, and OTP codes is something you'll often need in different Python projects. The `easy_generator` module provides simple helpers that make these common generation tasks easy to use without writing the underlying logic yourself.

## A small real-world example

Imagine you're creating a small application that needs a secure password for a new account, a unique identifier for a user, and an API key for accessing a service.

```python
from py_simple import generate_password, generate_uuid, generate_api_key

password = generate_password(16, uppercase_chars=3, digit_chars=3, special_chars=3)
user_id = generate_uuid()
api_key = generate_api_key()

print(password)
print(user_id)
print(api_key)
```

Example output:

```text
gT7@qL2#xP9!mK4z
3f2504e0-4f89-11d3-9a0c-0305e82c3301
J4Yx8Qv3... 
```

## What happened?

`generate_password()` creates a randomized password containing lowercase letters, uppercase letters, digits, and special characters according to the options you provide.

`generate_slug()` converts a valid string to a URL-friendly string. 

`generate_uuid()` generates a random UUID version 4, which is useful when you need a unique identifier.

`generate_api_key()` generates a secure, URL-safe random string using Python's `secrets` module, making it suitable for API keys and access tokens.

You can also generate QR codes and OTP codes:

```python
from py_simple import generate_qr_code, generate_otp

generate_qr_code("https://example.com")

otp = generate_otp(6)
print(otp)
```

`generate_qr_code()` creates a PNG QR code in the current directory without overwriting an existing QR code file.

`generate_otp()` generates a random OTP code with a minimum length of 4 characters. You can also include letters:

```python
from py_simple import generate_otp

code = generate_otp(6, with_letters=True)
print(code)
```

Example output:

```text
a7K2p9
```

## Why use these helpers?

Instead of repeatedly writing password generation, UUID, token, QR code, or OTP logic yourself, you can simply use:

```python
password = generate_password()
user_id = generate_uuid()
api_key = generate_api_key()
otp = generate_otp(6)
```

These helpers keep common generation tasks simple, readable, and beginner-friendly while handling the underlying character selection, randomness, formatting, and file creation for you.