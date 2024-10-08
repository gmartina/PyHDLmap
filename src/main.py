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
#                     "access": "read-write",
#                     "bitfields": [
#                         {"name": "ENABLE", "bitshift": 0, "bitwidth": 1, "description": "Enable control", "default_value": 0},
#                         {"name": "MODE", "bitshift": 1, "bitwidth": 3, "description": "Mode selection", "default_value": 0}
#                     ]
#                 },
#                 {
#                     "name": "STATUS_REG",
#                     "offset": "0x04",
#                     "access": "read-only",
#                     "bitfields": [
#                         {"name": "READY", "bitshift": 0, "bitwidth": 1, "description": "Ready status", "default_value": 0, "enum": {"OFF": 0, "ON": 1}}
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
#                     "access": "write-only",
#                     "bitfields": [
#                         {"name": "CONFIG", "bitshift": 0, "bitwidth": 4, "description": "Configuration settings", "default_value": 0}
#                     ]
#                 }
#             ]
#         }
#     ]
# }

def generate_register_map(json_file_path):
    # Load the JSON file
    with open(json_file_path, 'r') as json_file:
        register_maps = json.load(json_file).get("register_maps", [])

    # Generate one header file per register map
    for register_map in register_maps:
        map_name = register_map.get("name", "UNKNOWN_MAP")
        description = register_map.get("description", "No description available")
        base_address = register_map.get("base_address", "0x00000000")
        registers = register_map.get("registers", [])

        output_file_path = f"{map_name.lower()}_register_map.h"
        with open(output_file_path, 'w') as header_file:
            # Write header guard
            header_guard = os.path.basename(output_file_path).replace('.', '_').upper()
            header_file.write(f"#ifndef {header_guard}\n#define {header_guard}\n\n")

            # Write register map description and base address definition
            header_file.write(f"// Register Map: {map_name} - {description}\n")
            header_file.write(f"#define {map_name}_BASE_ADDRESS {base_address}\n\n")

            # Write register definitions
            for reg in registers:
                reg_name = reg.get("name", "UNKNOWN_REG")
                offset = reg.get("offset", "0x00")
                access = reg.get("access", "read-write")
                bitfields = reg.get("bitfields", [])

                # Register offset definition
                header_file.write(f"// Register: {reg_name}\n")
                header_file.write(f"// Access: {access}\n")
                header_file.write(f"#define {map_name}_{reg_name}_OFFSET ({offset})\n")
                header_file.write(f"#define {map_name}_{reg_name}_ADDRESS ({map_name}_BASE_ADDRESS + {map_name}_{reg_name}_OFFSET)\n\n")

                # Write bitfield definitions and macros
                for bitfield in bitfields:
                    bf_name = bitfield.get("name", "UNKNOWN_BF")
                    bitshift = bitfield.get("bitshift", 0)
                    bitwidth = bitfield.get("bitwidth", 1)
                    bf_description = bitfield.get("description", "No description available")
                    bf_default_value = bitfield.get("default_value", 0)
                    bf_mask = ((1 << bitwidth) - 1) << bitshift
                    bf_enum = bitfield.get("enum", None)

                    header_file.write(f"// Bitfield: {bf_name} ({bf_description})\n")
                    header_file.write(f"#define {map_name}_{reg_name}_{bf_name}_BITSHIFT ({bitshift})\n")
                    header_file.write(f"#define {map_name}_{reg_name}_{bf_name}_BITWIDTH ({bitwidth})\n")
                    header_file.write(f"#define {map_name}_{reg_name}_{bf_name}_DEFAULT_VALUE ({bf_default_value})\n")
                    header_file.write(f"#define {map_name}_{reg_name}_{bf_name}_MASK (0x{bf_mask:X})\n")

                    # Write ENUM definitions if available
                    if bf_enum:
                        for enum_name, enum_value in bf_enum.items():
                            header_file.write(f"#define {map_name}_{reg_name}_{bf_name}_{enum_name} ({enum_value})\n")

                    # Read macro
                    header_file.write(f"#define {map_name}_{reg_name}_{bf_name}_READ() \
    ((*((volatile unsigned int*){map_name}_{reg_name}_ADDRESS) & {map_name}_{reg_name}_{bf_name}_MASK) >> {map_name}_{reg_name}_{bf_name}_BITSHIFT)\n")

                    # Write macro (only if the access is read-write or write-only)
                    if access in ["read-write", "write-only"]:
                        header_file.write(f"#define {map_name}_{reg_name}_{bf_name}_WRITE(value) \
    do {{ \
        unsigned int reg_value = *((volatile unsigned int*){map_name}_{reg_name}_ADDRESS); \
        reg_value &= ~{map_name}_{reg_name}_{bf_name}_MASK; \
        reg_value |= ((value << {map_name}_{reg_name}_{bf_name}_BITSHIFT) & {map_name}_{reg_name}_{bf_name}_MASK); \
        *((volatile unsigned int*){map_name}_{reg_name}_ADDRESS) = reg_value; \
    }} while (0)\n\n")

            # Write end of header guard
            header_file.write(f"#endif // {header_guard}\n")

def generate_register_map_source(json_file_path):
    # Load the JSON file
    with open(json_file_path, 'r') as json_file:
        register_maps = json.load(json_file).get("register_maps", [])

    # Generate one source file per register map
    for register_map in register_maps:
        map_name = register_map.get("name", "UNKNOWN_MAP")
        registers = register_map.get("registers", [])

        output_file_path = f"{map_name.lower()}_register_map.c"
        with open(output_file_path, 'w') as source_file:
            # Include the corresponding header file
            source_file.write(f"#include \"{map_name.lower()}_register_map.h\"\n\n")

            # Add any additional C file content if needed (currently left empty)

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
                access = reg.get("access", "read-write")
                bitfields = reg.get("bitfields", [])

                # Register offset definition
                markdown_file.write(f"## Register: {reg_name}\n\n")
                markdown_file.write(f"**Offset**: `{offset}`\n\n")
                markdown_file.write(f"**Address**: `{map_name}_BASE_ADDRESS + {reg_name}_OFFSET`\n\n")
                markdown_file.write(f"**Access**: `{access}`\n\n")

                # Write bitfield definitions
                if bitfields:
                    markdown_file.write(f"### Bitfields\n\n")
                    for bitfield in bitfields:
                        bf_name = bitfield.get("name", "UNKNOWN_BF")
                        bitshift = bitfield.get("bitshift", 0)
                        bitwidth = bitfield.get("bitwidth", 1)
                        bf_description = bitfield.get("description", "No description available")
                        bf_default_value = bitfield.get("default_value", 0)
                        bf_mask = ((1 << bitwidth) - 1) << bitshift
                        bf_enum = bitfield.get("enum", None)

                        markdown_file.write(f"- **{bf_name}**: {bf_description}\n")
                        markdown_file.write(f"  - **Bitshift**: `{bitshift}`\n")
                        markdown_file.write(f"  - **Bitwidth**: `{bitwidth}`\n")
                        markdown_file.write(f"  - **Default Value**: `{bf_default_value}`\n")
                        markdown_file.write(f"  - **Bit Mask**: `0x{bf_mask:X}`\n")

                        # Write ENUM values if available
                        if bf_enum:
                            markdown_file.write(f"  - **Enum Values**:\n")
                            for enum_name, enum_value in bf_enum.items():
                                markdown_file.write(f"    - `{enum_name}`: `{enum_value}`\n")
                        markdown_file.write(f"\n")

def json_sanity_check(json_file_path):
    # Load the JSON file
    with open(json_file_path, 'r') as json_file:
        register_maps = json.load(json_file).get("register_maps", [])

    for register_map in register_maps:
        base_address = int(register_map.get("base_address", "0x00000000"), 16)
        registers = register_map.get("registers", [])

        # Check for overlapping register offsets
        register_addresses = set()
        for reg in registers:
            reg_name = reg.get("name", "UNKNOWN_REG")
            offset = int(reg.get("offset", "0x00"), 16)
            reg_address = base_address + offset

            if reg_address in register_addresses:
                raise ValueError(f"Overlap detected in register map '{register_map.get('name', 'UNKNOWN_MAP')}' at register '{reg_name}' with address 0x{reg_address:X}")
            register_addresses.add(reg_address)

            # Check for overlapping bitfields
            bitfield_ranges = set()
            bitfields = reg.get("bitfields", [])
            for bitfield in bitfields:
                bf_name = bitfield.get("name", "UNKNOWN_BF")
                bitshift = bitfield.get("bitshift", 0)
                bitwidth = bitfield.get("bitwidth", 1)
                bit_range = range(bitshift, bitshift + bitwidth)

                for bit in bit_range:
                    if bit in bitfield_ranges:
                        raise ValueError(f"Overlap detected in register '{reg_name}' bitfield '{bf_name}' in register map '{register_map.get('name', 'UNKNOWN_MAP')}'")
                    bitfield_ranges.add(bit)

if __name__ == "__main__":
    # Example usage
    json_file_path = "register_map.json"  # Path to the input JSON file
    output_markdown_path = "register_map.md"  # Path to the output markdown file

    # Sanity check the JSON
    try:
        json_sanity_check(json_file_path)
        print(f"JSON sanity check passed.")
    except ValueError as e:
        print(f"Sanity check failed: {e}")
        exit(1)

    generate_register_map(json_file_path)
    print(f"Register map header files generated.")

    generate_register_map_source(json_file_path)
    print(f"Register map source files generated.")

    generate_register_map_markdown(json_file_path, output_markdown_path)
    print(f"Register map markdown documentation generated: {output_markdown_path}")