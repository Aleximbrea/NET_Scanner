import functions

if __name__ == "__main__":
    
    # Checking if user has administrator privileges
    if not functions.is_admin():
        raise Exception('Administrator privileges missing!')