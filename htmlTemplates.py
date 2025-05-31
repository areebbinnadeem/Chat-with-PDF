css = '''
<style>
.chat-message {
    padding: 1.2rem 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    line-height: 1.5;
}
.chat-message.user {
    background-color: #2b313e;
    color: #fff;
    margin-left: 20%;
    border-bottom-right-radius: 0;
}
.chat-message.bot {
    background-color: #475063;
    color: #fff;
    margin-right: 20%;
    border-bottom-left-radius: 0;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    {{MSG}}
</div>
'''

user_template = '''
<div class="chat-message user">
    {{MSG}}
</div>
'''