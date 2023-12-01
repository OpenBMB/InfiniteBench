import jsonlines
import random 
import os
import re


def build_number_string():
    #####32
    # prompt = "There is an important info hidden inside a lot of irrelevant text. Find it. I will quiz you about the important information there.\n"
    #####25
    noise = "The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again.\n"
    #####26
    ans = "The sequence of digits is {key}. Remember it. {key} is the sequence of digits.\n"
    #####10
    question = "What is the sequence of digits?"


    target_length = [1024 * 64, 1024 * 128]
    num_noise = [2610, 5220]
    step = [45, 90]
    repeat_time = 10
    for i in range(1, 2):
        target_length_i = target_length[i]
        step_i = step[i]
        num_noise_i = num_noise[i]
        ret = []
        for j in range(0, num_noise_i+1, step_i):
            input_text =  noise * j + ans + noise * (num_noise_i - j)
            for t in range(repeat_time):
                keys = []
                for k in range(5):
                    keys.append(str(random.randint(0,9)))
                for k in range(5):
                    pos = random.randint(0,5+k-1)
                    keys.insert(pos, keys[pos])
                key_t = "".join(keys)
                ret.append({"context": input_text.replace("{key}", key_t), "answer": key_t, "input": question, "len": 26 * (num_noise_i - j)})
        fw = jsonlines.open("number_string.jsonl", 'w')
        fw.write_all(ret)
        fw.close()


def build_passkey():
    #####32
    # prompt = "There is an important info hidden inside a lot of irrelevant text. Find it and memorize them. I will quiz you about the important information there.\n"
    #####25
    noise = "The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again.\n"
    #####26
    ans = "The pass key is {key}. Remember it. {key} is the pass key.\n"
    #####10
    question = "What is the pass key?"

    target_length = [1024 * 32, 1024 * 64, 1024 * 128, 1024 * 256]
    num_noise = [1305, 2610, 5220, 10440]
    step = [15, 45, 90, 180]
    repeat_time = 5
    for i in range(2, 3):
        target_length_i = target_length[i]
        step_i = step[i]
        num_noise_i = num_noise[i]
        ret = []
        for j in range(0, num_noise_i+1, step_i):
            input_text = noise * j + ans + noise * (num_noise_i - j)
            for t in range(repeat_time):
                keys = []
                for k in range(5):
                    keys.append(str(random.randint(0,9)))
               
                key_t = "".join(keys)
                ret.append({"input": question, "context": input_text.replace("{key}", key_t), "answer": key_t, "len": 26 * (num_noise_i - j)})
        fw = jsonlines.open("passkey.jsonl", 'w')
        fw.write_all(ret)
        fw.close()


def build_kv_retrieval():

    target_length = [64 * 1024, 128 * 1024]
    # interv = [16, 7]
    nsample = [500, 500]
    nnoise = [928, 2500]
    for ii in range(1, 2):
        cnt = -1
        ret = []

        with jsonlines.open("kv-retrieval-3000_keys.jsonl") as fin:
            for line in fin:
                print(len(line["ordered_kv_records"]))
                # return 0
                cnt += 1
                if cnt == nsample[ii]:
                    break
                ans_id = min(int(cnt * nnoise[ii] / nsample[ii]), nnoise[ii])

                text = "JSON data:\n{"
                t = -1
                random.shuffle(line["ordered_kv_records"])
                for item in line["ordered_kv_records"]:
                    t += 1
                    if t == nnoise[ii]:
                        break
                    text += "\"" + item[0] + "\": \"" + item[1] + "\", "
                text = text[:-2] + '}'
                question = "\nKey: \"" + line["ordered_kv_records"][ans_id][0] +  "\"\nThe value associated with the specified key is: "
                # text += "\nKey: \"" + line["ordered_kv_records"][ans_id][0] +  "\"\nThe value associated with the specified key is: "
                # print(len(tokenizer.encode(text)))
                # break
                ret.append({"context": text, "input": question, "answer": line["ordered_kv_records"][ans_id][1]})
            
        
        fw = jsonlines.open("kv_retrieval.jsonl", 'w')
        fw.write_all(ret)
        fw.close()


if __name__ == "__main__":
    os.system("git clone https://github.com/nelson-liu/lost-in-the-middle.git")
    os.system("python3.10 -u lost-in-the-middle/scripts/make_kv_retrieval_data.py --num-keys 3000 --num-examples 500 --output-path kv-retrieval-3000_keys.jsonl.gz")
    os.system("gzip -d kv-retrieval-3000_keys.jsonl.gz")
    build_kv_retrieval()
    build_passkey()
    build_number_string()
