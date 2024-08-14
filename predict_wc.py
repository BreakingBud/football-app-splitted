import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Initialize Streamlit app
st.title("FIFA World Cup Knockout Stage Bracket")

# Draw the bracket programmatically
image_width, image_height = 800, 600
image = Image.new('RGB', (image_width, image_height), (255, 255, 255))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Draw the lines for the bracket
# Define some coordinates for where the lines should be drawn
line_coords = [
    # Round of 16
    (100, 50, 300, 50), (100, 150, 300, 150),
    (100, 250, 300, 250), (100, 350, 300, 350),
    (100, 450, 300, 450), (100, 550, 300, 550),
    (100, 650, 300, 650), (100, 750, 300, 750),

    # Quarter-finals
    (300, 100, 500, 100), (300, 300, 500, 300),
    (300, 500, 500, 500), (300, 700, 500, 700),

    # Semi-finals
    (500, 200, 700, 200), (500, 600, 700, 600),

    # Final
    (700, 400, 900, 400),
]

# Draw the lines on the image
for coords in line_coords:
    draw.line(coords, fill="black", width=5)

# Draw the team slots (text placeholders)
team_slots = [
    (50, 45), (50, 145), (50, 245), (50, 345),
    (50, 445), (50, 545), (50, 645), (50, 745),

    (350, 95), (350, 295), (350, 495), (350, 695),

    (550, 195), (550, 595),

    (750, 395)
]

# Placeholder group names
groups = [
    "Group A Winner", "Group B Runner-Up", 
    "Group C Winner", "Group D Runner-Up", 
    "Group E Winner", "Group F Runner-Up", 
    "Group G Winner", "Group H Runner-Up",
    "Group B Winner", "Group A Runner-Up",
    "Group D Winner", "Group C Runner-Up",
    "Group F Winner", "Group E Runner-Up",
    "Group H Winner", "Group G Runner-Up"
]

# Assign group names to corresponding slots in the bracket
group_matchup_order = [
    "Group A Winner", "Group B Runner-Up",
    "Group C Winner", "Group D Runner-Up",
    "Group E Winner", "Group F Runner-Up",
    "Group G Winner", "Group H Runner-Up",
    "Group B Winner", "Group A Runner-Up",
    "Group D Winner", "Group C Runner-Up",
    "Group F Winner", "Group E Runner-Up",
    "Group H Winner", "Group G Runner-Up"
]

# Draw the group names on the image
for position, group in zip(team_slots, group_matchup_order):
    draw.text(position, group, fill="black", font=font)

# Display the bracket
st.image(image, caption="Knockout Stage Bracket", use_column_width=True)
