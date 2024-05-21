import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model_name = ""
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

chatbot_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

def food_recommendation(messages, user_message):
    # if "점심" in user_message:
    #     bot_message = "점심으로 파스타는 어떠세요?"
    # elif "저녁" in user_message:
    #     bot_message = "저녁으로 스테이크는 어떠세요?"
    # elif "디저트" in user_message:
    #     bot_message = "디저트로 아이스크림은 어떠세요?"
    # else:
    #     bot_message = "어떤 음식을 추천해 드릴까요?"

    bot_response = chatbot_pipeline(user_message, max_length=100, num_return_sequences=1)[0]['generated_text']
    bot_message = bot_response

    messages.append((user_message, bot_message))
    return messages, ""

# Gradio 인터페이스 정의
with gr.Blocks(css="""
    @font-face {
    font-family: 'Katuri';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_13@1.0/Katuri.woff') format('woff');
    font-weight: normal;
    font-style: normal;
    }        
    @import url('//fonts.googleapis.com/earlyaccess/notosanskr.css');
               
               
    .user {
    background-color: #F7CAC9; 
    padding: 10px; 
    border-radius: 20px 20px 0 20px; 
    align-self: flex-end; 
    margin: 5px 0; 
    font-family: 'Noto Sans KR';
    }
    .bot {
    background-color: #ABCEF0; 
    padding: 10px; 
    border-radius: 20px 20px 20px 0; 
    align-self: flex-start; 
    margin: 5px 0; 
    font-family: 'Noto Sans KR';
    }
    
    .gr-chat-message {
        background-color: white;
        padding: 10px;
        border-radius: 15px;
        box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
        margin: 5px;
        position: relative;
    }
    .gr-chat-message.bot {
        background-color: #F7CAC9;  
        align-self: flex-start;
    }
    .gr-chat-message.user {
        background-color: #FFD740;
        align-self: flex-end;
    }
    .send-button {
        background-color: white !important;
        color: black !important;
        width: 10px;
        height: 50px;
        font-size: 14px !important;
        border: none !important; 
        border-radius: 5px !important;
        cursor: pointer !important;
    }

    .send-button:hover {
        background-color: #45a049 !important;
    }
    .chat-container {
        background: linear-gradient(to right, #6a11cb 0%, #2575fc 100%);
    }
               
    
""") as demo:
    gr.Markdown("<h1 style=\"text-align: center; color: black; font-family: 'Katuri', sans-serif; font-size: 32px\">🍽️ 메추리 🍽️</h1>")
    
    chatbot = gr.Chatbot()
    
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="음식 종류나 끼니를 입력하세요. 예: 점심, 저녁, 디저트")
        txt.submit(food_recommendation, [chatbot, txt], [chatbot, txt])
        submit_btn = gr.Button("보내기", elem_classes="send-button")

    def on_submit(user_message, state):
        return food_recommendation(state, user_message)
    
    submit_btn.click(on_submit, [txt, chatbot], [chatbot, txt])

    with gr.Row():
        gr.Markdown("<p style='text-align: center;'>챗봇에게 원하는 음식 종류나 끼니를 입력하면 추천해 드립니다!</p>")

demo.launch()
