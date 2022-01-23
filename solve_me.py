from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qsl
import pages


class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            with open(self.COMPLETED_TASKS_FILE, "r") as file:
                self.completed_items = file.readlines().strip()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def runserver(self):
        address = "127.0.0.1"
        port = 8000
        server_address = (address, port)
        httpd = HTTPServer(server_address, TasksServer)
        print(f"Started HTTP Server on http://{address}:{port}")
        httpd.serve_forever()

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "runserver":
            self.runserver()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics
$ python tasks.py runserver # Starts the tasks management server"""
        )

    def add(self, args):
        self.read_current()
        i = int(args[0])
        while i in self.current_items.keys():
            i = i + 1
        while i > int(args[0]):
            self.current_items[i] = self.current_items[i - 1]
            i = i - 1
        self.current_items[int(args[0])] = args[1]
        self.write_current()
        print(f'Added task: "{args[1]}" with priority {args[0]}')

    def done(self, args):
        self.read_current()
        item = self.current_items.pop(int(args[0]), "")
        if not item:
            print(f"Error: no incomplete item with priority {args[0]} exists.")
            return
        self.write_current()
        self.read_completed()
        self.completed_items.append(item)

        self.write_completed()
        print(f"Marked item as done.{item}")

    def delete(self, args):
        self.read_current()
        if not self.current_items.pop(int(args[0]), ""):
            print(
                f"Error: item with priority {args[0]} does not exist. Nothing deleted."
            )
            return
        self.write_current()
        print(f"Deleted item with priority {args[0]}")

    def ls(self):
        self.read_current()
        i = 1
        for key, value in self.current_items.items():
            print(f"{i}. {value} [{key}]")
            i = i + 1

    def report(self):
        self.read_current()
        print(f"Pending : {len(self.current_items)}")
        i = 1
        for key, value in self.current_items.items():
            print(f"{i}. {value} [{key}]")
            i = i + 1
        i = 1
        self.read_completed()
        print(f"\nCompleted : {len(self.completed_items)}")
        for item in self.completed_items:
            print(f"{i}. {item}")
            i = i + 1

    def render_pending_tasks(self):
        self.read_current()
        return pages.pending(self.current_items)

    def render_completed_tasks(self):
        self.read_completed()
        return pages.completed(self.completed_items)

    def render_add_task(self):
        return pages.form()

    def render_home(self):
        return pages.home()

    def render_action(self):
        return pages.action()


class TasksServer(TasksCommand, BaseHTTPRequestHandler):
    def do_GET(self):
        task_command_object = TasksCommand()
        if self.path == "/":
            content = task_command_object.render_home()
        elif self.path == "/tasks":
            content = task_command_object.render_pending_tasks()
        elif self.path == "/completed":
            content = task_command_object.render_completed_tasks()
        elif self.path.startswith("/action"):
            content = task_command_object.render_action()
            if self.path == "/action":
                pass
            else:
                try:
                    query = urlparse(self.path).query
                    value = dict(parse_qsl(query))
                    print("is in action")
                    if value["action"] == "complete":
                        self.done([value["priority"]])
                    elif value["action"] == "delete":
                        self.delete([value["priority"]])
                    else:
                        self.send_response(404)
                        self.end_headers()
                        return
                except:
                    self.send_response(404)
                    self.end_headers()
                    return
        elif self.path.startswith("/add"):
            content = task_command_object.render_add_task()
            if self.path == "/add":
                pass
            else:
                try:
                    query = urlparse(self.path).query
                    value = dict(parse_qsl(query))
                    self.add([value["priority"], value["task"]])
                except:
                    self.send_response(404)
                    self.end_headers()
                    return
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())
