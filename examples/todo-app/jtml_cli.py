import argparse
from compiler.compiler import JTMLCompiler

def compile_jtml(input_file, output_file, stage, progressive, pqtt_enabled):
    compiler = JTMLCompiler()

    if progressive:
        print(f"Performing progressive compilation for {input_file} with intermediate representations")
        intermediate_rep = compiler.progressive_compile([input_file], stage=stage)
        print(f"Generated Intermediate Representation: {intermediate_rep}")
        
        if stage == 'final':
            output = compiler.progressive_compile([input_file], stage='final')
            print(f"Final Compilation Result: {output}")
    else:
        output = compiler.compile([input_file])
    
    # Save the final output if in final stage
    if stage == 'final' or not progressive:
        if output is not None:
            with open(output_file, 'w') as f:
                f.write(output)
            print(f"Compiled output saved to {output_file}")
        else:
            print(f"No valid output generated for {output_file}.")

def main():
    parser = argparse.ArgumentParser(description='JTML Compiler with PQTT and Progressive Compilation')
    parser.add_argument('--input', type=str, required=True, help='Input JTML file')
    parser.add_argument('--output', type=str, required=True, help='Output HTML file')
    parser.add_argument('--stage', type=str, default='final', help='Stage of the compilation: intermediate or final')
    parser.add_argument('--progressive', action='store_true', help='Enable progressive compilation')
    parser.add_argument('--pqtt', action='store_true', help='Enable PQTT integration')

    args = parser.parse_args()
    compile_jtml(args.input, args.output, args.stage, args.progressive, args.pqtt)

if __name__ == "__main__":
    main()
