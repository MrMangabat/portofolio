from .node_graph_state import GraphState

def normalize_text(text: str) -> str:
    return text.lower().strip()

def validate_words(do_not_use_words: list[str], component_value: str) -> str:
    component_value_normalized = normalize_text(component_value)
    found_words = [word for word in do_not_use_words if normalize_text(word) in component_value_normalized]
    if found_words:
        raise ValueError(f"Found: {', '.join(found_words)}")
    
    return component_value

def invalid_sentences(sentences: list[str], context: str) -> str:
    context_normalized = normalize_text(context)
    found_sentences = [sentence for sentence in sentences if normalize_text(sentence) in context_normalized]
    if found_sentences:
        raise ValueError(f"Found: {', '.join(found_sentences)}")
    
    return context

def check_generation_secondary(state: GraphState) -> GraphState:
    # State
    messages = state['messages']
    iterations = state['iterations']
    error = state['error']
    generation = state['generation']
    no_go_words = state['words_to_avoid']  # Get the list of words not to use
    no_go_sentences = state['sentences_to_avoid']  # Get the list of sentences not to use
    
    print("---------------- CHECK SECONDARY ----------------")

    generation_components = {
        "company_name": generation.company_name,
        "introduction": generation.introduction,
        "job_title": generation.job_title,
        "motivation": generation.motivation,
        "skills": generation.skills,
        "continued_learning": generation.continued_learning,
        "thank_you": generation.thank_you
    }

    all_errors = []
    for component_name, component_value in generation_components.items():
        component_errors = []
        
        ############################# WORDS TO AVOID #############################
        try:
            validate_words(no_go_words, component_value)
        except ValueError as ve:
            print(f"Invalid words in: {component_name}: {ve}")
            component_errors.append(f"Invalid words: {ve}")
            # print("INVALID WORDS: ", component_errors)

        ############################# INVALID SENTENCES #############################
        try:
            invalid_sentences(no_go_sentences, component_value)
        except ValueError as ve:
            print(f"Invalid sentences in: {component_name}: {ve}")
            component_errors.append(f"Invalid sentences: {ve}")
            # print("INVALID SENTENCES: ", component_errors)

        if component_errors:
            all_errors.extend(component_errors)
        else:
            setattr(generation, component_name, component_value)

    if all_errors:
        print("--- APPLICATION ERRORS ---")
        error_message = [(
            "user", f"Errors: {all_errors}. Review and reflect these errors and prior attempts to solve the issue. #1 state what you think went wrong and #2 find other words or sentenes without changing the context. Return full solution. Use the output structure with company_name, job_title, introduction, motivation, skills, education, continued_learning, thank_you.")]
        messages = error_message
        error = "yes"
    else:
        print("--- NO APPLICATION ERRORS ---")
        error = "no"
    
    print("Final all_errors: ", all_errors)
    
    return {
        "generation": generation,
        "messages": messages,
        "iterations": iterations,
        "error": error
    }
