import subprocess
import argparse
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--textfile', type=str, help='A file containing the text to read.', default="tortoise/data/riding_hood.txt")
    parser.add_argument('--voice', type=str, help='Selects the voice to use for generation. See options in voices/ directory (and add your own!) '
                                                 'Use the & character to join two voices together. Use a comma to perform inference on multiple voices.', default='pat')
    parser.add_argument('--output_path', type=str, help='Where to store outputs.', default='results/longform/')
    parser.add_argument('--output_name', type=str, help='How to name the output file', default='combined.wav')
    parser.add_argument('--preset', type=str, help='Which voice preset to use.', default='standard')
    parser.add_argument('--regenerate', type=str, help='Comma-separated list of clip numbers to re-generate, or nothing.', default=None)
    parser.add_argument('--candidates', type=int, help='How many output candidates to produce per-voice. Only the first candidate is actually used in the final product, the others can be used manually.', default=1)
    parser.add_argument('--model_dir', type=str, help='Where to find pretrained model checkpoints. Tortoise automatically downloads these to .models, so this'
                                                      'should only be specified if you have custom checkpoints.', default='')
    parser.add_argument('--seed', type=int, help='Random seed which can be used to reproduce results.', default=None)
    parser.add_argument('--produce_debug_state', type=bool, help='Whether or not to produce debug_state.pth, which can aid in reproducing problems. Defaults to true.', default=True)
    parser.add_argument('--use_deepspeed', type=bool, help='Use deepspeed for speed bump.', default=False)
    parser.add_argument('--kv_cache', type=bool, help='If you disable this please wait for a long a time to get the output', default=True)
    parser.add_argument('--half', type=bool, help="float16(half) precision inference if True it's faster and take less vram and ram", default=True)

    args = parser.parse_args()

    with open(args.textfile, 'r', encoding='utf-8') as f:
        text = ' '.join([l for l in f.readlines()])

    # Define the possible characters at the end of a sentence
    chars = ['. ', '! ', '? ']
    # Replace the with uniqe characters
    for char in chars:
        text = text.replace(char, '°°')

    # Create the list of sentences
    results = text.split('°°')

    # Check how many sentences were in the text file
    dir = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
    if len(results) <= 3:
        subprocess.run(['python', 'read.py',
                        '--textfile', args.textfile,
                        '--output_path', args.output_path],
                       cwd=dir,
                       check=True)
    else:
        id = -1
        for result in results:
            id += 1
            subprocess.run(['python', 'do_tts.py',
                            '--text', result,
                            '--output_path', args.output_path,
                            '--name_id', str(id)],
                           cwd=dir,
                           check=True)
