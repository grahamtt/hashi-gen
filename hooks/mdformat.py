"""Formats readme via autohooks hook."""

import subprocess
import sys
from typing import Iterable, List, Optional, Union

from autohooks.api import error, ok
from autohooks.api.git import (
    get_staged_status,
    stage_files_from_status_list,
    stash_unstaged_changes,
)
from autohooks.api.path import match
from autohooks.config import Config
from autohooks.precommit.run import ReportProgress
from autohooks.terminal import out

DEFAULT_INCLUDE = ("*.md", "*.markdown")
DEFAULT_ARGUMENTS = ()


def _check_mdformat_installed() -> None:
    try:
        import mdformat  # pylint: disable=unused-import, import-outside-toplevel # noqa: F401,E501
    except ImportError:
        raise RuntimeError(
            "Could not find mdformat. "
            "Please add mdformat to your python environment."
        ) from None


def _get_mdformat_config(config: Config) -> Config:
    return config.get("tool", "autohooks", "plugins", "mdformat")


def _ensure_iterable(value: Union[str, List[str]]) -> List[str]:
    if isinstance(value, str):
        return [value]
    return value


def __get_include_from_config(config: Optional[Config]) -> Iterable[str]:
    if not config:
        return DEFAULT_INCLUDE

    mdformat_config = _get_mdformat_config(config)
    include = _ensure_iterable(mdformat_config.get_value("include", DEFAULT_INCLUDE))

    return include


def _get_mdformat_arguments(config: Optional[Config]) -> Iterable[str]:
    if not config:
        return DEFAULT_ARGUMENTS

    mdformat_config = _get_mdformat_config(config)
    arguments = _ensure_iterable(
        mdformat_config.get_value("arguments", DEFAULT_ARGUMENTS)
    )

    return arguments


def precommit(
    config: Optional[Config] = None,
    report_progress: Optional[ReportProgress] = None,
    **kwargs,  # pylint: disable=unused-argument
) -> int:
    """Run `mdformat` to format readme and etc.

    Args:
        config (Optional[Config]): The full config for the project. The config for this tool will be extracted from it
            later.
        report_progress (Optional[ReportProgress]): If set, the hook will use this to send updates when work is
            finished.
        **kwargs: Not used.

    Returns:
        int: Indicates the output status of the underlying process. 0 -> success, >0 -> failure
    """
    _check_mdformat_installed()

    include = __get_include_from_config(config)
    files = [f for f in get_staged_status() if match(f.path, include)]

    if report_progress:
        report_progress.init(len(files))

    ret = 0
    arguments = ["mdformat"]
    arguments.extend(_get_mdformat_arguments(config))

    with stash_unstaged_changes(files):
        for f in files:
            try:
                args = arguments.copy()
                args.append(str(f.absolute_path()))
                subprocess.check_output(args)
                ok(f"Running mdformat on {f.path}")
                if report_progress:
                    report_progress.update()
            except subprocess.CalledProcessError as e:
                ret = e.returncode
                error(f"Running mdformat on {f.path}")
                lint_errors = e.stdout.decode(
                    encoding=sys.getdefaultencoding(), errors="replace"
                ).split("\n")
                for line in lint_errors:
                    out(line)

        stage_files_from_status_list(files)

    return ret
