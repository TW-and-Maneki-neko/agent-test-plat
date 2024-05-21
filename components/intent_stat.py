import plotly.graph_objs as go

def plot_intent_dist(nlu_test_cases, intent_counts):
    # 将意图和对应的计数转换为列表
    intents = list(intent_counts.keys())
    counts = list(intent_counts.values())
    total_cases = len(nlu_test_cases)
    
    # 将意图和计数配对，然后按计数从高到低排序
    sorted_intents_counts = sorted(zip(intents, counts), key=lambda x: x[1], reverse=True)
    sorted_intents = [item[0] for item in sorted_intents_counts]
    sorted_counts = [item[1] for item in sorted_intents_counts]

    data = [go.Bar(
        x=sorted_counts,
        y=sorted_intents,
        orientation='h',  # 设置为水平条形图
        text=[f"{count} ({count/total_cases*100:.2f}%)" for count in sorted_counts],
        textposition='auto',
        marker=dict(
            color='rgba(58,200,225,0.5)',
            line=dict(color='rgb(8,48,107)', width=1.5)
        )
    )]

    layout = go.Layout(
        title='意图分布',
        xaxis=dict(title='测试用例数量', tickfont=dict(size=14)),
        yaxis=dict(title='意图', tickfont=dict(size=14)),
        bargap=0.1,
        bargroupgap=0.1,
        height=600,
    )

    fig = go.Figure(data=data, layout=layout)
    return fig
