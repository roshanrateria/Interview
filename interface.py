import gradio as gr
from utils import *

with gr.Blocks(gr.themes.Soft()) as interface:
    end_time_state = gr.State([0])
    with gr.Tab("Resume and Job Search"):
        gr.Markdown("# 📄 Job Assistant Chatbot")
        gr.Markdown("Upload your resume and ask for job suggestions, resume feedback, cover letters, or interview preparation.")
        chatbot = gr.Chatbot(type="messages")
        query_input = gr.MultimodalTextbox(interactive=True, placeholder="Enter message or upload resume...", show_label=False)
        submit_button = gr.Button("Send")
        submit_button.click(chatbot_interface, [chatbot, query_input], [chatbot, query_input])
        query_input.submit(chatbot_interface, [chatbot, query_input], [chatbot, query_input])
   
    with gr.Tab("Interview Mode"):
    
     with gr.Row():
        with gr.Column():
         question_type_dropdown = gr.Dropdown(["Technical", "HR"], label="Question Type")
         start_interview_button = gr.Button("Start Interview")
        with gr.Column():
         interview_timer = gr.Plot() 
     interview_question = gr.Markdown()

     start_interview_button.click(start_interview, [question_type_dropdown, end_time_state], [interview_question, interview_timer, end_time_state])

     interface.load(update_timer, inputs=[end_time_state], outputs=[interview_timer, submit_button,end_time_state], every=1.0)
     video_upload = gr.File(label="Upload Interview Video", file_types=["mp4"])
     analyze_button = gr.Button("Analyze")
     gaze_result = gr.Plot()
     emotion_result = gr.Plot()
     transcription = gr.Textbox(lines=3, label="Answer Transcription", interactive=False)
     analyze_button.click(analyze_video, [video_upload, end_time_state], [gaze_result, emotion_result, transcription, end_time_state])

    with gr.Tab("Evaluation"):
        evaluate_button = gr.Button("Get Score")
        score_output = gr.Plot(label="Score")
        feedback_output = gr.Markdown()
        evaluate_button.click(submit_answer, [interview_question, transcription], [score_output, feedback_output])


interface.launch()
