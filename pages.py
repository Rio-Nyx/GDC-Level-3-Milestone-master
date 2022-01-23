def form():
    return """<a href="/" style="display:flex;justify-content:center;text-decoration:none;font-size:2rem">
        <div style="width:50%;background-color:#BFFFFF;text-align:center;padding:1.5rem">Home</div>
      </a>
      <h1 style="text-align:center">Add a new task </h1>
      <div style="display:flex;justify-content:center;">
      <form action="/add">
        <label for="priority">Priority :</label><br>
        <input type="number" id="priority" name="priority"><br><br>
        <label for="task">Task:</label><br>
        <input type="text" id="task" name="task"><br><br>
        <input type="submit" value="Submit" style="width:50%">
      </form>
      </div>"""


def completed(completed_items):
    content = """<a href="/" style="display:flex;justify-content:center;text-decoration:none;font-size:2rem">
        <div style="width:50%;background-color:#BFFFFF;text-align:center;padding:1.5rem">Home</div>
      </a><h1> Completed Tasks </h1>"""
    content = content + "".join(["<li>" + value + "</li>" for value in completed_items])
    content = "<ul>" + content + "</ul>"
    return content


def pending(pending_items):
    content = """<a href="/" style="display:flex;justify-content:center;text-decoration:none;font-size:2rem">
        <div style="width:50%;background-color:#BFFFFF;text-align:center;padding:1.5rem">Home</div>
      </a><h1> Incomplete Tasks </h1>"""
    content = content + "".join(
        [
            ("<li>" + str(key) + ". " + value + "</li>")
            for key, value in pending_items.items()
        ]
    )
    content = "<ul>" + content + "</ul>"
    return content


def home():
    return """<h1 style="text-align:center">TodoList</h1>
      <a href="/add" style="display:flex;justify-content:center;text-decoration:none;font-size:2rem">
        <div style="width:50%;background-color:#BFFFFF;text-align:center;padding:1.5rem">Add a new Task</div>
      </a>
      <a href="/tasks" style="display:flex;justify-content:center;text-decoration:none;font-size:2rem">
        <div style="width:50%;background-color:#E7E9EB;text-align:center;padding:1.5rem">View Pending Tasks</div>
      </a>
      <a href="/completed" style="display:flex;justify-content:center;text-decoration:none;font-size:2rem">
        <div style="width:50%;background-color:#BFFFFF;text-align:center;padding:1.5rem">View Completed Tasks</div>
      </a>
      <a href="/action" style="display:flex;justify-content:center;text-decoration:none;font-size:2rem">
        <div style="width:50%;background-color:#E7E9EB;text-align:center;padding:1.5rem">Complete or Delete Tasks</div>
      </a>"""


def action():
    return """<a href="/" style="display:flex;justify-content:center;text-decoration:none;font-size:2rem">
        <div style="width:50%;background-color:#BFFFFF;text-align:center;padding:1.5rem">Home</div>
      </a>
      <h1 style="text-align:center">Delete or Complete a task </h1>
      <div style="display:flex;justify-content:center;">
      <form action="/action">
        <label for="priority">Priority :</label><br>
        <input type="number" id="priority" name="priority"><br><br>
        <label for="action">Action:</label><br>
        <select name="action" id="action">
        <option value="complete">Complete</option>
        <option value="delete">Delete</option>
        </select>
          <br><br>
  <input type="submit" value="Submit">
      </form>
      </div>"""
