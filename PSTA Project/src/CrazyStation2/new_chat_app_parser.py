import shutil

import streamlit as st
import os
from langchain.prompts import ChatPromptTemplate
import time
import llm_service as llmService
import utils
import db_service as dbService
from pyvis.network import Network
import math
from pl1_parser_all_vers4 import PL1FileParser
import datetime
import re

# Sprint 1
# First: take prompt and scan for any file name like "Give me the dependancies for BF4000M1" folder should be scanned for BF4000M1.csv
# Second: If file was found read first 2 lines and ask LLM first question with Colum prompt
# Third: Take response and ask third question to build py script
# Forth: save scrip and execute the script automatically

# Sprint 2
# Dependency graph
# First take prompt and scan for any possible application name like "BF4000M1".
# Second run query against possible names, on first response with data stop quering and save data as csv
# Third run python script to present user with a image of dependancies including programs


# Next steps 04/11/2024
# Ask for graph
# generate graph
# for each job get a list of programs
# document the list of programs, translate all commnets
# Get chat history to work, currently all history is not being sent to the model


# Code documentation
# First take prompt and identify possible program file name.
# Second search for the file names, stop on first one found
# Third give the file as context to docuemnt
# Forth provide the docuemnt to the user
# Idea: use this prompt to get some insights of the graph:
# Given the context form a neo4j database, the data describes the dependencies of and application, the jobs it uses and the programs the jobs call. What can you tell me about the data?
#
# context: {the response form the neo4j query}

def count_node_types(nodes, edges):
    counts = {
        'application': 0,
        'job': 0,
        'program': 0,
        'sub_program': 0
    }

    for node in nodes:
        if node['group'] in counts:
            counts[node['group']] += 1

    print(f"Applications: {counts['application']}")
    print(f"Jobs: {counts['job']}")
    print(f"Programs: {counts['program']}")
    print(f"Sub-programs: {counts['sub_program']}")
    print(f"Total nodes: {sum(counts.values())}")

    # programs = []
    # jobs = []
    # sub_programs = []
    # for node in nodes:
    #     print(f"Node: {node['label']} {node['group']} {node['id']}")
    #     if node['group'] == 'job':
    #         jobs.append(node['label'])
    #     if node['group'] == 'program':
    #         programs.append(node['label'])
    #     if node['group'] == 'sub_program':
    #         sub_programs.append(node['label'])
    #
    # print(f"Jobs: {jobs}")
    # print(f"Programs: {programs}")
    # print(f"Sub-programs: {sub_programs}")


def render_graph(nodes, edges):
    # Create containers
    filter_container = st.container()
    graph_container = st.container()

    # Add filters
    with filter_container:
        cols = st.columns(4)
        applications = cols[0].checkbox('Show Applications', value=True, key='app_filter')
        jobs = cols[1].checkbox('Show Jobs', value=True, key='job_filter')
        programs = cols[2].checkbox('Show Programs', value=True, key='prog_filter')
        sub_programs = cols[3].checkbox('Show Sub-Programs', value=True, key='sub_prog_filter')

    # Filter nodes based on checkbox selections
    filtered_nodes = [
        node for node in nodes
        if (node["group"] == 'application' and applications) or
           (node["group"] == 'job' and jobs) or
           (node["group"] == 'program' and programs) or
           (node["group"] == 'sub_program' and sub_programs)
    ]

    # Filter edges to only include connections between visible nodes
    visible_node_ids = {node["id"] for node in filtered_nodes}
    filtered_edges = [
        edge for edge in edges
        if edge["source"] in visible_node_ids and edge["target"] in visible_node_ids
    ]

    # Create Pyvis network
    net = Network(
        height="750px",
        width="100%",
        bgcolor="#ffffff",
        font_color="black",
        directed=True,
        notebook=False
    )

    # Configure network options for radial layout
    net.set_options("""
    {
        "layout": {
            "improvedLayout": true,
            "hierarchical": {
                "enabled": false
            }
        },
        "physics": {
            "enabled": false
        },
        "edges": {
            "color": {
                "color": "#000000",
                "hover": "#FF0000"
            },
            "font": {
                "size": 12,
                "align": "middle"
            },
            "smooth": {
                "type": "curvedCW",
                "roundness": 0.2
            },
            "arrows": {
                "to": {
                    "enabled": true,
                    "scaleFactor": 0.5
                }
            }
        },
        "interaction": {
            "dragNodes": false,
            "dragView": true,
            "zoomView": true,
            "hover": true,
            "navigationButtons": true
        },
        "nodes": {
            "fixed": true,
            "font": {
                "size": 14
            }
        }
    }""")

    # Calculate positions for radial layout
    app_nodes = [n for n in filtered_nodes if n["group"] == "application"]
    job_nodes = [n for n in filtered_nodes if n["group"] == "job"]
    prog_nodes = [n for n in filtered_nodes if n["group"] == "program"]
    sub_prog_nodes = [n for n in filtered_nodes if n["group"] == "sub_program"]

    # Center position
    center_x, center_y = 0, 0

    # Radius for each circle
    job_radius = 300
    prog_radius = 600
    sub_prog_radius = 900

    # Position application node in center
    for i, node in enumerate(app_nodes):
        net.add_node(
            node["id"],
            label=node["label"],
            color='grey',
            shape="dot",
            size=40,
            title=f"{node['group']}: {node['label']}",
            x=center_x,
            y=center_y,
            physics=False
        )

    # Position job nodes in first circle
    for i, node in enumerate(job_nodes):
        angle = (2 * 3.14159 * i) / len(job_nodes) if len(job_nodes) > 0 else 0
        x = center_x + job_radius * math.cos(angle)
        y = center_y + job_radius * math.sin(angle)
        net.add_node(
            node["id"],
            label=node["label"],
            color='lime',
            shape="dot",
            size=30,
            title=f"{node['group']}: {node['label']}",
            x=x,
            y=y,
            physics=False
        )

    # Position program nodes in second circle
    for i, node in enumerate(prog_nodes):
        angle = (2 * 3.14159 * i) / len(prog_nodes) if len(prog_nodes) > 0 else 0
        x = center_x + prog_radius * math.cos(angle)
        y = center_y + prog_radius * math.sin(angle)
        net.add_node(
            node["id"],
            label=node["label"],
            color='aqua',
            shape="dot",
            size=20,
            title=f"{node['group']}: {node['label']}",
            x=x,
            y=y,
            physics=False
        )

    for i, node in enumerate(sub_prog_nodes):
        angle = (2 * math.pi * i) / len(sub_prog_nodes) if len(sub_prog_nodes) > 0 else 0
        x = center_x + sub_prog_radius * math.cos(angle)
        y = center_y + sub_prog_radius * math.sin(angle)
        net.add_node(
            node["id"],
            label=node["label"],
            color='#FFA500',  # orange color for sub-programs
            shape="dot",
            size=15,
            title=f"{node['group']}: {node['label']}",
            x=x,
            y=y,
            physics=False
        )

    # Add filtered edges with labels
    for edge in filtered_edges:
        net.add_edge(
            edge["source"],
            edge["target"],
            title=edge.get("label", ""),
            label=edge.get("label", ""),
            arrows="to"
        )

    # Save and render
    net_file = "graph.html"
    net.save_graph(net_file)
    with graph_container:
        st.components.v1.html(open(net_file, "r", encoding="utf-8").read(), height=850)

    # Custom styling for Streamlit
    st.markdown(
        """
        <style>
        [data-testid="stCheckbox"] {
            background-color: white;
            padding: 5px;
            border-radius: 4px;
        }
        .appview-container {
            max-width: 95% !important;
            max-height: 90% !important;
        }
        .main > div {
            max-width: 95% !important;
            padding-left: 20px !important;
            padding-right: 20px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def add_sub_program_nodes(nodes, edges):
    """
    Identifies sub-programs based on call hierarchy:
    - Programs are called by applications or jobs only
    - Sub-programs are called by programs or other sub-programs
    """
    # Track programs that should be reclassified as sub-programs
    sub_programs = set()
    programs = {node["id"] for node in nodes if node["group"] == "program"}

    # First pass: identify programs called by other programs
    for edge in edges:
        source_node = next((node for node in nodes if node["id"] == edge["source"]), None)
        target_id = edge["target"]

        if (source_node and
                source_node["group"] in ["program", "sub_program"] and
                target_id in programs):
            sub_programs.add(target_id)

    # Second pass: check that remaining programs are only called by applications or jobs
    for node in nodes:
        if node["group"] == "program":
            # Get all incoming edges to this node
            incoming_edges = [edge for edge in edges if edge["target"] == node["id"]]

            for edge in incoming_edges:
                source_node = next((n for n in nodes if n["id"] == edge["source"]), None)
                if source_node and source_node["group"] not in ["application", "job"]:
                    sub_programs.add(node["id"])
                    break

    # Update the group type for identified sub-programs
    for node in nodes:
        if node["id"] in sub_programs:
            node["group"] = "sub_program"

    return nodes


def reclassify_self_calling_subprograms(nodes, edges):
    """
    Identifies sub-programs that call themselves and reclassifies them as programs.
    """
    # Find sub-programs with self-calls
    self_calling = set()

    for edge in edges:
        if edge['source'] == edge['target']:  # self-call detected
            source_node = next((node for node in nodes if node['id'] == edge['source'] and
                                node['group'] == 'sub_program'), None)
            if source_node:
                self_calling.add(source_node['id'])

    # Reclassify self-calling sub-programs as programs
    for node in nodes:
        if node['id'] in self_calling:
            node['group'] = 'program'

    return nodes


def extract_program_name(text):
    # Use string split to handle spaces and get all words
    words = text.upper().split()

    # Look for a word that matches the program name pattern
    for word in words:
        # Check if word starts with P and is 7 characters long
        if (len(word) == 7 and
                word.startswith('P') and
                word.strip('P0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$#@!%^&*') == ''):
            return word

    return None


def format_documentation(program_name, section_contents):
    """
    Format the documentation with consistent structure and formatting.
    
    Args:
        program_name (str): Name of the program
        section_contents (dict): Dictionary mapping section identifiers to content
    
    Returns:
        str: Formatted documentation with consistent structure
    """
    # Create the documentation structure
    doc = f"{program_name}\n"
    doc += f"Report date: {datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')}\n\n"
    
    # Define the documentation structure with main sections and subsections
    doc_structure = [
        {
            "id": 1,
            "title": "Program Overview",
            "subsections": [
                {"title": "Section 1: Overview and Introduction"},
                {"title": "Purpose and Main Functionality"},
                {"title": "Business Context and Importance"},
                {"title": "Key Stakeholders and Users"},
                {"title": "System Requirements"},
                {"title": "Technical Specifications"},
                {"title": "Performance Considerations"}
            ]
        },
        {
            "id": 2,
            "title": "Program Architecture",
            "subsections": [
                {"title": "Section 2: High-Level System Design and Integration"},
                {"title": "High-Level System Design"},
                {"title": "Core Components"},
                {"title": "Integration Points with Other Systems"},
                {"title": "Data Flow Architecture"},
                {"title": "Security Considerations"},
                {"title": "System Boundaries"},
                {"title": "External Interfaces"},
                {"title": "Technical Dependencies"}
            ]
        },
        {
            "id": 3,
            "title": "Program Structure",
            "subsections": [
                {"title": "Section 3: Procedures and Functions"},
                {"title": "A. Procedures and Functions"},
                {"title": "B. Call Hierarchy"}
            ]
        },
        {
            "id": 4,
            "title": "Data Management",
            "subsections": [
                {"title": "Section 4: Data Structures, File Operations, and Data Flow"},
                {"title": "A. Data Structures"},
                {"title": "B. File Operations"},
                {"title": "C. Data Flow"}
            ]
        },
        {
            "id": 5,
            "title": "Control Flow",
            "subsections": [
                {"title": "Section 5: Main Process Flow and Business Logic"}
            ]
        },
        {
            "id": 6,
            "title": "Error Handling",
            "subsections": [
                {"title": "Section 6: Error Handling, Recovery, Logging, and User Notifications"}
            ]
        },
        {
            "id": 7,
            "title": "Integration & Interfaces",
            "subsections": [
                {"title": "Section 7: External System Dependencies, Data Exchange Formats, and Communication Protocols"}
            ]
        }
    ]
    
    
    toc = "Table of Contents\n"
    for section in doc_structure:
        section_num = section["id"]
        section_title = section["title"]
        toc += f"{section_num}. {section_title}\n"
    toc += "\n"
    
    # Add table of contents to documentation
    doc += toc
    
    
    for i, section in enumerate(doc_structure):
        section_num = section["id"]
        section_title = section["title"]
        section_id = f"{section_num}"
        
        # Add main section heading
        doc += f"{section_num}. {section_title}\n\n"
        
        # Add first subsection heading if it exists (usually the "Section X:" heading)
        if section["subsections"] and section["subsections"][0]["title"].startswith("Section"):
            doc += f"{section['subsections'][0]['title']}\n\n"
        
        # Get content for this section if available
        if section_id in section_contents and section_contents[section_id].strip():
            doc += section_contents[section_id].strip() + "\n\n"
        
        # Add a horizontal line after each section (except the last one)
        if i < len(doc_structure) - 1:
            doc += "\n---\n\n"
    
    return doc


BASE_PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

SUMMARY_PROMPT_TEMPLATE = """
Summarize the following summaries:

{summaries}
based on the following question: {question}
"""

FILENAME_PROMPT_TEMPLATE = """
Given the following question, use the question as context, do not answer the question, only use it as context. Break down the question to identify possible key words that could identify a possible file name. 

Only give the key words in a comma separated list.

Question to be used as context:

"{context}"
"""

SECTION_CONTENT_PROMPT = """
Program: {program_name}

Based on these parsed code sections, provide content for {section_title}

{summaries}

{section_requirements}

IMPORTANT INSTRUCTIONS:
1. DO NOT include section numbers or headings in your response
2. DO NOT format with markdown headings
3. Start directly with the content
4. Provide specific examples from the code
5. Include exact procedure names, parameters, and code details when relevant
6. Document actual business rules found in the code
7. Use concrete examples, not general statements
8. Explain implementation details thoroughly
"""

if 'nodes' not in st.session_state:
    st.session_state['nodes'] = []

if 'edges' not in st.session_state:
    st.session_state['edges'] = []

if 'chat_history_summaries' not in st.session_state:
    st.session_state['chat_history_summaries'] = [{
        "role": "system",
        "content": "You are a software developer, helping humans with their code related questions."
    }]

if 'chat_history_sections' not in st.session_state:
    st.session_state['chat_history_sections'] = [{
        "role": "system",
        "content": "You are a technical documentation writer, focusing on creating detailed program documentation sections."
    }]

if 'auth_token' not in st.session_state:
    st.session_state['auth_token'] = ""

if 'start_time' not in st.session_state:
    st.session_state['start_time'] = time.time()

if 'expires_in' not in st.session_state:
    st.session_state['expires_in'] = 0

if 'llm_service' not in st.session_state:
    st.session_state['llm_service'] = llmService.LLMService()

if 'db_service' not in st.session_state:
    st.session_state['db_service'] = dbService.DBService()

if 'chunk_summaries' not in st.session_state:
    st.session_state['chunk_summaries'] = []

dependency_types = ["Job dependencies", "Create documentation"]
image_path = 'cda.png'

if not os.path.isfile(image_path):
    st.error(f"Image not found: {image_path}")
else:
    bin_str = utils.get_base64_of_bin_file(image_path)
    background_image = f"""
    <style>    
        [data-testid="stAppViewContainer"] > 
        .main 
        {{        background-image: url('data:image/png;base64,{bin_str}'); 
            background-size: 100vw 100vh;  
        
            /* This sets the size to cover 100% of the viewport width and height */
           
        }}    
    </style>    
    """
    st.markdown("<h1 style='color:white;'>COBOL Dependency Analyzer</h1>", unsafe_allow_html=True)
    st.markdown(background_image, unsafe_allow_html=True)

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])

    prompt = st.chat_input('Pass Your Prompt here')

    st.markdown(
        """
        <style>
        .stSelectbox label {
            color: white;
            
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    selected_dependency = st.selectbox("Select type", dependency_types)

    st.markdown(
        """
        <style>
        .stFileUploader label {
            color: white;
            
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # uploaded_file = st.file_uploader("Choose a file")

    # if uploaded_file is not None:
    #     save_uploaded_file(uploaded_file, './input')
    #     st.success(f"File {uploaded_file.name} saved successfully!")

    if st.session_state['nodes']:
        render_graph(st.session_state['nodes'], st.session_state['edges'])

if prompt:
    llm_response = ""
    llm_chat_response = ""
    fileName = ""  # name of the file

    if selected_dependency == "Create documentation":
        st.chat_message('user').markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        # clear output folder
        utils.delete_all_files_in_directory("./src/output/")

        name = extract_program_name(prompt)
        program_name = [name]
        st.session_state['chat_history_summaries'].append({"role": "assistant", "content": name})

        for name in program_name:
            name = name.strip().upper()
            fileName = name
            found_file = None

            found = False
            # Search for main program,sometimes has the extension .PGM
            search = utils.find_file(name)

            if search:
                found = True
                found_file = search
            search = utils.find_file(name + ".PGM")
            if search:
                found = True
                found_file = search
            
            if found:
                print(f"Program {name} found!")
                all_chunk_summaries = []
                all_chunks = []
                parser = PL1FileParser()
                temp_output = "temp_parse_output"

                # Parse file using the PL1 parser
                parser.parse_pl1_file(found_file, temp_output)

                # Process each parsed chunk by type
                i = 1
                for chunk_type in os.listdir(temp_output):
                    chunk_dir = os.path.join(temp_output, chunk_type)
                    if not os.path.isdir(chunk_dir):
                        continue

                    for chunk_file in os.listdir(chunk_dir):
                        with open(os.path.join(chunk_dir, chunk_file), 'r') as f:
                            content = f.read()
                            
                            prompt_template = ChatPromptTemplate.from_template(BASE_PROMPT_TEMPLATE)
                            section_context = f"""Code Section Type: {chunk_type}

                            {content}"""

                            question = "Give documentation for this code section focusing on: General Information, Change Log, inputs and outputs, Program Structure, Subprograms and Procedures, Error Handling. Translate all comments to English."
                            new_prompt = prompt_template.format(context=section_context, question=question)

                            st.session_state['chat_history_summaries'].append({"role": "user", "content": new_prompt})
                            st.session_state['chat_history_summaries'] = st.session_state['chat_history_summaries'][-2:]

                            llm_response = st.session_state['llm_service'].query_llm(new_prompt,
                                                                                    st.session_state['auth_token'],
                                                                                    st.session_state['chat_history_summaries'])

                            st.session_state['chat_history_summaries'].append({"role": "assistant", "content": llm_response})
                            document = llm_response.replace('```markdown', '').replace('```', '')

                            # Save individual section documentation
                            file_path = f'./output/{chunk_type}_section{i}_documentation.md'
                            i += 1
                            utils.save_as_markdown(document, file_path)
                            all_chunk_summaries.append(document)
                            all_chunks.append(content)

                # Clean up temporary parser output
                shutil.rmtree(temp_output)

                # Define documentation sections
                documentation_sections = [
                    {
                        "id": 1,
                        "title": "Program Overview",
                        "requirements": """
                        Provide information about:
                        - Purpose and main functionality
                        - Business context and importance
                        - Key stakeholders and users
                        - System requirements
                        - Technical specifications
                        - Performance considerations
                        """
                    },
                    {
                        "id": 2,
                        "title": "Program Architecture",
                        "requirements": """
                        Provide information about:
                        - High-level system design
                        - Integration points with other systems
                        - Data flow architecture
                        - Security considerations
                        - System boundaries
                        - External interfaces
                        - Technical dependencies
                        """
                    },
                    {
                        "id": 3,
                        "title": "Program Structure",
                        "requirements": """
                        Provide information about:
                        - Procedures and Functions:
                          - Each procedure's specific purpose
                          - Input/output parameters for each
                          - Validation rules and error handling
                          - Business rules implementation
                          - Performance considerations
                          - Dependencies between procedures
                        - Call Hierarchy:
                          - Call tree with relationships
                          - Execution paths
                          - Conditional calling patterns
                          - Recursive relationships
                          - Module dependencies
                        """
                    },
                    {
                        "id": 4,
                        "title": "Data Management",
                        "requirements": """
                        Provide information about:
                        - Data Structures:
                          - Each structure's purpose and fields
                          - Data types and constraints
                          - Validation rules
                          - Usage patterns
                          - Relationships between structures
                        - File Operations:
                          - Input/output files
                          - File formats and structures
                          - File handling procedures
                          - Error handling for files
                        - Data Flow:
                          - Data transformation logic
                          - Validation processes
                          - Data persistence methods
                        """
                    },
                    {
                        "id": 5,
                        "title": "Control Flow",
                        "requirements": """
                        Provide information about:
                        - Main process flow step by step
                        - Decision points and conditions
                        - Loop structures and their purposes
                        - Complex conditional logic
                        - Business rule implementations
                        """
                    },
                    {
                        "id": 6,
                        "title": "Error Handling",
                        "requirements": """
                        Provide information about:
                        - Error types and handling
                        - Recovery procedures
                        - Logging mechanisms
                        - User notifications
                        """
                    },
                    {
                        "id": 7,
                        "title": "Integration & Interfaces",
                        "requirements": """
                        Provide information about:
                        - External system dependencies
                        - Data exchange formats
                        - Communication protocols
                        """
                    }
                ]

                # Combine all summaries for context
                summaries = "\n\n".join(all_chunk_summaries)

                # Generate content for each section
                section_content_dict = {}
                
                for section in documentation_sections:
                    section_prompt = ChatPromptTemplate.from_template(SECTION_CONTENT_PROMPT)
                    
                    new_prompt = section_prompt.format(
                        program_name=name,
                        section_title=f"Section {section['id']}: {section['title']}",
                        summaries=summaries,
                        section_requirements=section["requirements"]
                    )

                    st.session_state['chat_history_sections'].append({
                        "role": "user",
                        "content": new_prompt
                    })
                    st.session_state['chat_history_sections'] = st.session_state['chat_history_sections'][-2:]

                    section_content = st.session_state['llm_service'].query_llm(
                        new_prompt,
                        st.session_state['auth_token'],
                        st.session_state['chat_history_sections']
                    )

                    st.session_state['chat_history_sections'].append({"role": "assistant", "content": section_content})
                    
                    # Clean up any markdown formatting the LLM might have added
                    section_content = re.sub(r'^#+\s+.*$', '', section_content, flags=re.MULTILINE)  # Remove headings
                    section_content = re.sub(r'^Section \d+:.*$', '', section_content, flags=re.MULTILINE)  # Remove section titles
                    
                    # Store the content for this section
                    section_content_dict[str(section['id'])] = section_content

                # Format the documentation with consistent structure
                final_summary = format_documentation(name, section_content_dict)

                # Save and convert to PDF
                utils.save_as_markdown(final_summary, f'./output/final_summary_{name}.md')
                llm_chat_response = final_summary

                utils.markdown_to_pdf(
                    markdown_content=final_summary,
                    output_file=f"./output/pdf/{name}.pdf"
                )

    elif selected_dependency == "Chat to code":
        st.chat_message('user').markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []
            
        st.session_state['chat_history'].append({"role": "user", "content": prompt})
        st.session_state['chat_history'] = st.session_state['chat_history'][-6:]

        # Get file name
        prompt_template = ChatPromptTemplate.from_template(FILENAME_PROMPT_TEMPLATE)
        new_prompt = prompt_template.format(context=prompt)
        llm_response = st.session_state['llm_service'].query_llm(new_prompt, st.session_state['auth_token'],
                                                                 st.session_state['chat_history'])
        st.session_state['chat_history'].append({"role": "assistant", "content": llm_response})

        file_names = llm_response.split(",")

        # Search for the csv of the potential file names
        found = False
        found_file = ""
        file_lines = ""

        for name in file_names:
            name = name.upper().strip()
            if name != ("GIVE" or "DOCUMENTATION"):
                name += ".PGM"
                search = utils.find_file(name)
                if search:
                    found = True
                    found_file = search

        if found:
            with open(found_file, 'r') as file:
                content = file.read()
                prompt_template = ChatPromptTemplate.from_template(BASE_PROMPT_TEMPLATE)
                question = "Give documentation in markdown for the file by focusing on these topics if available: General Information, Change Log, Program Structure and Error Handling. Translate all comments to English."
                new_prompt = prompt_template.format(context=content, question=question)
                llm_response = st.session_state['llm_service'].query_llm(new_prompt, st.session_state['auth_token'],
                                                                         st.session_state['chat_history'])
                st.session_state['chat_history'].append({"role": "assistant", "content": llm_response})

                cleand_response = llm_response.replace('```markdown', '').replace('```', '')

                file_path = f'./output/{name}.md'
                utils.save_as_markdown(cleand_response, file_path)

    else:
        st.chat_message('user').markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        # Get file name
        prompt_template = ChatPromptTemplate.from_template(FILENAME_PROMPT_TEMPLATE)
        new_prompt = prompt_template.format(context=prompt)
        st.session_state['chat_history_summaries'].append({"role": "user", "content": new_prompt})
        llm_response = st.session_state['llm_service'].query_llm(new_prompt, st.session_state['auth_token'],
                                                                 st.session_state['chat_history_summaries'])
        st.session_state['chat_history_summaries'].append({"role": "assistant", "content": llm_response})

        file_names = llm_response.split(",")

        # Search for the csv of the potential file names
        found = False
        found_file = ""
        file_lines = ""
        fname = ''
        fileName = ''

        for name in file_names:
            fname = name.upper().strip()
            if fname != "DEPENDENCIES":
                if st.session_state['db_service'].find_and_populate_from_xinfo_data(name, selected_dependency):
                    found = True
                    found_file = name.strip() + ".csv"
                    fileName = fname

        if found and fileName != '':
            def get_graph_data():
                # Query results from Neptune database
                results = st.session_state['db_service'].execute_ne04j_query(fileName)

                # Track unique nodes and mapping
                node_map = {}  # {(type, name): node_id}
                id_map = {}  # {old_id: new_id}
                next_id = 0

                st.session_state['nodes'] = []
                st.session_state['edges'] = []
                relationships = []

                # First pass: collect nodes and relationships
                for result in results['results']:
                    relationships.extend(result['relationships'])

                    for node in result['nodes']:
                        old_id = node['~id']
                        properties = node['~properties']

                        if old_id in id_map:
                            continue

                        # Determine node type and name
                        if 'program' in node['~labels']:
                            node_type = 'program'
                            name = properties.get('program_name', '')
                        elif 'application' in node['~labels']:
                            node_type = 'application'
                            name = properties.get('application_name', '')
                        elif 'job' in node['~labels']:
                            node_type = 'job'
                            name = properties.get('job_name', '')
                        else:
                            continue

                        unique_key = (node_type, name)

                        # Create new node if unique
                        if unique_key not in node_map:
                            new_id = str(next_id)
                            next_id += 1
                            node_map[unique_key] = new_id
                            id_map[old_id] = new_id

                            new_node = {
                                'id': new_id,
                                'label': name,
                                'group': node_type
                            }
                            st.session_state['nodes'].append(new_node)
                        else:
                            id_map[old_id] = node_map[unique_key]

                # Second pass: create edges
                seen_edges = set()
                for relationship in relationships:
                    source_id = relationship['~start']
                    target_id = relationship['~end']

                    if source_id not in id_map or target_id not in id_map:
                        continue

                    new_source = id_map[source_id]
                    new_target = id_map[target_id]
                    edge_key = (new_source, new_target, relationship['~type'])

                    if edge_key not in seen_edges:
                        seen_edges.add(edge_key)
                        st.session_state['edges'].append({
                            'source': new_source,
                            'target': new_target,
                            'label': relationship['~type']
                        })

                return st.session_state['nodes'], st.session_state['edges']

            nodes, edges = get_graph_data()
            if st.session_state['nodes']:
                nodes = add_sub_program_nodes(nodes, edges)
                nodes = reclassify_self_calling_subprograms(nodes, edges)
                render_graph(nodes, edges)

    st.markdown(
        """
            <style>
            .stChatMessage {
                background-color: white;
            }
            </style>
            """,
        unsafe_allow_html=True
    )
    st.chat_message('assistant').markdown(llm_chat_response)
    st.session_state.messages.append({'role': 'assistant', 'content': llm_chat_response})

    if selected_dependency == "Create documentation" and fileName != '':
        try:
            with open(f"./output/pdf/{fileName}.pdf", "rb") as file:
                btn = st.download_button(
                    label="Download PDF",
                    data=file,
                    file_name=f"{fileName}.pdf",
                    mime="application/pdf",
                )
        except FileNotFoundError:
            st.error(f"PDF file for {fileName} not found.")