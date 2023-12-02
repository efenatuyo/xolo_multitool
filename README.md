# xolo_multitool

this just the base

do pull requests for new module. (can change config -> `config.json` for it)


## Creating a Custom Tool

To create your own tool, follow these steps:

1. Create a new folder named after your tool in the "modules" directory.

2. Inside the tool folder, create a new file called `__init__.py`.

3. Define a class named `Run` in the `__init__.py` file. This class will serve as the entry point for your tool.

4. Implement the functionality you desire within the `Run` class. Remember to include an endpoint in your code to return back to the main code.

### Example Structure:

```plaintext
modules/
|-- your_tool_name/
|   |-- __init__.py
