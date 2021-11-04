from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import torch

tokenizer = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-3B")
model = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot-3B")


def conversation(text):
    inputs = tokenizer([text], return_tensors='pt')
    reply_ids = model.generate(**inputs)
    output = tokenizer.batch_decode(reply_ids)
    output = ' '.join(output)
    return output



input = "What do you think of Elon Musk and Jeff Bezos"
print(conversation(input))