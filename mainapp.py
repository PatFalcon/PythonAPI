import tkinter as tk
from tkinter import Entry, Button, Text, Scrollbar
from PIL import Image, ImageTk
import io
import requests
from tkinter import Toplevel
from tkinter import Toplevel, PhotoImage

#Insertion of API key
api_key = 'f1fa20e6d1718e55f14cfde6a6f78883'
base_url = 'https://api.themoviedb.org/3'

#Global variable to store the PhotoImage
current_poster = None

def search_movie(query):
    search_endpoint = '/search/movie'
    params = {'api_key': api_key, 'query': query}

    response = requests.get(base_url + search_endpoint, params=params)
    data = response.json()

    if 'results' in data:
        return data['results']
    else:
        return None

#Search Function 
def on_search():
    global search_results, current_index
    query = entry.get()
    search_results = search_movie(query)

    result_text.delete(1.0, tk.END) 
    description_text.delete(1.0, tk.END)
    current_index = 0 

    if search_results:
        display_movie(search_results[current_index])
    else:
        result_text.insert(tk.END, f"No results found for '{query}'")

#Display the movie details
def display_movie(movie):
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Title: {movie['title']} \nRelease Date: {movie['release_date']}")

    #Display the movie description in the new output box
    description_text.delete(1.0, tk.END)
    description_text.insert(tk.END, f"Description: {movie['overview']}")

    #Display the movie poster in the new output box
    display_movie_poster(movie['poster_path'])

#Function to display the movie poster
def display_movie_poster(poster_path):
    global current_poster

    if poster_path:
        poster_url = f"https://image.tmdb.org/t/p/original{poster_path}"
        response = requests.get(poster_url, stream=True)
        
        #Use Pillow to open and resize the image
        img = Image.open(io.BytesIO(response.content)).resize((200, 300))
        
        #Convert Pillow image to PhotoImage
        current_poster = ImageTk.PhotoImage(img)

        #Clear previous poster
        poster_label.config(image=None)
        
        poster_label.image = None

        #Display the new poster
        poster_label.config(image=current_poster)
        poster_label.image = current_poster

#Function to show the next movie
def show_next_movie():
    global current_index
    current_index += 1
    if current_index < len(search_results):
        display_movie(search_results[current_index])
    else:
        result_text.delete(1.0, tk.END)
        description_text.delete(1.0, tk.END)
        poster_label.config(image=None)
        poster_label.image = None
        result_text.insert(tk.END, "End of list reached")

#Function to show the previous movie
def show_previous_movie():
    global current_index
    current_index -= 1
    if current_index >= 0:
        display_movie(search_results[current_index])
    else:
        result_text.delete(1.0, tk.END)
        description_text.delete(1.0, tk.END)
        poster_label.config(image=None)
        poster_label.image = None
        result_text.insert(tk.END, "First movie displayed")

#Button for new window (About)
def open_new_window():
    new_window = Toplevel(window)
    new_window.title("About")
    new_window.geometry("900x700")
    new_window.config(bg="#717170")

    #Text heading
    About_text = tk.Label(new_window, text="About", font=("Overpass Mono", 40, "bold"), bg="#717170", fg="white")
    About_text.pack(padx=20, pady=0)

    #Load and display of image
    image_path = "coin.png"
    img = PhotoImage(file=image_path)

    image_label = tk.Label(new_window, image=img, bg="#717170", height=600, width=600)
    image_label.image = img
    image_label.place(x=100, y=3)

    #Description
    description_text = tk.Text(new_window, height=5, width=50, wrap=tk.WORD, bg="#717170", fg="white", font=("Overpass Mono", 10, "bold"))
    description_text.insert(tk.END, "Look4Movies is developed by John Patrick Falcon.\nSearching movies made convenient, made by movie lovers for movie lovers.")
    description_text.pack(padx=20, pady=20)
    description_text.place(x=250, y=530)

    #Close button
    close_button = tk.Button(new_window, text="Close", command=new_window.destroy, font=("Overpass Mono", 10, "bold"), bg="#ce7901", fg="white", width=10, height=1)
    close_button.pack(padx=20, pady=20)
    close_button.place(x=750, y=650)

#Window setup
window = tk.Tk()
window.title("Look4Movies by Pats")
window.resizable(0, 0)
window.geometry("900x700")
window.config(bg="#717170")

#User entry field
entry_label = tk.Label(window, text="Enter Movie Title:", fg="white", bg="#717170")
entry_label.place(x=356, y=175)
entry = Entry(window, width=30)
entry.place(x=356, y=210)

#Navbar
Navbar = tk.Label(window, fg="white", bg="#ff990a", width=200, height=10)
Navbar.pack(side='left', padx=20, pady=20)
Navbar.place(x=0, y=10)

#Text on top of Navbar
navbar_text = tk.Label(window, text="Look4Movies", fg="white", bg="#ff990a", font=("Overpass Mono", 40, "bold"))
navbar_text.pack(side='left', padx=20, pady=20)
navbar_text.place(x=50, y=60)

#Button to open a new window
new_window_button = tk.Button(window, text="About", command=open_new_window,font=("Overpass Mono", 10, "bold"), bg="#ce7901", fg="white", width=10, height=1)
new_window_button.pack(pady=10)
new_window_button.place(x=700, y=200)

#Search button function
search_button = Button(window, text="Search", command=on_search,font=("Overpass Mono", 10, "bold"), bg="#ce7901", fg="white", width=10, height=1)
search_button.pack(pady=10)
search_button.place(x=580, y=200)

#Title Display function
result_text = Text(window, height=5, width=40, wrap=tk.WORD)
result_text.pack(side='top', anchor='ne', padx=10, pady=10)
result_text.place(x=356, y=250)

#Movie Description function
description_text = Text(window, height=15, width=60, wrap=tk.WORD)
description_text.pack(pady=10)
description_text.place(x=356, y=340)

#Next and Previous buttons
next_button = tk.Button(window, text=">", command=show_next_movie, width=3, height=1, bg="#ce7901", fg="white",font=("Overpass Mono", 10, "bold"))
next_button.pack(side='right', padx=20, pady=70)
next_button.place(x=650, y=600)
previous_button = tk.Button(window, text="<",command=show_previous_movie, width=3, height=1, bg="#ce7901", fg="white", font=("Overpass Mono", 10, "bold"))
previous_button.pack(side='right', padx=20, pady=70)
previous_button.place(x=560, y=600)

#Poster display label
poster_label = tk.Label(window, bg="#717170")
poster_label.pack(side='left', padx=20, pady=20)
poster_label.place(x=80, y=215)

#Global variables
current_index = 0
search_results = []

#Start the main loop
window.mainloop()
