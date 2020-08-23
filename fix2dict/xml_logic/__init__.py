"""
XML-parsing logic for generic FIX Repository data. Several "flavors" of FIX
Repository are supported:

- FIX Basic,
- FIX Intermediate,
- FIX Unified,
- FIX Orchestra.

These are all similar enough to one another that we can reuse the same
parsing logic for everything. The parsing process it thus "fuzzy", i.e. it
accepts quite a lot more data than technically allowed by each standard in
attempt to simplify the process.
"""

from .elem_abbreviation import (
    xml_to_abbreviations,
    xml_to_abbreviation,
)  # NOQA
from .elem_category import xml_to_categories, xml_to_category  # NOQA
from .elem_component import (  # NOQA
    xml_to_components,  # NOQA
    xml_to_component,  # NOQA
    embed_msg_contents_into_component,  # NOQA
)
from .elem_datatype import xml_to_datatypes, xml_to_datatype  # NOQA
from .elem_enum import xml_to_enums, xml_to_enum  # NOQA
from .elem_field import (
    xml_to_fields,
    xml_to_field,
    embed_enums_into_field,
)  # NOQA
from .elem_message import (  # NOQA
    xml_to_messages,  # NOQA
    xml_to_message,  # NOQA
    embed_msg_contents_into_message,  # NOQA
)
from .elem_phrase import (  # NOQA
    xml_to_doc_definition,  # NOQA
    xml_to_docs_definitions,  # NOQA
    embed_docs,  # NOQA
)
from .elem_msg_content import xml_to_msg_contents, xml_to_msg_content  # NOQA
from .elem_section import xml_to_sections, xml_to_section  # NOQA
