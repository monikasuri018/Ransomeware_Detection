from crypto_module import encrypt_file, decrypt_file


# Create a harmless test file
with open("test_file.txt", "w") as file:
    file.write("This is a test file for our ransomware protection project.")


password = "Project123"


# Encrypt the file
encrypt_file(
    "test_file.txt",
    "test_file.txt.enc",
    password
)

print("🔐 File encrypted successfully!")


# Decrypt the file
success = decrypt_file(
    "test_file.txt.enc",
    "recovered_test_file.txt",
    password
)

if success:
    print("🔓 File recovered successfully!")
else:
    print("❌ Decryption failed!")