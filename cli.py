from router import Router

def start_cli(router):
    print("Router CLI Commands:")
    print(" - configure_interface <interface_id> <port>")
    print(" - set_link <interface_id> <neighbor_id> <cost>")
    print(" - start_routing")
    print(" - stop_routing")
    print(" - show_routing_table")
    print(" - exit")

    while True:
        command = input(f"Router {router.router_id} > ")
        if command == "exit":
            break
        elif command.startswith("configure_interface"):
            _, iface, port = command.split()
            router.configure_interface(iface, int(port))
        elif command.startswith("set_link"):
            _, iface, neighbor_id, cost = command.split()
            router.set_link(iface, int(neighbor_id), int(cost))
        elif command == "start_routing":
            router.start_routing()
        elif command == "stop_routing":
            router.stop_routing()
        elif command == "show_routing_table":
            router.show_routing_table()
        else:
            print("Unknown command")
