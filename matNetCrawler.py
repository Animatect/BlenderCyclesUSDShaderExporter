import bpy
import mathutils

def describe_shader_node(node):
    print('\n')
    print("Node:", node.name)
    print("Type:", node.type)
    
    inputs_to_traverse = []

    for input_socket in node.inputs:
        print("Input:", input_socket.name)

        if input_socket.type == 'RGBA':
            value = input_socket.default_value
            rgba_value = mathutils.Vector(value)
            print("Value (RGBA):", f'({rgba_value.x},{rgba_value.y},{rgba_value.z},{rgba_value.w})')

        elif input_socket.type == 'VALUE':
            print("Value (Float):", input_socket.default_value)

        elif input_socket.type == 'VECTOR':
            value = input_socket.default_value
            vector_value = mathutils.Vector(value)
            print("Value (Vector):", f'({vector_value.x},{vector_value.y},{vector_value.z}')

        elif input_socket.type == 'SHADER':
            print("Value (Shader): SHADER")

        elif input_socket.type == 'STRING':
            print("Value (String):", input_socket.default_value)

        else:
            print("Value:", input_socket.default_value)

        if input_socket.is_linked:
            for link in input_socket.links:
                output_node = link.from_node
                output_socket = link.from_socket
                print("Connected Node:", output_node.name)
                print("Connected Output:", output_socket.name)

                # Add connected nodes to the list for later traversal
                inputs_to_traverse.append(output_node)

    print()  # Print an empty line for better readability

    # Traverse the connected nodes after printing inputs
    for connected_node in inputs_to_traverse:
        describe_shader_node(connected_node)
                

def describe_shader_tree(material):
    print("Shader Tree for Material:", material.name)
    nodes = material.node_tree.nodes

    # Find the Material Output node
    output_node = next((node for node in nodes if node.type == 'OUTPUT_MATERIAL'), None)

    if output_node:
        describe_shader_node(output_node)

print("#############################")
        
# Iterate through all objects in the scene
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        print("Object:", obj.name)

        # Traverse materials of the object
        for slot in obj.material_slots:
            material = slot.material
            if material:
                describe_shader_tree(material)