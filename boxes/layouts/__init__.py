import pkgutil
import inspect
import importlib
import boxes

ui_groups_by_name = {}


class UIGroup:
    def __init__(self, name, title=None, description=""):
        self.name = name
        self.title = title or name
        self.description = description
        self.generators = []
        # register
        ui_groups_by_name[name] = self

    def add(self, box):
        self.generators.append(box)
        self.generators.sort(
            key=lambda b: getattr(b, '__name__', None) or b.__class__.__name__)


ui_groups = [
    UIGroup("Layout", description="Generators that need a layout input file")
]


def getAllLayouts():
    layouts = {}
    for importer, modname, ispkg in pkgutil.walk_packages(
            path=__path__,
            prefix=__name__ + '.'):
        module = importlib.import_module(modname)
        if module.__name__.split('.')[-1].startswith("_"):
            continue
        for k, v in module.__dict__.items():
            if v is boxes.Boxes:
                continue
            if (inspect.isclass(v) and issubclass(v, boxes.Boxes) and
                    v.__name__[0] != '_'):
                layouts[modname + '.' + v.__name__] = v
    return layouts


def getAllLayoutModules():
    layouts = {}
    for importer, modname, ispkg in pkgutil.walk_packages(
            path=__path__,
            prefix=__name__ + '.',
            onerror=lambda x: None):
        module = importlib.import_module(modname)
        layouts[modname.split('.')[-1]] = module
    return layouts
