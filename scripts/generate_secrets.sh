STORAGE_ENCRYPTION_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
JWT_SIGNING_KEY=$(openssl rand -hex 32)

# Verify they are set
echo "STORAGE_ENCRYPTION_KEY=$STORAGE_ENCRYPTION_KEY"
echo "JWT_SIGNING_KEY=$JWT_SIGNING_KEY"