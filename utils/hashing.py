import bcrypt

def hash_text(text: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(text.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_hashed_text(text: str, hashed: str) -> bool:
    return bcrypt.checkpw(text.encode('utf-8'), hashed.encode('utf-8'))

if __name__ == '__main__':
    password = "super secret password"
    hashed = hash_text(password)
    if verify_hashed_text(password, hashed):
        print("It Matches!")
    else:
        print("It Does not Match :(")