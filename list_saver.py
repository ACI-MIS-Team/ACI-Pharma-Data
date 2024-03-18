
import os
import time
import wavio, json, random, torch
import numpy as np
import sounddevice as sd


def main():
    
    sr = 16000
    
    dir = input("Who is this User? What is your name? : ")
    if not os.path.isdir(dir):
        os.mkdir(dir)
        print(f"Created directory: {dir}\n")
    else:
        print(f"Found existing directory: {dir}\n")
    
    recordCounter = 0
    
    cmd = input("Press 'enter' to Continue, Anything else to quit: ")
    if cmd == "":
        
        while True:
            word = create_randomized_word()
            
            list_of_audios = os.listdir(dir)
            if word in list_of_audios:
                continue
            
            cmd = input(f"[Enter] to start recording,  [q] to quit => Next Word - `{word}`:")
            if cmd == "":
                recording = []
                def callback(indata, frames, time, status):
                    recording.append(indata.copy())
                    
                # Create a stream object with callback
                with sd.InputStream(samplerate=sr, channels=1, callback=callback):
                    while True:
                        time.sleep(0.1)
                        if input() == "":  # Stop recording when 'q' is pressed
                            break

                # Convert list of numpy arrays into a single numpy array
                myrecording = np.concatenate(recording, axis=0)
                print(myrecording.shape)
                
                # if not filename.endswith(".wav"):
                filename = os.path.join(dir, word.replace(" ", "_") + ".wav")
                    
                    
                wavio.write(filename, myrecording, sr, sampwidth=2)
                recordCounter += 1
                print(f"Saved Recording - {recordCounter}, Filename -  {filename}")
            
            elif cmd == "q":
                print("Recording Suspended!")
                break
            else:
                print(f"{word} Skipped!")
                
    print(f'Total {recordCounter} recordings saved by User "{dir}", Bye!')


def create_randomized_word(json_data_path = 'data_gen_list.json', middle_part_prob = 0.75, packsize_prob = 0.5):
    with open(json_data_path, 'r') as f:
        data = json.load(f)
    
    first_part = random.choice(data['first_part'])
    middle_part = random.choice(data['middle_part'])
    final_part = random.choice(data['final_part'])
    pack_size = random.choice(data['pack_size'])
    
    if torch.rand((1)) >= middle_part_prob:
        single_product_name = f'{first_part} {middle_part} {final_part}'
    else:
        single_product_name = f'{first_part} {final_part}'
    
    if torch.rand((1)) >= packsize_prob:
        single_product_name = f'{single_product_name} {pack_size}'
    
    return single_product_name
   
if __name__ == '__main__':
    main()