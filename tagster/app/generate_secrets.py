import os

secrets_dir = '.streamlit'
secrets_path = os.path.join(secrets_dir, 'secrets.toml')

# Check if the directory exists, if not - create it
if not os.path.exists(secrets_dir):
    os.makedirs(secrets_dir)

def generate_secrets_toml():
    # Define the path for the secrets.toml file
    secrets_path = '.streamlit/secrets.toml'
    
    # Open the file in write mode
    with open(secrets_path, 'w') as file:
        # Iterate over environment variables
        for key, value in os.environ.items():
            # Write each environment variable in TOML format
            file.write(f'{key} = "{value}"\n')

if __name__ == "__main__":
    generate_secrets_toml()
