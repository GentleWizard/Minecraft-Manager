# pip install -r requirements.txt
# import logging
import webbrowser
import requests
import json
import tkinter as tk
import urllib.request
import io
from PIL import Image, ImageTk


# Function to update the available versions based on whether snapshots are selected or not
response = requests.get("https://meta.fabricmc.net/v2/versions/game")
version_data = response.json()

# Get stable versions
versions = [v["version"] for v in version_data if v["stable"]]

# Sorting options
sort_options = ["relevance", "downloads", "updated", "newest"]
type_options = ["mod", "modpack", "resourcepack", "shader"]
loader_options = ["fabric", "forge", "quilt"]

# Pagination
offset = 0
itterations = 0
button_data_list = {}
Wiki_data_list = {}
image_data_list = []


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


def sort_changed(*args):
    global selected_sort_final
    selected_sort_final = selected_sort.get()
    print(f'Selected Version: {selected_sort_final}')


def type_changed(*args):
    global selected_type_final
    selected_type_final = selected_type.get()
    print(f'Selected Version: {selected_type_final}')


def loader_changed(*args):
    global selected_loader_final
    selected_loader_final = loader_type.get()
    print(f'Selected Version: {selected_loader_final}')


# Function called when the user clicks the search button
def search_button_fix():
    global offset
    offset = 0
    search_modrinth()


data = []
searched = False


def search_modrinth(*args):
    global results_frame, itterations, button_data_list, Wiki_data_list, image_data_list
    if itterations > 0:
        results_frame.destroy()
        results_frame = tk.Frame(root, background="gray")
        results_frame.pack(fill="both")
        button_data_list = {}
        Wiki_data_list = {}
        image_data_list = []
        itterations = 0
        search_modrinth()
    else:
        try:
            global data, hit, total, searched
            facets = f'[["versions:{selected_version_final}"], ["project_type:{selected_type_final}"],["categories:{selected_loader_final}"]]'
            api_endpoint = "https://api.modrinth.com/v2/search"
            search_params = {
                "query": query_textbox_final,
                "index": selected_sort_final,
                "facets": facets,
                "limit": 3,
                "offset": offset,
            }
            # Make the request to the API
            response = requests.get(api_endpoint, params=search_params)
            data = json.loads(response.content)
            hit = data["hits"]
            total = data["total_hits"]

            print(
                f"-----------------\nSelected version: {selected_version_final}\nSelected sort: {selected_sort_final}\nQuery: {query_textbox_final}\nProject Type: {selected_type_final}\nLoader: {selected_loader_final}\n-----------------")
            display_results(data)
            page_number_func(offset)
            print(offset)
            searched = True
            return
        except NameError:
            on_Load_app()
            return


def on_Load_app():
    global button_data_list, Wiki_data_list, image_data_list, itterations, results_frame
    if itterations > 0:
        results_frame.destroy()
        results_frame = tk.Frame(root, background="gray")
        results_frame.pack(fill="both")
        button_data_list = {}
        Wiki_data_list = {}
        image_data_list = []
        itterations = 0
        on_Load_app()
    else:
        global data, hit, total, searched
        version = versions[0]
        project_type = "mod"
        loader_type = "fabric"
        facets = f'[["versions:{version}"], ["project_type:{project_type}"],["categories:{loader_type}"]]'
        api_endpoint = f"https://api.modrinth.com/v2/search"
        search_params = {
            "index": "relevance",
            "facets": facets,
            "limit": 3,
            "offset": offset,
        }
        response = requests.get(api_endpoint, params=search_params)
        data = json.loads(response.content)
        total = data["total_hits"]
        hit = data["hits"]
        print(offset)
        searched = True
        display_results(data)
        page_number_func(offset)


def download_version_changed(*args):
    global selected_download_version_final
    selected_download_version_final = selected_version.get()
    print(f'Selected Version: {selected_download_version_final}')


def download_file(url, name):
    print(f"Downloading {name} from {url}")


def Download(index):
    # modal widget to download mod
    Download_modal = tk.Toplevel(results_frame)
    Download_modal.title("Download")
    Download_modal.geometry("300x200")
    data = button_data_list[index]
    slug = data[0]
    title = data[1]

    project_id = slug
    api_endpoint = f"https://api.modrinth.com/v2/project/{project_id}/version"
    response = requests.get(api_endpoint)
    data_download = json.loads(response.content)

    download_label = tk.Label(Download_modal, text=f"Downloading: {title}")
    download_label.pack()
    dependency_info = []
    version_info = []
    # for version in data_download:
    #     if selected_version_final in version["game_versions"]:
    #         if selected_loader_final in version["loaders"]:
    #             version_name = version["name"]
    #             version_number = version["version_number"]
    #             loader = version["loaders"]
    #             for depends in version["dependencies"]:
    #                 if version_number[version_number] == version_id:
    #                     print(f"Processing dependency: {depends}")
    #                     dependency_info.append({
    #                         "dependency_type_dep": depends["dependency_type"],
    #                         "project_id_dep": depends["project_id"],
    #                         "version_id_dep": depends["version_id"],
    #                         "file_name_dep": depends["file_name"]
    #                     })
    #                     api_mod_endpoint = f"https://api.modrinth.com/v2/project/{dependency_info[0]}/version"
    #                     response_mod = requests.get(api_mod_endpoint)
    #                     data_mod = json.loads(response_mod.content)
    #                     if dependency_info[0] == "required":
    #                         for version_mod in data_mod:
    #                             version_id = version_mod["version_id"]
    #                             if dependency_info[2] == version_id:
    #                                 print(dependency_info[2])
    #                                 file_url_mod = version_mod["files"][0]["url"]
    #                                 file_name_mod = version_mod["files"][0]["filename"]
    #                                 for dependantcies in dependency_info:
    #                                     print(dependantcies["version_name"])
    #                                     dependantcies_download_button = tk.Button(
    #                                         Download_modal, text=f"Download: {dependantcies['version_name']}", command=lambda: download_file(file_url_mod, file_name_mod))
    #                                     version_mod_label = tk.Label(
    #                                         text=f":Dependency: {dependantcies['version_name']}")
    #                                     version_mod_label.pack()
    #             for file in version["files"]:
    #                 file_url = file["url"]
    #                 file_name = file["filename"]

    #                 version_info.append({
    #                     "name": version_name,
    #                     "version_number": version_number,
    #                     "file_url": file_url,
    #                     "file_name": file_name
    #                 })

    version_number = [info["version_number"] for info in version_info]
    selected_version = tk.StringVar(root)
    selected_version.set(version_number[0])
    download_dropdown = tk.OptionMenu(
        Download_modal, selected_version, *version_number)
    download_dropdown.config(font=("Arial"))
    download_dropdown.pack()

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


def display_results(data):
    for (i, hit) in enumerate(data["hits"]):
        global project_data, results, results_frame_list, itterations
        itterations += 1
        print(f"mod: {i + 1} of {len(data['hits'])} Loaded")
        # Create a frame for the search results
        results = tk.Frame(results_frame, pady=6, border=1,
                           relief="solid", background="gray")
        get_project = f"https://api.modrinth.com/v2/project/{hit['slug']}"
        response = requests.get(get_project)
        project_data = json.loads(response.content)

        # Display the mod title
        results_Title = tk.Label(results, state="normal", wraplength=500, justify="left",
                                 anchor="nw", text=f'{hit["title"]}', background="gray",
                                 font=("Arial", 12, "bold"), fg="white", padx=10)
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
                                      width=50, border=0, font=("Arial", 10, "bold"), padx=10, fg="white", background="#999999")
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
        button_data_list[i] = hit["slug"], hit["title"]
        results_download_button = tk.Button(
            results, text=f"Download", background="lightgray", command=lambda index=i: Download(index))
        results_download_button.pack(side="right", padx=3)

        # pack the results frame
        results.pack(fill="both")


def page_number_func(offset):
    global page_number, rounded_page
    if offset == 0:
        rounded_page = 1
    else:
        page = 1 + ((offset - 1) / 3)
        rounded_page = round(page)

    if 'page_number' not in globals() or not page_number.winfo_exists():
        page_number = tk.Label(nav_frame)
        page_number.pack(side="left", padx=280)
    else:
        page_number.destroy()
        page_number = tk.Label(nav_frame)
        page_number.pack(side="left", padx=280)
    page_number_nums = f'{rounded_page} / {int(total / 3)}'
    page_number.config(text=page_number_nums, background="#84898D",
                       height=1, width=5, font=("Arial", 10, "bold"))
    return


def next_page():
    global offset
    if rounded_page == int(total / 3):
        return
    elif searched == True:
        offset += 3
        search_modrinth()
    else:
        on_Load_app()


def previous_page():
    global offset
    if offset == 0:
        return
    else:
        offset -= 3
        search_modrinth()


# Define window dimensions
window_width = 700
window_height = 497

# Create the root window and get screen dimensions
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate screen position of root window
screen_y = (screen_height - window_height)
screen_x = (screen_width // 2 - window_width)

# Configure root window settings
root.geometry(f"700x497+{screen_y}+{screen_x}")
root.minsize(700, 497)
root.maxsize(700, 497)
root.configure(background="gray")

# Create frames for search results, navigation, and search bar
results_frame = tk.Frame(root, background="gray")
nav_frame = tk.Frame(root, background="#84898D", relief="solid", borderwidth=1)
search_frame = tk.Frame(root, width=700, height=100,
                        background="#84898D", relief="solid", borderwidth=1)

# Create a label and dropdown menu for selecting Minecraft version
selected_version = tk.StringVar()
selected_version.set(versions[0])
version_dropdown = tk.OptionMenu(search_frame, selected_version, *versions)
version_dropdown.config(background="#ACB3B8", relief="raised",
                        borderwidth=1, highlightthickness=0, font=("Arial", 10, "bold"))
selected_version.trace("w", version_changed)
selected_version_final = selected_version.get()

# Create a textbox for entering search queries
query_textbox = tk.StringVar()
query_textbox.trace("w", query_changed)
query_text = tk.Entry(search_frame, textvariable=query_textbox,
                      width=30, font=("Arial", 10, "bold"))

# Create a button to perform the mod search
search_button = tk.Button(search_frame, text="Search",
                          command=search_button_fix, background="#ACB3B8", font=("Arial", 10, "bold"))

# Create dropdown menus for sorting and filtering search results
selected_sort = tk.StringVar()
selected_sort.set(sort_options[0])
sort_dropdown = tk.OptionMenu(search_frame, selected_sort, *sort_options)
sort_dropdown.config(background="#ACB3B8", relief="raised",
                     borderwidth=1, highlightthickness=0, font=("Arial", 10, "bold"))
selected_sort.trace("w", sort_changed)
selected_sort_final = selected_sort.get()

selected_type = tk.StringVar()
selected_type.set(type_options[0])
type_dropdown = tk.OptionMenu(search_frame, selected_type, *type_options)
type_dropdown.config(background="#ACB3B8", relief="raised",
                     borderwidth=1, highlightthickness=0, font=("Arial", 10, "bold"))
selected_type.trace("w", type_changed)
selected_type_final = selected_type.get()

loader_type = tk.StringVar()
loader_type.set(loader_options[0])
loader_dropdown = tk.OptionMenu(search_frame, loader_type, *loader_options)
loader_dropdown.config(background="#ACB3B8", relief="raised",
                       borderwidth=1, highlightthickness=0, font=("Arial", 10, "bold"))
loader_type.trace("w", loader_changed)
loader_type_final = loader_type.get()
loader_changed()

# Create navigation buttons and page number label
prev_page_button = tk.Button(
    nav_frame, text="<<", background="#ACB3B8", command=previous_page, width=5, height=1, font=("Arial", 10, "bold"))
next_page_button = tk.Button(
    nav_frame, text=">>", background="#ACB3B8", command=next_page, width=5, height=1, font=("Arial", 10, "bold"))


# Pack navigation widgets into their frame
next_page_button.pack(side="right")
prev_page_button.pack(side="left")

# Pack search bar widgets into their frame
sort_dropdown.pack(side="left", padx=4)
type_dropdown.pack(side="left", padx=0)
version_dropdown.pack(side="left", padx=4)
search_button.pack(side='right', padx=4)
query_text.pack(side="right", padx=4)
loader_dropdown.pack(side="left", padx=0)

# Pack search bar and search results frames, and navigation frame at the bottom
search_frame.pack(fill="both", side="top")
results_frame.pack(fill="both")
nav_frame.pack(fill="both", side="bottom")

on_Load_app()
root.mainloop()
