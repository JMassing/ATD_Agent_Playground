import asyncio
import argparse

from pydantic_graph import Graph

from nodes.test_generator import TestGenerator
from nodes.test_runner import TestRunner
from nodes.test_state import TestState

async def main():
    parser = argparse.ArgumentParser(description='Generate and run tests for a code file')
    parser.add_argument('-c', '--code_file', type=str, help='Path to the code file to generate tests for', required=True)
    parser.add_argument('-o', '--test_output', type=str, help='Output path for the generated tests', required=True)
    parser.add_argument('-f', '--function_name', type=str, default="", help='Specific function name to generate tests for', required=False)
    
    args = parser.parse_args()
    
    graph_input = TestState(code_path=args.code_file, output_path=args.test_output, function_name=args.function_name)
    graph = Graph(nodes=(TestGenerator, TestRunner))

    result = await graph.run(start_node=TestGenerator(), state=graph_input) 
    print(f"{result.output}")

if __name__ == "__main__":
    asyncio.run(main())