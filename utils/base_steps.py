

def verify_envs(**kwargs):
    for k in kwargs.keys():
        if not kwargs.get(k):
            print(f"Variable {k} not found. Please insert in environment variables.")
            exit("Environment not found.")
    print("All environment variables found!")