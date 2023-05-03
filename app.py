import requests
import json
import tkinter as tk
import time

# Function to update the available versions based on whether snapshots are selected or not
response = requests.get("https://meta.fabricmc.net/v2/versions/game")
data = response.json()
versions = [v["version"] for v in data if v["stable"]]

def clear_text(*args):
    for text_widget in args:
        text_widget.delete("1.0", tk.END)


# Function called when the user changes the value in the search query textbox
def query_changed(*args):
    global query_textbox_final
    query_textbox_final = query_textbox.get()
    print(f'Search Query: {query_textbox_final}')
    return query_textbox

# Function called when the user changes the value in the version dropdown menu
def version_changed(*args):
    global selected_version_final
    selected_version_final = selected_version.get()
    print(f'Selected Version: {selected_version_final}')
    return selected_version

# Function to perform the mod search and display the results
def search(*args):
    global query_textbox_final, selected_version_final
    search_results_text.config(state="normal")
    api_endpoint = "https://api.modrinth.com/v2/search"
    search_params = {
        "query": query_textbox_final,
        "game_versions": selected_version_final,
        "project_type": "mod",
        "index": "relevance",
        "limit": 5,
    }

    response = requests.get(api_endpoint, params=search_params)
    data = json.loads(response.content)
    
    if not data["hits"]:
        search_results_text.delete("1.0", tk.END)  # clear previous search results
        search_results_text.config(state="disabled")
        return 
    
    
    clear_text(search_results_text)  # clear previous search results
    search_results_text.insert(tk.END, "Search Results:\n------------------------------\n")
    for hit in data["hits"]:
        search_results_text.insert(tk.END, f'Title: {hit["title"]}\n')
        search_results_text.insert(tk.END, f'Description: {hit["description"]}\n')
        search_results_text.insert(tk.END, f'Downloads: {hit["downloads"]}\n')
        search_results_text.insert(tk.END, f'Client Side: {hit["client_side"]}\n')
        search_results_text.insert(tk.END, f'Server Side: {hit["server_side"]}\n')
        search_results_text.insert(tk.END, '------------------------------\n')
    print(data)
    search_results_text.config(state="disabled")

# Create the root window
root = tk.Tk()
root.geometry("700x500")

# Create frames for search bar and search results
result_frame = tk.Frame(root)
search_frame = tk.Frame(root)


# Create a label and dropdown menu for selecting Minecraft version
version_label = tk.Label(search_frame, text="Select version:")
selected_version = tk.StringVar()
selected_version.set(versions[0])
version_dropdown = tk.OptionMenu(search_frame, selected_version, *versions)
selected_version.trace("w", version_changed)
selected_version_final = selected_version.get()

# Create a textbox for entering search queries
query_textbox = tk.StringVar()
query_textbox.trace("w", query_changed)
query_text = tk.Entry(search_frame, textvariable=query_textbox, width=50)

# Create a button to perform the mod search
search_button = tk.Button(search_frame, text="Search", command=search)

# Create a text widget for displaying search results
search_results_text = tk.Text(result_frame, state="disabled")

# Grid the search bar widgets
version_label.pack(side="left")
version_dropdown.pack(side="left")
query_text.pack(side="left")
search_button.pack(side='left')

# Place the search results text widget
search_results_text.pack(fill='both')

# Pack the search bar and search results frames
search_frame.pack(fill="both")
result_frame.pack(fill="both")

# Start the main event loop
root.mainloop()
