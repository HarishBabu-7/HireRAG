import streamlit as st
import time
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

# --- Configuration and Session State Initialization ---
st.set_page_config(
    page_title="Gemini-like Chatbot",
    layout="wide", # Use wide layout for better sidebar and main content separation
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {
        "Chat 1": [{"role": "assistant", "content": "Welcome! How can I help you with Chat 1?"}],
        "Chat 2": [{"role": "assistant", "content": "Hello! I'm ready for Chat 2."}]
    }
if "current_chat_name" not in st.session_state:
    st.session_state.current_chat_name = "New Chat"
    st.session_state.chat_history["New Chat"] = [] # Initialize new chat
if "show_options" not in st.session_state:
    st.session_state.show_options = False
if "drawing_mode" not in st.session_state:
    st.session_state.drawing_mode = False # To toggle canvas visibility
if "background_image_data" not in st.session_state:
    st.session_state.background_image_data = None
if "stroke_width" not in st.session_state:
    st.session_state.stroke_width = 3
if "stroke_color" not in st.session_state:
    st.session_state.stroke_color = "#eee"
if "bg_color" not in st.session_state:
    st.session_state.bg_color = "#fff"

# --- ML Model Placeholder ---
def get_ml_response(user_input, image_data=None, drawing_data=None):
    """
    Simulates an ML model response.
    Integrate your actual LLM/ML model here.
    """
    time.sleep(1) # Simulate processing time
    response = ""
    if image_data:
        response += "I received an image! "
        # In a real scenario, you'd send this image to a Vision model (e.g., Gemini Pro Vision)
    if drawing_data:
        response += "I received a drawing! "
        # You might process the drawing strokes or the resulting image
    if user_input:
        response += f"You said: '{user_input}'. "

    if not response:
        response = "Hello! How can I assist you today?"
    return response + " I'm a Gemini-like chatbot demo."

# --- Sidebar (Left Panel) ---
with st.sidebar:
    st.title("Gemini-like Chatbot ♊")

    # New Chat Button
    if st.button("✨ New Chat", use_container_width=True):
        new_chat_name = f"Chat {len(st.session_state.chat_history) + 1}"
        st.session_state.current_chat_name = new_chat_name
        st.session_state.chat_history[new_chat_name] = []
        st.session_state.messages = [] # Clear displayed messages for new chat
        st.session_state.drawing_mode = False # Hide canvas
        st.session_state.show_options = False # Hide options
        st.rerun()

    st.markdown("---")
    st.subheader("Current Chat")
    current_chat_name_input = st.text_input(
        "Edit Chat Name",
        st.session_state.current_chat_name,
        key="current_chat_name_input_box",
        label_visibility="collapsed"
    )
    if current_chat_name_input != st.session_state.current_chat_name:
        # Update chat name in history
        old_name = st.session_state.current_chat_name
        st.session_state.chat_history[current_chat_name_input] = st.session_state.chat_history.pop(old_name)
        st.session_state.current_chat_name = current_chat_name_input
        st.rerun() # Rerun to update the displayed name

    st.markdown("---")
    st.subheader("Chat History")
    history_placeholder = st.empty() # Placeholder for chat history links

    # Display chat history links
    with history_placeholder:
        for chat_name in st.session_state.chat_history.keys():
            if chat_name != st.session_state.current_chat_name:
                if st.button(chat_name, key=f"chat_link_{chat_name}", use_container_width=True):
                    st.session_state.current_chat_name = chat_name
                    st.session_state.messages = st.session_state.chat_history[chat_name]
                    st.session_state.drawing_mode = False # Hide canvas when switching chats
                    st.session_state.show_options = False # Hide options
                    st.rerun()
            else:
                st.markdown(f"**➤ {chat_name}**") # Highlight current chat

    st.markdown("---")
    st.subheader("Settings")
    # Toggle Option (e.g., Dark Mode - though Streamlit uses themes, this is a manual toggle)
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False

    if st.checkbox("Toggle Dark Mode (Simulated)", value=st.session_state.dark_mode):
        st.session_state.dark_mode = True
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #333;
                color: #eee;
            }
            .stChatMessage {
                background-color: #555 !important;
                border-radius: 10px;
            }
            .stChatMessage:nth-child(even) { /* User messages */
                background-color: #444 !important;
            }
            </style>
            """, unsafe_allow_html=True
        )
        st.session_state.stroke_color = "#eee" if st.session_state.dark_mode else "#222"
        st.session_state.bg_color = "#444" if st.session_state.dark_mode else "#fff"
    else:
        st.session_state.dark_mode = False
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #fff;
                color: #333;
            }
            .stChatMessage {
                background-color: #f0f2f6 !important;
                border-radius: 10px;
            }
            .stChatMessage:nth-child(even) { /* User messages */
                background-color: #e0e2e6 !important;
            }
            </style>
            """, unsafe_allow_html=True
        )
        st.session_state.stroke_color = "#222" if not st.session_state.dark_mode else "#eee"
        st.session_state.bg_color = "#fff" if not st.session_state.dark_mode else "#444"

    if st.button("🗑️ Clear Current Chat", use_container_width=True):
        st.session_state.chat_history[st.session_state.current_chat_name] = []
        st.session_state.messages = []
        st.session_state.drawing_mode = False
        st.session_state.show_options = False
        st.rerun()

# --- Main Chat Area ---
st.title(f"💬 {st.session_state.current_chat_name}")

# Display chat messages from current chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], caption="Uploaded Image", use_column_width=True)
        elif message["type"] == "drawing":
            st.image(message["content"], caption="User Drawing", use_column_width=True)


# --- Input Area at the Bottom ---
# Use a container for the input box and options to control their position
input_container = st.container()

with input_container:
    col1, col2 = st.columns([0.05, 0.95]) # Column for + button and chat input

    with col1:
        # '+' button to toggle options
        if st.button("➕", key="plus_button", help="Attach files or draw"):
            st.session_state.show_options = not st.session_state.show_options
            st.session_state.drawing_mode = False # Hide canvas if options are toggled

    with col2:
        user_prompt = st.chat_input("Message Gemini-like Bot...", key="chat_input_main")

    # Options area (Image Upload & Canvas)
    if st.session_state.show_options:
        with st.container(border=True): # Gives a nice border around the options
            st.subheader("Attach Options")
            uploaded_image = st.file_uploader(
                "Upload an Image", type=["png", "jpg", "jpeg"], key="image_uploader"
            )

            # Toggle Drawing Canvas
            if st.button("🎨 Draw on Canvas", key="toggle_canvas_button", use_container_width=True):
                st.session_state.drawing_mode = not st.session_state.drawing_mode
                if not st.session_state.drawing_mode:
                    st.session_state.background_image_data = None # Clear image when hiding canvas

            if uploaded_image is not None and st.session_state.drawing_mode:
                # If image uploaded and canvas is active, use image as background for canvas
                st.session_state.background_image_data = uploaded_image.read()
            elif uploaded_image is None:
                st.session_state.background_image_data = None # Clear if no image and canvas active

            if st.session_state.drawing_mode:
                st.markdown("---")
                st.subheader("Drawing Canvas")
                st.write("Draw something!")

                # Drawing controls
                col_canvas_controls = st.columns(3)
                with col_canvas_controls[0]:
                    st.session_state.stroke_width = st.slider("Stroke width: ", 1, 25, st.session_state.stroke_width, key="stroke_width_slider")
                with col_canvas_controls[1]:
                    st.session_state.stroke_color = st.color_picker("Stroke color: ", st.session_state.stroke_color, key="stroke_color_picker")
                with col_canvas_controls[2]:
                    st.session_state.bg_color = st.color_picker("Background color: ", st.session_state.bg_color, key="bg_color_picker")


                canvas_result = st_canvas(
                    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
                    stroke_width=st.session_state.stroke_width,
                    stroke_color=st.session_state.stroke_color,
                    background_color=st.session_state.bg_color,
                    background_image=Image.open(io.BytesIO(st.session_state.background_image_data)) if st.session_state.background_image_data else None,
                    height=300,
                    drawing_mode="freedraw",
                    key="canvas",
                )

                if canvas_result.image_data is not None:
                    # Convert to PIL Image for display/saving if needed
                    # img = Image.fromarray(canvas_result.image_data.astype("uint8"))
                    # st.image(img, caption="Your Drawing", use_column_width=True)
                    pass # We'll send this to the model only when user submits

# --- Handle User Input and Generate Response ---
if user_prompt:
    # Add user message to current chat history and display
    st.session_state.messages.append({"role": "user", "content": user_prompt, "type": "text"})
    st.session_state.chat_history[st.session_state.current_chat_name] = st.session_state.messages # Update current chat in history

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # If an image was uploaded, process it
    uploaded_image_data = None
    if uploaded_image is not None:
        uploaded_image_data = uploaded_image.getvalue()
        with st.chat_message("user"):
            st.image(uploaded_image_data, caption="Your Uploaded Image", use_column_width=True)
        st.session_state.messages.append({"role": "user", "content": uploaded_image_data, "type": "image"})
        st.session_state.chat_history[st.session_state.current_chat_name] = st.session_state.messages

    # If a drawing was made, process it
    drawing_image_data = None
    if st.session_state.drawing_mode and canvas_result.image_data is not None:
        # Convert numpy array to BytesIO to simulate file-like object for ML model
        img_byte_arr = io.BytesIO()
        Image.fromarray(canvas_result.image_data.astype("uint8")).save(img_byte_arr, format='PNG')
        drawing_image_data = img_byte_arr.getvalue()
        with st.chat_message("user"):
            st.image(drawing_image_data, caption="Your Drawing", use_column_width=True)
        st.session_state.messages.append({"role": "user", "content": drawing_image_data, "type": "drawing"})
        st.session_state.chat_history[st.session_state.current_chat_name] = st.session_state.messages


    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Pass image and drawing data to your ML model
            assistant_response = get_ml_response(user_prompt, uploaded_image_data, drawing_image_data)
            st.markdown(assistant_response)

        # Add assistant response to current chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response, "type": "text"})
        st.session_state.chat_history[st.session_state.current_chat_name] = st.session_state.messages

    # Reset options and drawing mode after submission
    st.session_state.show_options = False
    st.session_state.drawing_mode = False
    st.session_state.background_image_data = None # Clear image from canvas after sending
    # st.rerun() # This might be too aggressive and cause flickering if you're not careful

# --- Custom CSS for Layout and Styling ---
st.markdown(
    """
    <style>
    /* Ensure the main content pushes the input to the bottom */
    .main .block-container {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 90vh; /* Adjust as needed */
    }

    /* Style the chat messages */
    .stChatMessage {
        border-radius: 10px;
        padding: 10px 15px;
        margin-bottom: 10px;
        max-width: 70%; /* Limit width of chat bubbles */
        word-wrap: break-word; /* Ensure long words wrap */
    }
    .stChatMessage:nth-child(odd) { /* Assistant messages (first, third, etc.) */
        background-color: #f0f2f6; /* Light gray */
        align-self: flex-start;
        border-bottom-left-radius: 0;
    }
    .stChatMessage:nth-child(even) { /* User messages (second, fourth, etc.) */
        background-color: #e6f7ff; /* Light blue */
        align-self: flex-end;
        border-bottom-right-radius: 0;
    }

    /* Input area at the bottom */
    .stChatInputContainer {
        position: fixed; /* Fix at the bottom */
        bottom: 0;
        left: 0; /* Adjust if sidebar is dynamic */
        right: 0;
        background-color: var(--background-color); /* Use Streamlit's background var */
        padding: 10px 20px;
        border-top: 1px solid #ddd;
        z-index: 1000; /* Ensure it's on top */
        display: flex;
        align-items: center;
        width: calc(100% - var(--sidebar-width, 300px)); /* Adjust for sidebar */
        margin-left: var(--sidebar-width, 300px); /* Push input area over by sidebar width */
    }

    /* Adjust the chat input widget itself */
    .stChatInputContainer .stTextInput {
        flex-grow: 1; /* Allow input to take available space */
    }
    .stChatInputContainer button {
        margin-right: 10px; /* Space between plus button and input */
    }

    /* Adjust the main content to make space for the fixed input */
    .main .block-container {
        padding-bottom: 100px; /* Give space for the fixed input box */
    }

    /* Specific styling for the plus button to be more compact */
    #plus_button {
        background-color: transparent !important;
        border: none !important;
        color: #607D8B !important; /* Material Design Grey */
        font-size: 24px !important;
        padding: 0 !important;
        margin: 0 !important;
        height: auto !important;
        width: auto !important;
        line-height: 1; /* For better vertical alignment */
        display: flex;
        align-items: center;
        justify-content: center;
    }
    #plus_button:hover {
        color: #2196F3 !important; /* Blue on hover */
    }

    /* Hide the default Streamlit footer */
    footer { visibility: hidden; }

    /* Adjust for wide layout */
    .css-1d391kg { /* This is the class for the main content block container */
        max-width: none !important; /* Remove max-width restriction */
        padding-left: 1rem;
        padding-right: 1rem;
    }
    </style>
    """, unsafe_allow_html=True
)