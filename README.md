# JSON_edit

extension to edit json datasets with search etc - WIP


![image](https://github.com/FartyPants/JSON_edit/assets/23346289/1e849aa8-1f8a-4ba8-882f-35362f36bc9e)


The extension JSON_edit is a WebUI extension for editing JSON datasets, primarily focusing on instruction and output keys (or user-defined keys). Many of its functionalities are tied to buttons that act as "tools" to navigate, analyze, and modify the data.
Getting Started: Loading Your Data
Load JSON (upload_session_file & json_file_load):
How to Use: You have two ways to load your JSON file:
Drag & Drop: Drag your .json file directly onto the "Load JSON" file upload area. The file path will appear in the "JSON File" textbox.
Browse: Click the "Load JSON" area to open a file browser and select your .json file. The path will appear in the "JSON File" textbox.
Action: Once the file path is in the "JSON File" textbox, click the "Load JSON" button.
What it Does: This loads your entire JSON dataset into the editor. The "Instruct" markdown area will confirm successful loading and list the main keys found in your data (e.g., instruction, output). The first item of your dataset will immediately appear in the "Input" and "Output" textboxes. The "Position" slider will also update to show your current place and the total number of items.
2. Basic Navigation and Editing
Input/Output Textboxes (left_text, right_text):
How to Use: These are the main areas where you see and edit your data.
"Input": Displays the content of the left_key (default: 'instruction').
"Output": Displays the content of the right_key (default: 'output').
Action: You can directly type or paste text into these boxes.
What it Does: Any changes you make here are saved in memory for the current item. To make these changes permanent, you'll need to save the file (see "Saving Your Work").
Customizing Keys (left_key_name, right_key_name):
How to Use: If your JSON uses different key names than 'instruction' and 'output' (e.g., 'prompt' and 'response'), you can change them here before loading JSON
Action: Type the correct key names into the "Key" textboxes above the "Input" and "Output" areas before Load JSON
Move Forward ( >> button prev_nextbtn):
What it Does: Moves you to the next item in your dataset. The "Input" and "Output" boxes will update, and the "Instruct" area will show your current index.
Move Backward ( << button prev_prevbtn):
What it Does: Moves you to the previous item in your dataset. The "Input" and "Output" boxes will update, and the "Instruct" area will show your current index.
Go to First item (rewind_btn):
What it Does: Instantly jumps you to the very first item (index 0) in your dataset.
Position Slider (gr_sliderPos):
What it Does: Allows you to quickly jump to any specific item by its index in the dataset. Useful for navigating large files.
Insert (insert_button):
What it Does: Inserts a new, blank entry at your current position. The new entry will have "New input value" and "New output value" placeholders.
Delete (del_button and confirmation buttons):
How to Use: Click the "Delete" button. You will then see "Yes" and "No" confirmation buttons.
What it Does: If you click "Yes", the currently displayed item will be permanently removed from your dataset (in memory). Clicking "No" cancels the operation.
3. Saving and Backing Up Your Work
Save JSON (save_btn):
What it Does: Saves all your in-memory changes to the original JSON file you loaded. A copy is also saved in a logs folder (e.g., logs/your_file_name.json). The "Save JSON" button will temporarily turn into a download link for the saved file.
Important: Always save regularly to avoid losing work!
Backup (backup_btn):
What it Does: Creates a snapshot of your entire current dataset and saves it to logs/json_backup.json.
Recommendation: Use this before performing any large-scale deletions or modifications, as it's a quick way to create a safety net.
Restore (restore_btn and confirmation buttons):
How to Use: Click the "Restore" button. You will then see "Yes" and "No" confirmation buttons.
What it Does: If you click "Yes", it loads the last logs/json_backup.json file, overwriting your current in-memory dataset with the backup's content. Clicking "No" cancels.
Use Case: If you make a mistake with a bulk operation or simply want to revert to a previous state, this is your undo button.
4. Advanced Tools: Cleaning and Analyzing Your Data
These tools are found in the "Tools" accordion.
A. Finding and Deleting Based on Length Differences
These are great for finding entries where the "Input" and "Output" are vastly different in length, which can indicate issues like:
Incomplete responses
Prompts without answers
Badly formatted data
Next 50% I/R Diff (find_next):
How to Use: Click this button.
What it Does: Scans forward from your current position to find the next item where the character length of one field (Input or Output) is less than 50% (half) of the other field's length.
Example: If Input is 100 characters and Output is 40 characters (40% of 100), this will find it. If Input is 100 and Output is 60, it won't.
[DEL] All 50% I/R Diff (del_find_next):
How to Use: Click this button.
What it Does: WARNING: This will delete entries. It first creates a backup of your dataset, then finds all items in the entire dataset that match the "50% I/R Diff" criterion and deletes them.
Recommendation: Use "Backup" before running this!
Next THR I/R Diff (find_next75) & THR Slider (next_threshold):
How to Use: Adjust the "THR" slider (Threshold) to your desired percentage (e.g., 0.75 for 75%). Then, click the "Next THR I/R Diff" button.
What it Does: Similar to the 50% difference, but it finds the next item where the length of the shorter field is less than or equal to your specified "THR" percentage of the longer field.
Example: If THR is 0.75 (75%), and Input is 100 characters, it will find items where Output is 75 characters or less (or vice-versa). Lowering the THR finds more extreme differences.
[DEL] ALL THR I/R Diff (del_find_next75):
How to Use: Adjust the "THR" slider. Then, click this button.
What it Does: WARNING: This will delete entries. It first creates a backup, then finds all items in the entire dataset that match the length difference criterion based on your current "THR" setting and deletes them.
Recommendation: Use "Backup" before running this!
B. Finding Based on Character Length
Number of characters [NC] Slider (length_char):
How to Use: Set the desired character length using this slider.
[I/R] Less than NC (find_min_char):
How to Use: Set the "NC" slider, then click this button.
What it Does: Finds the next item where either the Input or the Output field has fewer characters than the "NC" value. Useful for identifying extremely short or potentially incomplete entries.
[I/R] More than NC (find_max_char):
How to Use: Set the "NC" slider, then click this button.
What it Does: Finds the next item where either the Input or the Output field has more characters than the "NC" value. Useful for finding very long entries that might exceed model context limits or contain extraneous information.
C. Specific Content Search
Search Textbox (search_text):
How to Use: Type the text you want to find into this box.
In Instruction (searchA):
How to Use: Enter search text, then click this button.
What it Does: Finds the next item where your search_text appears in the "Input" field.
In Result (searchB):
How to Use: Enter search text, then click this button.
What it Does: Finds the next item where your search_text appears in the "Output" field.
In Instr or Result (searchAB):
How to Use: Enter search text, then click this button.
What it Does: Finds the next item where your search_text appears in either the "Input" or "Output" field.
D. Data Analysis and Transformation
Find longest item (calc_max_token):
How to Use: Click this button.
What it Does: Scans your entire dataset to find the item (the combined length of Input + Output) that has the most characters. It then jumps to that item. It also tries to estimate the total token count for that item, which is crucial for ensuring your data fits within an AI model's context window.
Swap all <<->> (swap_in_out):
How to Use: Click this button.
What it Does: WARNING: This performs a bulk modification. It swaps the content of the "Input" and "Output" fields for every single item in your entire dataset.
Use Case: Extremely useful if your dataset was accidentally generated with instructions and outputs reversed.
Recommendation: Use "Backup" before running this!
Repeating Words (find_repeated):
How to Use: Click this button.
What it Does: Scans forward from your current position to find the next item where either the "Input" or "Output" field contains words that repeat consecutively (e.g., "the the the"). This can help identify artifacts or poor quality in generated text.

General Tips:
Watch the "Instruct" Area: This area provides feedback on actions, current index, and search results.
Progress Indicators: Most actions will briefly show a "Loading" or "Running" message.
Saving is Key: Remember that changes are only saved to your file when you click "Save JSON." Use "Backup" for extra safety before large operations.
