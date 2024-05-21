from utils import highlight_slot
import plotly.graph_objects as go


def generate_result_table(nlu_results, show_all):
    result_table = "<table>"
    result_table += "<tr><th>输入</th><th>实际意图</th><th>期望意图</th><th>实际槽位</th><th>意图置信度</th></tr>"

    for result in nlu_results:
        input_text = result["input"]
        expected_intent = result["expected_intent"]
        actual_intent = result["actual_intent"]
        expected_slots = result["expected_slots"]
        actual_slots = result["actual_slots"]
        confidence = result["confidence"]

        intent_color = "#35a835" if expected_intent == actual_intent else "#db3636"
        confidence_color = "#35a835" if confidence >= 0.7 else "#a3a005" if confidence >= 0.5 else "#db3636"

        # 在输入文本中高亮显示实体
        highlighted_input = input_text
        for slot_name, slot_details in actual_slots.items():
            slot_value = slot_details["value"]
            highlighted_input = highlighted_input.replace(slot_value, highlight_slot(input_text, slot_name, slot_value, confidence_color))

        # 判断是否需要显示该结果
        show_result = show_all or expected_intent != actual_intent or any(expected_slots[slot_name]["value"] != actual_slots.get(slot_name, {}).get("value", None) for slot_name in expected_slots) or confidence < 0.7

        if show_result:
            result_table += f"<tr><td>{input_text}</td><td style='color:{intent_color}'>{actual_intent}</td><td>{expected_intent}</td><td>{highlighted_input}</td><td style='color:{confidence_color}'>{confidence}</td></tr>"

    result_table += "</table>"

    return result_table

def plot_metrics_chart(metrics, metric_type):
    intents = list(metrics['intent_tp'].keys())
    fig = go.Figure()

    for intent in intents:
        tp = metrics['intent_tp'][intent]
        fp = metrics['intent_fp'][intent]
        fn = metrics['intent_fn'][intent]
        precision = tp / (tp + fp) if tp + fp > 0 else 0
        recall = tp / (tp + fn) if tp + fn > 0 else 0

        fig.add_trace(go.Bar(
            x=[intent],
            y=[precision if metric_type == "precision" else recall],
            name=intent,
            text=[f"{precision:.2f}" if metric_type == "precision" else f"{recall:.2f}"],
            textposition='auto'
        ))

    fig.update_layout(
        title=f"{metric_type.capitalize()} for Each Intent",
        xaxis_title="Intent",
        yaxis_title=metric_type.capitalize(),
        barmode='group'
    )

    return fig

def plot_slot_metrics_chart(metrics, intents):
    slot_fig = go.Figure()

    for intent in intents:
        for slot in set(metrics['slot_tp'][intent].keys()) | set(metrics['slot_fp'][intent].keys()) | set(metrics['slot_fn'][intent].keys()):
            tp = metrics['slot_tp'][intent][slot]
            fp = metrics['slot_fp'][intent][slot]
            fn = metrics['slot_fn'][intent][slot]
            precision = tp / (tp + fp) if tp + fp > 0 else 0
            recall = tp / (tp + fn) if tp + fn > 0 else 0

            slot_fig.add_trace(go.Bar(
                x=[f"{intent} - {slot}"],
                y=[precision],
                name=f"{intent} - {slot}",
                text=[f"{precision:.2f}"],
                textposition='auto'
            ))

            slot_fig.add_trace(go.Bar(
                x=[f"{intent} - {slot}"],
                y=[recall],
                name=f"{intent} - {slot}",
                text=[f"{recall:.2f}"],
                textposition='auto'
            ))

    slot_fig.update_layout(
        title="Precision and Recall for Each Slot",
        xaxis_title="Slot",
        yaxis_title="Metric Value",
        barmode='group'
    )

    return slot_fig