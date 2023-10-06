import gradio as gr
import modules.shared as shared
from pathlib import Path
import json
from functools import partial
import os


params = {
        "display_name": "JSON edit",
        "is_tab": True,
}

data = None
first_item_keys = None
data_index = 0
left_key = 'instruction'
right_key = 'output'
current_input_file = None
backup_file = None

# Function to load JSON data safely
def load_json_data(file):
    global data
    global data_index
    global current_input_file
    try:
        
        with open(file, 'r') as json_file:
            current_input_file = file
            data = json.load(json_file)
            if data:
                first_item_keys = list(data[0].keys())
                data_index = 0
                print(f"Keys in the JSON: {first_item_keys}")
                return f"JSON data loaded successfully. Keys in the JSON: {first_item_keys}"
                #for key in first_item_keys:
                #    print(key)
            else:
                current_input_file = None
                print("JSON data is empty or couldn't be loaded.")
                return "JSON data is empty or couldn't be loaded."

    except FileNotFoundError:
        current_input_file = None
        print("Error: JSON file not found.")
        return "JSON file not found."
    except json.JSONDecodeError:
        current_input_file = None
        print("Error: JSON file is not valid JSON.")
        return "JSON file is not valid JSON."


def find_next_diff():
    global data
    global left_key
    global right_key
    global data_index

    len1 = 0
    len2 = 0

    if data and isinstance(data, list) and 0 <= data_index < len(data):

        if data and isinstance(data, list) and data_index < len(data) - 1:
            data_index += 1

        for index, item in enumerate(data[data_index:], start=data_index):
            instruction_value = item.get(left_key, '')
            output_value = item.get(right_key, '')

            # Calculate the length difference
            length_diff = abs(len(instruction_value) - len(output_value))

            len1 = len(instruction_value)
            len2 = len(output_value)
            # Check if the length difference is greater than or equal to 50% of the shorter length
            min_length = min(len(instruction_value), len(output_value))
            
            if length_diff >= 0.5 * min_length:
                data_index = index  # Update the data_index
                break

    yield f"Lenghth {len1} vs {len2} at index: {data_index}/{len(data)-1}"              
    return 

def find_min_char_diff(characters):
    global data
    global left_key
    global right_key
    global data_index

    len1 = 0
    len2 = 0

    chars = int(characters)
    if data and isinstance(data, list) and 0 <= data_index < len(data):

        if data and isinstance(data, list) and data_index < len(data) - 1:
            data_index += 1

        for index, item in enumerate(data[data_index:], start=data_index):
            instruction_value = item.get(left_key, '')
            output_value = item.get(right_key, '')

            # Calculate the length difference
            length_diff = len(output_value)

            len1 = len(instruction_value)
            len2 = len(output_value)
            # Check if the length difference is greater than or equal to 50% of the shorter length
            
            
            if length_diff < chars:
                data_index = index  # Update the data_index
                yield f"OUT {len2} at index: {data_index}/{len(data)-1}"      
                return

    yield f"Current ndex: {data_index}/{len(data)-1}"          
    return 

def find_max_char_diff(characters):
    global data
    global left_key
    global right_key
    global data_index

    len1 = 0
    len2 = 0

    chars = int(characters)
    if data and isinstance(data, list) and 0 <= data_index < len(data):

        if data and isinstance(data, list) and data_index < len(data) - 1:
            data_index += 1

        for index, item in enumerate(data[data_index:], start=data_index):
            instruction_value = item.get(left_key, '')
            output_value = item.get(right_key, '')

            # Calculate the length difference
            length_diff = len(output_value)

            len1 = len(instruction_value)
            len2 = len(output_value)
            # Check if the length difference is greater than or equal to 50% of the shorter length
            
            
            if length_diff > chars:
                data_index = index  # Update the data_index
                yield f"OUT {len2} at index: {data_index}/{len(data)-1}"              
                return

    yield f"Current ndex: {data_index}/{len(data)-1}"  
    
    return 

def search_and_update_data_index(search_text):
    global data
    global left_key
    global data_index

    if data and isinstance(data, list) and 0 <= data_index < len(data):
        if data and isinstance(data, list) and data_index < len(data) - 1:
            data_index += 1

        for index, item in enumerate(data[data_index:], start=data_index):
            instruction_value = item.get(left_key, '')

            # Check if the search_text is present in the instruction_value
            if search_text in instruction_value:
                data_index = index  # Update the data_index
                yield f"Found '{search_text}' in instruction at index: {data_index}/{len(data) - 1}"
                return

    yield f"(Text not found) Current index: {data_index}/{len(data) - 1}"
    return

def search_and_update_data_index2(search_text):
    global data
    global left_key
    global data_index

    if data and isinstance(data, list) and 0 <= data_index < len(data):
        if data and isinstance(data, list) and data_index < len(data) - 1:
            data_index += 1

        for index, item in enumerate(data[data_index:], start=data_index):
            output_value = item.get(right_key, '')

            # Check if the search_text is present in the instruction_value
            if search_text in output_value:
                data_index = index  # Update the data_index
                yield f"Found '{search_text}' in output at index: {data_index}/{len(data) - 1}"
                return

    yield f"(Text not found) Current index: {data_index}/{len(data) - 1}"
    return

def search_and_update_data_index3(search_text):
    global data
    global left_key
    global data_index

    if data and isinstance(data, list) and 0 <= data_index < len(data):
        if data and isinstance(data, list) and data_index < len(data) - 1:
            data_index += 1

        for index, item in enumerate(data[data_index:], start=data_index):
            output_value = item.get(right_key, '')
            instruction_value = item.get(left_key, '')

            # Check if the search_text is present in the instruction_value
            if search_text in output_value or search_text in instruction_value:
                data_index = index  # Update the data_index
                yield f"Found '{search_text}' in item at index: {data_index}/{len(data) - 1}"
                return

    yield f"(Text not found) Current index: {data_index}/{len(data) - 1}"
    return


def calc_max_token_fn():
    global data
    global left_key
    global right_key
    global data_index

    data_index = 0
    data_idx_atMax = 0
    max_token = 0

    if data and isinstance(data, list) and 0 <= data_index < len(data):

        for index, item in enumerate(data[data_index:], start=data_index):
           
            instruction_value = item.get(left_key, '')
            output_value = item.get(right_key, '')

            encoded_tokens  = len(instruction_value)
            encoded_tokens2  = len(output_value)

            encoded_tokensT = encoded_tokens + encoded_tokens2

            #yield f"Size [IN+OUT] {encoded_tokensT} characters at index: {index}/{len(data)-1}"  
            
            if max_token < encoded_tokensT:
                max_token = encoded_tokensT
                data_idx_atMax = index

    data_index = data_idx_atMax

    yield f"Size MAx [IN+OUT] {max_token} at index: {data_idx_atMax}/{len(data)-1}"              
    return 
# Function to get 'instruction' and 'output' values
def get_instruction_and_output():
    global data
    global left_key
    global right_key
    global data_index

    if data and isinstance(data, list) and 0 <= data_index < len(data):
        item = data[data_index]
        if left_key in item:
            instruction_value = str(item.get(left_key, ''))
        else:
            instruction_value = f'Item has no key {left_key}'

        if right_key in item:
            output_value = str(item.get(right_key, ''))
        else:
            output_value = f'Item has no key {right_key}'

        # Replace '\n' with actual line breaks
        instruction_value = instruction_value.replace('\\n', '\n')
        output_value = output_value.replace('\\n', '\n')

        return instruction_value, output_value
    else:
        return None, None

# Function to move the index forward
def move_index_forward():
    global data_index
    if data and isinstance(data, list) and data_index < len(data) - 1:
        data_index += 1
    yield f"Current index: {data_index}/{len(data)-1}"    

# Function to move the index backward
def move_index_backward():
    global data_index
    if data and isinstance(data, list) and data_index > 0:
        data_index -= 1

    yield f"Current index: {data_index}/{len(data)-1}"

def rewindzero():
    global data_index
    if data and isinstance(data, list) and data_index > 0:
        data_index = 0
    yield f"Current index: {data_index}/{len(data)-1}"

def set_instruction_and_output(instruction, output):
    global data
    global left_key
    global right_key
    global data_index

    if data and isinstance(data, list) and 0 <= data_index < len(data):
        # Replace line breaks with '\n'
        #formatted_instruction = instruction.replace('\n', '\\n')
        #formatted_output = output.replace('\n', '\\n')

        # Update the 'instruction' and 'output' values in the data
        item = data[data_index]
        if left_key in item:
            item[left_key] = str(instruction)
        if right_key in item:
            item[right_key] = str(output)


        # Optionally, save the updated data back to the JSON file if needed
        #save_updated_data_to_file()

def delete_current_item():
    global data
    global data_index

    if data and isinstance(data, list) and 0 <= data_index < len(data):
        # Delete the current item at data_index
        deleted_item = data.pop(data_index)

        # Optionally, save the updated data back to the JSON file if needed
        #save_updated_data_to_file()

        return deleted_item  # You can return the deleted item if you want

def insert_item():
    global data
    global left_key
    global right_key
    global data_index

    if data and isinstance(data, list) and 0 <= data_index <= len(data):
        # Replace line breaks with '\n'
        formatted_input = 'New input value'
        formatted_output = 'New output value'

        # Create a new item with 'left_key' and 'right_key' values
        new_item = {left_key: formatted_input, right_key: formatted_output}

        # Insert the new item at data_index
        data.insert(data_index, new_item)

        # Optionally, save the updated data back to the JSON file if needed
        #save_updated_data_to_file()


def save_updated_data_to_file():
    global data
    global current_input_file

    # Check if data is not None, current_input_file is not None, and is a list
    if data and current_input_file is not None and isinstance(data, list):

        if not Path('logs').exists():
            Path('logs').mkdir()

        filename = os.path.basename(current_input_file)
        filepath = Path(f'logs/{filename}')


        try:
            with open(filepath, 'w') as json_file:
                json.dump(data, json_file, indent=4)  # Save the updated data back to the file
            yield f"Updated JSON data saved to {filepath}.",filepath
        except FileNotFoundError:
            yield f"Error: File not found: {filepath}.",None
        except json.JSONDecodeError:
            yield f"Error: Invalid JSON data in file: {filepath}.",None
        except Exception as e:
            yield f"An error occurred while saving the data: {str(e)}.",None
    else:
        yield "No data to save or current input file is missing.",None

def save_updated_data_to_backup_file():
    global data
    global backup_file
    
    # Check if data is not None, current_input_file is not None, and is a list
    if data and isinstance(data, list):

        if not Path('logs').exists():
            Path('logs').mkdir()

        filename = "json_backup.json"
        backup_file = Path(f'logs/{filename}')


        try:
            with open(backup_file, 'w') as json_file:
                json.dump(data, json_file, indent=4)  # Save the updated data back to the file
            yield f"Updated JSON data saved to {backup_file}."
        except FileNotFoundError:
            yield f"Error: File not found: {backup_file}."
        except json.JSONDecodeError:
            yield f"Error: Invalid JSON data in file: {backup_file}."
        except Exception as e:
            yield f"An error occurred while saving the data: {str(e)}."
    else:
        yield "No data to save or current input file is missing."


def load_backup_data():
    global backup_file
    if backup_file:
        ret = load_json_data(backup_file)
        yield ret
    else:
        yield "No backup file has been created yet"


def create_delete_buttons(delete_function, outputs):
    del_button = gr.Button('Delete', elem_classes="small-button", variant='secondary')
    del_button_yes = gr.Button('Yes',visible=False, elem_classes="small-button", variant='stop')
    del_button_no = gr.Button('No',visible=False, elem_classes="small-button", variant='primary')

    def yes_no_show():
        return gr.update(visible = True),gr.update(visible = True)

    def yes_no_hide():
        return gr.update(visible = False),gr.update(visible = False)

    del_button.click(yes_no_show,None,[del_button_yes,del_button_no])

    del_button_yes.click(delete_function,None,None).then(yes_no_hide,None,[del_button_yes,del_button_no]).then(
        get_instruction_and_output,None,outputs) #[left_text,right_text]

    del_button_no.click(yes_no_hide,None,[del_button_yes,del_button_no])

    return del_button, del_button_yes, del_button_no    

def ui():
    global params

    with gr.Row():
        with gr.Column():
            with gr.Row():
                with gr.Column():
                    upload_session_file = gr.File(type='file', file_types=['.json'], label='Load JSON')
                    with gr.Row():    
                        json_file = gr.Textbox(label="JSON File", value='')
                        json_file_load = gr.Button("Load JSON",elem_classes="small-button",  variant='primary')
                with gr.Column():
                    instruct = gr.Markdown('load file')
    
    with gr.Row():
        with gr.Column():
            left_key_name = gr.Textbox(label="Key", value= left_key, lines=1)
            left_text = gr.Textbox(label="Input", value='', lines=10)
        with gr.Column():
            right_key_name = gr.Textbox(label="Key", value= right_key,  lines=1)
            right_text = gr.Textbox(label="Otput", value='',  lines=10)
    with gr.Row():
        with gr.Column():
            with gr.Row():
                prev_prevbtn = gr.Button('<<', variant='primary')
                prev_nextbtn = gr.Button('>>',variant='primary')
            with gr.Row():
                with gr.Accordion("Tools"):   
                    with gr.Row():
                        rewind_btn = gr.Button('Go to First item', elem_classes="small-button")
                        find_next = gr.Button('Next 50% I/R Diff', elem_classes="small-button") 
                        calc_max_token = gr.Button('Find longest item', elem_classes="small-button")   
                    with gr.Row():
                        length_char = gr.Slider(label='Number of characters [NC]', minimum=1, maximum=2048, value=256, step=1)
                        find_min_char = gr.Button("[Result] Less than NC", elem_classes="small-button", variant='secondary')
                        find_max_char = gr.Button("[Result] More than NC", elem_classes="small-button", variant='secondary')    
                    with gr.Row():
                        search_text = gr.Textbox(label='Search', value='', lines=1)
                        searchA = gr.Button("In Instruction", elem_classes="small-button", variant='secondary')
                        searchB = gr.Button("In Result", elem_classes="small-button", variant='secondary')
                        searchAB = gr.Button("In Instr or Result", elem_classes="small-button", variant='secondary')
                    

        with gr.Column():
            with gr.Row():
                insert_button = gr.Button('Insert', elem_classes="small-button", variant='secondary')
                del_button = gr.Button('Delete', elem_classes="small-button", variant='secondary')
                del_button_yes = gr.Button('Yes',visible=False, elem_classes="small-button", variant='stop')
                del_button_no = gr.Button('No',visible=False, elem_classes="small-button", variant='primary')
                save_btn = gr.Button('Save JSON', elem_classes="small-button",variant='primary')
                save_file_down = gr.File(type='file', file_types=['.json'], visible = False)
            with gr.Row():
                backup_btn = gr.Button("Backup", elem_classes="small-button", variant='secondary')
                restore_btn = gr.Button("Restore", elem_classes="small-button", variant='secondary')
                restore_button_yes = gr.Button('Yes',visible=False, elem_classes="small-button", variant='stop')
                restore_button_no = gr.Button('No',visible=False, elem_classes="small-button", variant='primary')
 
    def file_dropped(file_obj):
        #file_obj.name orig_name
        global current_input_file
        if file_obj:
            name = file_obj.name
            current_input_file = name
            return name
        else:
            current_input_file = None
            return ''
                
    upload_session_file.change(file_dropped,upload_session_file,json_file)

    json_file_load.click(load_json_data,json_file,instruct).then(get_instruction_and_output,None,[left_text,right_text])

    def update_lk(lk):
        global left_key
        global right_key
        left_key = lk
        yield f"Keys: {first_item_keys} Updated Input key: {left_key}"


    left_key_name.change(update_lk,left_key_name,instruct,queue=False)

    def update_rk(rk):
        global right_key
        global left_key
        global first_item_keys

        right_key = rk
        yield f"Keys: {first_item_keys} Updated Output key: {right_key}"

    right_key_name.change(update_rk,right_key_name,instruct,queue=False)    

    prev_prevbtn.click(move_index_backward,None,instruct).then(get_instruction_and_output,None,[left_text,right_text])
    prev_nextbtn.click(move_index_forward,None,instruct).then(get_instruction_and_output,None,[left_text,right_text])
    
    def make_file_visible():
        return gr.update(visible = True)
    
    save_btn.click(save_updated_data_to_file,None,[instruct,save_file_down]).then(make_file_visible,None,save_file_down)

    left_text.change(set_instruction_and_output,[left_text,right_text],None)
    right_text.change(set_instruction_and_output,[left_text,right_text],None)

    def yes_no_show(text = ''):
        return gr.update(visible = True),gr.update(visible = True),text

    def yes_no_hide():
        return gr.update(visible = False),gr.update(visible = False)

    del_button.click(partial(yes_no_show, text='Delete current item?'),None,[del_button_yes,del_button_no,instruct])

    del_button_yes.click(delete_current_item,None,None).then(yes_no_hide,None,[del_button_yes,del_button_no]).then(
        get_instruction_and_output,None,[left_text,right_text])
    
    del_button_no.click(yes_no_hide,None,[del_button_yes,del_button_no])

    insert_button.click(insert_item,None,None).then(get_instruction_and_output,None,[left_text,right_text])

    rewind_btn.click(rewindzero,None,instruct).then(get_instruction_and_output,None,[left_text,right_text])

    find_next.click(find_next_diff,None,instruct).then(get_instruction_and_output,None,[left_text,right_text])


    find_min_char.click(find_min_char_diff,length_char,instruct).then(get_instruction_and_output,None,[left_text,right_text])
    find_max_char.click(find_max_char_diff,length_char,instruct).then(get_instruction_and_output,None,[left_text,right_text])


    calc_max_token.click(calc_max_token_fn,None,instruct).then(get_instruction_and_output,None,[left_text,right_text])

    searchA.click(search_and_update_data_index,search_text,instruct).then(get_instruction_and_output,None,[left_text,right_text])
    searchB.click(search_and_update_data_index2,search_text,instruct).then(get_instruction_and_output,None,[left_text,right_text])
    searchAB.click(search_and_update_data_index3,search_text,instruct).then(get_instruction_and_output,None,[left_text,right_text])

    backup_btn.click(save_updated_data_to_backup_file,None,instruct)
    #restore_btn.click(load_backup_data,None,instruct).then(get_instruction_and_output,None,[left_text,right_text])

    restore_btn.click(partial(yes_no_show, text='Restore from backup?'),None,[restore_button_yes,restore_button_no,instruct])

    restore_button_yes.click(load_backup_data,None,instruct).then(yes_no_hide,None,[restore_button_yes,restore_button_no]).then(
        get_instruction_and_output,None,[left_text,right_text])
    
    restore_button_no.click(yes_no_hide,None,[restore_button_yes,restore_button_no])
