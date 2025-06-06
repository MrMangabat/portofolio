from ...cover_letter.graph_nodes.node_graph_state import GraphState
from llm_agents.validation_chain import validation_context_chain
from prompt_templates.sentence_word_validation_prompt import validator_parser

def llm_validation(state: GraphState, llm_model) -> GraphState:
    messages = state['messages']
    context_iteration = state['context_iteration']
    no_go_words = state['words_to_avoid']
    no_go_sentences = state['sentences_to_avoid']
    skill = state['unique_skills']
    generation = state['generation']

    context_validation = validation_context_chain(
        llm_model=llm_model,
        skill_set=skill,
        cover_letter_generation=generation,
        some_no_go_words=no_go_words,
        some_invalid_sentences=no_go_sentences,
        messages=messages,
        parser=validator_parser
    )
    
    # Add messages
    messages = [
        ('system', f""" Attempt to correct context: \n
         {context_validation.introduction}, \n
         {context_validation.motivation}, \n
         {context_validation.skills}, \n
         {context_validation.continued_learning}, \n
         {context_validation.thank_you}""")
    ]
    
    context_iteration += 1
    print("\n")
    print("\n------ CONTEXT VALIDATION", context_iteration, "------\n")
    print("\n")

    # Return the updated state
    return {
        "generation": context_validation,
        "context_iteration": context_iteration,
        "messages": messages,
    }