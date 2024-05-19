import streamlit as st
from components.result_stat import generate_result_table, plot_metrics_chart, plot_slot_metrics_chart
from components.intent_stat import plot_intent_dist

from config import AGENT_PROJECT_DIR
from utils import load_test_cases, test_nlu, calculate_metrics

def nlu_test_cases_tab():
    st.header("针对 NLU 测试")

    nlu_test_cases = load_test_cases(AGENT_PROJECT_DIR, 'nlu')[0:10]

    # 统计各个意图的测试用例数量
    intent_counts = {}
    for case in nlu_test_cases:
        intent = case["expected_intent"]
        intent_counts[intent] = intent_counts.get(intent, 0) + 1

    fig = plot_intent_dist(nlu_test_cases, intent_counts)
    st.plotly_chart(fig)

    st.markdown("---")

    # 添加按钮
    if st.button("运行NLU测试"):
        nlu_results = test_nlu(nlu_test_cases)
        st.write("测试结果：")

        # 使用 session_state 来存储复选框的状态
        if 'show_all' not in st.session_state:
            st.session_state.show_all = False

        # 添加复选框
        def update_show_all():
            st.session_state.show_all = not st.session_state.show_all

        st.checkbox("显示所有结果", value=st.session_state.show_all, on_change=update_show_all)

        # 渲染结果表格
        result_table = generate_result_table(nlu_results, st.session_state.show_all)
        table_container = st.markdown(result_table, unsafe_allow_html=True)

        # 重新渲染表格以反映复选框的变化
        if st.session_state.show_all:
            result_table = generate_result_table(nlu_results, True)
        else:
            result_table = generate_result_table(nlu_results, False)
        table_container.markdown(result_table, unsafe_allow_html=True)

        st.markdown("---")

        # 计算并显示各个意图的准确率和召回率
        st.subheader("各个意图的准确率和召回率：")
        stats = calculate_metrics(nlu_results)
        # 绘制意图准确率和召回率图表
        
        precision_fig = plot_metrics_chart(stats, "precision")
        recall_fig = plot_metrics_chart(stats, "recall")
        st.plotly_chart(precision_fig)
        st.plotly_chart(recall_fig)

        # 绘制槽位准确率和召回率图表
        slot_fig = plot_slot_metrics_chart(stats, intent_counts.keys())
        st.plotly_chart(slot_fig)
