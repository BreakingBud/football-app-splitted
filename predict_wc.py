import streamlit as st
import plotly.graph_objects as go
from preprocess import load_and_preprocess_data
from model import train_model, predict_match

def create_knockout_bracket(teams, winners=None):
    st.title("FIFA World Cup Knockout Stage Bracket")

    if winners is None:
        winners = [""] * 8  # Empty placeholders for winners

    fig = go.Figure()

    # Round of 16
    fig.add_trace(go.Scatter(
        x=[1, 1], y=[1, 2],
        mode="text",
        text=[teams[0], teams[1]],
        textposition="middle center",
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=[1, 1], y=[3, 4],
        mode="text",
        text=[teams[2], teams[3]],
        textposition="middle center",
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=[1, 1], y=[5, 6],
        mode="text",
        text=[teams[4], teams[5]],
        textposition="middle center",
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=[1, 1], y=[7, 8],
        mode="text",
        text=[teams[6], teams[7]],
        textposition="middle center",
        showlegend=False
    ))

    # Quarterfinals
    fig.add_trace(go.Scatter(
        x=[2, 2], y=[1.5, 3.5],
        mode="text",
        text=[winners[0], winners[1]],
        textposition="middle center",
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=[2, 2], y=[5.5, 7.5],
        mode="text",
        text=[winners[2], winners[3]],
        textposition="middle center",
        showlegend=False
    ))

    # Semifinals
    fig.add_trace(go.Scatter(
        x=[3, 3], y=[2.5, 6.5],
        mode="text",
        text=[winners[4], winners[5]],
        textposition="middle center",
        showlegend=False
    ))

    # Final
    fig.add_trace(go.Scatter(
        x=[4], y=[4.5],
        mode="text",
        text=[winners[6]],
        textposition="middle center",
        showlegend=False
    ))

    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=600,
        width=800,
        showlegend=False
    )

    st.plotly_chart(fig)

# Load preprocessed data and model
try:
    X_train, X_test, y_train, y_test, label_encoders, scaler, home_team_encoder = load_and_preprocess_data('data.zip', 'extracted_path')
    model = train_model(X_train, y_train, X_train.shape[1])

    # Placeholder teams for the bracket
    teams = [
        "Group A Winner", "Group B Runner-Up",
        "Group C Winner", "Group D Runner-Up",
        "Group B Winner", "Group A Runner-Up",
        "Group D Winner", "Group C Runner-Up",
        "Group E Winner", "Group F Runner-Up",
        "Group G Winner", "Group H Runner-Up",
        "Group F Winner", "Group E Runner-Up",
        "Group H Winner", "Group G Runner-Up"
    ]

    # Placeholder winners for the first round
    winners = [teams[i] for i in range(8)]  # This should be replaced with actual prediction logic

    # Create the knockout bracket
    create_knockout_bracket(teams, winners)

except Exception as e:
    st.error(f"An error occurred: {e}")
