import plotly.graph_objs as go

def plot_intent_dist(nlu_test_cases, intent_counts):
    intents = list(intent_counts.keys())
    counts = list(intent_counts.values())
    total_cases = len(nlu_test_cases)

    data = [go.Bar(
        x=intents,
        y=counts,
        text=[f"{count} ({count/total_cases*100:.2f}%)" for count in counts],
        textposition='auto',
        marker=dict(
            color='rgba(58,200,225,0.5)',
            line=dict(color='rgb(8,48,107)', width=1.5)
        )
    )]

    layout = go.Layout(
        title='意图分布',
        xaxis=dict(title='意图', tickfont=dict(size=14)),
        yaxis=dict(title='测试用例数量', tickfont=dict(size=14)),
        bargap=0.1,
        bargroupgap=0.1
    )

    fig = go.Figure(data=data, layout=layout)
    return fig