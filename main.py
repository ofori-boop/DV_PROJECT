from router import Router
from cli import start_cli

def main():
    router_id = int(input("Enter Router ID (e.g., 10, 20): "))
    router = Router(router_id)
    start_cli(router)

if __name__ == "__main__":
    main()
