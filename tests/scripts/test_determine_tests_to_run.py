import pytest

from scripts.determine_tests_to_run import (
    Import,
    get_changed_source_files,
    get_changed_test_files,
    get_import_paths,
    parse_imports,
)


@pytest.fixture
def diffed_files():
    # Used to mock `git diff HEAD <BRANCH> --name-only`
    diffed_files = [
        "README.md",
        ".dockerignore",
        "great_expectations/util.py",
        "tests/integration/test_script_runner.py",
        "tests/__init.py",
        "tests/test_fixtures/custom_pandas_dataset.py",
        "tests/datasource/conftest.py",
        "tests/datasource/test_datasource.py",
        "great_expectations/rule_based_profiler/README.md",
    ]
    return diffed_files


@pytest.fixture
def parsed_imports():
    # Used to mock the result of converting AST import notes into an intermediary format
    filename = "great_expectations/my_fake_source_file.py"
    parsed = [
        Import(source=filename, module=[], name=["configparser"], alias=None),
        Import(source=filename, module=[], name=["copy"], alias=None),
        Import(source=filename, module=[], name=["datetime"], alias=None),
        Import(source=filename, module=[], name=["errno"], alias=None),
        Import(source=filename, module=[], name=["itertools"], alias=None),
        Import(source=filename, module=[], name=["json"], alias=None),
        Import(source=filename, module=[], name=["logging"], alias=None),
        Import(source=filename, module=[], name=["os"], alias=None),
        Import(source=filename, module=[], name=["shutil"], alias=None),
        Import(source=filename, module=[], name=["sys"], alias=None),
        Import(source=filename, module=[], name=["traceback"], alias=None),
        Import(source=filename, module=[], name=["uuid"], alias=None),
        Import(source=filename, module=[], name=["warnings"], alias=None),
        Import(source=filename, module=[], name=["webbrowser"], alias=None),
        Import(
            source=filename, module=["collections"], name=["OrderedDict"], alias=None
        ),
        Import(source=filename, module=["typing"], name=["Any"], alias=None),
        Import(source=filename, module=["typing"], name=["Callable"], alias=None),
        Import(source=filename, module=["typing"], name=["Dict"], alias=None),
        Import(source=filename, module=["typing"], name=["List"], alias=None),
        Import(source=filename, module=["typing"], name=["Optional"], alias=None),
        Import(source=filename, module=["typing"], name=["Union"], alias=None),
        Import(source=filename, module=["typing"], name=["cast"], alias=None),
        Import(source=filename, module=[], name=["requests"], alias=None),
        Import(
            source=filename, module=["dateutil", "parser"], name=["parse"], alias=None
        ),
        Import(source=filename, module=["ruamel", "yaml"], name=["YAML"], alias=None),
        Import(
            source=filename, module=["ruamel", "yaml"], name=["YAMLError"], alias=None
        ),
        Import(
            source=filename,
            module=["ruamel", "yaml", "comments"],
            name=["CommentedMap"],
            alias=None,
        ),
        Import(
            source=filename,
            module=["ruamel", "yaml", "constructor"],
            name=["DuplicateKeyError"],
            alias=None,
        ),
        Import(
            source=filename,
            module=["great_expectations", "checkpoint"],
            name=["Checkpoint"],
            alias=None,
        ),
        Import(
            source=filename,
            module=["great_expectations", "checkpoint"],
            name=["LegacyCheckpoint"],
            alias=None,
        ),
        Import(
            source=filename,
            module=["great_expectations", "checkpoint"],
            name=["SimpleCheckpoint"],
            alias=None,
        ),
        Import(
            source=filename,
            module=["great_expectations", "checkpoint", "types", "checkpoint_result"],
            name=["CheckpointResult"],
            alias=None,
        ),
        Import(
            source=filename,
            module=["great_expectations", "core", "batch"],
            name=["Batch"],
            alias=None,
        ),
        Import(
            source=filename,
            module=["great_expectations", "core", "batch"],
            name=["BatchRequest"],
            alias=None,
        ),
        Import(
            source=filename,
            module=["great_expectations", "core", "batch"],
            name=["IDDict"],
            alias=None,
        ),
        Import(
            source=filename,
            module=["great_expectations", "core", "batch"],
            name=["RuntimeBatchRequest"],
            alias=None,
        ),
        Import(
            source=filename,
            module=["great_expectations", "core", "batch"],
            name=["get_batch_request_dict"],
            alias=None,
        ),
        Import(
            source=filename,
            module=["great_expectations", "core", "batch"],
            name=["get_batch_request_from_acceptable_arguments"],
            alias=None,
        ),
        Import(
            source=filename,
            module=["great_expectations", "core", "expectation_suite"],
            name=["ExpectationSuite"],
            alias=None,
        ),
        Import(
            source=filename,
            module=["great_expectations", "core", "expectation_validation_result"],
            name=["get_metric_kwargs_id"],
            alias=None,
        ),
        Import(
            source=filename,
            module=["great_expectations", "core", "id_dict"],
            name=["BatchKwargs"],
            alias=None,
        ),
        Import(
            source=filename,
            module=["great_expectations", "core", "metric"],
            name=["ValidationMetricIdentifier"],
            alias=None,
        ),
        Import(
            source=filename,
            module=["great_expectations", "core", "run_identifier"],
            name=["RunIdentifier"],
            alias=None,
        ),
        Import(
            source=filename,
            module=["great_expectations"],
            name=["DataContext"],
            alias=None,
        ),
        Import(
            source=filename,
            module=["great_expectations"],
            name=["exceptions"],
            alias="ge_exceptions",
        ),
    ]
    return parsed


def test_get_changed_source_files(diffed_files):
    res = get_changed_source_files(files=diffed_files, source_path="great_expectations")
    assert res == ["great_expectations/util.py"]


def test_get_changed_test_files(diffed_files):
    res = get_changed_test_files(files=diffed_files, tests_path="tests")
    assert res == [
        "tests/integration/test_script_runner.py",
        "tests/datasource/test_datasource.py",
    ]


def test_parse_imports(tmpdir, parsed_imports):
    temp_file = tmpdir.mkdir("tmp").join("ge_imports.py")
    import_statements = """
import configparser
import copy
import datetime
import errno
import itertools
import json
import logging
import os
import shutil
import sys
import traceback
import uuid
import warnings
import webbrowser
from collections import OrderedDict
from typing import Any, Callable, Dict, List, Optional, Union, cast

import requests
from dateutil.parser import parse
from ruamel.yaml import YAML, YAMLError
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.constructor import DuplicateKeyError

from great_expectations.checkpoint import Checkpoint, LegacyCheckpoint, SimpleCheckpoint
from great_expectations.checkpoint.types.checkpoint_result import CheckpointResult
from great_expectations.core.batch import (
    Batch,
    BatchRequest,
    IDDict,
    RuntimeBatchRequest,
    get_batch_request_dict,
    get_batch_request_from_acceptable_arguments,
)
from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.core.expectation_validation_result import get_metric_kwargs_id
from great_expectations.core.id_dict import BatchKwargs
from great_expectations.core.metric import ValidationMetricIdentifier
from great_expectations.core.run_identifier import RunIdentifier
from great_expectations import DataContext
from great_expectations import exceptions as ge_exceptions
    """
    temp_file.write(import_statements)

    expected_imports = parsed_imports
    actual_imports = parse_imports(temp_file)

    assert len(actual_imports) == len(parsed_imports)
    for actual, expected in zip(actual_imports, expected_imports):
        assert (
            actual.module == expected.module
            and actual.name == expected.name
            and actual.alias == expected.alias
        )


def test_get_import_paths(parsed_imports):
    paths = get_import_paths(parsed_imports)
    assert paths == [
        "great_expectations/checkpoint/checkpoint.py",
        "great_expectations/checkpoint/util.py",
        "great_expectations/checkpoint/actions.py",
        "great_expectations/checkpoint/__init__.py",
        "great_expectations/checkpoint/configurator.py",
        "great_expectations/checkpoint/types/__init__.py",
        "great_expectations/checkpoint/types/checkpoint_result.py",
        "great_expectations/checkpoint/checkpoint.py",
        "great_expectations/checkpoint/util.py",
        "great_expectations/checkpoint/actions.py",
        "great_expectations/checkpoint/__init__.py",
        "great_expectations/checkpoint/configurator.py",
        "great_expectations/checkpoint/types/__init__.py",
        "great_expectations/checkpoint/types/checkpoint_result.py",
        "great_expectations/checkpoint/checkpoint.py",
        "great_expectations/checkpoint/util.py",
        "great_expectations/checkpoint/actions.py",
        "great_expectations/checkpoint/__init__.py",
        "great_expectations/checkpoint/configurator.py",
        "great_expectations/checkpoint/types/__init__.py",
        "great_expectations/checkpoint/types/checkpoint_result.py",
        "great_expectations/checkpoint/types/checkpoint_result.py",
        "great_expectations/core/batch.py",
        "great_expectations/core/batch.py",
        "great_expectations/core/batch.py",
        "great_expectations/core/batch.py",
        "great_expectations/core/batch.py",
        "great_expectations/core/batch.py",
        "great_expectations/core/expectation_suite.py",
        "great_expectations/core/expectation_validation_result.py",
        "great_expectations/core/id_dict.py",
        "great_expectations/core/metric.py",
        "great_expectations/core/run_identifier.py",
        "great_expectations/data_context/data_context.py",
        "great_expectations/exceptions/exceptions.py",
    ]