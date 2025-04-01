import streamlit as st
import os
import re
from langchain.prompts import ChatPromptTemplate
import time
import llm_service as llmService
import Current.utils as utils
import db_service as dbService
from pyvis.network import Network
import math
import datetime
import sys
import subprocess
import concurrent.futures

# COBOL specific prompt template
COBOL_BASE_PROMPT_TEMPLATE = """
You are an expert COBOL documentation specialist creating comprehensive documentation for COBOL programs. Keep your analysis focused, precise, and thorough. Emphasize business purpose over technical details.

Analyze the following COBOL code section and document according to this structure:

# COBOL Program Analysis

## Program Overview
- Program Name: {program_name}
- Program Type: [Batch/Online/Service]
- Main Purpose: [Brief overview]

## Business Context
- Describe the business function and importance

## Key Features
- List and explain major program features

## Input and Output
- Detail key files, parameters, and data sources used
- Describe outputs generated

## Program Logic
- Explain major processing sections and business rules

## Error Handling
- Describe error conditions and recovery procedures

## Integration Points
- Note interfaces with other systems and programs

Analyze this COBOL code carefully:

{context}
"""

# PL/1 specific prompt template
PL1_BASE_PROMPT_TEMPLATE = """
You are an expert PL/1 documentation specialist creating comprehensive documentation for PL/1 programs. Keep your analysis focused, precise, and thorough. Emphasize business purpose over technical details.

Analyze the following PL/1 code section and document according to this structure:

# PL/1 Program Analysis

## Program Overview
- Program Name: {program_name}
- Program Type: [Batch/Online/Service]
- Main Purpose: [Brief overview]

## Business Context
- Describe the business function and importance

## Key Features
- List and explain major program features

## Input and Output
- Detail key files, parameters, and data sources used
- Describe outputs generated

## Program Structure
- Explain main procedures and their functions
- Describe key processing blocks

## Error Handling
- Describe ON-conditions and exception handling

## Integration Points
- Note interfaces with other systems and procedures

Analyze this PL/1 code carefully:

{context}
"""

# Enhanced summary prompt template that works for both languages
ENHANCED_SUMMARY_PROMPT_TEMPLATE = """
You are creating comprehensive documentation for a {language} program. Synthesize the provided analyses into a single, well-structured document following this format:

# {program_name} - Program Documentation

## Table of Contents
1. High Level Overview
2. Program Logic and Functionality
3. Data Flow and Dependencies
4. Database Information
5. Error and Abend Handling
6. Input and Output Processing
7. Integration Information
8. Programs Called

## 1. High Level Overview of This Program

### 1.1 Program Name
{program_name}

### 1.2 Main Purpose
[Concise statement of primary purpose]

### 1.3 Business Context
[Business context and importance]

### 1.4 Key Features
[Numbered list of key features]

### 1.5 Input Output
[Input sources and output destinations]

### 1.6 Integration
[Integration with other systems]

## 2. Program Logic And Functionality
[Major processing sections with explanations]

## 3. The Data Flow And Data Dependencies
[Data flow and dependencies]

## 4. Database Information
[Database interactions]

## 5. Error And Abend Handling
[Error handling strategy]

## 6. The Input And Output Processing
[Input/output processing details]

## 7. Integration Information
[Integration points]

## 8. Programs Called
[Programs called]

Your documentation must be:
1. Comprehensive yet concise
2. Well-structured with consistent formatting
3. Business-focused
4. Free of redundancies

Synthesize this information from the provided analyses:

{summaries}
"""

if 'nodes' not in st.session_state:
    st.session_state['nodes'] = []

if 'edges' not in st.session_state:
    st.session_state['edges'] = []

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [{
        "role": "system",
        "content": "You are a software developer, helping humans with their code related questions."
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

    if st.session_state['nodes']:
        render_graph(st.session_state['nodes'], st.session_state['edges'])


def extract_program_names(prompt_text):
    """
    Extract potential program names from user prompt using regex patterns
    instead of an LLM query.
    
    Args:
        prompt_text: User's input prompt text
        
    Returns:
        list: List of potential program names found in the text
    """
    # Common patterns for program names in requests
    patterns = [
        # Look for "program/file/document XYZ123"
        r'(?:program|file|document|code)\s+([A-Z0-9_]+)',
        
        # Look for "XYZ123.PGM" or similar
        r'([A-Z0-9_]+)(?:\.PGM|\.CBL|\.COB|\.PLI)',
        
        # Look for "XYZ123" in quotes
        r'["\']([A-Z0-9_]+)["\']',
        
        # Look for capitalized words that might be program names
        r'\b([A-Z0-9][A-Z0-9_]{2,})\b'
    ]
    
    # Convert to uppercase for easier matching
    prompt_upper = prompt_text.upper()
    
    # Collect all potential matches
    potential_names = []
    for pattern in patterns:
        matches = re.findall(pattern, prompt_upper)
        if matches:
            # Flatten if any match groups returned lists
            flat_matches = [m if isinstance(m, str) else m[0] for m in matches]
            potential_names.extend(flat_matches)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_names = [name for name in potential_names if not (name in seen or seen.add(name))]
    
    # Filter out common words that might be caught but aren't likely program names
    common_words = {'THE', 'AND', 'FOR', 'WITH', 'PROGRAM', 'FILE', 'CODE', 'DOCUMENT', 
                    'PLEASE', 'NEED', 'WANT', 'ANALYZE', 'CREATE', 'DOCUMENTATION', 
                    'DEPENDENCIES'}
    
    filtered_names = [name for name in unique_names if name not in common_words]
    
    return filtered_names


def process_chunk(chunk, template, program_name, auth_token, chat_history):
    """
    Process a single chunk of code and generate documentation for it.
    This function is designed to be used with concurrent processing.
    """
    prompt_template = ChatPromptTemplate.from_template(template)
    prompt = prompt_template.format(
        context=chunk, 
        program_name=program_name
    )
    
    # Use a minimal chat history to avoid token limits
    limited_history = chat_history[-2:] if len(chat_history) > 2 else chat_history.copy()
    limited_history.append({"role": "user", "content": prompt})
    
    # Query the LLM for this chunk
    llm_service = llmService.LLMService()  # Create a new instance for thread safety
    llm_response = llm_service.query_llm(
        prompt,
        auth_token,
        limited_history
    )
    
    # Clean up the response
    document = llm_response.replace('```markdown', '').replace('```', '')
    return document


def generate_documentation(file_path, program_name):
    """
    Optimized documentation generation function for COBOL and PL/1 programs.
    Uses parallel processing and adaptive chunking for efficiency.
    
    Args:
        file_path: Path to the program file
        program_name: Name of the program
        
    Returns:
        str: The generated documentation in markdown format
    """
    # Create directories if they don't exist
    os.makedirs("./output", exist_ok=True)
    os.makedirs("./output/pdf", exist_ok=True)
    
    # Detect language
    language = utils.detect_language(file_path)
    
    progress_bar = st.progress(10)
    status_text = st.empty()
    status_text.info(f"🔍 Detected {language} program. Preparing for analysis...")
    
    # Select appropriate prompt template based on language
    template = COBOL_BASE_PROMPT_TEMPLATE if language == 'COBOL' else PL1_BASE_PROMPT_TEMPLATE
    
    # Process file with optimized chunking
    progress_bar.progress(15)
    status_text.info(f"✂️ Splitting {program_name} into optimal chunks...")
    chunks = utils.optimized_file_splitter(file_path, language)
    
    # Show chunking info
    progress_bar.progress(20)
    status_text.info(f"🔍 Analyzing {program_name} ({language}) - {len(chunks)} chunks...")
    
    # Process chunks in parallel for better efficiency
    all_chunk_summaries = []
    
    # Use concurrent futures for parallel processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(4, len(chunks))) as executor:
        # Submit all chunks for processing
        future_to_chunk = {
            executor.submit(
                process_chunk, 
                chunk, 
                template, 
                program_name, 
                st.session_state['auth_token'],
                st.session_state['chat_history']
            ): i for i, chunk in enumerate(chunks)
        }
        
        # Process results as they complete
        for i, future in enumerate(concurrent.futures.as_completed(future_to_chunk)):
            progress_value = 20 + int(50 * (i + 1) / len(chunks))
            progress_bar.progress(progress_value)
            status_text.info(f"🔍 Processing chunk {i+1} of {len(chunks)}... ({progress_value}%)")
            
            chunk_idx = future_to_chunk[future]
            try:
                document = future.result()
                # Save individual chunk analysis
                file_path_chunk = f'./output/chunk_summary{chunk_idx+1}_documentation.md'
                utils.save_as_markdown(document, file_path_chunk)
                all_chunk_summaries.append(document)
            except Exception as exc:
                status_text.warning(f"⚠️ Error processing chunk {chunk_idx+1}: {exc}")
    
    # Update progress
    progress_bar.progress(75)
    status_text.info(f"📝 Generating final comprehensive documentation...")
    
    # Generate the consolidated summary with the enhanced summary prompt
    summary_prompt = ChatPromptTemplate.from_template(ENHANCED_SUMMARY_PROMPT_TEMPLATE)
    summaries = '\n'.join(all_chunk_summaries)
    final_prompt = summary_prompt.format(
        summaries=summaries, 
        program_name=program_name,
        language=language
    )
    
    final_summary = st.session_state['llm_service'].query_llm(
        final_prompt, 
        st.session_state['auth_token'],
        st.session_state['chat_history']
    )
    
    # Clean up the final summary
    cleaned_summary = final_summary.replace('```markdown', '').replace('```', '')
    
    # Save the final documentation
    md_path = f'./output/final_summary_{program_name}.md'
    utils.save_as_markdown(cleaned_summary, md_path)
    
    # Update progress
    progress_bar.progress(90)
    status_text.info(f"📄 Generating PDF document...")
    
    # Generate PDF with enhanced formatting
    utils.generate_enhanced_pdf(
        markdown_content=cleaned_summary,
        output_file=f"./output/pdf/{program_name}.pdf",
        program_name=program_name,
        language=language
    )
    
    # Finalize progress
    progress_bar.progress(100)
    status_text.success(f"✅ Documentation successfully generated for {program_name} ({language})!")
    
    return cleaned_summary


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
        angle = (2 * math.pi * i) / (len(sub_prog_nodes) or 1)
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

if prompt:
    llm_response = ""
    llm_chat_response = ""
    fileName = ""  # name of the file

    if selected_dependency == "Create documentation":
        st.chat_message('user').markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        # Clear output folder
        utils.delete_all_files_in_directory("./output/")

        # Show progress indicator
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.info("🔍 Analyzing request...")
        
        # Extract potential file names directly using regex
        program_names = extract_program_names(prompt)
        
        progress_bar.progress(10)
        status_text.info("🔍 Searching for program file...")
        
        found = False
        found_file = None
        fileName = ""
        
        for name in program_names:
            name = name.strip()
            fileName = name
            
            # Search for main program, various extensions possible
            search = utils.find_file(name)
            if search:
                found = True
                found_file = search
            else:
                search = utils.find_file(name + ".PGM")
                if search:
                    found = True
                    found_file = search

            if found:
                progress_bar.progress(20)
                status_text.info(f"📋 Found program file: {fileName}. Beginning analysis...")
                
                # Generate documentation using the optimized approach
                llm_chat_response = generate_documentation(found_file, fileName)
                break
        
        # If no files found from regex extraction, try some common fallback names
        if not found:
            fallback_names = ["MAIN", "PROGRAM", "MAINPGM", "MAINPROG"]
            for name in fallback_names:
                search = utils.find_file(name)
                if search:
                    found = True
                    found_file = search
                    fileName = name
                    progress_bar.progress(20)
                    status_text.info(f"📋 Found program file: {fileName}. Beginning analysis...")
                    llm_chat_response = generate_documentation(found_file, fileName)
                    break
            
        if not found:
            progress_bar.progress(100)
            status_text.error("❌ Program file not found. Please check the program name.")
            llm_chat_response = "Sorry, I couldn't find the program file you requested. Please specify the program name more clearly in your request."

    elif selected_dependency == "Job dependencies":
        st.chat_message('user').markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        # Get file name using regex extraction
        program_names = extract_program_names(prompt)

        # Search for the csv of the potential file names
        found = False
        found_file = ""
        file_lines = ""
        fname = ''
        fileName = ''

        for name in program_names:
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

    if selected_dependency == "Create documentation" and found and fileName != '':
        try:
            with open(f"./output/pdf/{fileName}.pdf", "rb") as file:
                btn = st.download_button(
                    label="Download PDF",
                    data=file,
                    file_name=f"{fileName}.pdf",
                    mime="application/pdf",
                )
        except Exception as e:
            st.error(f"Error preparing download: {e}")