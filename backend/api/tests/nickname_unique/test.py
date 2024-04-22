from hashlib import sha256

def generate_nickname(email: str) -> str:
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"
    hashed_email = sha256(string=email.encode()).hexdigest()
    hashed_email = [(chr(int(i) + 97) if i.isdigit() else i) for i in hashed_email]
    nickname = ""
    for char in hashed_email:
        if len(nickname) >= 15:
            break
        if char in consonants:
            nickname += char
            if len(nickname) < 15:
                nickname += vowels[int(ord(char)) % len(vowels)]
        elif char in vowels:
            nickname += consonants[int(ord(char)) % len(consonants)]
    while len(nickname) < 15:
        nickname += consonants[int(hashed_email[0], base=16) % len(consonants)]

    return nickname

def main():
    email = input("Enter your email: ")
    nickname = generate_nickname(email)
    print(f"Your nickname is: {nickname}")

if __name__ == "__main__":
    main()