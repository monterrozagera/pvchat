import authentication

auth = authentication.Authentication()

# new_key = auth.generateKey()
new_key = auth.loadKey('new_key.key')

encrypted_message = auth.encryptMessage(new_key, 'simon')
print(encrypted_message)
decrypted_message = auth.decryptMessage(new_key, encrypted_message)
print("this was your message: ")
print(decrypted_message)

print('\n\n')
print('this key was used')
print(new_key)

auth.exportKey(new_key)