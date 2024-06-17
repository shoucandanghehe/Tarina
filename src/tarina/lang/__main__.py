from argparse import ArgumentParser
from tarina.lang.schema import write_lang_schema
from tarina.lang.model import write_model
from pathlib import Path
import json

CONFIG_TEMPLATE = """\
{
  "default": "zh-CN",
  "frozen": [],
  "require": []
}
"""

CONFIG_INIT = """\
# This file is @generated by tarina.lang CLI tool
# It is not intended for manual editing.

from pathlib import Path

from tarina.lang import lang


lang.load(Path(__file__).parent)
"""


TEMPLATE_SCHEMA = """\
{
  "title": "Template",
  "description": "Template for lang items to generate schema for lang files",
  "type": "object",
  "properties": {
    "scopes": {
      "title": "Scopes",
      "description": "All scopes of lang items",
      "type": "array",
      "uniqueItems": true,
      "items": {
        "title": "Scope",
        "description": "First level of all lang items",
        "type": "object",
        "properties": {
          "scope": {
            "type": "string",
            "description": "Scope name"
          },
          "types": {
            "type": "array",
            "description": "All types of lang items",
            "uniqueItems": true,
            "items": {
              "oneOf": [
                {
                  "type": "string",
                  "description": "Value of lang item"
                },
                {
                  "type": "object",
                  "properties": {
                    "subtype": {
                      "type": "string",
                      "description": "Subtype name of lang item"
                    },
                    "types": {
                      "type": "array",
                      "description": "All subtypes of lang items",
                      "uniqueItems": true,
                      "items": {
                        "$ref": "#/properties/scopes/items/properties/types/items"
                      }
                    }
                  }
                }
              ]
            }
          }
        }
      }
    }
  }
}
"""

TEMPLATE_TEMPLATE = """\
{
  "$schema": ".template.schema.json",
  "scopes": []
}
"""

LANG_TEMPLATE_JSON = """\
{
  "$schema": ".lang.schema.json"
}
"""

LANG_TEMPLATE_YAML = """\
# $schema: .lang.schema.json

"""

def new(*_):
    i18n_dir = Path.cwd() / "i18n"
    if i18n_dir.exists():
        print("i18n directory already exists")
        return
    i18n_dir.mkdir()
    print(f"i18n directory created: {i18n_dir}")


def init(*_):
    root = Path.cwd()
    config_file = root / ".config.json"
    init_file = root / "__init__.py"
    template_file = root / ".template.json"
    template_schema = root / ".template.schema.json"

    with config_file.open("w+") as f:
        f.write(CONFIG_TEMPLATE)

    with init_file.open("w+") as f:
        f.write(CONFIG_INIT)

    with template_file.open("w+") as f:
        f.write(TEMPLATE_TEMPLATE)

    with template_schema.open("w+") as f:
        f.write(TEMPLATE_SCHEMA)

    print(
        f"""\
files created:
- {config_file}
- {template_file}

please edit the files to fit your needs
    """
    )


def default(args):
    root = Path.cwd()
    config_file = root / ".config.json"
    if not config_file.exists():
        print("config file not found")
        return

    with config_file.open("r") as f:
        config = json.load(f)

    if args.locale:
        config["default"] = args.locale
        with config_file.open("w") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"default lang scope set to: {args.locale}")
    else:
        print(f"default lang scope: {config['default']}")


def schema(*_):
    root = Path.cwd()
    schema_file = root / ".lang.schema.json"
    created = not schema_file.exists()

    with (root / ".template.schema.json").open("w+") as f:
        f.write(TEMPLATE_SCHEMA)
    try:
        write_lang_schema(Path.cwd())
    except Exception as e:
        print(repr(e))
    else:
        print(f"schema for lang file {'created' if created else 'updated'}. Now you can create or update your lang files.")


def model(*_):
    root = Path.cwd()
    model_file = root / "model.py"
    init_file = root / "__init__.py"
    created = not model_file.exists()
    try:
        write_model(Path.cwd())
        with init_file.open("r") as f:
            lines = f.readlines()
        if lines[-1] != "from .model import Lang as Lang\n":
            with init_file.open("a") as f:
                f.write("\nfrom .model import Lang as Lang\n")
    except Exception as e:
        print(repr(e))
    else:
        print(f"model for lang file {'created' if created else 'updated'}. Now you can create or update your lang files.")



def create(args):
    root = Path.cwd()
    if args.yaml:
        lang_file = root / f"{args.name}.yaml"

        with lang_file.open("w+") as f:
            f.write(LANG_TEMPLATE_YAML)
    else:
      lang_file = root / f"{args.name}.json"

      with lang_file.open("w+") as f:
          f.write(LANG_TEMPLATE_JSON)

    print(f"lang file created: {lang_file}")


def delete(args):
    root = Path.cwd()
    lang_file = root / f"{args.name}.json"

    if lang_file.exists():
        lang_file.unlink()
        print(f"lang file deleted: {lang_file}")
    else:
        print(f"lang file not found: {lang_file}")



def main():
    parser = ArgumentParser(description="tarina-lang CLI tool")

    subparsers = parser.add_subparsers(dest="command")

    new_parser = subparsers.add_parser("new", help="create a new i18n directory")
    new_parser.set_defaults(func=new)

    init_parser = subparsers.add_parser("init", help="initialize a new lang configs")
    init_parser.set_defaults(func=init)

    default_parser = subparsers.add_parser("default", help="show or set default lang locale")
    default_parser.add_argument("locale", type=str, nargs="?", help="lang locale to set as default")
    default_parser.set_defaults(func=default)

    schema_parser = subparsers.add_parser("schema", help="generate or update lang schema and template schema")
    schema_parser.set_defaults(func=schema)

    model_parser = subparsers.add_parser("model", help="generate or update lang model")
    model_parser.set_defaults(func=model)

    create_parser = subparsers.add_parser("create", help="create a new lang file")
    create_parser.add_argument("name", type=str, help="name of the lang file")
    create_parser.add_argument("--yaml", action="store_true", help="create a yaml file instead of json")
    create_parser.set_defaults(func=create)

    delete_parser = subparsers.add_parser("delete", help="delete a lang file")
    delete_parser.add_argument("name", type=str, help="name of the lang file")
    delete_parser.set_defaults(func=delete)

    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
