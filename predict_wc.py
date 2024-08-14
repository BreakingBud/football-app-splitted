import streamlit as st
import plotly.graph_objects as go

def create_knockout_bracket(teams):
    st.title("FIFA World Cup Knockout Stage Bracket")

    fig = go.Figure()

    # Round of 16
    for i in range(8):
        fig.add_trace(go.Scatter(
            x=[1, 2],
            y=[8-i, 8-i],
            mode="lines+text",
            text=[teams[i*2], teams[i*2+1]],
            textposition="top center"
        ))
        fig.add_trace(go.Scatter(
            x=[2],
            y=[8-i],
            mode="markers+text",
            text=["Winner {}".format(i+1)],
            textposition="middle right"
        ))

    # Quarterfinals
    for i in range(4):
        fig.add_trace(go.Scatter(
            x=[3, 4],
            y=[7-i*2, 7-i*2],
            mode="lines+text",
            text=["Winner {}".format(i*2+1), "Winner {}".format(i*2+2)],
            textposition="top center"
        ))
        fig.add_trace(go.Scatter(
            x=[4],
            y=[7-i*2],
            mode="markers+text",
            text=["QF Winner {}".format(i+1)],
            textposition="middle right"
        ))

    # Semifinals
    for i in range(2):
        fig.add_trace(go.Scatter(
            x=[5, 6],
            y=[5-i*4, 5-i*4],
            mode="lines+text",
            text=["QF Winner {}".format(i*2+1), "QF Winner {}".format(i*2+2)],
            textposition="top center"
        ))
        fig.add_trace(go.Scatter(
            x=[6],
            y=[5-i*4],
            mode="markers+text",
            text=["SF Winner {}".format(i+1)],
            textposition="middle right"
        ))

    # Final
    fig.add_trace(go.Scatter(
        x=[7, 8],
        y=[4, 4],
        mode="lines+text",
        text=["SF Winner 1", "SF Winner 2"],
        textposition="top center"
    ))
    fig.add_trace(go.Scatter(
        x=[8],
        y=[4],
        mode="markers+text",
        text=["Champion"],
        textposition="middle right"
    ))

    fig.update_layout(
        showlegend=False,
        xaxis=dict(showticklabels=False),
        yaxis=dict(showticklabels=False),
        title="Knockout Stage Bracket"
    )

    st.plotly_chart(fig)

# Assuming you have already preprocessed data and trained a model
try:
    # Dummy team names for placeholder purposes
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

    create_knockout_bracket(teams)

except Exception as e:
    st.error(f"An error occurred: {e}")
