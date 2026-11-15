import streamlit as st
from openai import OpenAI

# 1. 把你刚才拿到的智谱 Key 填在下面引号里（格式是 xxx.xxx）
client = OpenAI(
    api_key=st.secrets["ZHIPU_API_KEY"], 
    base_url="https://open.bigmodel.cn/api/paas/v4/" 
)

st.set_page_config(page_title="Dsy AI", page_icon="🤖")
st.title("🤖 Dsy AI 网站")
st.markdown("⭐ 如果你觉得这个 AI 好玩，请去 [GitHub 给我的项目点个 Star](https://github.com/dsy66063/MyAI-web) ⭐")
st.caption("基于智谱免费大模型打造")

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "你是一个聪明、友好的AI助手"}]

# 显示历史聊天
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 接收用户输入
if prompt := st.chat_input("说点什么吧..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="glm-4-flash",  # 这是永久免费的模型
                messages=st.session_state.messages,
                stream=True 
            )
            
            def stream_data():
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
                        
            reply = st.write_stream(stream_data)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"报错了: {e}")
