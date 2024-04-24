from g2p import make_g2p

transducer = make_g2p('eng', 'eng-ipa')

def rate_apply(batch, rank=None, audio_column_name="audio", text_column_name="text"):
    if isinstance(batch[audio_column_name], list):  
        speaking_rates = []
        phonemes_list = []
        for text, audio in zip(batch[text_column_name], batch[audio_column_name]):
            phonemes = transducer(text).output_string
            
            sample_rate = audio["sampling_rate"]
            audio_length = len(audio["array"].squeeze()) / sample_rate
            
            if audio_length > 0:
                speaking_rate = len(phonemes) / audio_length
            else:
                speaking_rate = 0
            
            speaking_rates.append(speaking_rate)
            phonemes_list.append(phonemes)
        
        batch["speaking_rate"] = speaking_rates
        batch["phonemes"] = phonemes_list
    else:
        phonemes = transducer(batch[text_column_name]).output_string
            
        sample_rate = batch[audio_column_name]["sampling_rate"]
        audio_length = len(batch[audio_column_name]["array"].squeeze()) / sample_rate
        if audio_length > 0:
            speaking_rate = len(phonemes) / audio_length
        else:
            speaking_rate = 0
                        
        batch["speaking_rate"] = speaking_rate
        batch["phonemes"] = phonemes

    return batch