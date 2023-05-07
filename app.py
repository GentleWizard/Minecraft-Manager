# pip install -r requirements.txt
# import logging
import webbrowser
import requests
import json
import tkinter as tk
import urllib.request
from PIL import Image, ImageTk
import io


# Set up logging


# Function to update the available versions based on whether snapshots are selected or not
response = requests.get("https://meta.fabricmc.net/v2/versions/game")
data = response.json()
versions = [v["version"] for v in data if v["stable"]]
sort_options = ["relevance", "downloads", "updated", "newest"]
type_options = ["mod", "modpack", "resourcepack", "shader"]

# Function to clear the text in the search query textbox


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


def sort_changed(*args):
    global selected_sort_final
    selected_sort_final = selected_sort.get()
    print(f'Selected Version: {selected_sort_final}')
    return selected_sort


def type_changed(*args):
    global project_type
    selected_type_final = selected_type.get()
    print(f'Selected Version: {selected_type_final}')
    return selected_type


# Function called when the user clicks the search button


def search_modrinth(*args):
    global query_textbox_final, selected_version_final, data, hit, url, search_params
    facets = f'[["versions:{selected_version_final}"], ["project_type:{selected_type_final}"]]'
    api_endpoint = "https://api.modrinth.com/v2/search"
    search_params = {
        "query": query_textbox_final,
        "index": selected_sort_final,
        "facets": facets,
        "limit": 3,
    }
    # Make the request to the API
    response = requests.get(api_endpoint, params=search_params)
    data = json.loads(response.content)
    hit = data["hits"]
    print(
        f"Searching with: Selected version {selected_version_final}, Selected sort {selected_sort_final}, Query {query_textbox_final}, Project Type {selected_type_final}, Version {selected_version_final}")
    display_results(data)


def Download(index):
    # modal widget to download mod
    Download_modal = tk.Toplevel(results_frame)
    Download_modal.title("Download")
    Download_modal.geometry("300x200")

    data = button_data_list[index]
    title = data[0]
    version = data[1]

    Download_modal_label = tk.Label(Download_modal, text=f"{title}, {version}")
    Download_modal_label.pack(padx=20, pady=20)

    print(button_data_list[index])

    Download_modal.grab_set()
    Download_modal.mainloop()


def open_link(index):

    data = Wiki_data_list[index]
    # print(data)
    source_url = data[1]
    wiki_url = data[0]
    try:
        webbrowser.open(data[wiki_url])
        print("opening Wiki")
    except TypeError:
        webbrowser.open(source_url)
        print("opening Source")
    except Exception:
        print("Error")


button_data_list = {}
Wiki_data_list = {}
image_data_list = []


def display_results(data):
    # Function to display the search results
    for i, hit in enumerate(data["hits"]):
        global project_data, results, results_frame_list
        # Create a frame for the search results
        results = tk.Frame(results_frame, pady=6, border=1,
                           relief="solid", background="gray")
        get_project = f"https://api.modrinth.com/v2/project/{hit['slug']}"
        response = requests.get(get_project)
        project_data = json.loads(response.content)

        # Display the mod title
        results_Title = tk.Label(results, state="normal", wraplength=500, justify="left", anchor="nw",
                                 text=f'{hit["title"]}', background="gray", font=("Arial", 12, "bold"), fg="white", padx=10)
        results_Title.pack(expand=True)

        # Display the mod icon
        icons = hit["icon_url"]
        image_data_list.append(icons)
        url = image_data_list[i]

        req = urllib.request.Request(url, headers={
            'User-Agent': f'GentleWizard/{hit["title"]}/'})
        image_data = urllib.request.urlopen(req).read()
        image = Image.open(io.BytesIO(image_data))
        max_width = 100  # maximum width of the image
        max_height = 100  # maximum height of the image
        width, height = image.size
        aspect_ratio = width / height
        if width > height:
            width = min(width, max_width)
            height = int(width / aspect_ratio)
        else:
            height = min(height, max_height)
            width = int(height * aspect_ratio)
        image = image.resize((width, height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        results_image = tk.Label(results, image=photo)
        results_image.photo = photo
        results_image.pack(side="left", before=results_Title)

        # Display the mod description
        results_description = tk.Text(results, state="normal", wrap="word", height=5,
                                      width=50, border=0, font=("Arial", 10), padx=10, fg="white", background="#999999")
        results_description.insert(tk.END, f'{hit["description"]}')
        results_description.pack(fill="x", expand=True)
        results_description.config(state="disabled")

        # Display the mod downloads
        results_downloads = tk.Label(results, state="normal", wraplength=500, justify="left", anchor="nw",
                                     text=f'Downloads: {hit["downloads"]}', relief="solid", borderwidth=1, padx=5, background="lightgray")
        results_downloads.pack(side="left", padx=3)

        # Display weather the mod is client side
        results_client_side = tk.Label(results, state="normal", wraplength=500, justify="left", anchor="nw",
                                       text=f'Client Side: {hit["client_side"]}', relief="solid", borderwidth=1, padx=5, background="lightgray")
        results_client_side.pack(side="left", padx=3)

        # Display weather the mod is server side
        results_server_side = tk.Label(results, state="normal", wraplength=500, justify="left", anchor="nw",
                                       text=f'Server Side: {hit["server_side"]}', relief="solid", borderwidth=1, padx=5, background="lightgray")
        results_server_side.pack(side="left", padx=3,)

        # Display the mod wiki

        Wiki_data_list[i] = project_data["wiki_url"], project_data["source_url"]
        results_view_button = tk.Button(
            results, text="Wiki", background="lightgray", command=lambda index=i: open_link(index))
        results_view_button.pack(side="right", padx=3)

        # Display the mod download
        button_data_list[i] = hit["title"], hit["versions"][-1]
        results_download_button = tk.Button(
            results, text=f"Download", background="lightgray", command=lambda index=i: Download(index))
        results_download_button.pack(side="right", padx=3)

        # pack the results frame
        results.pack(fill="both")


def next_page():
    return


def previous_page():
    return


# Create the root window
root = tk.Tk()
root.geometry("700x500")
root.configure(background="gray")

results_frame = tk.Frame(root, background="gray")
nav_frame = tk.Frame(root, background="#84898D", relief="solid", borderwidth=1)
search_frame = tk.Frame(root, width=700, height=100,
                        background="#84898D", relief="solid", borderwidth=1)

# Create a label and dropdown menu for selecting Minecraft version
selected_version = tk.StringVar()
selected_version.set(versions[0])
version_dropdown = tk.OptionMenu(search_frame, selected_version, *versions)
version_dropdown.config(background="#ACB3B8", relief="raised",
                        borderwidth=1, highlightthickness=0, width=10)
selected_version.trace("w", version_changed)
selected_version_final = selected_version.get()

# Create a textbox for entering search queries
query_textbox = tk.StringVar()
query_textbox.trace("w", query_changed)
query_text = tk.Entry(search_frame, textvariable=query_textbox, width=30,)

# Create a button to perform the mod search
search_button = tk.Button(search_frame, text="Search",
                          command=search_modrinth, background="#ACB3B8")

selected_sort = tk.StringVar()
selected_sort.set(sort_options[0])
sort_dropdown = tk.OptionMenu(search_frame, selected_sort, *sort_options)
sort_dropdown.config(background="#ACB3B8", relief="raised",
                     borderwidth=1, highlightthickness=0)
selected_sort.trace("w", sort_changed)
selected_sort_final = selected_sort.get()

selected_type = tk.StringVar()
selected_type.set(type_options[0])
type_dropdown = tk.OptionMenu(search_frame, selected_type, *type_options)
type_dropdown.config(background="#ACB3B8", relief="raised",
                     borderwidth=1, highlightthickness=0)
selected_type.trace("w", type_changed)
selected_type_final = selected_type.get()

next_page_button = tk.Button(
    nav_frame, text=">>", background="#ACB3B8", command=next_page, width=5, height=1)
prev_page_button = tk.Button(
    nav_frame, text="<<", background="#ACB3B8", command=previous_page, width=5, height=1)
next_page_button.pack(side="right", padx=10)
prev_page_button.pack(side="left", padx=10)
# Pack the widgets in the search bar frame
sort_dropdown.pack(side="left", padx=2)
type_dropdown.pack(side="left", padx=2)
version_dropdown.pack(side="left", padx=2)
query_text.pack(side="left", padx=2)
search_button.pack(side='left')


# Pack the search bar and search results frames
search_frame.pack(fill="both", side="top")
results_frame.pack(fill="both")
nav_frame.pack(fill="both", side="bottom")

# Start the main event loop
root.mainloop()
