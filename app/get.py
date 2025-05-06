import bcrypt

password = "090807Dan4ik@".encode('utf-8')
hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

print(hashed_password.decode())
