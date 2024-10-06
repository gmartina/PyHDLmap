import json
import os

# Example JSON structure:
# {
#     "register_maps": [
#         {
#             "name": "MAP1",
#             "description": "First register map",
#             "base_address": "0x40000000",
#             "registers": [
#                 {
#                     "name": "CONTROL_REG",
#                     "offset": "0x00",
#                     "bitfields": [
#                         {"name": "ENABLE", "bitshift": 0, "bitwidth": 1, "description": "Enable control"},
#                         {"name": "MODE", "bitshift": 1, "bitwidth": 3, "description": "Mode selection"}
#                     ]
#                 },
#                 {
#                     "name": "STATUS_REG",
#                     "offset": "0x04",
#                     "bitfields": [
#                         {"name": "READY", "bitshift": 0, "bitwidth": 1, "description": "Ready status"}
#                     ]
#                 }
#             ]
#         },
#         {
#             "name": "MAP2",
#             "description": "Second register map",
#             "base_address": "0x50000000",
#             "registers": [
#                 {
#                     "name": "CONFIG_REG",
#                     "offset": "0x00",
#                     "bitfields": [
#                         {"name": "CONFIG", "bitshift": 0, "bitwidth": 4, "description": "Configuration settings"}
#                     ]
#                 }
#             ]
#         }
#     ]
# }

def generate_register_map(json_file_path, output_file_path):
    # Load the JSON file
    with open(json_file_path, 'r') as json_file:
        register_maps = json.load(json_file).get("register_maps", [])

    # Create and open the output .h file
    with open(output_file_path, 'w') as header_file:
        # Write header guard
        header_guard = os.path.basename(output_file_path).replace('.', '_').upper()
        header_file.write(f"#ifndef {header_guard}\n#define {header_guard}\n\n")

        # Write register map definitions
        for register_map in register_maps:
            map_name = register_map.get("name", "UNKNOWN_MAP")
            description = register_map.get("description", "No description available")
            base_address = register_map.get("base_address", "0x00000000")
            registers = register_map.get("registers", [])

            # Write register map description and base address definition
            header_file.write(f"// Register Map: {map_name} - {description}\n")
            header_file.write(f"#define {map_name}_BASE_ADDRESS {base_address}\n\n")

            # Write register definitions
            for reg in registers:
                reg_name = reg.get("name", "UNKNOWN_REG")
                offset = reg.get("offset", "0x00")
                bitfields = reg.get("bitfields", [])

                # Register offset definition
                header_file.write(f"// Register: {reg_name}\n")
                header_file.write(f"#define {map_name}_{reg_name}_OFFSET ({offset})\n")
                header_file.write(f"#define {map_name}_{reg_name}_ADDRESS ({map_name}_BASE_ADDRESS + {map_name}_{reg_name}_OFFSET)\n\n")

                # Write bitfield definitions
                for bitfield in bitfields:
                    bf_name = bitfield.get("name", "UNKNOWN_BF")
                    bitshift = bitfield.get("bitshift", 0)
                    bitwidth = bitfield.get("bitwidth", 1)
                    bf_description = bitfield.get("description", "No description available")

                    header_file.write(f"// Bitfield: {bf_name} ({bf_description})\n")
                    header_file.write(f"#define {map_name}_{reg_name}_{bf_name}_BITSHIFT ({bitshift})\n")
                    header_file.write(f"#define {map_name}_{reg_name}_{bf_name}_BITWIDTH ({bitwidth})\n\n")

        # Write end of header guard
        header_file.write(f"#endif // {header_guard}\n")

def generate_register_map_markdown(json_file_path, output_file_path):
    # Load the JSON file
    with open(json_file_path, 'r') as json_file:
        register_maps = json.load(json_file).get("register_maps", [])

    # Create and open the output .md file
    with open(output_file_path, 'w') as markdown_file:
        # Write documentation for each register map
        for register_map in register_maps:
            map_name = register_map.get("name", "UNKNOWN_MAP")
            description = register_map.get("description", "No description available")
            base_address = register_map.get("base_address", "0x00000000")
            registers = register_map.get("registers", [])

            # Write register map description
            markdown_file.write(f"# Register Map: {map_name}\n\n")
            markdown_file.write(f"**Description**: {description}\n\n")
            markdown_file.write(f"**Base Address**: `{base_address}`\n\n")

            # Write register definitions
            for reg in registers:
                reg_name = reg.get("name", "UNKNOWN_REG")
                offset = reg.get("offset", "0x00")
                bitfields = reg.get("bitfields", [])

                # Register offset definition
                markdown_file.write(f"## Register: {reg_name}\n\n")
                markdown_file.write(f"**Offset**: `{offset}`\n\n")
                markdown_file.write(f"**Address**: `{map_name}_BASE_ADDRESS + {reg_name}_OFFSET`\n\n")

                # Write bitfield definitions
                if bitfields:
                    markdown_file.write(f"### Bitfields\n\n")
                    for bitfield in bitfields:
                        bf_name = bitfield.get("name", "UNKNOWN_BF")
                        bitshift = bitfield.get("bitshift", 0)
                        bitwidth = bitfield.get("bitwidth", 1)
                        bf_description = bitfield.get("description", "No description available")

                        markdown_file.write(f"- **{bf_name}**: {bf_description}\n")
                        markdown_file.write(f"  - **Bitshift**: `{bitshift}`\n")
                        markdown_file.write(f"  - **Bitwidth**: `{bitwidth}`\n\n")

if __name__ == "__main__":
    # Example usage
    json_file_path = "register_map.json"  # Path to the input JSON file
    output_header_path = "register_map.h"    # Path to the output header file
    output_markdown_path = "register_map.md"  # Path to the output markdown file

    generate_register_map(json_file_path, output_header_path)
    print(f"Register map header file generated: {output_header_path}")

    generate_register_map_markdown(json_file_path, output_markdown_path)
    print(f"Register map markdown documentation generated: {output_markdown_path}")