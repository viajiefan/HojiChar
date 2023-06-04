import logging
from typing import Iterator

import hojichar

logger = logging.getLogger(__name__)


def process_iter(
    input_iter: Iterator[str],
    filter: hojichar.Compose,
    exit_on_error: bool,
) -> Iterator[str]:
    """
    Getting an iterator of string, processing by given hojichar.Compose filter,
    and iterate processed string.

    Args:
        input_iter (Iterator[str]): Input iterator.
        filter (hojichar.Compose): Processing filter.
        exit_on_error (bool): Halt with error while processing.

    Raises:
        e: Exception raised during processing in hojichar.Compose

    Yields:
        Iterator[str]: Processed text
    """
    for line in input_iter:
        try:
            doc = filter.apply(hojichar.Document(line))
            if not doc.is_rejected:
                yield doc.text
        except Exception as e:
            if exit_on_error:
                raise e
            else:
                logger.error(f"Caught {type(e)}. Skip processing the line: `{line}`")
                continue
