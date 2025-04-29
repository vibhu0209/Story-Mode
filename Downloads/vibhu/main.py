import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import pygame
import pyttsx3
import threading
import os
import time
import random
import json
from ttkthemes import ThemedTk
import customtkinter as ctk

class AustenStoryCreator:
    def __init__(self):
        self.setup_audio()
        self.load_story_elements()
        self.create_gui()
        self.current_story_state = {}
        
    def setup_audio(self):
        pygame.mixer.init()
        self.bg_music_paths = {
            "Romance": "music/romance.mp3",
            "Drama": "music/drama.mp3",
            "Mystery": "music/mystery.mp3",
            "Comedy": "music/comedy.mp3",
            "Tragedy": "music/tragedy.mp3"
        }
        
        try:
            # Test if text-to-speech is available
            engine = pyttsx3.init()
            engine.stop()
            self.voice_enabled = True
        except:
            self.voice_enabled = False
            
        self.music_playing = False
        self.voice_playing = False
        self.current_engine = None

    def load_story_elements(self):
        # Load story elements from JSON files
        with open('data/characters.json', 'r') as f:
            self.character_traits = json.load(f)
        with open('data/settings.json', 'r') as f:
            self.settings = json.load(f)
        with open('data/plots.json', 'r') as f:
            self.plot_elements = json.load(f)
            
        # Get the absolute path to the images directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(base_dir, 'images')
        
        print(f"Base directory: {base_dir}")
        print(f"Images directory: {images_dir}")
        
        # Verify images exist
        for theme in ["romance", "drama", "mystery", "comedy", "tragedy"]:
            image_path = os.path.join(images_dir, f"{theme}_bg.png")
            
            
        self.themes = {
            "Romance": {
                "color": "#fff0f5", 
                "image": os.path.join(images_dir, "romance_bg.png")
            },
            "Drama": {
                "color": "#fce4ec", 
                "image": os.path.join(images_dir, "drama_bg.png")
            },
            "Mystery": {
                "color": "#e0e0e0", 
                "image": os.path.join(images_dir, "mystery_bg.png")
            },
            "Comedy": {
                "color": "#e6f0ff", 
                "image": os.path.join(images_dir, "comedy_bg.png")
            },
            "Tragedy": {
                "color": "#fdf6e3", 
                "image": os.path.join(images_dir, "tragedy_bg.png")
            }
        }

    def create_gui(self):
        # Create themed window
        self.root = ThemedTk(theme="clearlooks")
        self.root.title("📚 The Austen Experience")
        self.root.geometry("1200x800")
        
        # Configure the root window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        
        # Create tabs
        self.create_story_tab()
        self.create_settings_tab()
        self.create_help_tab()
        
        # Bind resize event
        self.root.bind('<Configure>', self.on_window_resize)

    def create_story_tab(self):
        story_frame = ttk.Frame(self.notebook)
        self.notebook.add(story_frame, text="Create Story")
        
        # Configure story frame grid
        story_frame.grid_rowconfigure(1, weight=1)
        story_frame.grid_columnconfigure(0, weight=1)
        
        # Create header
        self.create_header(story_frame)
        
        # Create character creation section
        self.create_character_creation(story_frame)
        
        # Create story options section
        self.create_story_options(story_frame)
        
        # Create output area
        self.create_output_area(story_frame)
        
        # Create control panel
        self.create_control_panel(story_frame)

    def create_header(self, parent):
        header = ttk.Frame(parent)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        title = ttk.Label(header, 
                         text="The Austen Experience", 
                         font=("Playfair Display", 28, "bold"))
        title.grid(row=0, column=0, pady=(0,2))
        
        subtitle = ttk.Label(header,
                           text="Create your own Regency-era romance",
                           font=("Georgia", 14, "italic"))
        subtitle.grid(row=1, column=0, pady=(0,2))
        
        header.grid_columnconfigure(0, weight=1)

    def create_character_creation(self, parent):
        character_frame = ttk.LabelFrame(parent, 
                                       text="Character Creation",
                                       padding=(15, 5, 15, 15))
        character_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(5,10))
        
        # Heroine creation
        self.create_character_section(character_frame, "Heroine", 0)
        # Hero creation
        self.create_character_section(character_frame, "Hero", 1)

    def create_character_section(self, parent, char_type, row):
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, pady=5, sticky="ew")
        
        # Configure columns for better spacing
        for i in range(6):
            frame.grid_columnconfigure(i, weight=1)
        
        ttk.Label(frame, text=f"{char_type}'s Name:").grid(row=0, column=0, padx=5, sticky="e")
        name_entry = ttk.Entry(frame, width=20)
        name_entry.grid(row=0, column=1, padx=5, sticky="w")
        
        ttk.Label(frame, text="Personality:").grid(row=0, column=2, padx=5, sticky="e")
        personality = ttk.Combobox(frame, 
                                 values=self.character_traits["personalities"],
                                 width=20)
        personality.grid(row=0, column=3, padx=5, sticky="w")
        
        ttk.Label(frame, text="Social Status:").grid(row=0, column=4, padx=5, sticky="e")
        status_key = "female_status" if char_type == "Heroine" else "male_status"
        status = ttk.Combobox(frame, 
                             values=self.character_traits[status_key],
                             width=20)
        status.grid(row=0, column=5, padx=5, sticky="w")
        
        setattr(self, f"{char_type.lower()}_name", name_entry)
        setattr(self, f"{char_type.lower()}_personality", personality)
        setattr(self, f"{char_type.lower()}_status", status)

    def create_story_options(self, parent):
        options_frame = ttk.LabelFrame(parent,
                                     text="Story Elements",
                                     padding=(15, 5, 15, 15))
        options_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0,10))
        
        options_frame.grid_columnconfigure(1, weight=1)
        options_frame.grid_columnconfigure(3, weight=1)
        
        ttk.Label(options_frame, text="Theme:").grid(row=0, column=0, padx=(0,5))
        self.theme_var = tk.StringVar()
        theme_select = ttk.Combobox(options_frame,
                                  textvariable=self.theme_var,
                                  values=list(self.themes.keys()),
                                  width=30)
        theme_select.grid(row=0, column=1, padx=5, sticky="w")
        theme_select.bind('<<ComboboxSelected>>', self.on_theme_change)
        
        ttk.Label(options_frame, text="Setting:").grid(row=0, column=2, padx=5)
        self.setting_var = tk.StringVar()
        self.setting_select = ttk.Combobox(options_frame,
                                         textvariable=self.setting_var,
                                         values=self.settings["locations"],
                                         width=30)
        self.setting_select.grid(row=0, column=3, padx=5, sticky="w")

    def create_output_area(self, parent):
        output_frame = ttk.Frame(parent)
        output_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0,10))
        
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_rowconfigure(0, weight=1)
        
        self.story_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=("Playfair Display", 12),
            bg="white",
            relief="solid",
            borderwidth=1,
            height=12,
            padx=20,
            pady=10
        )
        self.story_text.grid(row=0, column=0, sticky="nsew")
        
        self.story_text.tag_configure('body', spacing1=10, spacing2=2, spacing3=10, justify='center')
        self.story_text.tag_configure('typing', font=("Playfair Display", 12))

    def create_control_panel(self, parent):
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=(0,10))
        
        buttons = [
            ("Generate Story", self.generate_story, "#4CAF50"),
            ("Read Aloud", self.speak_story, "#2196F3"),
            ("Stop Reading", self.stop_speaking, "#f44336"),
            ("Export PDF", self.export_to_pdf, "#9C27B0"),
            ("Toggle Music", self.toggle_music, "#FF9800"),
            ("Clear", self.clear_all, "#f44336")
        ]
        
        for text, command, color in buttons:
            btn = ttk.Button(control_frame,
                           text=text,
                           command=command,
                           style=f"Accent.TButton")
            btn.pack(side=tk.LEFT, padx=5)

    def create_settings_tab(self):
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Create settings container
        settings_container = ttk.Frame(settings_frame, padding=20)
        settings_container.pack(fill=tk.BOTH, expand=True)
        
        # Appearance Settings
        appearance_frame = ttk.LabelFrame(settings_container, text="Appearance", padding=10)
        appearance_frame.pack(fill=tk.X, pady=5)
        
        # Font Settings
        font_frame = ttk.LabelFrame(appearance_frame, text="Font Settings", padding=10)
        font_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(font_frame, text="Story Font Size:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.font_size = tk.StringVar(value="12")
        font_size_combo = ttk.Combobox(font_frame, textvariable=self.font_size, 
                                     values=["10", "12", "14", "16", "18"])
        font_size_combo.grid(row=0, column=1, padx=5, pady=5)
        font_size_combo.bind('<<ComboboxSelected>>', self.update_font_size)
        
        # Theme Settings
        theme_frame = ttk.LabelFrame(appearance_frame, text="Theme", padding=10)
        theme_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(theme_frame, text="Application Theme:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.app_theme = tk.StringVar(value="clearlooks")
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.app_theme,
                                 values=["clearlooks", "equilux", "adapta", "arc"])
        theme_combo.grid(row=0, column=1, padx=5, pady=5)
        theme_combo.bind('<<ComboboxSelected>>', self.update_theme)
        
        # Custom styling for adapta theme
        self.adapta_colors = {
            "primary": "#FF6B6B",  # Coral red
            "secondary": "#4ECDC4",  # Turquoise
            "accent": "#FFD166",  # Yellow
            "background": "#FFFFFF",  # Pure white background
            "text": "#000000",  # Black text for maximum contrast
            "button_bg": "#4ECDC4",  # Turquoise for button background
            "button_text": "#000000",  # Black text for buttons
            "button_hover": "#FFD166",  # Yellow hover state
            "button_hover_text": "#000000",  # Black text for button hover
            "tab_bg": "#4ECDC4",  # Turquoise
            "tab_selected": "#FFD166",  # Yellow
            "tab_text": "#000000",  # Black text for tabs
            "combo_bg": "#FFFFFF",  # White background for combo
            "combo_text": "#000000",  # Black text for combo
            "scale_bg": "#4ECDC4",  # Turquoise
            "check_bg": "#FFFFFF",  # White background
            "check_text": "#000000",  # Black text
            "label_frame_text": "#000000"  # Black text for frame labels
        }
        
        # Audio Settings
        audio_frame = ttk.LabelFrame(settings_container, text="Audio Settings", padding=10)
        audio_frame.pack(fill=tk.X, pady=5)
        
        # Voice Settings
        voice_frame = ttk.LabelFrame(audio_frame, text="Voice Settings", padding=10)
        voice_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(voice_frame, text="Voice Speed:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.voice_speed = tk.StringVar(value="150")
        speed_scale = ttk.Scale(voice_frame, from_=100, to=300, variable=self.voice_speed,
                              orient=tk.HORIZONTAL, command=self.update_voice_speed)
        speed_scale.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Music Settings
        music_frame = ttk.LabelFrame(audio_frame, text="Music Settings", padding=10)
        music_frame.pack(fill=tk.X, pady=5)
        
        self.music_enabled = tk.BooleanVar(value=True)
        music_check = ttk.Checkbutton(music_frame, text="Enable Background Music",
                                    variable=self.music_enabled)
        music_check.pack(padx=5, pady=5, anchor="w")
        
        # Save Settings Button
        save_frame = ttk.Frame(settings_container)
        save_frame.pack(fill=tk.X, pady=20)
        
        save_btn = ttk.Button(save_frame, text="Save Settings", command=self.save_settings)
        save_btn.pack(side=tk.RIGHT, padx=5)

    def create_help_tab(self):
        help_frame = ttk.Frame(self.notebook)
        self.notebook.add(help_frame, text="Help")
        
        # Create help container
        help_container = ttk.Frame(help_frame, padding=20)
        help_container.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for help sections
        help_notebook = ttk.Notebook(help_container)
        help_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Getting Started
        getting_started = ttk.Frame(help_notebook, padding=10)
        help_notebook.add(getting_started, text="Getting Started")
        
        getting_started_text = """Welcome to The Austen Experience!

This application allows you to create your own Regency-era romance stories in the style of Jane Austen.

To create a story:
1. Fill in the character details for both the Heroine and Hero
2. Select a theme and setting for your story
3. Click 'Generate Story' to create your tale
4. Use the controls to read aloud, export, or clear the story

The application features:
- Multiple story themes (Romance, Drama, Mystery, etc.)
- Customizable characters with different personalities
- Text-to-speech narration
- Background music
- PDF export capability

For more detailed information, please refer to the other help sections."""
        
        ttk.Label(getting_started, text=getting_started_text, wraplength=600, justify=tk.LEFT).pack(pady=10)
        
        # Character Creation
        character_help = ttk.Frame(help_notebook, padding=10)
        help_notebook.add(character_help, text="Character Creation")
        
        character_text = """Character Creation Guide:

Heroine and Hero:
- Name: Enter a suitable Regency-era name
- Personality: Choose from various personality traits
- Social Status: Select appropriate social standing

Personality Traits:
- Witty: Sharp intellect and ready humor
- Reserved: Quiet dignity and careful observation
- Spirited: Vivacious charm and boundless energy
- Proud: Dignified bearing and refined sensibilities
- Gentle: Tender heart and gracious manner

Social Status Options:
- Female: Lady, Gentlewoman, etc.
- Male: Gentleman, Baronet, etc.

Choose combinations that create interesting dynamics for your story."""
        
        ttk.Label(character_help, text=character_text, wraplength=600, justify=tk.LEFT).pack(pady=10)
        
        # Story Elements
        story_help = ttk.Frame(help_notebook, padding=10)
        help_notebook.add(story_help, text="Story Elements")
        
        story_text = """Story Elements Guide:

Themes:
- Romance: Classic love stories with happy endings
- Drama: Intense emotional conflicts and resolutions
- Mystery: Intriguing puzzles and revelations
- Comedy: Light-hearted and humorous tales
- Tragedy: Deeply emotional stories with bittersweet endings

Settings:
Choose from various Regency-era locations:
- Country estates
- London townhouses
- Seaside resorts
- Country villages

The combination of theme and setting sets the stage for your story."""
        
        ttk.Label(story_help, text=story_text, wraplength=600, justify=tk.LEFT).pack(pady=10)
        
        # Controls
        controls_help = ttk.Frame(help_notebook, padding=10)
        help_notebook.add(controls_help, text="Controls")
        
        controls_text = """Application Controls:

Generate Story:
- Creates a new story based on your selections
- Uses a typewriter effect for dramatic presentation

Read Aloud:
- Uses text-to-speech to narrate the story
- Can be stopped at any time
- Voice settings can be adjusted in Settings

Export PDF:
- Saves the current story as a PDF
- Includes proper formatting and styling

Toggle Music:
- Enables/disables background music
- Music changes with the selected theme

Clear:
- Resets all input fields
- Clears the current story"""
        
        ttk.Label(controls_help, text=controls_text, wraplength=600, justify=tk.LEFT).pack(pady=10)

    def update_font_size(self, event=None):
        size = int(self.font_size.get())
        self.story_text.configure(font=("Playfair Display", size))

    def update_theme(self, event=None):
        theme = self.app_theme.get()
        self.root.set_theme(theme)
        
        style = ttk.Style()
        
        # Reset all styles to default first
        style.theme_use(theme)
        
        # Apply custom styling ONLY for adapta theme
        if theme == "adapta":
            # Configure base styles with strong contrast
            style.configure("TFrame", 
                          background=self.adapta_colors["background"])
            
            # Configure labels with dark text
            style.configure("TLabel", 
                          background=self.adapta_colors["background"],
                          foreground=self.adapta_colors["text"],
                          font=("Comic Sans MS", 11, "bold"))
            
            # Configure LabelFrame with dark text
            style.configure("TLabelframe",
                          background=self.adapta_colors["background"])
            style.configure("TLabelframe.Label",
                          foreground=self.adapta_colors["label_frame_text"],
                          background=self.adapta_colors["background"],
                          font=("Comic Sans MS", 11, "bold"))
            
            # Configure buttons with hover effect and visible text
            style.configure("TButton",
                          background=self.adapta_colors["button_bg"],
                          foreground=self.adapta_colors["button_text"],
                          font=("Comic Sans MS", 11, "bold"),
                          padding=10)
            style.map("TButton",
                     background=[("active", self.adapta_colors["button_hover"]),
                               ("pressed", self.adapta_colors["button_hover"])],
                     foreground=[("active", self.adapta_colors["button_hover_text"]),
                               ("pressed", self.adapta_colors["button_hover_text"])])
            
            # Configure comboboxes with white background and black text
            style.configure("TCombobox",
                          background=self.adapta_colors["combo_bg"],
                          foreground=self.adapta_colors["combo_text"],
                          selectbackground=self.adapta_colors["accent"],
                          selectforeground=self.adapta_colors["text"],
                          fieldbackground=self.adapta_colors["combo_bg"],
                          font=("Comic Sans MS", 10))
            
            # Configure checkbuttons with dark text
            style.configure("TCheckbutton",
                          background=self.adapta_colors["check_bg"],
                          foreground=self.adapta_colors["check_text"],
                          font=("Comic Sans MS", 11))
            
            # Configure scales with contrasting colors
            style.configure("Horizontal.TScale",
                          background=self.adapta_colors["background"],
                          troughcolor=self.adapta_colors["scale_bg"])
            
            # Configure notebook and tabs
            style.configure("TNotebook",
                          background=self.adapta_colors["background"])
            
            style.configure("TNotebook.Tab",
                          background=self.adapta_colors["tab_bg"],
                          foreground=self.adapta_colors["tab_text"],
                          padding=[10, 5],
                          font=("Comic Sans MS", 11, "bold"))
            
            style.map("TNotebook.Tab",
                     background=[("selected", self.adapta_colors["tab_selected"])],
                     foreground=[("selected", self.adapta_colors["tab_text"])])
            
            # Configure entry fields with white background and black text
            style.configure("TEntry",
                          fieldbackground=self.adapta_colors["combo_bg"],
                          foreground=self.adapta_colors["combo_text"],
                          font=("Comic Sans MS", 10))
            
            # Configure scrollbars
            style.configure("Vertical.TScrollbar",
                          background=self.adapta_colors["tab_bg"],
                          troughcolor=self.adapta_colors["background"],
                          arrowcolor=self.adapta_colors["text"])
            
            style.configure("Horizontal.TScrollbar",
                          background=self.adapta_colors["tab_bg"],
                          troughcolor=self.adapta_colors["background"],
                          arrowcolor=self.adapta_colors["text"])
        else:
            # For other themes, use their default styles
            style.configure("TLabel", font=("Helvetica", 10))
            style.configure("TButton", font=("Helvetica", 10))
            style.configure("TCheckbutton", font=("Helvetica", 10))
            style.configure("TCombobox", font=("Helvetica", 10))
            style.configure("TNotebook.Tab", font=("Helvetica", 10))
            style.configure("TLabelframe.Label", font=("Helvetica", 10))

    def update_voice_speed(self, value):
        if self.current_engine:
            self.current_engine.setProperty('rate', int(value))

    def save_settings(self):
        settings = {
            "font_size": self.font_size.get(),
            "app_theme": self.app_theme.get(),
            "voice_speed": self.voice_speed.get(),
            "music_enabled": self.music_enabled.get()
        }
        
        try:
            with open('settings.json', 'w') as f:
                json.dump(settings, f)
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

    def generate_story(self):
        # Validate inputs
        if not self.validate_inputs():
            return
            
        # Get all input values
        story_data = {
            "heroine": {
                "name": self.heroine_name.get(),
                "personality": self.heroine_personality.get(),
                "status": self.heroine_status.get()
            },
            "hero": {
                "name": self.hero_name.get(),
                "personality": self.hero_personality.get(),
                "status": self.hero_status.get()
            },
            "theme": self.theme_var.get(),
            "setting": self.setting_var.get()
        }
        
        # Generate story using the story elements
        story = self.create_story(story_data)
        
        # Display with typewriter effect
        self.typewriter_effect(story)

    def validate_inputs(self):
        required_fields = [
            (self.heroine_name.get(), "Heroine's name"),
            (self.hero_name.get(), "Hero's name"),
            (self.heroine_personality.get(), "Heroine's personality"),
            (self.hero_personality.get(), "Hero's personality"),
            (self.theme_var.get(), "Theme"),
            (self.setting_var.get(), "Setting")
        ]
        
        for value, field_name in required_fields:
            if not value.strip():
                messagebox.showwarning(
                    "Missing Information",
                    f"Please provide the {field_name}."
                )
                return False
        return True

    def create_story(self, data):
        theme = data['theme'].lower().replace(' ', '_')
        method_name = f"generate_{theme}_story"
        story_generator = getattr(self, method_name, self.generate_default_story)
        return story_generator(data)

    def generate_default_story(self, data):
        return f"""In the elegant society of {data['setting']}, where manners and propriety reigned supreme, 
the {data['heroine']['personality'].lower()} Miss {data['heroine']['name']}, a {data['heroine']['status'].lower()},
found her life taking an unexpected turn.

It was during one of Lady Catherine's renowned evening gatherings that she first encountered 
Mr. {data['hero']['name']}, a {data['hero']['personality'].lower()} {data['hero']['status'].lower()},
whose presence caused quite a stir among the local gentry.

Through a series of social gatherings and chance encounters, they discovered that first impressions 
are not always to be trusted, and that the heart often has wisdom that reason cannot comprehend.

And so, in the time-honored tradition of all good stories, they found that happiness often comes 
not in the way we expect, but in the way that suits us best."""

    def typewriter_effect(self, text):
        self.story_text.delete(1.0, tk.END)
        
        def type_text():
            # Add initial newline for spacing
            self.story_text.insert(tk.END, '\n')
            
            # Split text into paragraphs
            paragraphs = text.split('\n\n')
            
            for i, paragraph in enumerate(paragraphs):
                # Type each character with delay
                for char in paragraph:
                    self.story_text.insert(tk.END, char, ('body', 'typing'))
                    self.story_text.see(tk.END)
                    self.story_text.update()
                    
                    # Adjust delay based on punctuation
                    if char in '.!?':
                        time.sleep(0.1)  # Longer pause for sentence endings
                    elif char in ',;:':
                        time.sleep(0.05)  # Medium pause for other punctuation
                    else:
                        time.sleep(0.02)  # Quick typing for regular characters
                
                # Add paragraph breaks except for the last paragraph
                if i < len(paragraphs) - 1:
                    self.story_text.insert(tk.END, '\n\n')
            
            # Apply final formatting
            self.story_text.tag_add('body', '1.0', tk.END)
        
        # Run typing effect in a separate thread
        threading.Thread(target=type_text, daemon=True).start()

    def speak_story(self):
        if not self.voice_enabled:
            messagebox.showerror("Error", "Text-to-speech not available")
            return
            
        text = self.story_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showinfo("Notice", "No story to read")
            return
            
        def speak():
            try:
                if self.current_engine:
                    try:
                        self.current_engine.stop()
                    except:
                        pass
                    self.current_engine = None
                
                engine = pyttsx3.init()
                self.current_engine = engine
                
                voices = engine.getProperty('voices')
                for voice in voices:
                    if "female" in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
                
                self.voice_playing = True
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                print(f"Error in text-to-speech: {e}")
                messagebox.showerror("Error", "Failed to read text aloud")
            finally:
                self.voice_playing = False
                try:
                    if self.current_engine:
                        self.current_engine.stop()
                        self.current_engine = None
                except:
                    pass
            
        threading.Thread(target=speak, daemon=True).start()

    def stop_speaking(self):
        if self.voice_playing:
            self.voice_playing = False
            try:
                if self.current_engine:
                    self.current_engine.stop()
                    self.current_engine = None
            except:
                pass

    def toggle_music(self):
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False
        else:
            theme = self.theme_var.get()
            if theme in self.bg_music_paths:
                try:
                    pygame.mixer.music.load(self.bg_music_paths[theme])
                    pygame.mixer.music.play(-1)
                    self.music_playing = True
                except:
                    messagebox.showerror("Error", "Could not play music")

    def export_to_pdf(self):
        text = self.story_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "No story to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not file_path:
            return
            
        # Create PDF with fancy formatting
        self.create_fancy_pdf(text, file_path)

    def create_fancy_pdf(self, text, file_path):
        # Create a more sophisticated PDF with proper formatting
        # This is a placeholder for the PDF creation logic
        pass

    def clear_all(self):
        self.story_text.delete(1.0, tk.END)
        self.heroine_name.delete(0, tk.END)
        self.hero_name.delete(0, tk.END)
        self.heroine_personality.set('')
        self.hero_personality.set('')
        self.heroine_status.set('')
        self.hero_status.set('')
        self.theme_var.set('')
        self.setting_var.set('')

    def on_window_resize(self, event):
        # Only handle window resize events
        if event.widget == self.root:
            # Get new dimensions
            width = event.width
            height = event.height
            
            # Update notebook size
            self.notebook.config(width=width, height=height)
            
            # Update background if theme is selected
            if hasattr(self, 'current_theme') and self.current_theme:
                self.apply_theme(self.current_theme)

    def on_theme_change(self, event=None):
        theme = self.theme_var.get()
        if theme in self.themes:
            self.current_theme = theme
            self.apply_theme(theme)

    def apply_theme(self, theme):
        theme_data = self.themes[theme]
        
        try:
            # Load and resize background image
            bg_image = Image.open(theme_data["image"])
            
            # Get current window dimensions
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            
            # Calculate aspect ratios
            window_ratio = window_width / window_height
            image_ratio = bg_image.width / bg_image.height
            
            # Calculate new dimensions maintaining aspect ratio and ensuring full coverage
            if window_ratio > image_ratio:
                # Window is wider than image
                new_width = window_width
                new_height = int(window_width / image_ratio)
            else:
                # Window is taller than image
                new_height = window_height
                new_width = int(window_height * image_ratio)
            
            # Resize image with high-quality resampling
            bg_image = bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage and store reference
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            
            # Create a new canvas for the background if it doesn't exist
            if not hasattr(self, 'canvas'):
                self.canvas = tk.Canvas(self.main_container, highlightthickness=0)
                self.canvas.grid(row=0, column=0, sticky="nsew")
                self.notebook.lift()  # Ensure notebook stays on top
            
            # Clear canvas and draw new background
            self.canvas.delete("all")
            
            # Calculate position to center the image
            x = (window_width - new_width) // 2
            y = (window_height - new_height) // 2
            
            # Draw the background image
            self.canvas.create_image(x, y, image=self.bg_photo, anchor="nw")
            
            # Ensure notebook stays on top
            self.notebook.lift()
            
        except Exception as e:
            print(f"Error loading background image: {e}")
            import traceback
            traceback.print_exc()
        
        # Handle music transition
        if self.music_playing:
            self.toggle_music()  # Stop current music
            self.toggle_music()  # Start new theme music

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AustenStoryCreator()
    app.run()
