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

from .elem_abbreviation import xml_to_abbreviation, xml_to_abbreviations  # NOQA
from .elem_category import xml_to_categories, xml_to_category  # NOQA
from .elem_component import embed_msg_contents_into_component  # NOQA
from .elem_component import xml_to_component  # NOQA
from .elem_component import xml_to_components  # NOQA; NOQA
from .elem_datatype import xml_to_datatype, xml_to_datatypes  # NOQA
from .elem_enum import xml_to_enum, xml_to_enums  # NOQA
from .elem_field import embed_enums_into_field, xml_to_field, xml_to_fields  # NOQA
from .elem_message import embed_msg_contents_into_message  # NOQA
from .elem_message import xml_to_message  # NOQA
from .elem_message import xml_to_messages  # NOQA; NOQA
from .elem_msg_content import xml_to_msg_content, xml_to_msg_contents  # NOQA
from .elem_phrase import embed_docs  # NOQA
from .elem_phrase import xml_to_doc_definition  # NOQA
from .elem_phrase import xml_to_docs_definitions  # NOQA; NOQA
from .elem_section import xml_to_section, xml_to_sections  # NOQA
