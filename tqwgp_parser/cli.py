# -*- coding: utf-8 -*-
"""
    tqwgp-parser.cli
    ~~~~~~~~~~~~~~~~~~~~~
    CLI for the TQWGP parser, allowing to parse JSON, Yaml and Toml.

    This is a Work-in-Progress.

    :copyright: (c) 2021 Yoan Tournade.
"""
import os
import click
import codecs
import pprint
import yaml
import json
import toml
from .files.loaders import load_document_from_project, load_document_with_inheritance
from . import parse_quote, parse_invoices
from .constants import DOCUMENT_TYPE_INVOICE, DOCUMENT_TYPE_QUOTE

DEFAULT_DOCUMENT_TYPES_PATH = {
    "invoices.yml": DOCUMENT_TYPE_INVOICE,
    "quote.yml": DOCUMENT_TYPE_QUOTE,
}
DEFAULT_DOCUMENT_TYPES_PARSER = {
    DOCUMENT_TYPE_INVOICE: parse_invoices,
    DOCUMENT_TYPE_QUOTE: parse_quote,
}

# TODO Add native Python.
DEFAULT_FILE_FORMAT_PARSERS = {
    "yaml": {
        "open_fn": lambda path: codecs.open(path, "r", "utf-8"),
        "parser_fn": lambda content: yaml.load(content, Loader=yaml.SafeLoader),
    },
    "json": {
        "open_fn": lambda path: codecs.open(path, "r", "utf-8"),
        "parser_fn": lambda content: json.loads(content),
    },
    "toml": {
        "open_fn": lambda path: codecs.open(path, "r", "utf-8"),
        "parser_fn": lambda content: toml.loads(content),
    },
}

# CLI declaration.
@click.group()
def cli():
    pass

@cli.command()
@click.argument("project_specifier")
@click.option(
    "--file-format",
    type=click.Choice(["yaml", "json", "toml"], case_sensitive=False),
    default="yaml"
)
@click.option("-v", "--verbose", default=False, help="Verbose mode")
@click.option(
    "--projects-base-path",
    default="",
    help="The projects base path from which the project specifier refer.",
)
@click.option('--verbose', '-v', is_flag=True, help="Print more output.", default=False)
@click.option('--enable-parsing/--disable-parsing', default=True)
def show(project_specifier, file_format="yaml", projects_base_path="", verbose=False, enable_parsing=True):
    """Load and show parsed documents for the project specifier"""
    # TODO Arg to open only certain types.
    # TODO Arg to specify default_document_path?
    print("Verbose mode is {0}".format("on" if verbose else "off"))
    print(f"Searching project files in ({project_specifier})...")
    loaded_documents = []
    for default_document_path, document_type in DEFAULT_DOCUMENT_TYPES_PATH.items():
        project_path, document_path, project_name = load_document_from_project(
            project_specifier,
            default_projects_dir=projects_base_path,
            default_document_path=default_document_path,
        )
        # TODO Infer types (when full document path is specified).
        print("Loading input file ({0})...".format(document_path))
        # Use the file format parser.
        file_format_parser = DEFAULT_FILE_FORMAT_PARSERS[file_format]
        input_document = load_document_with_inheritance(
            document_path,
            open_fn=file_format_parser["open_fn"],
            parser_fn=file_format_parser["parser_fn"],
        )
        loaded_document = {
            "project_path": project_path,
            "document_path": document_path,
            "project_name": project_name,
            "document_type": document_type,
            "file_format": file_format,
            # verbose
            "document_content": input_document,
        }
        if enable_parsing:
            document_type_parser = DEFAULT_DOCUMENT_TYPES_PARSER[document_type]
            loaded_document = {
                **loaded_document,
                "parsed_document": document_type_parser(input_document),
            }
        if verbose or not enable_parsing:
            loaded_document = {
                **loaded_document,
                "document_content": input_document,
            }
        loaded_documents.append(loaded_document)

    pprint.pprint(loaded_documents)


if __name__ == "__main__":
    cli()
