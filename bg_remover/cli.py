import argparse
import os
from bg_remover.core import process_file, process_folder

def main():
    parser = argparse.ArgumentParser(description="Image Background Remover CLI")
    parser.add_argument("--input", "-i", required=True, help="Input file or folder path")
    parser.add_argument("--output", "-o", required=True, help="Output file or folder path")
    parser.add_argument("--model", "-m", default="u2net", help="Model name (e.g. u2net, isnet-general-use, u2net_human_seg)")
    
    args = parser.parse_args()
    
    if os.path.isdir(args.input):
        print(f"Processing directory: {args.input} with model {args.model}")
        process_folder(args.input, args.output, model_name=args.model)
    elif os.path.isfile(args.input):
        print(f"Processing file: {args.input} with model {args.model}")
        # If output is an existing directory, we infer the output filename
        if os.path.isdir(args.output) or not args.output.lower().endswith('.png'):
            if not os.path.exists(args.output):
                os.makedirs(args.output)
            output_filename = os.path.splitext(os.path.basename(args.input))[0] + '_nobg.png'
            output_path = os.path.join(args.output, output_filename)
        else:
            output_path = args.output
            
        process_file(args.input, output_path, model_name=args.model)
    else:
        print(f"Error: Input path '{args.input}' does not exist.")

if __name__ == "__main__":
    main()
