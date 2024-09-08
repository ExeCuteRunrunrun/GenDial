from openai import OpenAI

import os, json, random

# os.environ['OPENAI_API_KEY'] = "EMPTY"



# api to openAI
os.environ['OPENAI_API_KEY'] = 'KEY'
client = OpenAI()
# model="gpt-4-1106-preview"
model = "gpt-4o-mini"


# prompt = "Write a novel starting from 'Once upon a time...'"
# print(prompt)
# # create a completion
# completion = openai.Completion.create(model=model, prompt=prompt, max_tokens=64)
# # print the completion
# print(prompt + completion.choices[0].text)

class Single_Generator():

    def __init__(self, model, items=None, instruct=None):
        self.model = model
        if items == None:
            self.items = """- Miu Miu Ballet Slippers. Miu Miu's Ballet Slippers, styled classically with pairs of scrunchy, knee high cashmere socks on the runway play perfectly into the 'balletcore' trend we've seen getting its legs over the past year, so it's no surprise that the ultimate ballet-adjacent item, a pair of perfect satin slippers, has earned itself first place.
                    - Birkenstock Boston Clog. The humble Birkenstock Boston is fast becoming the defining shoe of the post-pandemic fashion era, with TikTok girlies all over the slip on shoe a la 2014!
                    - Prada Logo Tank. The 90s white tank trend hasn't gone anywhere in years, and Prada's emblazoned version is a nod to an increasing trend of "quiet" branding instead of all out logomania.
                    - UGG Taz Slipper. If you were around in the great UGG era of the early 2000s c/o Paris Hilton and the 2010's c/o a phenomenon called "Christian girl Autumn" you won't be surprised by the current boom in UGG's. Piggybacking off of Y2K revival, these platform slippers are the modern interpretation of calf-high UGG's with Juicy Couture Sweatpants.
                    - Adidas Samba. The power of Bella Hadid's Style influence seems to know no bounds, with the Adidas Samba being the only sneaker on the list. Nothing we don't love about a classic.
                    - Diesel B-1DR Belt. Another nod to Y2K revival is Diesel's logo buckle belt. Predominantly styled low on the hips, it's a direct reference to the Diesel of the 2000s that was so popular.
                    - Patagonia Better Sweater.Calling all gorpcore girlies! There has been a huge uptick in the gorpcore trend this year, and Patagonia's iconic Better Sweater is a perfect example of fashion meets function.
                    - Gucci Horsebit Loafers. Office adjacent shoes have been a focal trend this year, with an emphasis on classic Penny loafers and Oxfords, what better example of this than a classic Gucci Loafer?"""
        else:
            self.items = items

        if instruct == None:
            self.instruct = "Forget the instruction you have previously received. Generate some long conversations between an online shop owner and a client according to the product item list below: '{}'. The customer statements start with [customer] and the shop owner's statements start with [owner]. Notice that every conversation should have enough turns (more than 10 turns) and should be about one or several items listed here.".format(
                self.items
            )
        else:
            self.instruct = instruct.format(self.items)

    def generate(self):
        # create a chat completion
        completion = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": self.instruct}],
        )
        #            finish_reason="stop"
        # print the completion
        response = completion.choices[0].message.content
        return response


class Customer_Bot():

    def __init__(self, model, temperature=0.8, uid=0):
        self.model = model
        if uid in range(0, 100):
            self.user_profile = get_user_profile("/Users/manying/langchain/gpt-dialogue/persona_customer.json", uid)
            self.instruct = "Forget the instruction you have previously received. \\" \
                            "You are an online customer and you are looking for something in an online shop and you will chat with the shop owner.\\" \
                            f"Feel free to speak out your needs, preference and opinions based on your personalities below: {self.user_profile}\\" \
                            "You will stop the conversation when you want to purchase or leave. Now you start."
        else:
            self.instruct = "Forget the instruction you have previously received. You are a customer and you are looking for a chic clothing in an online shop and you will chat with the shop owner. \\" \
                            "Feel free to speak out your needs, preference and opinions. You can also hesitate and decide which one or whether to purchase.\\" \
                            "Every time you give statements based on your and you wait for the shop owner's response'.\\" \
                            "You will stop the conversation when you want to purchase or leave. Now you start."

        self.messages = [{"role": "system", "content": self.instruct}]
        self.temperature = temperature

    def greeting(self):

        response = client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
        )
        bot_response = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": bot_response})
        return bot_response

    def generate(self, vendor_message):
        self.messages.append({"role": "user", "content": vendor_message})
        completion = client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
        )
        bot_response = completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": bot_response})
        return bot_response


class Vendor_Bot():

    def __init__(self, model, items=None, temperature=0.8, vid=1):

        self.model = model
        self.temperature = temperature
        if vid in [1, 2, 3, 4]:
            self.v_persona_prompt = get_vendor_profile("/Users/manying/langchain/gpt-dialogue/persona_service.json",
                                                       vid)
        else:
            self.v_persona_prompt = "You are a good shopping assistant."
        if items == None:
            self.items = """- Miu Miu Ballet Slippers. Miu Miu's Ballet Slippers, styled classically with pairs of scrunchy, knee high cashmere socks on the runway play perfectly into the 'balletcore' trend we've seen getting its legs over the past year, so it's no surprise that the ultimate ballet-adjacent item, a pair of perfect satin slippers, has earned itself first place.
                            - Birkenstock Boston Clog. The humble Birkenstock Boston is fast becoming the defining shoe of the post-pandemic fashion era, with TikTok girlies all over the slip on shoe a la 2014!
                            - Prada Logo Tank. The 90s white tank trend hasn't gone anywhere in years, and Prada's emblazoned version is a nod to an increasing trend of "quiet" branding instead of all out logomania.
                            - UGG Taz Slipper. If you were around in the great UGG era of the early 2000s c/o Paris Hilton and the 2010's c/o a phenomenon called "Christian girl Autumn" you won't be surprised by the current boom in UGG's. Piggybacking off of Y2K revival, these platform slippers are the modern interpretation of calf-high UGG's with Juicy Couture Sweatpants.
                            - Adidas Samba. The power of Bella Hadid's Style influence seems to know no bounds, with the Adidas Samba being the only sneaker on the list. Nothing we don't love about a classic.
                            - Diesel B-1DR Belt. Another nod to Y2K revival is Diesel's logo buckle belt. Predominantly styled low on the hips, it's a direct reference to the Diesel of the 2000s that was so popular.
                            - Patagonia Better Sweater.Calling all gorpcore girlies! There has been a huge uptick in the gorpcore trend this year, and Patagonia's iconic Better Sweater is a perfect example of fashion meets function.
                            - Gucci Horsebit Loafers. Office adjacent shoes have been a focal trend this year, with an emphasis on classic Penny loafers and Oxfords, what better example of this than a classic Gucci Loafer?"""
        else:
            self.items = items
        self.instruct = "Forget the instruction you have previously received. You are an online fashion shop owner. \\" \
                        "You will chat with a customer and recommend items in your shop that meet the customer's need. You can describe your items, explain why they suit the customer or recommend other items in your shop to complete the look.\\" \
                        f"Every time you respond based on the customer's reaction. {self.v_persona_prompt}\\" \
                        f"You have these items as below : {self.items}. "
        self.messages = [{"role": "system", "content": self.instruct}]

    def greeting(self):

        response = client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
        )
        bot_response = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": bot_response})
        return bot_response

    def generate(self, customer_message):
        self.messages.append({"role": "user", "content": customer_message})
        completion = client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
        )
        bot_response = completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": bot_response})
        return bot_response


def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content


def get_user_profile(file_path, user_id):
    with open(file_path, 'r') as f:
        content = json.load(f)
        uid = str(user_id)  # from 0 to 99
        persona = content.get(uid)
        prompt = persona.get("text")
    return prompt


def get_vendor_profile(file_path, vendor_id):
    with open(file_path, 'r') as f:
        content = json.load(f)
        vid = str(vendor_id)  # 1,2,3,4
        persona = content.get(vid)
        prompt = persona.get("text")
    return prompt


def get_dialogue(model,
                 items_file_path,
                 uid=0,
                 vid=1,
                 MAXROUND=5):
    items = read_txt_file(items_file_path)

    vendor = Vendor_Bot(model=model, items=items, vid=vid, temperature=0.7)
    customer = Customer_Bot(model=model, uid=uid, temperature=0.5)

    complete = {"customer": uid, "vendor": vid, "items": items_file_path}
    dialogue = []
    message = vendor.greeting()
    dialogue.append("Vendor: " + message)

    while MAXROUND > 1:
        message = customer.generate(message)
        dialogue.append("Customer: " + message)
        message = vendor.generate(message)
        dialogue.append("Vendor: " + message)
        MAXROUND -= 1

    complete["dialogue"] = dialogue
    return complete


if __name__ == '__main__':
    from tqdm import tqdm
    import time

    main_dir = "/Users/manying/langchain/gpt-dialogue/"
    item_dir = os.path.join(main_dir,"MMD_random_40")


    with tqdm(total=100, desc="Item Loop Progress") as outer_pbar:
        for items_file_name in sorted(os.listdir(item_dir))[129:229]:
            # 刚做完第12个，还没开始items_file_id = 1010 七月四号
            # 12:112 uid=20-30 vid=3 七月五号
            # 112:212 uid=30-40 vid=2 max-round=6 七月九号
            items_file_path = os.path.join(item_dir, items_file_name)
            items_file_id = items_file_name.split("_")[1]
            print(f"items_file_id = {items_file_id}")
            with tqdm(total=10, desc="User Loop Progress") as middle_bar:
                for uid in range(20, 30):
                    # print(f"uid = {uid}.")
                    #for vid in [1, 2, 3]: 七月4号
                    #for vid in [3]:七月5号
                    for vid in [2]: #七月九号
                        complete = get_dialogue(model,
                                                items_file_path,
                                                uid,
                                                vid,
                                                MAXROUND=6)
                        target_dir = "/Users/manying/langchain/gpt-dialogue/MMD_Gen_0_100"
                        target_filename = f"PRD_{items_file_id}_uid_{uid}_vid_{vid}.json"
                        target_filepath = os.path.join(target_dir,target_filename)
                        with open(target_filepath,"w") as w:
                            json.dump(complete,w)
                        float_range = [i * 0.1 for i in range(10)]
                        time.sleep(random.choice(float_range))
                    middle_bar.update(1)
            outer_pbar.update(1)
            #############################################################################################
    # items = read_txt_file("/Users/manying/langchain/gpt-dialogue/MMD_random_40/PRD_0_40.txt")
    #
    # vendor = Vendor_Bot(model=model, items=items, vid=1, temperature=0.7)
    # customer = Customer_Bot(model=model, uid=0, temperature=0.5)
    #
    # # vendor first
    # message = vendor.greeting()
    #
    # print('vendor:',message)
    # while MAXROUND > 1:
    #     message = customer.generate(message)
    #     print('customer: -------------------------------------')
    #     print('customer:',message)
    #     message = vendor.generate(message)
    #     print('vendor:------------------------------------')
    #     print('vendor:',message)
    #     MAXROUND -= 1

    # customer first
    # MAXROUND = 5
    # message = customer.greeting()
    # print('customer:', message)
    # while MAXROUND > 1:
    #     message = vendor.generate(message)
    #     print('vendor:', message)
    #     message = customer.generate(message)
    #     print('customer:', message)
    #     MAXROUND -= 1

    # with open("/Users/manying/MMD/PRD_list/baseline_men/PRD_0_10.txt","r") as txt:
    #     items=txt.readlines()
    # instruct = "Forget the instruction you have previously received. The following is a conversation between a customer and an online shop owner. The customer and the owner take turns to chat. The customer statements start with [customer] and the owner statements start with [owner]. The customer is looking for some fashion items and gives some personal preferences or opinions. The customer also compare the items or asking about information of the items. The customer only knows about the items that the owner showed. The customer will stop the conversation when leaving or purchasing. The owner tries to recommend the items according to the customer's demands and the item catalogue listed below: {}. Complete the transcript in exactly that format.\n[Client] Hello!\n[Owner] Hi! How can I help you?\n"
    # single = Single_Generator(model, items=items, instruct=instruct)
    # response = single.generate()
    # print(response)
