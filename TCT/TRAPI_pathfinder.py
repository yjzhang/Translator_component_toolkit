from .utils import select_predicates_API, rank_by_primary_infores, merge_ranking_by_number_of_infores
from . import translator_query, node_normalizer



def pathfinder(input_node1, input_node2, intermediate_categories, APInames, metaKG, API_predicates, input_node1_category=[], input_node2_category=[]):
    """
    This function is used to find paths between two input nodes with intermediate categories.
    This runs the query in two directions, starting at node1 and node2.

    --------------
    Parameters:
    input_node1 (str): The CURIE id of the first input node.
    input_node2 (str): The CURIE id of the second input node.
    intermediate_categories (list): A list of intermediate categories to be used in the path finding process.
    APInames: output of translator_query.get_translator_API_predicates()
    metaKG: output of translator_query.get_translator_API_predicates()
    API_predicates: output of translator_query.get_translator_API_predicates()
    --------------
    Returns:
    paths (DataFrame): A DataFrame containing the paths found between the two input nodes.
    result1 (dict): The result of the query for the first input node.
    result2 (dict): The result of the query for the second input node.
    result_parsed1 (DataFrame): The parsed results for the first input node.
    result_parsed2 (DataFrame): The parsed results for the second input node.
    result_ranked_by_primary_infores1 (DataFrame): The ranked results for the first input node based on primary infores.
    result_ranked_by_primary_infores2 (DataFrame): The ranked results for the second
    --------------
    Example:
    >>> paths, result1, result2, result_parsed1, result_parsed2, result_ranked_by_primary_infores1, result_ranked_by_primary_infores2 = Path_finder('NCBIGene:7477', 'NCBIGene:4869', ['biolink:Gene', 'biolink:Protein']) # Input genes are WNT7B, NPM1

    --------------
    """
    input_node1_id = input_node1
    input_node2_id = input_node2
    normalized_node_dict = node_normalizer.get_normalized_nodes([input_node1_id, input_node2_id])
    input_node1_info = normalized_node_dict[input_node1]
    print(input_node1_info)
    input_node1_list = [input_node1_id]
    if len(input_node1_category) == 0:
        input_node1_category = input_node1_info.types
    else:
        input_node1_category = list(set(input_node1_category).intersection(set(input_node1_info.types)))
        if len(input_node1_category) == 0:
            input_node1_category = input_node1_info.types

    input_node2_info = normalized_node_dict[input_node2_id]
    print(input_node2_info)
    input_node2_list = [input_node2_id]

    if len(input_node2_category) == 0:
        input_node2_category = input_node2_info.types
    else:
        input_node2_category = list(set(input_node2_category).intersection(set(input_node2_info.types)))
        if len(input_node2_category) == 0:
            input_node2_category = input_node2_info.types


    # Step 5: Select predicates and APIs based on the intermediate categories
    sele_predicates1, sele_APIs1, API_URLs1 = select_predicates_API(input_node1_category,
                                                                intermediate_categories,
                                                                metaKG, APInames)
    sele_predicates2, sele_APIs2, API_URLs2 = select_predicates_API(input_node2_category,
                                                                intermediate_categories,
                                                                metaKG, APInames)

    query_json1 = translator_query.build_query_json(input_node1_list,  # a list of identifiers for input node1
                                    intermediate_categories,  # a list of categories of the intermediate node
                                    sele_predicates1) # a list of predicates

    query_json2 = translator_query.build_query_json(input_node2_list,  # a list of identifiers for input node2
                                    intermediate_categories,  # a list of categories of the intermediate node
                                    sele_predicates2) # a list of predicates

    result1 = translator_query.parallel_api_query(query_json=query_json1,
                             selected_APIs = sele_APIs1,
                             APInames=APInames,
                             API_predicates=API_predicates,
                             max_workers=len(sele_APIs1))
    result2 = translator_query.parallel_api_query(query_json=query_json2,
                                selected_APIs = sele_APIs2,
                                APInames=APInames,
                                API_predicates=API_predicates,
                                max_workers=len(sele_APIs2))

    result_parsed1 = translator_query.parse_KG(result1)
        # Step 7: Ranking the results. This ranking method is based on the number of unique
        # primary infores. It can only be used to rank the results with one defined node.
    result_ranked_by_primary_infores1 = rank_by_primary_infores(result_parsed1, input_node1_id)   # input_node1_id is the curie id of the

    result_parsed2 = translator_query.parse_KG(result2)
    result_ranked_by_primary_infores2 = rank_by_primary_infores(result_parsed2, input_node2_id)   # input_node2_id is the curie id of the

    possible_paths = len(set(result_ranked_by_primary_infores1['output_node']).intersection(set(result_ranked_by_primary_infores2['output_node'])))
    print("Number of possible paths: ", possible_paths)

    paths = merge_ranking_by_number_of_infores(result_ranked_by_primary_infores1, result_ranked_by_primary_infores2,
                                            top_n = 30,
                                            fontsize=10,
                                            title_fontsize=12,)

    return paths, result1, result2, result_parsed1, result_parsed2, result_ranked_by_primary_infores1, result_ranked_by_primary_infores2

