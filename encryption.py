from passlib.hash import pbkdf2_sha256
#enc_string = pbkdf2_sha256.encrypt("mypassword123",rounds=12000,salt_size=32)  #depreciated
enc_string1 = pbkdf2_sha256.hash("mypassword123",rounds=12000,salt_size=32)

print(enc_string1)

#verify raw string
print(pbkdf2_sha256.verify('mypassword123',enc_string1))
print(pbkdf2_sha256.verify('mypassword456',enc_string1))
