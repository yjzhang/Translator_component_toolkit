# translator graph node
from dataclasses import dataclass

@dataclass
class TranslatorAttribute:
    """
    Class thar represents Translator node or edge attributes
    """

    attribute_type_id: str

    value: object

    value_type_id: str | None = None

    original_attribute_name: str | None = None

    value_url: str | None = None

    attribute_source: str | None = None

    description: str | None = None

    attributes: list | None = None



@dataclass
class TranslatorNode:
    """
    Class for Translator graph nodes.
    """

    curie: str
    "CURIE identifier"

    label: str | None = None
    "human-readable name for the node"

    types: list[str] | None = None
    "list of biolink types"

    # TODO: add quantifiers/qualifiers?
    # TODO: add edges too?

    synonyms: list[str] | None = None
    "list of synonymous labels"

    curie_synonyms: list[str] | None = None
    "list of synonymous CURIE ids (in the same order as synonyms)"

    attributes: list = []
    "List of node attributes (which are key-value pairs."

    # identifier is just another way to access/set the CURIE.
    @property
    def identifier(self):
        """identifier is the CURIE id for the node."""
        return self.curie

    @identifier.setter
    def identifier(self, i):
        """identifier is the CURIE id for the node."""
        self.curie = i

    @property
    def categories(self):
        return self.types



@dataclass
class TranslatorEdge:
    """
    Class that represents Translator edges.
    """

    subject: str
    "The subject is a CURIE id for a node."

    object: str
    "The obj (object) is a CURIE id for a node."

    predicate: str
    "Predicates"

    attributes: list = []
