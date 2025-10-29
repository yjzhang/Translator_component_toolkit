from . import translator_query, node_normalizer

# ARAGORN:

ARAGORN_URL = 'https://aragorn.test.transltr.io/aragorn/'

def aragorn_pathfinder(input_node1_id:str, input_node2_id:str):
    """
    ARAGORN docs: https://aragorn.test.transltr.io/aragorn/docs

    Params
    ------
    input_node1_id : str
        CURIE id for the first input node.
    input_node2_id : str
        CURIE id for the second input node.

    """
    # TODO
