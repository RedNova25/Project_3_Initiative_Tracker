from langchain_classic.chains.conversation.base import ConversationChain
from langchain_classic.memory import ConversationSummaryMemory, ConversationBufferWindowMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from app.models.combatant_model import CombatantModel, CharacterClass

gen_llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0.4
)

def invoke_llm(prompt):
    return gen_llm.invoke(prompt)

# answers questions about Dungeons and Dragons 5th edition exclusively
def get_gen_chat_chain() -> ConversationChain:
    llm = ChatOllama(
        model="llama3.1:8b",
        temperature=0.3
    )
    memory = ConversationSummaryMemory(llm=llm)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful chatbot for answering questions about Dungeons and Dragons 5th Edition. "
                   "You will exclusively talk about Dungeons and Dragons 5th edition, and "
                   "inform the user politely if they are not on topic, saying you can't help them. "
                   "Help them with any questions they have about the game system, and help them create "
                   "powerful characters and builds that also align with the type of character they want to make. "
                   "OUTPUT IN RAW TEXT."),
        ("user", "Conversation History: {history}, "
                 "Current Input: {input}")
    ])
    memory_chain = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt
    )
    return memory_chain

def get_make_chars_chain() -> ConversationChain:
    llm = ChatOllama(
        model="gemma3:4b",
        temperature=0.45
    )
    memory = ConversationBufferWindowMemory(k=4, memory_key="history")

    # This is clunky: Going to rewrite the prompt with a {history} variable
    # These older Memory classes need a {history} variable to store the previous messages
    memory_prompt = ChatPromptTemplate.from_messages([
        ("system", f"you are trying to create an array of JSON objects based on parsing "
                   f"Dungeons and Dragons 5th Edition characters from the user's input. "
                   f"Please inform the user if you can not create JSON objects that are compliant with the schema below. "
                   f"When creating the JSON objects, you will not have to use all of the info the user gives; Only use info relevant to filling out the JSON Schema. "
                   f"The JSON objects in the array must have these fields {{{CombatantModel.model_fields}}} "
                   f"where the CharacterClass is within these values {[c.value for c in CharacterClass]}. "
                   f"Make sure to output the full JSON object, putting in null for all values you still need from the user, "
                   f"EXCEPT for other_init_mod, which you can put as the default value (0) if the user doesn't specify. "
                   f"If other_init_mod (other initiative modifier) is not specified by the user, DO NOT ASK THEM TO PROVIDE it. "
                   f"Try to assume values before asking the user about fields in the schema they never specified. "
                   f"Only ask the user for more info IF YOU ABSOLUTELY MUST. "
                   f"IMPORTANT: When you autocorrect spelling mistakes by the user for the 'class' field, do so WITHOUT telling or asking the user. "
                   f"YOU MUST NOT ASK THEM ABOUT AUTOCORRECTING OR SPELLING MISTAKES, JUST FIX IT. "
                   f"If there are multiple characters, put them all in the same JSON block as a JSON array. "
                   f"Keep your response concise and to the point. if you want to ask the user for more info, PUT THIS QUESTION BEFORE THE JSON ARRAY BLOCK. "
                   f"DO NOT ASK THEM IF THEY WANT TO ADD ANOTHER CHARACTER. "
                   f"IMPORTANT: The final JSON array block MUST be the VERY LAST thing in the response, AFTER everything else. "
                   f"DO NOT include any text after the JSON array block."),
        ("user", "Conversation History: {history}, "
                 "Current Input: {input}")
    ])

    memory_chain = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=memory_prompt,
        input_key='input'
    )

    return memory_chain
