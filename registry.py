
class RegistrationSystem:

    def __init__(self):
        self.registry = {}

    def add_runnable(self, name, module_obj, *metatags, **kw):
        """
        Add a class, function or other object as a tool to the registry.
        saved to the registry for later use.
        uses import statement rather than saving module obj directly
        so that the registry can be saved and loaded easily.
        scanmod can create a dict of a module's object tree.
        then a module's object tree info can be registered to the registry for use by the application.
        """
        self.registry[name] = {
            'name' : module_obj.__name__,
            'module': module_obj.__module__,
            'metatags': metatags,
            'parameters': kw,
            'doc': module_obj.__doc__
        }

    def get_runnable(self, name):
        if name in self.registry:
            return self.registry[name]
        else:
            return None

    def get_runnables(self, tags=None):
        if not tags:
            return self.registry
        else:
            runnables = {}
            for name, tool in self.registry.items():
                for tag in tags:
                    if tag in tool['metatags']:
                        runnables[name] = tool
                        break
            return runnables

    def remove_runnable(self, name):
        if name in self.registry:
            del self.registry[name]
        else:
            print("Tool not found")

    def backup_registry(self, file_path):
        """ Create a backup of the registry dict to file."""
        with open(file_path, 'w') as f:
            registry_str = str(self.registry)
            f.write(registry_str)

    def load_registry(self, file_path):
        """ Load registry from file. """
        with open(file_path, 'r') as f:
            self.registry = eval(f.read())

    def __len__(self):
        return len(self.registry)

    def __getitem__(self, key):
        # if has key,else check tags and return dict
        if key in self.registry:
            return self.registry[key]

    def __str__(self):
        return str(self.registry)

    def __repr__(self):
        return repr(self.registry)

    def __contains__(self, item):
        return item in self.registry

    def __iter__(self):
        return iter(self.registry)


# Example usage
import math

regsys = RegistrationSystem()

# Add tools to the registry
regsys.add_runnable('atan2', math.atan2, 'tangent', 'triangles', arg1='x', arg2='y')
regsys.add_runnable('log10', math.log10, 'logarithm', arg1='value1')

# Retrieve tools from the registry
tool1 = regsys.get_runnable('atan2')
tool2 = regsys.get_runnable('log10')

#ackup the registry
regsys.backup_registry('registry.json')

# remove a tool
regsys.remove_runnable('atan2')


if tool1:
    print(f"Tool 1: {tool1}")
else:
    print("Tool 1 not found in the registry")

if tool2:
    print(f"Tool 2: {tool2}")
else:
    print("Tool 2 not found in the registry")
