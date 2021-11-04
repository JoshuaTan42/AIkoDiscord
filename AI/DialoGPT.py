from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")


def conversation(text):
    chat_history_ids = []
    count = 0
    while count != 100_000:
        new_user_input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors='pt')
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=1) if count > 0 else new_user_input_ids
        chat_history_ids = model.generate(
            bot_input_ids,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            temperature=0.7)
        count += 1
        if count == 99_999:
            chat_history_ids = []
            count = 0
            print("reset")
        else:
            return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
