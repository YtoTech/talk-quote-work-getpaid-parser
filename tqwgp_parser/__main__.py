# -*- coding: utf-8 -*-
"""
    tqwgp-parser.cli
    ~~~~~~~~~~~~~~~~~~~~~
    CLI for the TQWGP parser, allowing to parse JSON, Yaml and Toml.

    This is a Work-in-Progress.

    :copyright: (c) 2021 Yoan Tournade.
"""
import os
import sys
import os.path
import click
import codecs
import pprint
import yaml
import json
import toml
import io
from contextlib import redirect_stdout
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


def discover_and_loads_documents_from_directory(
    project_specifier,
    file_format="yaml",
    projects_base_path="",
    verbose=False,
    enable_parsing=True,
):
    loaded_documents = []
    for default_document_path, document_type in DEFAULT_DOCUMENT_TYPES_PATH.items():
        status, project_path, document_path, project_name = load_document_from_project(
            project_specifier,
            default_projects_dir=projects_base_path,
            default_document_path=default_document_path,
            throw_error=False,
        )
        if status != "ok":
            print(f"{status}: {project_path}")
            continue
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
    return loaded_documents


def discover_and_loads_documents(
    project_specifier,
    file_format="yaml",
    projects_base_path="",
    verbose=False,
    enable_parsing=True,
    recursive=False,
    debug=False,
):
    debug_ouput = ""
    debug_ouput_io = io.StringIO() if not debug else sys.stdout
    loaded_documents = []
    with redirect_stdout(debug_ouput_io):
        if recursive:
            print(
                f"Starting recursive projects discovery in {projects_base_path}:{project_specifier}..."
            )
        # Always loads from first path.
        print(f"Searching project files in {projects_base_path}:{project_specifier}...")
        loaded_documents.extend(
            discover_and_loads_documents_from_directory(
                project_specifier,
                file_format=file_format,
                projects_base_path=projects_base_path,
                verbose=verbose,
                enable_parsing=enable_parsing,
            )
        )
        if recursive:
            for root, dirs, files in os.walk(
                os.path.join(projects_base_path, project_specifier)
            ):
                for dir_name in dirs:
                    print(f"Searching project files in {root}/{dir_name}...")
                    loaded_documents.extend(
                        discover_and_loads_documents_from_directory(
                            os.path.join(root, dir_name),
                            file_format=file_format,
                            projects_base_path=None,
                            verbose=verbose,
                            enable_parsing=enable_parsing,
                        )
                    )
    debug_ouput = debug_ouput_io.getvalue() if not debug else None

    final_ouput = {"documents": loaded_documents}
    if verbose:
        final_ouput = {
            **final_ouput,
            "debug_ouput": debug_ouput,
        }
    return final_ouput


# CLI declaration.
@click.group()
def cli():
    pass


@cli.command()
@click.argument("project_specifier")
@click.option(
    "--file-format",
    type=click.Choice(["yaml", "json", "toml"], case_sensitive=False),
    default="yaml",
)
@click.option("-v", "--verbose", default=False, help="Verbose mode")
@click.option(
    "--projects-base-path",
    default="",
    help="The projects base path from which the project specifier refer.",
)
# TODO Enable recursive.
@click.option("--verbose", "-v", is_flag=True, help="Print more output.", default=False)
@click.option("--debug", is_flag=True, help="Disable stdout capturing.", default=False)
@click.option("--enable-parsing/--disable-parsing", default=True)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help="Enable recursive documents discovery (from the project specifier).",
    default=False,
)
def show(
    project_specifier,
    file_format="yaml",
    projects_base_path="",
    verbose=False,
    enable_parsing=True,
    recursive=False,
    debug=False,
):
    """Load and show parsed documents for the project specifier"""
    # TODO Arg to open only certain types.
    # TODO Arg to specify default_document_path?
    final_ouput = discover_and_loads_documents(
        project_specifier,
        file_format=file_format,
        projects_base_path=projects_base_path,
        verbose=verbose,
        enable_parsing=enable_parsing,
        recursive=recursive,
        debug=debug,
    )
    pprint.pprint(final_ouput)


@cli.command()
@click.argument("project_specifier")
@click.option(
    "--file-format",
    type=click.Choice(["yaml", "json", "toml"], case_sensitive=False),
    default="yaml",
)
@click.option("-v", "--verbose", default=False, help="Verbose mode")
@click.option(
    "--projects-base-path",
    default="",
    help="The projects base path from which the project specifier refer.",
)
@click.option("--verbose", "-v", is_flag=True, help="Print more output.", default=False)
@click.option("--debug", is_flag=True, help="Disable stdout capturing.", default=False)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help="Enable recursive documents discovery (from the project specifier).",
    default=False,
)
def stats(
    project_specifier,
    file_format="yaml",
    projects_base_path="",
    verbose=False,
    recursive=False,
    debug=False,
):
    """Load and process documents statistics for the project specifier"""
    loaded_documents = discover_and_loads_documents(
        project_specifier,
        file_format=file_format,
        projects_base_path=projects_base_path,
        verbose=verbose,
        enable_parsing=True,
        recursive=recursive,
        debug=debug,
    )
    BASE_STATS = {
        # TODO Start date, end date
        # TODO Date filter.
        "total_vat_excl": 0,
        "total_vat_incl": 0,
        "vat": 0,
        # TODO Var rate.
        "count": 0,
        "lines_count": 0,
    }
    statistics = {}

    def add_to_stats(current_stats, parsed_document):
        if not parsed_document.get("price"):
            return current_stats
        return {
            **current_stats,
            "total_vat_excl": current_stats["total_vat_excl"]
            + parsed_document["price"]["total_vat_excl"],
            "total_vat_incl": current_stats["total_vat_incl"]
            + parsed_document["price"]["total_vat_incl"],
            "vat": current_stats["vat"] + parsed_document["price"]["vat"],
            "count": current_stats["count"] + 1,
            "lines_count": current_stats["lines_count"]
            + (
                len(parsed_document.get("lines", []))
                or len(parsed_document.get("prestations", []))
            ),
        }

    for document in loaded_documents["documents"]:
        stat_key = f"{document['document_type']}s"
        if stat_key not in statistics:
            statistics[stat_key] = {
                **BASE_STATS,
            }
        if document["document_type"] == "invoice":
            for invoice in document["parsed_document"]["invoices"]:
                statistics[stat_key] = add_to_stats(statistics[stat_key], invoice)
        else:
            statistics[stat_key] = add_to_stats(
                statistics[stat_key], document["parsed_document"]
            )
    pprint.pprint(statistics)


if __name__ == "__main__":
    cli()
